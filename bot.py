import os
import time
import yt_dlp
import undetected_chromedriver as uc
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 🟢 Telegram Bot Token (ប្តូរតាម Bot របស់អ្នក)
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# 📂 Directory សម្រាប់ទាញយក
DOWNLOAD_DIR = "downloads"

# 🟢 Telegram Channel/Group ID
CHAT_ID = "@your_channel_or_group"

# 🔹 Function ទាញយកវីដេអូពី TikTok / Douyin
async def download_video(url):
    """ Function to Download Video from TikTok/Douyin """
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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(video_url)
        time.sleep(5)  # Wait for page to load

        video_tag = driver.find_element("xpath", "//video")
        video_url = video_tag.get_attribute("src")

        driver.quit()
        return video_url
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# 🔹 Function to Handle Messages
async def handle_message(update: Update, context: CallbackContext):
    """ Function to Handle TikTok/Douyin Links """
    url = update.message.text

    if "tiktok.com" in url:
        await update.message.reply_text("🔍 កំពុងពិនិត្យ TikTok Link...")

        # ✅ ទាញយកវីដេអូ TikTok
        video_path = await download_video(url)
    
    elif "douyin.com" in url:
        await update.message.reply_text("🔍 កំពុងទាញយកវីដេអូ Douyin...")

        # ✅ ទាញយកវីដេអូ Douyin
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

# 🔹 Function Start Bot
async def start(update: Update, context: CallbackContext):
    """ Function to Start the Bot """
    await update.message.reply_text("👋 សួស្តី! បញ្ជូន link TikTok ឬ Douyin មកខ្ញុំ!")

# 🔹 Function Run Bot
def main():
    """ Run the Telegram Bot """
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
