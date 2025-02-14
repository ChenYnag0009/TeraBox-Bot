import os
import logging
import yt_dlp
from pyrogram import Client, filters

# Telegram Bot Credentials
API_ID = "26775695"
API_HASH = "b15bb60859bef151762fc5d9eb206c67"
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Create Bot Client
app = Client("douyin_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Download Function
def download_douyin_video(url):
    try:
        output_dir = "downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        ydl_opts = {
            "format": "best",
            "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
            "quiet": True,
            "nocheckcertificate": True,  # Avoid SSL certificate issues
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            return video_path
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return None

# Start Command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("សួស្ដី! ផ្ញើលីង Douyin ដើម្បីទាញយកវីដេអូ។")

# Handle Douyin Video Links
@app.on_message(filters.text & filters.regex(r"https?://www\.douyin\.com/video/\d+"))
def download_video(client, message):
    url = message.text
    logging.debug(f"Received URL: {url}")  # Log the URL to check it
    message.reply_text("⏳ កំពុងទាញយកវីដេអូ...")

    video_path = download_douyin_video(url)
    if video_path:
        logging.debug(f"Video path: {video_path}")  # Log the video path
        message.reply_video(video_path, caption="✅ Douyin Video Downloaded!")
        os.remove(video_path)  # Delete after sending
    else:
        logging.error(f"Failed to download video: {url}")  # Log the failure
        message.reply_text("❌ មិនអាចទាញយកវីដេអូបាន!")

# Run the bot
app.run()
