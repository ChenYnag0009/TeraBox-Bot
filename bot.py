from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

def download_video(url):
    options = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a TikTok or Douyin link!")

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    if "tiktok.com" in url or "douyin.com" in url:
        video_path = download_video(url)
        update.message.reply_video(video=open(video_path, 'rb'))
    else:
        update.message.reply_text("Send a valid TikTok or Douyin link!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
