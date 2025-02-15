import os
import requests
import urllib
from pyquery import PyQuery as PQ
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download Douyin video
def download_video(download_author, title, url):
    if not os.path.exists(download_author):
        os.makedirs(download_author)
    response_video = requests.get(url)
    video_path = os.path.join(download_author, f"{title}.mp4")
    with open(video_path, 'wb') as file:
        file.write(response_video.content)
    return video_path

# Function to get the actual Douyin video URL
def get_douyin_url(url):
    if 'douyin.com/video/' in url:
        return url
    response = requests.get(url, allow_redirects=False)
    get_url = response.headers['Location']
    if 'douyin.com/share/video/' in get_url:
        get_url = get_douyin_url(get_url)
    return get_url

# Function to extract video information (title, author, video URL)
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

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please send a Douyin video URL to download and upload.")

# Function to handle video download and upload to Telegram
async def download_and_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the URL from the user's message
        url = update.message.text.strip()
        
        # Get the Douyin video URL
        video_url = get_douyin_url(url)
        author, title, video_url = extract_video_info(video_url)

        # Send message indicating the bot is starting the download
        await update.message.reply_text(f"Downloading: {title} by {author}...")

        # Download the video
        video_path = download_video(author, title, video_url)

        # Send the video to the user
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption=f"{title} by {author}")

        # Optionally, remove the video file after upload
        os.remove(video_path)
        
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {str(e)}")

# Function to handle errors
def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Update {update} caused error {context.error}")

# Main function to set up the bot
def main():
    # Replace 'YOUR_TOKEN' with your Telegram bot token
    application = Application.builder().token('8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk').build()

    # Command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_upload))

    # Error handler
    application.add_error_handler(error)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
