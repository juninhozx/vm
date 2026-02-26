from typing import Union

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMINS
from database import cur, save

@Client.on_callback_query(filters.regex("^stockg$") & filters.user(ADMINS))
async def panel(c: Client, m: Union[Message, CallbackQuery]):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🎫 Estoque Contas", callback_data="stockcontas contas"),
            ],
            [
                InlineKeyboardButton("🪪 Estoque Docs", callback_data="stockdoc docscnh"),
            ],
            [
                InlineKeyboardButton("🎟 Estoque Logins", callback_data="stocklogins logins"),
            ],
            [
                InlineKeyboardButton("🎫 Estoque Vales", callback_data="stockvales vales"),
            ],
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="painel"),
           ],   
      ]
 )

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text

    await send(
        """<b>📋 Painel De Estoques</b>
<i>Selecione Qual Você Vai Ver</i>""",
        reply_markup=kb,
    )