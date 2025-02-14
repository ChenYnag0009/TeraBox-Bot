import os
import time
import yt_dlp
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🟢 Telegram Bot Token (Replace with your Bot Token)
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# 📂 Directory for downloading videos
DOWNLOAD_DIR = "downloads"

# 🟢 Telegram Channel/Group ID (Replace with your Channel/Group ID)
CHAT_ID = "@your_channel_or_group"

# 🟢 TikTok Image Download Function (Optional)
def download_tiktok_image(url):
    """ Function to download TikTok profile picture """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_path = f"{DOWNLOAD_DIR}/tiktok_profile.jpg"
            with open(img_path, "wb") as file:
                file.write(response.content)
            return img_path
        return None
    except Exception as e:
        print(f"❌ Error downloading TikTok image: {e}")
        return None

# 🔹 Video Download Function
async def download_video(url):
    """ Function to download video from TikTok or Douyin """
    options = {
        "format": "best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

# 🔹 Message Handler Function
async def handle_message(update: Update, context: CallbackContext):
    """ Function to handle TikTok/Douyin video URLs or image URLs """
    url = update.message.text.strip()

    if "tiktok.com" in url or "douyin.com" in url:
        await update.message.reply_text("🔍 Searching and downloading your video...")

        # ✅ Download video from TikTok or Douyin
        video_path = await download_video(url)

        if video_path and os.path.exists(video_path):
            # Send video to user
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Your downloaded video")

            # Send video to Channel (Optional)
            await context.bot.send_video(chat_id=CHAT_ID, video=open(video_path, "rb"), caption="🎬 New Video Uploaded to Channel")

            os.remove(video_path)  # 🗑️ Clean up the downloaded file
        else:
            await update.message.reply_text("❌ Unable to download the video!")

    elif "tiktok.com" in url and "photo" in url:
        # Optional: Download TikTok Profile Image
        image_path = download_tiktok_image(url)

        if image_path and os.path.exists(image_path):
            # Send image to user
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, "rb"), caption="📸 Your TikTok profile image")
            os.remove(image_path)  # 🗑️ Clean up the downloaded image
        else:
            await update.message.reply_text("❌ Unable to download the TikTok image!")
    
    else:
        await update.message.reply_text("❌ Please send a valid TikTok or Douyin video URL!")

# 🔹 Start Command Function
async def start(update: Update, context: CallbackContext):
    """ Function to start the bot and show a welcome message """
    await update.message.reply_text("👋 Hello! Send a TikTok or Douyin video link and I'll download it for you!")

# 🔹 Run the Bot Function
def main():
    """ Run the Telegram Bot """
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

# 🔥 Start the Bot
if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    main()
