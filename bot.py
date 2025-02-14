import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Telegram Bot API Token
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# ✅ Function ទាញយក Video
def download_douyin_video(video_url):
    output_filename = "douyin_video.mp4"
    command = ["yt-dlp", "-o", output_filename, video_url]

    try:
        subprocess.run(command, check=True)
        return output_filename
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

# ✅ Function ប្រតិបត្តិ Telegram Bot
async def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    if "douyin.com" in user_text:
        await update.message.reply_text("⏳ កំពុងទាញយក...")
        try:
            video_path = download_douyin_video(user_text)
            if video_path:
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
