import os
from time import sleep, localtime, time
import asyncio
import threading
from time import sleep
from pyrogram import Client , filters, errors
from pyrogram.types import Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaDocument, InputMediaPhoto, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineQueryResultCachedPhoto
from pyrogram.errors import MessageNotModified, PeerIdInvalid

api_id = 22824836
api_hash = "631cdc26b7b6e6a6e850cd2757c1b4aa"
bot_token = "6537175395:AAH_tzMBbLvPEoGtFagHPjBTtAh2bFkWz_w"
bot = Client("bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
userbot = Client("userbot", api_id=api_id, api_hash=api_hash) #+5351278196

ADMINS = ["raydel0307","ValleSoft","tumulatico98"]
ADMINS_T = ["raydel0307","ValleSoft","tumulatico98"]
seg = 0

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

def update_progress_bar_2(index,max,size=15,step_size=7):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += '['
		while(index_make<size):
			if porcent >= index_make * step_size:make_text+='●'
			else:make_text+='○'
			index_make+=1
		make_text += ']'
		return make_text
	except Exception as ex:
		return ''

async def downloadmessage_tg_up(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		percentage = chunk / filesize
		percentage *= 100
		percentage = round(percentage)
		msg = f"𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜: [ {percentage}% ]\n"
		try:
			msg+=update_progress_bar_2(chunk,filesize)+ "\n"
		except:pass
		msg+= f"{sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n"
		msg+= f"⚡️Speed: {sizeof_fmt(mbs)}/s\n\n"	
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except:pass
		seg = localtime().tm_sec

async def downloadmessage_progres(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		percentage = chunk / filesize
		percentage *= 100
		percentage = round(percentage)
		msg = f"𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠: [ {percentage}% ]\n"
		try:
			msg+=update_progress_bar_2(chunk,filesize)+ "\n"
		except:pass
		msg+= f"{sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n"
		msg+= f"⚡️Speed: {sizeof_fmt(mbs)}/s\n\n"
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except MessageNotModified:
			  pass
		seg = localtime().tm_sec

async def handle_private(message,chatid,msgid,username):
	print("handle_private")
	msg  = await userbot.get_messages(chatid,msgid)

	if "text" in str(msg):
		await bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
		return

	smsg = await bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
	start = time()
	filename = "__SAVE RESCTRICTED CONTENT__"
	file = await userbot.download_media(msg, progress=downloadmessage_progres, progress_args=(filename,start,smsg))
	filename = file.split("/")[-1]
	path = f"downloads/{username}/{filename}"
	os.rename(file,path)
	file = path
	
	if "Document" in str(msg):
		try:
			thumb = await userbot.download_media(msg.document.thumbs[0].file_id)
		except: thumb = None
		
		start = time()
		await bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id,progress=downloadmessage_tg_up,progress_args=(filename,start,smsg))
		if thumb != None: os.remove(thumb)

	elif "Video" in str(msg):
		try: 
			thumb = await userbot.download_media(msg.video.thumbs[0].file_id)
		except: thumb = None

		start = time()
		await bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id,progress=downloadmessage_tg_up,progress_args=(filename,start,smsg))
		if thumb != None: os.remove(thumb)

	elif "Animation" in str(msg):
		await bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
		   
	elif "Sticker" in str(msg):
		await bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

	elif "Voice" in str(msg):
		start = time()
		await bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id,progress=downloadmessage_tg_up,progress_args=(filename,start,smsg))

	elif "Audio" in str(msg):
		try:
			thumb = await userbot.download_media(msg.audio.thumbs[0].file_id)
		except: thumb = None
		
		start = time()	
		await bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id,progress=downloadmessage_tg_up,progress_args=(filename,start,smsg))   
		if thumb != None: os.remove(thumb)

	elif "Photo" in str(msg):
		await bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

	os.remove(file)
	if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
	await bot.delete_messages(message.chat.id,[smsg.id])

@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client, message):
	username = message.from_user.username
	if not username in ADMINS:
		await bot.send_message(username,"🚷 **No tienes acceso**")
		return
	if not os.path.exists(f"downloads/{username}/"):
		os.mkdir(f"downloads/{username}/")
	chat_id = message.chat.id
	user_id = message.from_user.id
	first_name = message.from_user.first_name
	msg = f"⭐️ Hola **{first_name}**\n\n"
	msg+= "➣ 𝘽𝙤𝙩 𝙙𝙚𝙙𝙞𝙘𝙖𝙙𝙤 𝙖 𝙚𝙭𝙩𝙧𝙖𝙚𝙧 𝙘𝙤𝙣𝙩𝙚𝙣𝙞𝙙𝙤 𝙙𝙚 𝘾𝙖𝙣𝙖𝙡𝙚𝙨/𝙂𝙧𝙪𝙥𝙤𝙨 𝙘𝙤𝙣 𝙥𝙧𝙤𝙩𝙚𝙘𝙘𝙞ó𝙣 𝙘𝙤𝙣𝙩𝙧𝙖 𝙧𝙚𝙚𝙣𝙫í𝙤\n\n"
	msg+= "➣ __SUPPORT: @ValleSoft__\n"
	msg+= "➣ __DEV: @raydel0307__\n"
	button1 = InlineKeyboardButton("HELP|AYUDA","_help")
	buttons = [[button1]]
	reply_markup = InlineKeyboardMarkup(buttons)
	await bot.send_message(user_id,msg,reply_markup=reply_markup)
	return

@bot.on_message(filters.command("add", prefixes="/") & filters.private)
async def add(client, message):
	global ADMINS
	username = message.from_user.username
	if not username in ADMINS_T:
		await bot.send_message(username,"🚷 **No puedes usar este commando**")
		return
	user = message.text.split(" ",1)[1]
	ADMINS.append(user)
	await bot.send_message(username,f"✅ @{user} ya tiene acceso al bot")
	return

@bot.on_message(filters.command("ban", prefixes="/") & filters.private)
async def add(client, message):
	global ADMINS
	username = message.from_user.username
	if not username in ADMINS_T:
		await bot.send_message(username,"🚷 **No puedes usar este commando**")
		return
	user = message.text.split(" ",1)[1]
	if user in ADMINS:
		ADMINS.append(user)
		await bot.send_message(username,f"❌ @{user} ya no tiene acceso al bot")
	else:
		await bot.send_message(username,f"❌ @{user} no pertenece al bot")
	return

@bot.on_callback_query()
async def callback_data(bot,callback):
	username = callback.from_user.username
	user_id = callback.from_user.id
	first_name = callback.from_user.first_name
	data = str(callback.data).split(" ")
	call_back = callback.message
	chat_id = callback.id
	if data[0]=="_help":
		msg = "𝙃𝙀𝙇𝙋|𝘼𝙔𝙐𝘿𝘼\n\n"
		msg+= "𝐏𝐀𝐑𝐀 𝐂𝐀𝐍𝐀𝐋𝐄𝐒 𝐏𝐔𝐁𝐋𝐈𝐂𝐎𝐒:\n- 𝐄𝐧𝐯𝐢𝐚𝐦𝐞 𝐞𝐥 𝐞𝐧𝐥𝐚𝐜𝐞 𝐝𝐢𝐫𝐞𝐜𝐭𝐨 𝐝𝐞𝐥 𝐦𝐞𝐧𝐬𝐚𝐣𝐞.\n\n"
		msg+= "𝐏𝐀𝐑𝐀 𝐂𝐀𝐍𝐀𝐋𝐄𝐒 𝐏𝐑𝐈𝐕𝐀𝐃𝐎𝐒:\n- 𝐄𝐧𝐯𝐢𝐚𝐦𝐞 𝐞𝐥 𝐞𝐧𝐥𝐚𝐜𝐞 𝐝𝐞 𝐢𝐧𝐯𝐢𝐭𝐚𝐜𝐢𝐨𝐧\n- 𝐄𝐧𝐯𝐢𝐚𝐦𝐞 𝐞𝐥 𝐦𝐞𝐧𝐬𝐚𝐣𝐞 𝐝𝐢𝐫𝐞𝐜𝐭𝐨 𝐝𝐞𝐥 𝐦𝐞𝐧𝐬𝐚𝐣𝐞"
		await call_back.edit_text(msg)
		return

@bot.on_message((filters.regex("https://") | filters.regex("http://")) & filters.private)
async def down_link(client: Client, message: Message):
	username = message.from_user.username
	if not username in ADMINS:
		await bot.send_message(username,"🚷 **No tienes acceso**")
		return
	if not os.path.exists(f"downloads/{username}/"):
		os.mkdir(f"downloads/{username}/")
	user_path = f"downloads/{username}/"
	send = message.reply
	user_id = message.from_user.id

	if "https://t.me/" in message.text:
		datas = message.text.split("/")
		msgid = int(datas[-1].split("?")[0])
		#chat privados
		if "https://t.me/c/" in message.text:
			chatid = int("-100" + datas[-2])
			try:
				await handle_private(message,chatid,msgid,username)
			except Exception as e:
				await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
		else:
			#public chat
			username = datas[-2]
			msg  = await bot.get_messages(username,msgid)
			try:
				await bot.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id)
			except:
				try:
					await handle_private(message,username,msgid,username)
				except Exception as e:
					await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

	else: #"https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text
		print("enlace")
		try:
			try:
				await userbot.join_chat(message.text)
			except Exception as e: 
				await bot.send_message(user_id,f"**Error** : __{e}__", reply_to_message_id=message.id)
				return
			await bot.send_message(user_id,"**Chat Joined**", reply_to_message_id=message.id)
		except UserAlreadyParticipant:
			await bot.send_message(user_id,"**Chat alredy Joined**", reply_to_message_id=message.id)
		except InviteHashExpired:
			await bot.send_message(user_id,"**Invalid Link**", reply_to_message_id=message.id)
try:
	os.unlink("bot.session")
except:pass
try:
	os.unlink("bot.session-journal")
except:pass

print("started")
bot.start()
userbot.start()
print(10)
bot.loop.run_forever()
userbot.run_forever()