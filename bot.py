import os
import re
import requests
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🟢 Telegram Bot Token (ប្តូរតាម Bot របស់អ្នក)
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# 🟢 Telegram Chat ID (Channel ឬ Group ID)
CHAT_ID = "https://t.me/+OFh_AF1NpII1ZTRl"

# 📂 Directory សម្រាប់ទាញយក
DOWNLOAD_DIR = "downloads"

# 🔹 Function ទាញយកវីដេអូពី TikTok / Douyin
async def download_video(url):
    """ Function ទាញយកវីដេអូពី TikTok / Douyin """
    options = {
        "format": "best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# 🔹 Function ទាញយក Douyin Video URL
def get_douyin_video_url(video_url):
    """ Function ទាញយក Douyin Video URL """
    match = re.search(r"video/(\d+)", video_url)
    if not match:
        return None
    video_id = match.group(1)

    api_urls = [
        f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}",
        f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for api_url in api_urls:
        response = requests.get(api_url, headers=headers)
        data = response.json()

        if "item_list" in data and data["item_list"]:
            return data["item_list"][0]["video"]["play_addr"]["url_list"][0]

    return None  # ❌ Video Not Found

# 🔹 Function Start Bot
async def start(update: Update, context: CallbackContext):
    """ Function ចាប់ផ្តើម Bot """
    await update.message.reply_text("👋 សួស្តី! បញ្ជូន link TikTok ឬ Douyin មកខ្ញុំ!")

# 🔹 Function Handle Message
async def handle_message(update: Update, context: CallbackContext):
    """ Function ប xử lý Link TikTok / Douyin """
    url = update.message.text

    if "tiktok.com" in url or "douyin.com" in url:
        await update.message.reply_text("🔍 កំពុងទាញយកវីដេអូ...")

        # 👉 ចាប់ផ្តើមទាញយក
        if "douyin.com" in url:
            video_url = get_douyin_video_url(url)
            if not video_url:
                await update.message.reply_text("❌ មិនអាចទាញយក Douyin Video បាន!")
                return
            url = video_url

        video_path = await download_video(url)

        # 👉 ផ្ញើវីដេអូទៅ Telegram
        if os.path.exists(video_path):
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Douyin/TikTok Video")
            
            # 👉 ផ្ញើទៅ Telegram Channel (បើអ្នកចង់)
            await context.bot.send_video(chat_id=CHAT_ID, video=open(video_path, "rb"), caption="🎬 New Video Uploaded!")

            os.remove(video_path)  # 🗑️ លុបឯកសារ
        else:
            await update.message.reply_text("❌ ទាញយកបរាជ័យ!")

    else:
        await update.message.reply_text("❌ សូមបញ្ជូន Link TikTok ឬ Douyin ត្រឹមត្រូវ!")

# 🔹 Function Run Bot
def main():
    """ ចាប់ផ្តើម Telegram Bot """
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

# 🔥 Start Bot
if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    main()
