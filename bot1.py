import telebot
import yt_dlp

bot = telebot.TeleBot('8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Send me a Douyin video URL to download.')

@bot.message_handler(content_types=['text'])
def download_video(message):
    try:
        url = message.text
        ydl_opts = {'outtmpl': 'videos/%(title)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        bot.send_message(message.chat.id, 'Video downloaded successfully!')
    except Exception as e:
        bot.send_message(message.chat.id, f'An error occurred: {str(e)}')

bot.polling()
