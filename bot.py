import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Token Bot
TOKEN = "7949532801:AAEt7J_hZeqvpD84onD9e8ndHILSCyKkWLw"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ថតសម្រាប់ផ្ទុកឯកសារ Download
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("👋 សួស្តី! ផ្ញើលิงค์ TeraBox មកខ្ញុំ ដើម្បីទាញយកឯកសារ។")

@dp.message_handler()
async def handle_link(message: types.Message):
    url = message.text.strip()
    if "terabox.com" in url or "1024terabox.com" in url:
        await message.reply("🔄 កំពុងដោនឡូត...")
        
        # បម្លែង TeraBox Link ទៅជា Direct Download Link
        direct_link = f"https://teradlrobot.cheemsbackup.workers.dev/?url={url}"

        # បង្កើតឈ្មោះឯកសារ
        file_name = os.path.join(DOWNLOAD_FOLDER, "downloaded_file")
        
        # Download File
        response = requests.get(direct_link, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            await message.reply("✅ ដោនឡូតជោគជ័យ! កំពុងផ្ញើឯកសារ...")

            # ផ្ញើឯកសារទៅ Telegram
            with open(file_name, "rb") as file:
                await message.answer_document(file)

            # Delete File After Sending
            os.remove(file_name)
            await message.reply("🗑️ ឯកសារត្រូវបានលុបដោយស្វ័យប្រវត្តិ។")

        else:
            await message.reply("❌ មិនអាចទាញយកឯកសារបាន!")

    else:
        await message.reply("❌ សូមផ្ញើលิงค์ TeraBox ត្រឹមត្រូវ!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
