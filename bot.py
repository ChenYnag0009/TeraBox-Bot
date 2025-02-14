import os
import yt_dlp
from pyrogram import Client, filters

# Telegram Bot Credentials
API_ID = "26775695"
API_HASH = "b15bb60859bef151762fc5d9eb206c67"
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

app = Client("douyin_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Download Function
def download_douyin_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.on_message(filters.command("start"))
def start(_, message):
    message.reply_text("សួស្ដី! ផ្ញើលីង Douyin ដើម្បីទាញយកវីដេអូ។")

@app.on_message(filters.text & filters.regex(r"https?://www\.douyin\.com/video/\d+"))
def download_video(_, message):
    url = message.text
    try:
        video_path = download_douyin_video(url)
        message.reply_video(video_path, caption="✅ Douyin Video Downloaded!")
        os.remove(video_path)  # Delete after sending
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")

app.run()
