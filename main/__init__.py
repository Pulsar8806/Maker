import aiohttp
from pyrogram import Client
from config import *

app = Client(
  "bot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)

print("[INFO]: BOTU BAŞLAT...")
app.start()

print("[INFO]: AIOHTTP ISTEMCISINI BAŞLATIYOR")
session = aiohttp.ClientSession()
