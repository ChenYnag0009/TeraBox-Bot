from pyrogram import Client, filters
import requests

# Telegram Bot API Credentials
API_ID = "26775695"  # បញ្ចូល API ID របស់អ្នក
API_HASH = "b15bb60859bef151762fc5d9eb206c67"
BOT_TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# ចាប់ផ្តើម Bot
bot = Client("tiktok_downloader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function ទាញយកវីដេអូ TikTok
def download_tiktok_video(url):
    api_url = f"https://api.tikmate.app/api/lookup?url={url}"
    response = requests.get(api_url).json()
    if "videoUrl" in response:
        return response["videoUrl"]
    return None

# Command ទាញយក TikTok
@bot.on_message(filters.command("tiktok") & filters.private)
def tiktok_download(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        message.reply("សូមបញ្ជូល Link TikTok!")
        return
    
    video_url = download_tiktok_video(message.command[1])
    if video_url:
        message.reply_video(video_url, caption="វីដេអូរបស់អ្នក")
    else:
        message.reply("មិនអាចទាញយកបាន!")

bot.run()
