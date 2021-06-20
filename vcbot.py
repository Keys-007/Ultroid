import logging

from pyUltroid import udB, vcbot
from pyUltroid.dB.database import Var

from pyrogram import Client, filters
from pytgcalls import PyTgCalls, PyLogs

LOG_CHANNEL = int(udB.get("LOG_CHANNEL"))

logging.basicConfig(level=logging.INFO)

SESSION = udB.get("VC_SESSION")

Client = Client(SESSION,
                api_id=Var.API_ID,
                api_hash=Var.API_HASH)

CallsClient = PyTgCalls(Client, log_mode=PyLogs.ultra_verbose)

@Client.on_message(filters.me & filters.group & filters.regex("^.play (.*)"))
async def startup(_, message):
    song = message.matches[0].group(1)
    await message.edit_text('`Processing...`')
    await CallsClient.join_group_call(message.chat.id, song)

@pytgcalls.on_stream_end()
async def handler(chat_id: int):
	await CallsClient.leave_group_call(chat_id)

CallsClient.run()