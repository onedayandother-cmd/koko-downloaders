import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# بياناتك الخاصة بالبوت الثالث
API_ID = 20209272
API_HASH = "08361988c289fcbb31a417c32701edf8"
BOT_TOKEN = "8540714719:AAFrxHMhgZj4uIn6pW95AkA8yvhGAeRGN8Q"

app = Client("kokovideos3_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ أهلاً بك في kokovideos3_bot!\nأرسل رابط فيديو أو بلاي لست وسأقوم بالتحميل فوراً (حتى 2 جيجا).")

@app.on_message(filters.text & ~filters.command("start"))
async def downloader(client, message):
    url = message.text
    if not url.startswith("http"): return
    
    status = await message.reply_text("⏳ جاري سحب البيانات والتحميل... انتظر قليلاً")
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': False,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'entries' in info:
                for entry in info['entries']:
                    file_path = ydl.prepare_filename(entry)
                    await status.edit(f"📤 جاري رفع: {entry['title']}")
                    await client.send_video(message.chat.id, video=file_path)
                    if os.path.exists(file_path): os.remove(file_path)
            else:
                file_path = ydl.prepare_filename(info)
                await status.edit("📤 جاري الرفع لتليجرام...")
                await client.send_video(message.chat.id, video=file_path)
                if os.path.exists(file_path): os.remove(file_path)
        await status.delete()
    except Exception as e:
        await status.edit(f"❌ حدث خطأ: {str(e)}")

app.run()
