import os
import re
import requests
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from playwright.async_api import async_playwright

# Telegram Bot Token
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# Douyin Video Downloader
async def download_douyin_video(url):
    try:
        ydl_opts = {
            "outtmpl": "douyin_video.mp4",
            "format": "best",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "douyin_video.mp4"
    except Exception as e:
        print(f"Download error: {e}")
        return None

# Douyin Image Downloader
async def download_douyin_image(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        await page.wait_for_selector("img")
        img_url = await page.locator("img").get_attribute("src")

        if img_url:
            img_path = "douyin_image.jpg"
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as f:
                f.write(img_data)
            await browser.close()
            return img_path
        await browser.close()
        return None

# Handle Telegram Messages
async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()

    if "douyin.com" in url:
        await update.message.reply_text("🔍 Downloading from Douyin...")

        # Download Video
        video_path = await download_douyin_video(url)
        if video_path and os.path.exists(video_path):
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"), caption="🎬 Your Douyin Video")
            os.remove(video_path)
        else:
            await update.message.reply_text("❌ Failed to download video!")

        # Download Image
        image_path = await download_douyin_image(url)
        if image_path and os.path.exists(image_path):
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, "rb"), caption="📸 Your Douyin Image")
            os.remove(image_path)
        else:
            await update.message.reply_text("❌ Failed to download image!")

    else:
        await update.message.reply_text("❌ Please send a valid Douyin URL!")

# Start Command Handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Send me a Douyin video/image link and I'll download it for you!")

# Main function to start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
