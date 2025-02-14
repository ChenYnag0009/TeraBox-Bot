import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# បញ្ចូល API Token របស់អ្នក
TOKEN = '8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk'

# មុខងារដើម្បីទាញយកវីដេអូពី Douyin
def extract_video_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # ស្វែងរកតំណភ្ជាប់វីដេអូ
            video_url = re.findall(r'"play_addr":"(https?://[^"]+)"', response.text)
            if video_url:
                return video_url[0].replace('\\u002F', '/')
    except Exception as e:
        print(f"Error: {e}")
    return None

# មុខងារដើម្បីដំណើរការពាក្យបញ្ជា /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('សួស្តី! សូមផ្ញើតំណភ្ជាប់ Douyin មកខ្ញុំដើម្បីទាញយកវីដេអូ។')

# មុខងារដើម្បីដំណើរការតំណភ្ជាប់
async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    video_url = extract_video_url(url)
    if video_url:
        await update.message.reply_video(video_url)
    else:
        await update.message.reply_text('មិនអាចទាញយកវីដេអូបានទេ។')

# មុខងារដើម្បីចាប់ផ្តើម bot
def main():
    # បង្កើត Application
    application = Application.builder().token(TOKEN).build()

    # បន្ថែម handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ចាប់ផ្តើម bot
    application.run_polling()

if __name__ == '__main__':
    main()
