import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Telegram Bot API Token
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# ✅ Function ដើម្បីទាញយក Video URL ពី Douyin
def get_douyin_video_url(video_url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # ✅ បញ្ជាក់ path ទៅ WebDriver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(video_url)
        time.sleep(5)  # 🕒 រងចាំ 5 វិនាទី
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_src = video_element.get_attribute("src")
        return video_src
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

# ✅ Function ទាញយក Video
def download_video(video_url, filename="douyin_video.mp4"):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return filename
    else:
        return None

# ✅ Function ប្រតិបត្តិ Telegram Bot
async def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    if "douyin.com" in user_text:
        await update.message.reply_text("⏳ កំពុងទាញយក...")
        try:
            video_src = get_douyin_video_url(user_text)
            if video_src:
                video_path = download_video(video_src)
                await update.message.reply_video(video=open(video_path, "rb"))
                os.remove(video_path)
            else:
                await update.message.reply_text("❌ មិនអាចទាញយកវីដេអូបាន!")
        except Exception as e:
            await update.message.reply_text(f"❌ បរាជ័យ: {str(e)}")
    else:
        await update.message.reply_text("📌 សូមផ្ញើ Link Douyin!")

# ✅ Function ដើម្បីចាប់ផ្តើម Bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
