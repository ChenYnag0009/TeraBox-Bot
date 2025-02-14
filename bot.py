from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp
import asyncio

BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

async def download_video(url):
    options = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me a TikTok or Douyin link!")

async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    if "tiktok.com" in url or "douyin.com" in url:
        video_path = await download_video(url)
        await update.message.reply_video(video=open(video_path, 'rb'))
    else:
        await update.message.reply_text("Send a valid TikTok or Douyin link!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
