import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Telegram Bot API Token
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# Function ទាញយកវីដេអូពី Douyin
def download_douyin_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "douyin_video.mp4",
        "cookiefile": "cookies.txt",  # ប្រើ cookies ដើម្បីអោយ Douyin អនុញ្ញាត
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "douyin_video.mp4"

# Function ដើម្បីប្រើ Bot
async def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    if "douyin.com" in user_text:
        await update.message.reply_text("⏳ កំពុងទាញយក...")
        try:
            video_path = download_douyin_video(user_text)
            await update.message.reply_video(video=open(video_path, "rb"))
            os.remove(video_path)
        except Exception as e:
            await update.message.reply_text(f"❌ បរាជ័យ: {str(e)}")
    else:
        await update.message.reply_text("📌 សូមផ្ញើ Link Douyin!")

# Function ដើម្បីចាប់ផ្តើម Bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
