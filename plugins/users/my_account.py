from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import cur, save
from utils import get_info_wallet

import datetime
from typing import Union
import asyncio

@Client.on_callback_query(filters.regex(r"^user_info$"))
async def user_info(c: Client, m: CallbackQuery):
    hora_atual = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))

    hora_atual_str = hora_atual.strftime('%H:%M:%S')

    data_atual = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))

    data_atual_str = data_atual.strftime('%d/%m/%Y')
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
             [
                 InlineKeyboardButton("💳 Histórico", callback_data="history"),
				 InlineKeyboardButton("💸 Resgatar Gift", callback_data="gift"),
			 ],
			 [
				 InlineKeyboardButton("📬 Cadastrar", callback_data="swap_info"),
				 InlineKeyboardButton("📭 Resgatar", callback_data="swap"),
			 ],
			 [
				 InlineKeyboardButton("⬅️ Menu Principal", callback_data="start"),
             ],

        ]
    )
    link = f"https://t.me/{c.me.username}?start={m.from_user.id}"
    await m.edit_message_text(
        f"""<a href='https://d6xcmfyh68wv8.cloudfront.net/blog-content/uploads/2020/10/Card-pre-launch_blog-feature-image1.png'>&#8204</a><b><b>📛 Seu Nome: {m.from_user.first_name}</b>
<b>🆔 Seu ID: <code>{m.from_user.id}</code></b>

<b>🥇 Bônus De Recarga: Desativado</b>

<b>📆 Data Atual: {data_atual_str}</b>
<b>🕒 Hora Atual: {hora_atual_str}</b>

<b>🔗 - SISTEMA DE AFILIADOS COMO FUNCIONA:</b>
		
<i>📎 -  Compartilhe Seu Link Abaixo e Ganhe Saldo No Bot a Cada Vez Que Seu Filiado Adicionar Saldo:</i>

<b>🔗 - Seu link de afiliação:
<code>{link}</code></b>

<b>♻️ - A Cada Recarga Você Ganha 10% Do Que Seu Filiado Recarregar No Bot!</b>

<b>🔱 - Agora Tudo Ficou Mais Fácil, Navegue Pelos Botões Abaixo e Olhe Seu Histórico,  Termos De Trocas ou Os Valores Do Aluguel De Nossos Bots!</>

<b>⬇️ - Confira Abaixo:</b>""",
        reply_markup=kb,
    )


@Client.on_callback_query(filters.regex(r"^dev$"))
async def btc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
      
            [
				InlineKeyboardButton("⚜️ Alugar Bot", url="https://t.me/LittleNucky"),
				InlineKeyboardButton("⚜️ Atualizações", url="https://t.me/RefsLittleNucky"),
			],
			[
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="start"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""<a href='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZwK3NiWuYaWJO0iqE_cjIzX7fTBWcGRlhgQ&usqp=CAU'>&#8204</a><b>⚙️ | Versão do bot: 4.6

➤ Ultima Atualização: 05/09/2023

➤ Atualizações Da Versã

 ➜ Sistema De Afliado Aprimorado

 ➜ Sistema De AntiFlood Do Pix
 
 ➜ Historico Com Todas As Compras Separadas
 
 ➜ Sistema Ant Flood No Chat

 ➜ Pix Automatico Com Mercado Pago

 ➜ Sistema De Admin Completo

✅ | Bot by: @LittleNucky</b>""",
        reply_markup=kb,
    ) 
    
@Client.on_callback_query(filters.regex(r"^gift$"))
async def gift(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            
             [
                 InlineKeyboardButton("⬅️ Menu Principal", callback_data="user_info"),
             ],

        ]
    )
    link = f""
    await m.edit_message_text(
        f"""<b><a href='https://i.ibb.co/r0jsL20/IMG-20230712-135120-982.jpg'>&#8204</a>🎁 Resgatar Gift</b>
<i>- Aqui você resgatar o gift com facilidade, digite seu gift como o exemplo abaixo.</i>

<i>🏷 - Exemplo: /resgatar FOX0FCOT7OTH</i>

<i>♻️ - Não tente dar um de espertinho e tentar floodar vários códigos ao mesmo tempo, temos vários de segurança AntiFlood, Caso você Floodar irá tomar ban!</i>

{get_info_wallet(m.from_user.id)}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^history$"))
async def history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
        
        [
			 InlineKeyboardButton("🪪 Historico de DOC", callback_data="buy_history_doc"),
		],
        [ 
		     InlineKeyboardButton("🎟 Historico de LOGINS", callback_data="buy_history_log"),
		],
		[
		     InlineKeyboardButton("🎫 Historico de VALES", callback_data="buy_history_vales"),
        ],
        [
             InlineKeyboardButton("◀️ Menu Principal", callback_data="user_info"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""<a href='https://d6xcmfyh68wv8.cloudfront.net/blog-content/uploads/2020/10/Card-pre-launch_blog-feature-image1.png'>&#8204</a>♻️ - Selecione qual historico de compras você deseja ver:</b>""",
        reply_markup=kb,
    )
    
@Client.on_callback_query(filters.regex(r"^buy_history_doc$"))
async def buy_history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT nome, cpf, linkdoc, bought_date , level, score ,localidade FROM docs_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
NOME|CPF|LINK|COMPRADO|TIPO|SCORE|CIDADE

{cards_txt}""",
        reply_markup=kb,
    )
    
@Client.on_callback_query(filters.regex(r"^buy_history_vales$"))
async def buy_history_vales(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cpf,limite,cidade bought_date FROM vales_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CPF|LIMIE|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_log$"))
async def buy_history_log(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="buy_history_log"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cidade bought_date FROM logins_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^swap$"))
async def swap_points(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="user_info"),
            ],
        ]
    )

    user_id = m.from_user.id
    balance, diamonds = cur.execute(
        "SELECT balance, balance_diamonds FROM users WHERE id=?", [user_id]
    ).fetchone()

    if diamonds >= 100:
        add_saldo = round((diamonds / 2), 2)
        new_balance = round((balance + add_saldo), 2)

        txt = f"⚜️ Seus <b>{diamonds}</b> pontos foram convertidos em R$ <b>{add_saldo}</b> de saldo."

        cur.execute(
            "UPDATE users SET balance = ?, balance_diamonds=?  WHERE id = ?",
            [new_balance, 0, user_id],
        )
        return await m.edit_message_text(txt, reply_markup=kb)

    await m.answer(
        "⚠️ Você não tem pontos suficientes para realizar a troca. O mínimo é 100 pontos.",
        show_alert=True,
    )


@Client.on_callback_query(filters.regex(r"^swap_info$"))
async def swap_info(c: Client, m: CallbackQuery):
    await m.message.delete()

    cpf = await m.message.ask(
        "<b>👤 CPF da lara (válido) da lara que irá pagar</b>",
        reply_markup=ForceReply(),
        timeout=120,
    )
    name = await m.message.ask(
        "<b>👤 Nome completo do pagador</b>", reply_markup=ForceReply(), timeout=120
    )
    email = await m.message.ask(
        "<b>📧 E-mail</b>", reply_markup=ForceReply(), timeout=120
    )
    cpf, name, email = cpf.text, name.text, email.text
    cur.execute(
        "UPDATE users SET cpf = ?, name = ?, email = ?  WHERE id = ?",
        [cpf, name, email, m.from_user.id],
    )
    save()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Menu Principal", callback_data="start"),
            ]
        ]
    )
    await m.message.reply_text(
        "<b>✅️ Seus dados foram alterados com sucesso.</b>", reply_markup=kb
    )



