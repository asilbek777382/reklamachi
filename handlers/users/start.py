import os
import uuid

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, ContentType

from keyboards.inline.boshi import boshi


from loader import dp, bot,db
from states.kirish import kirish, xabar_sozlash_state, tastiq, xabar_set_bol, kanal, xabarn_sozlash

from aiogram import types

from aiogram.types import ChatType




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message,state:FSMContext):
    # select = db.select_message()
    # await message.answer(select)
    if message.chat.type == ChatType.PRIVATE:
        try:
            a = db.select_user(user_id=message.from_user.id)
            if a:
                print(1)

                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"🏻 Assalomu alaykum {message.from_user.last_name} \nGroup Help sizning guruhlaringizni oson va xavfsiz boshqarish uchun eng takomillashgan botdir!\n\n👉🏻 Botni guruhingizga qo'shing va ishga tushishi uchun Admin huquqini bering!\n\n❓ QANDAY BUYRUQLAR BOR?\n Barcha buyruqlarni ko'rish va ular qanday ishlashini bilish uchun /help buyrug'ini yuboring!\n\n📃 Privacy policy )",
                                       reply_markup=boshi)
                await state.finish()
            else:
                print(2)
                b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
                await kirish.login.set()
                but_id = await state.update_data({'but_id': b.message_id})
                await kirish.login.set()

                # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")

        except:

            print(3)
            # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")
            b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
            but_id=await state.update_data({'but_id':b.message_id})
            await kirish.login.set()






    elif message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:

        # Guruh ID sini oling

        group_id = message.chat.id

        # Botning o'zi guruhda adminmi yoki yo'qmi tekshiramiz

        bot_member = await bot.get_chat_member(message.chat.id, bot.id)

        if bot_member.status in ['administrator', 'creator']:

            # Agar bot admin yoki yaratuvchi bo'lsa, foydalanuvchini tekshiramiz

            chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

            if chat_member.is_chat_admin():

                # Admin yoki yaratuvchi bo'lsa, foydalanuvchini ma'lumotlarini chiqaramiz

                user_info = f"Foydalanuvchi: {message.from_user.full_name}\nID: {message.from_user.id}\nGuruh ID: {group_id}\nAdmin yoki Yaratuvchi"

                await bot.send_message(chat_id=message.chat.id,text=f'Salom {message.from_user.first_name}! \nMeni guruhga sozlash uchun, /set dan foydalaning.')

                print(user_info)

            else:

                # Agar foydalanuvchi admin bo'lmasa

                await bot.send_message(chat_id=message.from_user.id, text=
                    "Siz botni ishlata olmaysiz, faqat admin yoki guruh yaratuvchisi foydalanishi mumkin.")

        else:

            # Agar bot admin bo'lmasa

            await bot.send_message(chat_id=message.from_user.id,text="Iltimos, botni admin qiling, shunda men ishlay olaman.")

    else:

        await bot.send_message(chat_id=message.from_user.id,text="Bu buyruq faqat shaxsiy chat va guruhlarda ishlaydi.")



@dp.callback_query_handler(text='chiqish')
async def start(message: CallbackQuery, state: FSMContext):
        await message.message.delete()
        v = db.delete_sh(user_id=message.from_user.id)

        await message.answer(text='Siz muvaffaqiyatli ravshta chiqib ketdingiz.', show_alert=True)
        b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
        await kirish.login.set()
        but_id = await state.update_data({'but_id': b.message_id})
        await kirish.login.set()


#/set
import urllib.parse
@dp.message_handler(commands=['set'])
async def send_welcome(message: types.Message,state:FSMContext):
    await message.delete()
    if message.chat.type == ChatType.PRIVATE:
        try:
            a = db.select_user(user_id=message.from_user.id)
            if a:
                user_id_to_check = message.from_user.id  # Tekshirmoqchi bo'lgan foydalanuvchi ID'si
                channel_baza = db.select_channels()

                channel_ids = []  # Tekshirmoqchi bo'lgan kanal ID'lari

                for channel in channel_baza:
                    channel_ids.append(channel[8])  # Kanal ID'sini oladi

                channels = []
                channel_ids_found = []

                for channel_id in channel_ids:
                    try:
                        administrators = await bot.get_chat_administrators(channel_id)

                        if any(admin.user.id == user_id_to_check for admin in administrators):
                            chat = await bot.get_chat(channel_id)

                            # Agar kanal ro'yxatda yo'q bo'lsa, qo'shadi
                            if chat.title not in channels:
                                channels.append(chat.title)
                                channel_ids_found.append(channel_id)

                    except Exception as e:
                        print('xato id tekshirish')

                if channels:
                    # Tugmalar yaratish
                    keyboard = InlineKeyboardMarkup(row_width=1)  # Har bir qator uchun 1 ta tugma
                    for channel, channel_id in zip(channels, channel_ids_found):
                        # Kanal nomidagi maxsus belgilarni to'g'ri yuborish uchun URL orqali kodlash
                        encoded_channel_name = urllib.parse.quote_plus(channel)
                        callback_data = f"kanal:{channel_id}:{user_id_to_check}:{encoded_channel_name}"
                        button = InlineKeyboardButton(text=channel, callback_data=callback_data)
                        keyboard.add(button)

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Guruh sozlamalari:\nQuyidagi kanallardan birini tanlang:",
                                           reply_markup=keyboard)
                    await kanal.kanal.set()

                else:
                    await bot.send_message(chat_id=message.from_user.id, text="Siz hali hech qanday kanal qo'shganingiz yo'q.")

            else:
                print(2)
                b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
                await kirish.login.set()
                but_id = await state.update_data({'but_id': b.message_id})
                await kirish.login.set()

                # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")

        except:

            print(3)
            # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")
            b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
            but_id=await state.update_data({'but_id':b.message_id})
            await kirish.login.set()

    elif message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:

        # Guruh ID sini oling

        group_id = message.chat.id

        # Botning o'zi guruhda adminmi yoki yo'qmi tekshiramiz

        bot_member = await bot.get_chat_member(message.chat.id, bot.id)

        if bot_member.status in ['administrator', 'creator']:

            # Agar bot admin yoki yaratuvchi bo'lsa, foydalanuvchini tekshiramiz

            chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

            if chat_member.is_chat_admin():

                # Admin yoki yaratuvchi bo'lsa, foydalanuvchini ma'lumotlarini chiqaramiz

                user_info = f"Foydalanuvchi: {message.from_user.full_name}\nID: {message.from_user.id}\nGuruh ID: {group_id}\nAdmin yoki Yaratuvchi"

                bot_info = await bot.get_me()
                bot_username = bot_info.username
                m = await bot.send_message(chat_id=message.chat.id,
                                                text='Sozlamalar menyusi shaxsiy suhbatga yuborildi',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                                                                                       InlineKeyboardButton(
                                                                                                           text="👉 Botga o'tish",                                                                                   url=f"https://t.me/{bot_username}")]]))
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Sizning guruhingiz: {message.chat.full_name} \n\nTanlang:",
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                           InlineKeyboardButton(text="🕘 Takroriy xabarlar",
                                                                callback_data=f'tak_xabar:{message.chat.id}:{message.from_user.id}:{message.chat.full_name}')]]))
                await state.finish()
                d = time.sleep(5)
                await bot.delete_message(chat_id=message.chat.id, message_id=m.message_id)

                print(user_info)

            else:

                # Agar foydalanuvchi admin bo'lmasa

                await message.reply(
                    "Siz botni ishlata olmaysiz, faqat admin yoki guruh yaratuvchisi foydalanishi mumkin.")

        else:

            # Agar bot admin bo'lmasa

            await message.reply(text="Iltimos, botni admin qiling, shunda men ishlay olaman.")

    else:

        await message.reply(text="Bu buyruq faqat shaxsiy chat va guruhlarda ishlaydi.")

import time






@dp.callback_query_handler(state=kanal.kanal)
async def on_chat_member_update(message: CallbackQuery,state:FSMContext):
    mal=message.data.rsplit(":")
    kanal_id=mal[1]

    if mal[0]=='kanal':
        await message.message.delete()

        a = time.localtime()  # Hozirgi vaqtni olish

        try:

            sele = db.select_message(users_id=message.from_user.id, gurux_id=kanal_id)

            # Xabar matnini tayyorlash

            xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
            xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

            son = 1  # Boshlang'ich qiymat

            # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
            tugmalar = []

            for select in sele:
                va = select[11]
                vaqt = va.split(':')

                if select[10] == 'off':  # Agar holat "off" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ O'chiq ❌\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                             callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="O'chiq ❌",
                                             callback_data=f"status_off:{select[0]}:{mal[1]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[1]}:{mal[2]}")
                    ])
                elif select[10] == 'on':  # Agar holat "on" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ Faol ✅\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                             callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[1]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[1]}:{mal[2]}")
                    ])

                son += 1

            # Xabarni yuborish
            # await bot.send_message(chat_id=message.from_user.id,text=sele)
            messagee = await bot.send_message(
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                    [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                          callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')],
                    [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                    [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                ])
            )

            # Davlatni yangilash
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'chat_id': mal[1]})
            await state.update_data({'message_id': messagee.message_id})

        except:

            tugma = await bot.send_message(chat_id=message.from_user.id,
                                           text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                               text="➕ Xabar qo'shish",
                                               callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')], [
                                                                                                  InlineKeyboardButton(
                                                                                                      text='Tayyor 👌',
                                                                                                      callback_data='tayyor')],
                                                                                              [InlineKeyboardButton(
                                                                                                  text='🔙 Ortga',
                                                                                                  callback_data='ortga')]]))
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'message_id': tugma.message_id})
            await state.update_data({'chat_id': mal[1]})


    if mal[0]=='/start':
        try:
            a = db.select_user(user_id=message.from_user.id)
            if a:
                print(1)

                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"🏻 Assalomu alaykum {message.from_user.last_name} \nGroup Help sizning guruhlaringizni oson va xavfsiz boshqarish uchun eng takomillashgan botdir!\n\n👉🏻 Botni guruhingizga qo'shing va ishga tushishi uchun Admin huquqini bering!\n\n❓ QANDAY BUYRUQLAR BOR?\n Barcha buyruqlarni ko'rish va ular qanday ishlashini bilish uchun /help buyrug'ini yuboring!\n\n📃 Privacy policy )",
                                       reply_markup=boshi)
                await state.finish()
            else:
                print(2)
                b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
                await kirish.login.set()
                but_id = await state.update_data({'but_id': b.message_id})
                await kirish.login.set()

                # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")

        except:

            print(3)
            # await bot.send_message(chat_id=message.from_user.id,text=text=f"Kechirasiz siz bu botni ishlata olmaysiz.")
            b=await bot.send_message(chat_id=message.from_user.id, text='Loginni kiriting:')
            but_id=await state.update_data({'but_id':b.message_id})
            await kirish.login.set()
        mal=await state.get_data()
        mes_id=mal.get("mes_id")

        if message.message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:

            bot_info = await bot.get_me()
            bot_username = bot_info.username
            m=await bot.edit_message_text(message_id=mes_id,chat_id=message.message.chat.id,text='Sozlamalar menyusi shaxsiy suhbatga yuborildi',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="👉 Botga o'tish",url=f"https://t.me/{bot_username}")]]))
            a = time.localtime()

            await bot.send_message(chat_id=message.from_user.id,text=f"Sizning guruhingiz: {message.message.chat.full_name} \n\nTanlang:",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🕘 Takroriy xabarlar", callback_data=f'tak_xabar:{message.message.chat.id}:{message.from_user.id}:{message.message.chat.full_name}')]]))
            await state.finish()
            d=time.sleep(5)
            await bot.delete_message(chat_id=message.message.chat.id,message_id=m.message_id)






@dp.chat_member_handler()
async def on_chat_member_update(chat_member_updated: ChatMemberUpdated):

        # Faqat bot admin qilinganda amal qiladi


            if chat_member_updated.new_chat_member.user.id == bot.id and chat_member_updated.new_chat_member.is_chat_admin():

                # Kim botni admin qilganini tekshiramiz

                if chat_member_updated.from_user:
                    admin_user_info = f"Botni admin qilgan foydalanuvchi: {chat_member_updated.from_user.full_name}\nID: {chat_member_updated.from_user.id}"

                    print(admin_user_info)

                    await bot.send_message(chat_member_updated.chat.id, "Bot admin qilindi.")

                    await bot.send_message(chat_member_updated.chat.id,
                                           f"Botni admin qilgan foydalanuvchi: {chat_member_updated.from_user.full_name}")

def number_to_emoji(number: int) -> str:
                    # Emojilarni belgilash
                    emoji_map = {
                        '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
                        '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '0': '0️⃣'
                    }

                    # Sonni emoji formatiga o'zgartirish
                    return ''.join(emoji_map.get(digit, '') for digit in str(number))


@dp.callback_query_handler()
async def on_chat_member_update(message: CallbackQuery, state: FSMContext):
    mal = message.data.split(':')  # Callback'dagi ma'lumotlarni ajratish

    try:
        tekshir=db.select_user(user_id=mal[2])

        if mal[0] == 'tak_xabar' and int(mal[2]) == int(message.from_user.id) and tekshir:
            await message.message.delete()

            a = time.localtime()  # Hozirgi vaqtni olish

            try:

                sele = db.select_message(users_id=message.from_user.id, gurux_id=mal[1])


                # Xabar matnini tayyorlash

                xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
                xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

                son = 1  # Boshlang'ich qiymat

                # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
                tugmalar = []

                for select in sele:
                    va =select[11]
                    vaqt=va.split(':')

                    if select[10] == 'off':  # Agar holat "off" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ O'chiq ❌\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="O'chiq ❌", callback_data=f"status_off:{select[0]}:{mal[1]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[1]}:{mal[2]}")
                        ])
                    elif select[10] == 'on':  # Agar holat "on" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ Faol ✅\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[1]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[1]}:{mal[2]}")
                        ])

                    son += 1

                # Xabarni yuborish
                # await bot.send_message(chat_id=message.from_user.id,text=sele)
                messagee=await bot.send_message(
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                        [InlineKeyboardButton(text="➕ Xabar qo'shish", callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],
                        [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                    ])
                )

                # Davlatni yangilash

                await xabar_sozlash_state.boshi.set()
                await state.update_data({'chat_id': mal[1]})
                await state.update_data({'message_id': messagee.message_id})

            except:




                    tugma=await bot.send_message(chat_id=message.from_user.id,text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ Xabar qo'shish",callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],[InlineKeyboardButton(text='🔙 Ortga',callback_data='ortga')]]))
                    await xabar_sozlash_state.boshi.set()
                    await state.update_data({'message_id':tugma.message_id})
                    await state.update_data({'chat_id': mal[1]})


    except:
        await message.message.delete()
        await message.message.answer("Siz bu funksiyani ishlatish uchun botda ro'yxatdan o'tgan bo'lishingiz kerak")

        await state.finish()

            # except:
            #

@dp.callback_query_handler(state=xabar_sozlash_state.boshi,text='tayyor')
async def start(message: CallbackQuery, state: FSMContext):
    await message.message.delete()
    await message.message.answer("Sozlamalar o'chgartirildi")
    await state.finish()

@dp.callback_query_handler(state=xabar_sozlash_state.boshi,text='ortga')
async def start(message: CallbackQuery, state: FSMContext):
    await message.message.delete()
    await message.message.answer("Sozlamalar o'chgartirildi")
    await state.finish()


@dp.callback_query_handler(state=xabar_sozlash_state.boshi)
async def start(message: CallbackQuery, state: FSMContext):
    mal=message.data.rsplit(':')

    mes_id=await state.get_data()
    message_id=mes_id.get('message_id')
    a=time.localtime()

    if mal[0]=='status_on':
        db.update_xabar(id=mal[1],xolati='off')
        try:
            sele = db.select_message(users_id=message.from_user.id, gurux_id=mal[2])

            # Xabar matnini tayyorlash
            xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
            xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

            son = 1  # Boshlang'ich qiymat

            # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
            tugmalar = []

            for select in sele:
                va = select[11]
                vaqt = va.split(':')

                if select[10] == 'off':  # Agar holat "off" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ O'chiq ❌\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="O'chiq ❌",
                                             callback_data=f"status_off:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])
                elif select[10] == 'on':  # Agar holat "on" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ Faol ✅\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])

                son += 1

            # Xabarni yuborish
            # await bot.send_message(chat_id=message.from_user.id,text=sele)
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                    [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                          callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],
                    [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                    [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                ])
            )

            # Davlatni yangilash
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})

        except Exception:
            await message.answer('starus_on_salom')
            tugma = await bot.send_message(chat_id=message.from_user.id,
                                           text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                               text="➕ Xabar qo'shish",
                                               callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')], [
                                                                                                  InlineKeyboardButton(
                                                                                                      text='Tayyor 👌',
                                                                                                      callback_data='tayyor')],
                                                                                              [InlineKeyboardButton(
                                                                                                  text='🔙 Ortga',
                                                                                                  callback_data='ortga')]]))
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'message_id': tugma.message_id})
            await state.update_data({'chat_id': mal[2]})

    if mal[0] == 'status_off':
        db.update_xabar(id=mal[1], xolati='on')
        try:
            sele = db.select_message(users_id=message.from_user.id, gurux_id=mal[2])

            # Xabar matnini tayyorlash
            xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
            xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

            son = 1  # Boshlang'ich qiymat

            # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
            tugmalar = []

            for select in sele:
                va = select[11]
                vaqt = va.split(':')

                if select[10] == 'off':  # Agar holat "off" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ O'chiq ❌\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="O'chiq ❌",
                                             callback_data=f"status_off:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])
                elif select[10] == 'on':  # Agar holat "on" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ Faol ✅\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])

                son += 1

            # Xabarni yuborish
            # await bot.send_message(chat_id=message.from_user.id,text=sele)
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                    [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                          callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],
                    [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                    [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                ])
            )

            # Davlatni yangilash
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})

        except:

            await message.answer('status_off_salom')
            tugma = await bot.send_message(chat_id=message.from_user.id,
                                           text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                               text="➕ Xabar qo'shish",
                                               callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')], [
                                               InlineKeyboardButton(
                                                   text='Tayyor 👌',
                                                   callback_data='tayyor')],
                                               [InlineKeyboardButton(
                                                   text='🔙 Ortga',
                                                   callback_data='ortga')]]))

            await xabar_sozlash_state.boshi.set()
            await state.update_data({'message_id': tugma.message_id})
            await state.update_data({'chat_id': mal[2]})
    if mal[0]=='delete_xabar':


        klaviatura = InlineKeyboardMarkup(row_width=1)
        klaviatura.add(
            InlineKeyboardButton("✅ O'chirish", callback_data=f'tastiq_xa:{mal[1]}:{mal[2]}'),
            InlineKeyboardButton("❌ O'chirmaslik", callback_data=f'tastiq_yoq:{mal[1]}:{mal[2]}')
        )
        messagee = await bot.edit_message_text(
            message_id=message_id,
            chat_id=message.from_user.id,
            text="O'chirishga ishonchingiz komilmi?",
            reply_markup=klaviatura)

        # Davlatni yangilash
        await xabar_sozlash_state.boshi.set()
        await state.update_data({'chat_id': mal[2]})
        await state.update_data({'message_id': messagee.message_id})
        await tastiq.tastiq.set()

    if mal[0] == 'xabar_set_bol':

        mal = message.data.rsplit(':')
        message_id_ol = await state.get_data('message_id')
        message_id = message_id_ol.get('message_id')
        select = db.select_message(users_id=message.from_user.id, id=mal[1])

        off = '❌'
        on = '✅'

        xabar_text = f"🕑 Takroriy xabarlar\n\n"
        for selet in select:
            # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
            print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

            # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
            xabar_qadash = on if selet[6] == 'on' else off
            songgi_xabar_ochirish = on if selet[7] == 'on' else off

            va = selet[11]
            vaqt = va.split(':')

            a = time.localtime()
            xabar_text += f"💡 Holat: {selet[10]}\n"
            xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
            xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
            xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
            xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

        # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
        messagee = await bot.edit_message_text(
            message_id=message_id,
            chat_id=message.from_user.id,
            text=xabar_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[1]}:{selet[6]}'),
                ],
                [
                    InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[1]}:{selet[6]}'),
                ],
                [
                    InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[1]}:{selet[6]}'),
                ],
                [
                    InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                         callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
                ],
                [
                    InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                         callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
                ],
                [
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                ]
            ])
        )

        # Davlatni yangilash
        await xabar_set_bol.xabar_set_bol.set()
        await state.update_data({'chat_id': mal[1]})
        await state.update_data({'message_id': messagee.message_id})

    mal=message.data.rsplit(':')

    a=time.localtime()
    malu=await state.get_data()
    chat_id_ol=malu.get('chat_id')
    if mal[0]=='xabar_qoshish':

        try:
            db.add_message(gurux_id=chat_id_ol, users_id=message.from_user.id, xolati='off',
                           matn="Xabar o'rnatilmagan.",
                           rasm='None', video='None', url_tugmachalar='None', vaqt='24:soat', tugash_sanasi='None',
                           xabarni_qadash='off', songgi_xabarni_ochirish='off')








            await xabar_sozlash_state.boshi.set()

            sele = db.select_message(users_id=message.from_user.id, gurux_id=chat_id_ol)

            # Xabar matnini tayyorlash

            xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
            xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

            son = 1  # Boshlang'ich qiymat

            # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
            tugmalar = []

            for select in sele:
                va = select[11]
                vaqt = va.split(':')

                if select[10] == 'off':  # Agar holat "off" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ O'chiq ❌\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="O'chiq ❌", callback_data=f"status_off:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])
                elif select[10] == 'on':  # Agar holat "on" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ Faol ✅\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                    ])

                son += 1

            # Xabarni yuborish
            # await bot.send_message(chat_id=message.from_user.id,text=sele)
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                    [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                          callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],
                    [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                    [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                ])
            )



            # Davlatni yangilash
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


            # for selekt in sele:
            #     if selekt
        except:

            try:

                sele = db.select_message(users_id=message.from_user.id, gurux_id=chat_id_ol)

                # Xabar matnini tayyorlash

                xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
                xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

                son = 1  # Boshlang'ich qiymat

                # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
                tugmalar = []

                for select in sele:
                    va = select[11]
                    vaqt = va.split(':')

                    if select[10] == 'off':  # Agar holat "off" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ O'chiq ❌\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                                 callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="O'chiq ❌", callback_data=f"status_off:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])
                    elif select[10] == 'on':  # Agar holat "on" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ Faol ✅\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                                 callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])

                    son += 1
                # Xabarni yuborish
                # await bot.send_message(chat_id=message.from_user.id,text=sele)
                messagee=await bot.send_message(
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                        [InlineKeyboardButton(text="➕ Xabar qo'shish", callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],
                        [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                    ])
                )


                # Davlatni yangilash
                await xabar_sozlash_state.boshi.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})

            except:




                    tugma=await bot.send_message(chat_id=message.from_user.id,text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ Xabar qo'shish",callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],[InlineKeyboardButton(text='🔙 Ortga',callback_data='ortga')]]))

                    await xabar_sozlash_state.boshi.set()
                    await state.update_data({'message_id':tugma.message_id})
                    await state.update_data({'chat_id': mal[2]})
                    await message.answer(2.2)



















@dp.callback_query_handler(state=xabar_set_bol.xabar_set_bol)
async def start(message: CallbackQuery, state: FSMContext):

    mal=message.data.split(':')
    a=time.localtime()

    chat_id2=await state.get_data()
    chat_id=chat_id2.get('chat_id')
    message_id_ol = await state.get_data()
    message_idd = message_id_ol.get('message_id')

    gurux_id = db.select_message_one(users_id=message.from_user.id, id=chat_id)


    if mal[0]=='ortga':

        try:

            sele = db.select_message(users_id=message.from_user.id, gurux_id=gurux_id[8])



            xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
            xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

            son = 1  # Boshlang'ich qiymat

            # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
            tugmalar = []

            for select in sele:
                va = select[11]
                vaqt = va.split(':')

                if select[10] == 'off':  # Agar holat "off" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ O'chiq ❌\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                             callback_data=f"xabar_set_bol:{select[0]}:{gurux_id[8]}"),
                        InlineKeyboardButton(text="O'chiq ❌",
                                             callback_data=f"status_off:{select[0]}:{gurux_id[8]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{gurux_id[8]}")
                    ])
                elif select[10] == 'on':  # Agar holat "on" bo'lsa
                    xabar_text += f"🗯{number_to_emoji(son)}\n"
                    xabar_text += f"├ Faol ✅\n"
                    xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                    xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                    xabar_text += f"└ {select[1]}\n\n"

                    # Tugmalarni qo'shish
                    tugmalar.append([
                        InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}",
                                             callback_data=f"xabar_set_bol:{select[0]}:{gurux_id[8]}"),
                        InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{gurux_id[8]}"),
                        InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{gurux_id[8]}")
                    ])

                son += 1

            # Xabarni yuborish
            # await bot.send_message(chat_id=message.from_user.id,text=sele)
            message_id_ol=await state.get_data()
            message_id=message_id_ol.get('message_id')

            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                    [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                          callback_data=f'xabar_qoshish:{message.message.message_id}:{gurux_id[8]}')],
                    [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                    [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                ])
            )


            # Davlatni yangilash
            await xabar_sozlash_state.boshi.set()
            await state.update_data({'chat_id': gurux_id[8]})
            await state.update_data({'message_id': messagee.message_id})

        except:

            tugma = await bot.send_message(chat_id=message.from_user.id,
                                           text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                               text="➕ Xabar qo'shish",
                                               callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[1]}')], [
                                                                                                  InlineKeyboardButton(
                                                                                                      text='Tayyor 👌',
                                                                                                      callback_data='tayyor')],
                                                                                              [InlineKeyboardButton(
                                                                                                  text='🔙 Ortga',
                                                                                                  callback_data='ortga')]]))

            await xabar_sozlash_state.boshi.set()
            await state.update_data({'message_id': tugma.message_id})
            await state.update_data({'chat_id': {gurux_id[8]}})

    if mal[0] == 'xabarni_qadash':

        if mal[2] == 'on':

            db.update_xabarni_qadash(xabarni_qadash='off', id=mal[1])

            mal = message.data.rsplit(':')
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            select = db.select_message(users_id=message.from_user.id, id=mal[1])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
                print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

                # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
                xabar_qadash = on if selet[6] == 'on' else off
                songgi_xabar_ochirish = on if selet[7] == 'on' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"💡 Holat: {selet[10]}\n"
                xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
                xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
                xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
                xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                             callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                             callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
                    ],
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabar_set_bol.xabar_set_bol.set()
            await state.update_data({'chat_id': mal[1]})
            await state.update_data({'message_id': messagee.message_id})

        if mal[2] == 'off':

            db.update_xabarni_qadash(xabarni_qadash='on', id=mal[1])

            mal = message.data.rsplit(':')
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            select = db.select_message(users_id=message.from_user.id, id=mal[1])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
                print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

                # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
                xabar_qadash = on if selet[6] == 'on' else off
                songgi_xabar_ochirish = on if selet[7] == 'on' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"💡 Holat: {selet[10]}\n"
                xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
                xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
                xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
                xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                             callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                             callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
                    ],
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabar_set_bol.xabar_set_bol.set()
            await state.update_data({'chat_id': mal[1]})
            await state.update_data({'message_id': messagee.message_id})

    if mal[0] == 'songgi_xabarni_ochirish':

        if mal[2] == 'on':

            db.update_songgi_xabarni_ochirish(songgi_xabarni_ochirish='off', id=mal[1])

            mal = message.data.rsplit(':')
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            select = db.select_message(users_id=message.from_user.id, id=mal[1])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
                print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

                # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
                xabar_qadash = on if selet[6] == 'on' else off
                songgi_xabar_ochirish = on if selet[7] == 'on' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"💡 Holat: {selet[10]}\n"
                xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
                xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
                xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
                xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                             callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                             callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
                    ],
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabar_set_bol.xabar_set_bol.set()
            await state.update_data({'chat_id': mal[1]})
            await state.update_data({'message_id': messagee.message_id})

        if mal[2] == 'off':

            db.update_songgi_xabarni_ochirish(songgi_xabarni_ochirish='on', id=mal[1])

            mal = message.data.rsplit(':')
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            select = db.select_message(users_id=message.from_user.id, id=mal[1])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
                print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

                # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
                xabar_qadash = on if selet[6] == 'on' else off
                songgi_xabar_ochirish = on if selet[7] == 'on' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"💡 Holat: {selet[10]}\n"
                xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
                xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
                xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
                xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                             callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                             callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
                    ],
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabar_set_bol.xabar_set_bol.set()
            await state.update_data({'chat_id': mal[1]})
            await state.update_data({'message_id': messagee.message_id})











    if mal[0]=='xabarn_sozlash':
        await xabarn_sozlash.xabarn_sozlash.set()



        select = db.select_message(users_id=message.from_user.id, id=mal[1])

        off = '❌'
        on = '✅'

        xabar_text = f"🕑 Takroriy xabarlar\n\n"
        for selet in select:

            matn = on if selet[1] != "Xabar o'rnatilmagan." else off
            media = on if selet[2] and selet[3] != 'None' else off
            url_tugma = on if selet[4] != 'None' else off

            va = selet[11]
            vaqt = va.split(':')

            a = time.localtime()
            xabar_text += f"📄 Matn: {matn}\n"
            xabar_text += f"📸 Media : {media}\n"
            xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

        # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
        message_id_ol = await state.get_data('message_id')
        message_id = message_id_ol.get('message_id')
        messagee = await bot.edit_message_text(
            message_id=message_id,
            chat_id=message.from_user.id,
            text=xabar_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[1]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish", callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[1]}"),
                ],
                [
                    InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[1]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish", callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[1]}"),
                ],
                [
                    InlineKeyboardButton("🔠 URL tugmachalar", callback_data=f'url_tugma:{message.from_user.id}:{mal[1]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish", callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[1]}"),
                ],

                [
                    InlineKeyboardButton(f"👀 To'liq ko'rish",
                                         callback_data=f'toliq_korish:{message.from_user.id}:{mal[1]}'),
                ],

                [
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
                ]
            ])
        )

        # Davlatni yangilash

        await state.update_data({'chat_id': mal[1]})
        await state.update_data({'message_id': messagee.message_id})


# Lambda orqali markup yaratish
markup = lambda button_data: types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=name.strip(), url=url.strip())]
        for item in button_data if item.strip() and len(item.split('-')) == 2
        for name, url in [item.split('-')]
    ]
)





from aiogram.types import InputMediaPhoto, InputFile,InputMediaVideo
@dp.callback_query_handler(state=xabarn_sozlash.xabarn_sozlash)
async def start(message: CallbackQuery, state: FSMContext):

        mal = message.data.rsplit(':')
        message_id_ol = await state.get_data('message_id')
        message_id = message_id_ol.get('message_id')
        if mal[0] == 'ortga':

            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
                print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")

                # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
                xabar_qadash = on if selet[6] == 'on' else off
                songgi_xabar_ochirish = on if selet[7] == 'on' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"💡 Holat: {selet[10]}\n"
                xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
                xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
                xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
                xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("✍️ Xabarni sozlash", callback_data=f'xabarn_sozlash:{mal[2]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("🔄 Takrorlash", callback_data=f'takrorlash:{mal[2]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton("⏲ Tugash sanasi", callback_data=f'tugash_sanasi:{mal[2]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
                                             callback_data=f'xabarni_qadash:{mal[2]}:{selet[6]}'),
                    ],
                    [
                        InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
                                             callback_data=f'songgi_xabarni_ochirish:{mal[2]}:{selet[7]}'),
                    ],
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabar_set_bol.xabar_set_bol.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


        if mal[0]=='matn':

            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee=await bot.edit_message_text(chat_id=message.from_user.id,message_id=message_id,text="👉🏻 Sozlamoqchi bo'lgan xabarni hoziroq yuboring.\nSiz uni allaqachon formatlashtirilgan holda yuborishingiz yoki HTML-dan foydalanishingiz mumkin.",reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='🚫 Xabarni olib tashlash',callback_data=f'xabarni_olib_tashlash:{message.from_user.id}:{mal[2]}')
                    ],
                    [
                        InlineKeyboardButton(text='❌ Xabarni bekor qilish', callback_data=f'xabarni_bekor_qilish:{message.from_user.id}:{mal[2]}')
                    ]
                ]
            ))
            await xabarn_sozlash.matn.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})



        if mal[0]=='media':

            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee=await bot.edit_message_text(chat_id=message.from_user.id,message_id=message_id,text="👉🏻 O'zingiz o'rnatmoqchi bo'lgan ommaviy axborot vositalarini \nyuboring  (fotosuratlar, videolar)).",reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='🚫 Xabarni olib tashlash',callback_data=f'xabarni_olib_tashlash:{message.from_user.id}:{mal[2]}')
                    ],
                    [
                        InlineKeyboardButton(text='❌ Xabarni bekor qilish', callback_data=f'xabarni_bekor_qilish:{message.from_user.id}:{mal[2]}')
                    ]
                ]
            ))
            await xabarn_sozlash.media.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})



        if mal[0]=='url_tugma':

            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text="👉🏻 Yaxshi, endi matnlarni va havolalarni inline klaviaturaga kiritish uchun tugmalar ro'yxatini quyidagi holatda yuboring:\n\n`Tugma nomi - havola`\n`Tugma nomi - havola`\n\n• Agar siz bitta qatorda 2 tugmachani o'rnatmoqchi bo'lsangiz, ularni `||` (bo'sh joysiz) ushbu belgi bilan ajrating.\n• Agar guruhingizda Qoidalar boʻlimi faol bo'lsa, siz inline tugmaga guruh qoidalarini biriktirishingiz mumkin, buning uchun `Tugma nomi - Rules` shaklida yuboring.\n\nMisol uchun:\n`Guruh - t.me/username && Kanal - @username`\n`Guruh qoidalari - rules`",
                parse_mode="MARKDOWN",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='🚫 Xabarni olib tashlash',
                                                 callback_data=f'xabarni_olib_tashlash:{message.from_user.id}:{mal[2]}')
                        ],
                        [
                            InlineKeyboardButton(text='❌ Xabarni bekor qilish',
                                                 callback_data=f'xabarni_bekor_qilish:{message.from_user.id}:{mal[2]}')
                        ]
                    ]
                )
            )


            await xabarn_sozlash.url_tugma.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


        if mal[0]=="xabarni_korish_matn":
            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])
            if selet[1] =="Xabar o'rnatilmagan." and selet[2] == 'None' and selet[3] =='None' and selet[4] == "None":
                await message.answer("Xabar o'rnatilmagan.",show_alert=True)
            else:
                messagee=await bot.edit_message_text(chat_id=message.from_user.id,message_id=message_id,text=selet[1],reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga_matn_kor:{message.from_user.id}:{mal[2]}')
                    ]
                    ]
                ))
                await xabarn_sozlash.xabarn_sozlash.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})



        if mal[0]=="xabarni_korish_url_tugma":
            mal = message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')

            # Ma'lumotlar bazasidan xabarni olish
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])

            # Xabarlar bo'sh yoki noto'g'ri bo'lsa
            if selet[4] == "None":
                await message.answer("Xabar to'liq o'rnatilmagan.", show_alert=True)
            else:
                # InlineKeyboardMarkup yaratish
                markup = lambda button_data: types.InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [types.InlineKeyboardButton(text=name.strip(), url=url.strip())]
                                        for item in button_data if item.strip() and len(item.split('-')) == 2
                                        for name, url in [item.split('-')]
                                        if url.strip().startswith("http")  # Faqat to'g'ri URL'larni qo'shish
                                    ] + [[types.InlineKeyboardButton(text="🔙 Ortga",
                                                                     callback_data=f"ortga_url_tugma:{message.from_user.id}:{mal[2]}")]]
                )

                # Tugma ma'lumotlarini olish va ajratish
                button_info = selet[4]  # bu yerda sizning tugma ma'lumotlaringiz bo'lishi kerak
                button_data = button_info.split('||')  # agar qatorlar '||' bilan ajratilgan bo'lsa

                # `markup` natijasini `reply_markup`ga uzatish
                messagee = await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=message_id,
                    text="Tugmalar ro'yxati:",
                    reply_markup=markup(button_data)  # Natijani uzatyapmiz
                )

                # Holatni yangilash
                await xabarn_sozlash.xabarn_sozlash.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})




        if mal[0] == "toliq_korish":
                mal = message.data.rsplit(":")
                message_id_ol = await state.get_data('message_id')
                message_id = message_id_ol.get('message_id')

                # Ma'lumotlar bazasidan xabarni olish
                selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])

                # Xabarlar bo'sh yoki noto'g'ri bo'lsa



                if selet[1] == "Xabar o'rnatilmagan." and selet[2] == 'None' and selet[3] == 'None' and selet[4] == "None":
                    await message.answer("Xabar to'liq o'rnatilmagan.", show_alert=True)

                else:
                    # InlineKeyboardMarkup yaratish
                    markup = lambda button_data: types.InlineKeyboardMarkup(
                        inline_keyboard=[
                                            [types.InlineKeyboardButton(text=name.strip(), url=url.strip())]
                                            for item in button_data if item.strip() and len(item.split('-')) == 2
                                            for name, url in [item.split('-')]
                                            if url.strip().startswith("http")  # Faqat to'g'ri URL'larni qo'shish
                                        ] + [[types.InlineKeyboardButton(text="🔙 Ortga",
                                                                         callback_data=f"ortga_toliq_korish:{message.from_user.id}:{mal[2]}")]]
                    )

                    # Tugma ma'lumotlarini olish va ajratish
                    button_info = selet[4]  # bu yerda sizning tugma ma'lumotlaringiz bo'lishi kerak
                    button_data = button_info.split('||')  # agar qa
                    if selet[2] != 'None':

                        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
                        photo = InputFile(f'media/{selet[2]}')
                        messagee = await bot.send_photo(chat_id=message.from_user.id,caption=selet[1],
                                                        reply_markup=markup(button_data), photo=photo)

                        await xabarn_sozlash.xabarn_sozlash.set()
                        await state.update_data({'chat_id': mal[2]})
                        await state.update_data({'message_id': messagee.message_id})
                    else:
                        # InlineKeyboardMarkup yaratish
                        markup = lambda button_data: types.InlineKeyboardMarkup(
                            inline_keyboard=[
                                                [types.InlineKeyboardButton(text=name.strip(), url=url.strip())]
                                                for item in button_data if item.strip() and len(item.split('-')) == 2
                                                for name, url in [item.split('-')]
                                                if url.strip().startswith("http")  # Faqat to'g'ri URL'larni qo'shish
                                            ] + [[types.InlineKeyboardButton(text="🔙 Ortga",
                                                                             callback_data=f"ortga_toliq_korish:{message.from_user.id}:{mal[2]}")]]
                        )

                        # Tugma ma'lumotlarini olish va ajratish
                        button_info = selet[4]  # bu yerda sizning tugma ma'lumotlaringiz bo'lishi kerak
                        button_data = button_info.split('||')  # agar qa
                        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
                        video = InputFile(f'media/{selet[3]}')
                        sal = await message.message.answer('Media yuborilmoqda kuting.⌛️')
                        messagee = await bot.send_video(chat_id=message.from_user.id,caption=selet[1],
                                        reply_markup=markup(button_data), video=video)
                        await bot.delete_message(chat_id=message.from_user.id, message_id=sal.message_id)
                        await xabarn_sozlash.xabarn_sozlash.set()
                        await state.update_data({'chat_id': mal[2]})
                        await state.update_data({'message_id': messagee.message_id})

        if mal[0]=="ortga_matn_kor":
            mal = message.data.rsplit(":")
            await xabarn_sozlash.xabarn_sozlash.set()

            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

            # Davlatni yangilash

            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})



        if mal[0]=="xabarni_korish_matn":
            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])
            # if selet[1] == "Xabar o'rnatilmagan." and selet[2] == 'None' and selet[3] == 'None' and selet[4] == "None":
            if selet[1] == "Xabar o'rnatilmagan.":
                await message.answer("Xabar o'rnatilmagan.",show_alert=True)
            else:
                messagee=await bot.edit_message_text(chat_id=message.from_user.id,message_id=message_id,text=selet[1],reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga_matn_kor:{message.from_user.id}:{mal[2]}')
                    ]
                    ]
                ))
                await xabarn_sozlash.xabarn_sozlash.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})

        if mal[0] == "toliq_korish":
            mal = message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])

            if selet[1] == "Xabar o'rnatilmagan." and selet[2] == 'None' and selet[3] == 'None' and selet[4] == "None":
                await message.answer("Xabar to'liq o'rnatilmagan.", show_alert=True)
            else:
                markup = lambda button_data: types.InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [types.InlineKeyboardButton(text=name.strip(), url=url.strip())]
                                        for item in button_data if item.strip() and len(item.split('-')) == 2
                                        for name, url in [item.split('-')]
                                    ] + [[types.InlineKeyboardButton(text="🔙 Ortga", callback_data=f"ortga_toliq_korish:{message.from_user.id}:{mal[2]}")]]
                    # "Ortga" tugmasi qo'shilmoqda
                )

                button_info = selet[4]  # bu yerda sizning tugma ma'lumotlaringiz bo'lishi kerak

                # Ikkita tugma ma'lumotlarini olish
                button_data = button_info.split('||')  # agar qatorlar '||' bilan ajratilgan bo'lsa


                messagee = await bot.edit_message_text(chat_id=message_id,text="Tugmalar ro'yxati:", reply_markup=markup)

                await xabarn_sozlash.xabarn_sozlash.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})

        if mal[0]=="xabarni_korish_media":
            mal=message.data.rsplit(":")
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])
            if selet[2] == 'None' and selet[3] =='None':
                await message.answer("Media o'rnatilmagan.",show_alert=True)
            else:
                if selet[2] !='None':

                    await bot.delete_message(chat_id=message.from_user.id,message_id=message_id)
                    photo = InputFile(f'media/{selet[2]}')
                    messagee=await bot.send_photo(chat_id=message.from_user.id,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga_media_kor:{message.from_user.id}:{mal[2]}')
                        ]
                        ]
                    ),photo=photo)

                    await xabarn_sozlash.xabarn_sozlash.set()
                    await state.update_data({'chat_id': mal[2]})
                    await state.update_data({'message_id': messagee.message_id})
                else:
                    await bot.delete_message(chat_id=message.from_user.id,message_id=message_id)
                    video = InputFile(f'media/{selet[3]}')
                    sal=await message.message.answer('Media yuborilmoqda kuting.⌛️')
                    messagee=await bot.send_video(chat_id=message.from_user.id,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga_media_kor:{message.from_user.id}:{mal[2]}')
                        ]
                        ]
                    ),video=video)
                    await bot.delete_message(chat_id=message.from_user.id,message_id=sal.message_id)
                    await xabarn_sozlash.xabarn_sozlash.set()
                    await state.update_data({'chat_id': mal[2]})
                    await state.update_data({'message_id': messagee.message_id})


        if mal[0]=="url_tugma":
            mal = message.data.rsplit(":")

            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            selet = db.select_message_one(users_id=message.from_user.id, id=mal[2])

            if selet[4] == "None":
                await message.answer("Url tugma o'rnatilmagan.", show_alert=True)
            else:
                if selet[4] != 'None':



                    messagee = await bot.edit_message_text(chat_id=message.from_user.id,message_id=message_id,text=selet[4],
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='🔙 Ortga',
                                                                                 callback_data=f'ortga_media_kor:{message.from_user.id}:{mal[2]}')
                                                        ]
                                                    ]
                                                    ), photo=photo)

                    await xabarn_sozlash.xabarn_sozlash.set()
                    await state.update_data({'chat_id': mal[2]})
                    await state.update_data({'message_id': messagee.message_id})
                else:
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
                    video = InputFile(f'media/{selet[3]}')
                    sal = await message.message.answer('Media yuborilmoqda kuting.⌛️')
                    messagee = await bot.send_video(chat_id=message.from_user.id,
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='🔙 Ortga',
                                                                                 callback_data=f'ortga_media_kor:{message.from_user.id}:{mal[2]}')
                                                        ]
                                                    ]
                                                    ), video=video)
                    await bot.delete_message(chat_id=message.from_user.id, message_id=sal.message_id)
                    await xabarn_sozlash.xabarn_sozlash.set()
                    await state.update_data({'chat_id': mal[2]})
                    await state.update_data({'message_id': messagee.message_id})



        if mal[0] == "ortga_url_tugma":
            mal = message.data.rsplit(":")
            await xabarn_sozlash.xabarn_sozlash.set()

            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

            # Davlatni yangilash

            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


        if mal[0] == "ortga_toliq_korish":
            mal = message.data.rsplit(":")


            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"
            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            await bot.delete_message(chat_id=message.from_user.id,message_id=message_id)
            messagee = await bot.send_message(

                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )
            await xabarn_sozlash.xabarn_sozlash.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


        if mal[0] == "ortga_media_kor":
            mal = message.data.rsplit(":")


            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"
            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            await bot.delete_message(chat_id=message.from_user.id,message_id=message_id)
            messagee = await bot.send_message(

                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

            # Davlatni yangilash
            await xabarn_sozlash.xabarn_sozlash.set()
            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})



        if mal[0]=="ortga_matn_kor":
            mal = message.data.rsplit(":")
            await xabarn_sozlash.xabarn_sozlash.set()

            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

            # Davlatni yangilash

            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})


@dp.callback_query_handler(state=xabarn_sozlash.url_tugma)
async def start(message: CallbackQuery, state: FSMContext):
    mal = message.data.rsplit(":")
    await xabarn_sozlash.xabarn_sozlash.set()

    select = db.select_message(users_id=message.from_user.id, id=mal[2])

    off = '❌'
    on = '✅'

    xabar_text = f"🕑 Takroriy xabarlar\n\n"
    for selet in select:
        matn = on if selet[1] != "Xabar o'rnatilmagan." else off
        media = on if selet[2] and selet[3] != 'None' else off
        url_tugma = on if selet[4] != 'None' else off

        va = selet[11]
        vaqt = va.split(':')

        a = time.localtime()
        xabar_text += f"📄 Matn: {matn}\n"
        xabar_text += f"📸 Media : {media}\n"
        xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

    # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
    message_id_ol = await state.get_data('message_id')
    message_id = message_id_ol.get('message_id')
    messagee = await bot.edit_message_text(
        message_id=message_id,
        chat_id=message.from_user.id,
        text=xabar_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                InlineKeyboardButton("👀 Xabarni ko'rish",
                                     callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
            ],
            [
                InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                InlineKeyboardButton("👀 Xabarni ko'rish",
                                     callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
            ],
            [
                InlineKeyboardButton("🔠 URL tugmachalar",
                                     callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                InlineKeyboardButton("👀 Xabarni ko'rish",
                                     callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
            ],

            [
                InlineKeyboardButton(f"👀 To'liq ko'rish",
                                     callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
            ],

            [
                InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
            ]
        ])
    )

    # Davlatni yangilash

    await state.update_data({'chat_id': mal[2]})
    await state.update_data({'message_id': messagee.message_id})


@dp.message_handler(state=xabarn_sozlash.media,content_types=[ContentType.PHOTO, ContentType.VIDEO])
async def start(message: types.Message , state: FSMContext):
    IMG_DIR, VID_DIR = 'images/', 'videos/'
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(VID_DIR, exist_ok=True)
    if message.content_type == ContentType.PHOTO:
        file_id, ext, folder = message.photo[-1].file_id, 'jpg', IMG_DIR
    elif message.content_type == ContentType.VIDEO:
        file_id, ext, folder = message.video.file_id, 'mp4', VID_DIR

    unique_name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(folder, unique_name)
    await bot.download_file_by_id(file_id, path)
    mal=await state.get_data()
    mal_id=mal.get('chat_id')
    db.update_xabar_matn(matn=path,id=mal_id)
    messagee=await message.reply(text="✅ Xabar o'rnatildi.",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'xabarni_bekor_qilish:{message.from_user.id}:{mal_id}')
                ]]))
    await state.update_data({'chat_id': mal_id})
    await state.update_data({'message_id': messagee.message_id})



@dp.callback_query_handler(state=xabarn_sozlash.media)
async def start(message: CallbackQuery, state: FSMContext):
        mal = message.data.rsplit(":")
        select = db.select_message(users_id=message.from_user.id, id=mal[2])
        if mal[0] == "xabarni_olib_tashlash":
            if select[2]!='None':
                os.remove(f"media/images{select[2]}")
                db.update_xabar_rasm(rasm="None", id=mal[2])
                await xabarn_sozlash.xabarn_sozlash.set()

                select = db.select_message(users_id=message.from_user.id, id=mal[2])

                off = '❌'
                on = '✅'

                xabar_text = f"🕑 Takroriy xabarlar\n\n"
                for selet in select:
                    matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                    media = on if selet[2] and selet[3] != 'None' else off
                    url_tugma = on if selet[4] != 'None' else off

                    va = selet[11]
                    vaqt = va.split(':')

                    a = time.localtime()
                    xabar_text += f"📄 Matn: {matn}\n"
                    xabar_text += f"📸 Media : {media}\n"
                    xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

                # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
                message_id_ol = await state.get_data('message_id')
                message_id = message_id_ol.get('message_id')
                messagee = await bot.edit_message_text(
                    message_id=message_id,
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                        ],
                        [
                            InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                        ],
                        [
                            InlineKeyboardButton("🔠 URL tugmachalar",
                                                 callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                        ],

                        [
                            InlineKeyboardButton(f"👀 To'liq ko'rish",
                                                 callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                        ],

                        [
                            InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                        ]
                    ])
                )
            if select[3]!='None':
                os.remove(f"media/videos{select[2]}")
                db.update_xabar_video(video="None", id=mal[2])
                await xabarn_sozlash.xabarn_sozlash.set()

                select = db.select_message(users_id=message.from_user.id, id=mal[2])

                off = '❌'
                on = '✅'

                xabar_text = f"🕑 Takroriy xabarlar\n\n"
                for selet in select:
                    matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                    media = on if selet[2] and selet[3] != 'None' else off
                    url_tugma = on if selet[4] != 'None' else off

                    va = selet[11]
                    vaqt = va.split(':')

                    a = time.localtime()
                    xabar_text += f"📄 Matn: {matn}\n"
                    xabar_text += f"📸 Media : {media}\n"
                    xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

                # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
                message_id_ol = await state.get_data('message_id')
                message_id = message_id_ol.get('message_id')
                messagee = await bot.edit_message_text(
                    message_id=message_id,
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                        ],
                        [
                            InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                        ],
                        [
                            InlineKeyboardButton("🔠 URL tugmachalar",
                                                 callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                            InlineKeyboardButton("👀 Xabarni ko'rish",
                                                 callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                        ],

                        [
                            InlineKeyboardButton(f"👀 To'liq ko'rish",
                                                 callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                        ],

                        [
                            InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                        ]
                    ])
                )
        else:


            await xabarn_sozlash.xabarn_sozlash.set()

            select = db.select_message(users_id=message.from_user.id, id=mal[2])

            off = '❌'
            on = '✅'

            xabar_text = f"🕑 Takroriy xabarlar\n\n"
            for selet in select:
                matn = on if selet[1] != "Xabar o'rnatilmagan." else off
                media = on if selet[2] and selet[3] != 'None' else off
                url_tugma = on if selet[4] != 'None' else off

                va = selet[11]
                vaqt = va.split(':')

                a = time.localtime()
                xabar_text += f"📄 Matn: {matn}\n"
                xabar_text += f"📸 Media : {media}\n"
                xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

            # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
            message_id_ol = await state.get_data('message_id')
            message_id = message_id_ol.get('message_id')
            messagee = await bot.edit_message_text(
                message_id=message_id,
                chat_id=message.from_user.id,
                text=xabar_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                    ],
                    [
                        InlineKeyboardButton("🔠 URL tugmachalar",
                                             callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                        InlineKeyboardButton("👀 Xabarni ko'rish",
                                             callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                    ],

                    [
                        InlineKeyboardButton(f"👀 To'liq ko'rish",
                                             callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                    ],

                    [
                        InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                    ]
                ])
            )

        # Davlatni yangilash

            await state.update_data({'chat_id': mal[2]})
            await state.update_data({'message_id': messagee.message_id})

@dp.message_handler(state=xabarn_sozlash.matn)
async def start(message: types.Message , state: FSMContext):
    mal=await state.get_data()
    mal_id=mal.get('chat_id')
    db.update_xabar_matn(matn=message.text,id=mal_id)
    messagee=await message.reply(text="✅ Xabar o'rnatildi.",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'xabarni_bekor_qilish:{message.from_user.id}:{mal_id}')
                ]]))
    await state.update_data({'chat_id': mal_id})
    await state.update_data({'message_id': messagee.message_id})

    # db.update_xabar_matn(id)
@dp.callback_query_handler(state=xabarn_sozlash.matn)
async def start(message: CallbackQuery, state: FSMContext):
    mal = message.data.rsplit(":")
    if mal[0] == "xabarni_olib_tashlash":
        db.update_xabar_matn(matn="Xabar o'rnatilmagan.", id=mal[2])
        await xabarn_sozlash.xabarn_sozlash.set()

        select = db.select_message(users_id=message.from_user.id, id=mal[2])

        off = '❌'
        on = '✅'

        xabar_text = f"🕑 Takroriy xabarlar\n\n"
        for selet in select:
            matn = on if selet[1] != "Xabar o'rnatilmagan." else off
            media = on if selet[2] and selet[3] != 'None' else off
            url_tugma = on if selet[4] != 'None' else off

            va = selet[11]
            vaqt = va.split(':')

            a = time.localtime()
            xabar_text += f"📄 Matn: {matn}\n"
            xabar_text += f"📸 Media : {media}\n"
            xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

        # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
        message_id_ol = await state.get_data('message_id')
        message_id = message_id_ol.get('message_id')
        messagee = await bot.edit_message_text(
            message_id=message_id,
            chat_id=message.from_user.id,
            text=xabar_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                ],
                [
                    InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                ],
                [
                    InlineKeyboardButton("🔠 URL tugmachalar",
                                         callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                ],

                [
                    InlineKeyboardButton(f"👀 To'liq ko'rish",
                                         callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                ],

                [
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                ]
            ])
        )
    else:
        await xabarn_sozlash.xabarn_sozlash.set()

        select = db.select_message(users_id=message.from_user.id, id=mal[2])

        off = '❌'
        on = '✅'

        xabar_text = f"🕑 Takroriy xabarlar\n\n"
        for selet in select:
            matn = on if selet[1] != "Xabar o'rnatilmagan." else off
            media = on if selet[2] and selet[3] != 'None' else off
            url_tugma = on if selet[4] != 'None' else off

            va = selet[11]
            vaqt = va.split(':')

            a = time.localtime()
            xabar_text += f"📄 Matn: {matn}\n"
            xabar_text += f"📸 Media : {media}\n"
            xabar_text += f"🔠 URL tugmachalar:{url_tugma}\n"

        # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
        message_id_ol = await state.get_data('message_id')
        message_id = message_id_ol.get('message_id')
        messagee = await bot.edit_message_text(
            message_id=message_id,
            chat_id=message.from_user.id,
            text=xabar_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton("📄 Matn", callback_data=f'matn:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_matn:{message.from_user.id}:{mal[2]}"),
                ],
                [
                    InlineKeyboardButton("📸 Media", callback_data=f'media:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_media:{message.from_user.id}:{mal[2]}"),
                ],
                [
                    InlineKeyboardButton("🔠 URL tugmachalar",
                                         callback_data=f'url_tugma:{message.from_user.id}:{mal[2]}'),
                    InlineKeyboardButton("👀 Xabarni ko'rish",
                                         callback_data=f"xabarni_korish_url_tugma:{message.from_user.id}:{mal[2]}"),
                ],

                [
                    InlineKeyboardButton(f"👀 To'liq ko'rish",
                                         callback_data=f'toliq_korish:{message.from_user.id}:{mal[2]}'),
                ],

                [
                    InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[2]}')
                ]
            ])
        )

        # Davlatni yangilash

        await state.update_data({'chat_id': mal[2]})
        await state.update_data({'message_id': messagee.message_id})


@dp.callback_query_handler(state=tastiq.tastiq)
async def start(message: CallbackQuery, state: FSMContext):

    mal=message.data.rsplit(":")


    if mal[0]=='tastiq_xa':
        await xabar_sozlash_state.boshi.set()
        a=time.localtime()
        db.delete_message(id=mal[1])
        try:
                sele = db.select_message(users_id=message.from_user.id, gurux_id=mal[2])

                # Xabar matnini tayyorlash
                xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
                xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

                son = 1  # Boshlang'ich qiymat

                # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
                tugmalar = []

                for select in sele:
                    va =select[11]
                    vaqt=va.split(':')

                    if select[10] == 'off':  # Agar holat "off" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ O'chiq ❌\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="O'chiq ❌", callback_data=f"status_off:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])
                    elif select[10] == 'on':  # Agar holat "on" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ Faol ✅\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])

                    son += 1

                # Xabarni yuborish
                # await bot.send_message(chat_id=message.from_user.id,text=sele)
                mes_id_ol=await state.get_data()
                message_id=mes_id_ol.get('message_id')
                messagee = await bot.edit_message_text(
                    message_id=message_id,
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                        [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                              callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],
                        [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                        [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                    ])
                )

                await xabar_sozlash_state.boshi.set()


                # Davlatni yangilash

                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})

        except:

                    await xabar_sozlash_state.boshi.set()
                    tugma=await bot.send_message(chat_id=message.from_user.id,text=f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ Xabar qo'shish",callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],[InlineKeyboardButton(text='🔙 Ortga',callback_data='ortga')]]))

                    await xabar_sozlash_state.boshi.set()
                    await state.update_data({'message_id':tugma.message_id})
                    await state.update_data({'chat_id': mal[2]})

    if mal[0]=='tastiq_yoq':
        await xabar_sozlash_state.boshi.set()
        a=time.localtime()
        try:
                sele = db.select_message(users_id=message.from_user.id, gurux_id=mal[2])

                # Xabar matnini tayyorlash

                xabar_text = f"🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingiz mumkin.\n\n"
                xabar_text += f"Hozirgi vaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}\n\n"

                son = 1  # Boshlang'ich qiymat

                # InlineKeyboardMarkup tugmalarini yaratish uchun ro'yxat
                tugmalar = []

                for select in sele:
                    va =select[11]
                    vaqt=va.split(':')

                    if select[10] == 'off':  # Agar holat "off" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ O'chiq ❌\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="O'chiq ❌", callback_data=f"status_off:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])
                    elif select[10] == 'on':  # Agar holat "on" bo'lsa
                        xabar_text += f"🗯{number_to_emoji(son)}\n"
                        xabar_text += f"├ Faol ✅\n"
                        xabar_text += f"├ Vaqt: {a.tm_hour}:{a.tm_min}\n"
                        xabar_text += f"├ Har {vaqt[0]} {vaqt[1]}\n"
                        xabar_text += f"└ {select[1]}\n\n"

                        # Tugmalarni qo'shish
                        tugmalar.append([
                            InlineKeyboardButton(text=f"🗯{number_to_emoji(son)}", callback_data=f"xabar_set_bol:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="Faol ✅", callback_data=f"status_on:{select[0]}:{mal[2]}"),
                            InlineKeyboardButton(text="🗑", callback_data=f"delete_xabar:{select[0]}:{mal[2]}")
                        ])

                    son += 1

                # Xabarni yuborish
                # await bot.send_message(chat_id=message.from_user.id,text=sele)
                mes_id_ol = await state.get_data()
                message_id = mes_id_ol.get('message_id')
                messagee = await bot.edit_message_text(
                    message_id=message_id,
                    chat_id=message.from_user.id,
                    text=xabar_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=tugmalar + [
                        [InlineKeyboardButton(text="➕ Xabar qo'shish",
                                              callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],
                        [InlineKeyboardButton(text='Tayyor 👌', callback_data='tayyor')],
                        [InlineKeyboardButton(text='🔙 Ortga', callback_data='ortga')]
                    ])
                )


                # Davlatni yangilash
                await xabar_sozlash_state.boshi.set()
                await state.update_data({'chat_id': mal[2]})
                await state.update_data({'message_id': messagee.message_id})

        except:



                    await xabar_sozlash_state.boshi.set()
                    tugma=await bot.send_message(chat_id=message.from_user.id,text=f" 🕑 Takroriy xabarlar\nUshbu menyudan siz guruhda bir necha daqiqada/soat ichida takroriy yuboriladigan xabarlarni o'rnatishingizmumkin.\n\nHozirgivaqt: {a.tm_mday}/{a.tm_mon}/{a.tm_year} {a.tm_hour}:{a.tm_min}",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ Xabar qo'shish",callback_data=f'xabar_qoshish:{message.message.message_id}:{mal[2]}')],[InlineKeyboardButton(text='Tayyor 👌',callback_data='tayyor')],[InlineKeyboardButton(text='🔙 Ortga',callback_data='ortga')]]))

                    await xabar_sozlash_state.boshi.set()
                    await state.update_data({'message_id':tugma.message_id})
                    await state.update_data({'chat_id': mal[2]})

@dp.message_handler(state=kirish.login)
async def start(message: types.Message, state: FSMContext):
        await state.update_data({'login': message.text})
        mal=await state.get_data()
        but_id=mal.get('but_id')
        await bot.delete_message(chat_id=message.from_user.id,message_id=but_id)
        await message.delete()
        b=await bot.send_message(chat_id=message.from_user.id, text='Parolni kiriting')
        but_id = await state.update_data({'but_id': b.message_id})
        await kirish.parol.set()

@dp.message_handler(state=kirish.parol)
async def start(message: types.Message, state: FSMContext):
        mal = await state.get_data()
        but_id = mal.get('but_id')
        await bot.delete_message(chat_id=message.from_user.id, message_id=but_id)
        await message.delete()
        await state.update_data({'parol': message.text})
        mal = await state.get_data()
        login = mal.get('login')
        # a = db.select_user(login=login, parol=int(message.text), user_id=0)
        # await bot.send_message(chat_id=message.from_user.id,text=a[1])
        try:
            mal = await state.get_data()
            login = mal.get('login')
            parol = mal.get('parol')
            a = db.select_user(login=login, parol=message.text, user_id=0)
            if a:

                await bot.send_message(chat_id=message.from_user.id, text=
                f"🏻 Assalomu alaykum {message.from_user.last_name} \nGroup Help sizning guruhlaringizni oson va xavfsiz boshqarish uchun eng takomillashgan botdir!\n\n👉🏻 Botni guruhingizga qo'shing va ishga tushishi uchun Admin huquqini bering!\n\n❓ QANDAY BUYRUQLAR BOR?\n Barcha buyruqlarni ko'rish va ular qanday ishlashini bilish uchun /help buyrug'ini yuboring!\n\n📃 Privacy policy )",
                                       reply_markup=boshi)
                db.add_user(login=login, parol=int(message.text), user_id=int(message.from_user.id))
                await state.finish()
            else:
                print(4)
                await bot.send_message(chat_id=message.from_user.id, text=f"Kechirasiz siz bu botni ishlata olmaysiz.")
                await state.finish()
        except:
            print(5)
            await bot.send_message(chat_id=message.from_user.id, text=f"Kechirasiz siz bu botni ishlata olmaysiz.")
            await state.finish()



