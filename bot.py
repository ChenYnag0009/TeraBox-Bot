import os
import time
from playwright.sync_api import sync_playwright
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🟢 Telegram Bot Token
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# 📂 Directory for downloading files (Videos, Images)
DOWNLOAD_DIR = "downloads"

# 🟢 Telegram Channel/Group ID
CHAT_ID = "@your_channel_or_group"

# 🔹 Download Video from TikTok or Douyin using Playwright
def download_video(url):
    """ Function to download video from TikTok/Douyin """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the video to load
        page.wait_for_selector("video")

        # Find video source URL
        video_url = page.locator("video").get_attribute("src")
        if video_url:
            video_path = f"{DOWNLOAD_DIR}/video.mp4"
            # Download video
            page.goto(video_url)
            with open(video_path, 'wb') as f:
                f.write(page.content())
            browser.close()
            return video_path
        else:
            browser.close()
            return None

# 🔹 Download Profile Image from TikTok
def download_tiktok_image(url):
    """ Function to download TikTok profile picture """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the profile image to load
        page.wait_for_selector("img")
        
        # Extract the profile image source URL
        img_url = page.locator("img").get_attribute("src")
        if img_url:
            img_path = f"{DOWNLOAD_DIR}/tiktok_profile.jpg"
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_path, "wb") as file:
                    file.write(response.content)
            browser.close()
            return img_path
        else:
            browser.close()
            return None

# 🔹 Download Thumbnail Image from Douyin
def download_douyin_image(url):
    """ Function to download Douyin thumbnail image """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the thumbnail to load
        page.wait_for_selector("img")
        
        # Extract the thumbnail image URL
        img_url = page.locator("img").get_attribute("src")
        if img_url:
            img_path = f"{DOWNLOAD_DIR}/douyin_thumbnail.jpg"
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_path, "wb") as file:
                    file.write(response.content)
            browser.close()
            return img_path
        else:
            browser.close()
            return None

# 🔹 Handle Messages and URLs
async def handle_message(update: Update, context: CallbackContext):
    """ Function to handle incoming URLs """
    url = update.message.text.strip()

    if "tiktok.com" in url:
        await update.message.reply_text("🔍 Searching and downloading your video or image...")

        if "photo" in url:  # Handle image download from TikTok
            image_path = download_tiktok_image(url)
            if image_path and os.path.exists(image_path):
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, "rb"), caption="📸 Your TikTok profile image")
                os.remove(image_path)  # 🗑️ Clean up the downloaded image
            else:
                await update.message.reply_text("❌ Unable to download the TikTok profile image!")
        else:  # Handle video download from TikTok
            video_path = download_video(url)
            if video_path and os.path.exists(video_path):
                await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Your downloaded video")
                os.remove(video_path)  # 🗑️ Clean up the downloaded file
            else:
                await update.message.reply_text("❌ Unable to download the video!")

    elif "douyin.com" in url:
        await update.message.reply_text("🔍 Searching and downloading your video or image...")

        if "photo" in url:  # Handle image download from Douyin
            image_path = download_douyin_image(url)
            if image_path and os.path.exists(image_path):
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, "rb"), caption="📸 Your Douyin thumbnail image")
                os.remove(image_path)  # 🗑️ Clean up the downloaded image
            else:
                await update.message.reply_text("❌ Unable to download the Douyin thumbnail image!")
        else:  # Handle video download from Douyin
            video_path = download_video(url)
            if video_path and os.path.exists(video_path):
                await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Your downloaded video")
                os.remove(video_path)  # 🗑️ Clean up the downloaded file
            else:
                await update.message.reply_text("❌ Unable to download the video!")

    else:
        await update.message.reply_text("❌ Please send a valid TikTok or Douyin video URL!")

# 🔹 Start Command
async def start(update: Update, context: CallbackContext):
    """ Start the bot and send welcome message """
    await update.message.reply_text("👋 Hello! Send a TikTok or Douyin video or image link and I'll download it for you!")

# 🔹 Run the Bot
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
