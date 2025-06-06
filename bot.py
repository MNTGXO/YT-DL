import asyncio
import feedparser
import logging
import threading
import requests
import re
import cloudscraper
import io
from flask import Flask
from bs4 import BeautifulSoup
from pyrogram import Client, errors
from urllib.parse import urlparse
from config import BOT, API, OWNER, CHANNEL

# ** Peer ID Fix **
from pyrogram import utils as pyroutils
pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -10099999999999

# ------------------ Logging Setup ------------------
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# ------------------ Flask App for Health Check ------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8000)


# ------------------ Bot Class ------------------
class MN_Bot(Client):
    MAX_MSG_LENGTH = 4000

    def __init__(self):
        super().__init__(
            "MN-Bot",
            api_id=API.ID,
            api_hash=API.HASH,
            bot_token=BOT.TOKEN,
            plugins=dict(root="plugins"),
            workers=16,
        )
        self.channel_id = CHANNEL.ID


    async def start(self):
        await super().start()
        me = await self.get_me()
        BOT.USERNAME = f"@{me.username}"
        self.mention = me.mention
        self.username = me.username
        await self.send_message(chat_id=OWNER.ID,
                                text=f"{me.first_name} ✅✅ BOT started successfully ✅✅")
        logging.info(f"✅ {me.first_name} BOT started successfully")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")

# ------------------ Main ------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    MN_Bot().run()
