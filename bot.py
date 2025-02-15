import os
import requests
import urllib
from pyquery import PyQuery as PQ
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging to get error messages in Telegram bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download Douyin video
def download_video(download_author, title, url):
    if download_author not in os.listdir():
        os.mkdir(download_author)
    response_video = requests.get(url)
    with open(f"{download_author}/{title}.mp4", 'wb') as file:
        file.write(response_video.content)
    return f"{title} 下载完成！"

# Function to get Douyin video URL
def get_douyin_url(url):
    if 'douyin.com/video/' in url:
        return url
    response = requests.get(url, allow_redirects=False)
    get_url = response.headers['Location']
    if 'douyin.com/share/video/' in get_url:
        get_url = get_douyin_url(get_url)
    return get_url

# Main function to extract video and author info
def extract_video_info(url):
    response = requests.get(url)
    data = PQ(response.text)
    title = data('title').text()
    script = data('script#RENDER_DATA').text()
    script_js = urllib.parse.unquote(script)
    title1 = script_js.find('"nickname":"')
    title2 = script_js.find('","remarkName"')
    author = script_js[title1+12:title2]
    url1 = script_js.find('"playApi":"')
    url2 = script_js.find('","bitRateList"')
    video_url = 'http:' + script_js[url1+11:url2]
    return author, title, video_url

# Telegram bot function to handle video requests
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Please send a Douyin video URL to download.")

def download(update: Update, context: CallbackContext):
    try:
        url = update.message.text.strip()
        video_url = get_douyin_url(url)
        author, title, video_url = extract_video_info(video_url)
        update.message.reply_text(f"Starting download: {title} by {author}...")
        status = download_video(author, title, video_url)
        update.message.reply_text(status)
    except Exception as e:
        update.message.reply_text(f"Error occurred: {str(e)}")

def main():
    # Replace 'YOUR_TOKEN' with your Telegram Bot API token
    updater = Updater('8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
