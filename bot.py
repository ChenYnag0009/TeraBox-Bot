import os
import re
import requests
import yt_dlp
import undetected_chromedriver as uc
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🟢 Telegram Bot Token (ប្តូរតាម Bot របស់អ្នក)
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# 🟢 Telegram Chat ID (Channel ឬ Group ID)
CHAT_ID = "@https://t.me/+OFh_AF1NpII1ZTRl"

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
    """ Scrape Douyin Video URL using Selenium """
    try:
        driver = uc.Chrome()
        driver.get(video_url)
        time.sleep(5)  # Wait for page to load

        video_tag = driver.find_element("xpath", "//video")
        video_url = video_tag.get_attribute("src")

        driver.quit()
        return video_url
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# 🔹 Function ទាញយករូបភាពពី TikTok
def download_tiktok_images(url):
    """ Function ទាញយករូបភាពពី TikTok """
    options = {"quiet": True, "skip_download": True}
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

        if "photo_collection" in info:
            images = [img["url"] for img in info["photo_collection"]]
            return images

    return None

# 🔹 Function Start Bot
async def start(update: Update, context: CallbackContext):
    """ Function ចាប់ផ្តើម Bot """
    await update.message.reply_text("👋 សួស្តី! បញ្ជូន link TikTok ឬ Douyin មកខ្ញុំ!")

# 🔹 Function Handle Message
async def handle_message(update: Update, context: CallbackContext):
    """ Function ប xử lý Link TikTok / Douyin """
    url = update.message.text

    if "tiktok.com" in url:
        await update.message.reply_text("🔍 កំពុងពិនិត្យ TikTok Link...")

        # ✅ ពិនិត្យរូបភាព
        images = download_tiktok_images(url)
        if images:
            for img_url in images:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url, caption="🖼 TikTok Image")
            return
        
        # ✅ ប្រសិនបើមិនមែនរូបភាព → ទាញយកវីដេអូ
        video_path = await download_video(url)
    
    elif "douyin.com" in url:
        await update.message.reply_text("🔍 កំពុងទាញយកវីដេអូ Douyin...")
        
        video_url = get_douyin_video_url(url)
        if not video_url:
            await update.message.reply_text("❌ មិនអាចទាញយក Douyin Video បាន!")
            return

        video_path = await download_video(video_url)

    else:
        await update.message.reply_text("❌ សូមបញ្ជូន Link TikTok ឬ Douyin ត្រឹមត្រូវ!")
        return

    # ✅ ផ្ញើវីដេអូទៅ Telegram
    if os.path.exists(video_path):
        await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Video Downloaded")

        # 👉 ផ្ញើទៅ Telegram Channel (បើអ្នកចង់)
        await context.bot.send_video(chat_id=CHAT_ID, video=open(video_path, "rb"), caption="🎬 New Video Uploaded!")

        os.remove(video_path)  # 🗑️ លុបឯកសារ
    else:
        await update.message.reply_text("❌ ទាញយកបរាជ័យ!")

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
