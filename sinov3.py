# if mal[0] == 'xabar_set_bol':
#
#     mal = message.data.rsplit(':')
#     message_id_ol = await state.get_data('message_id')
#     message_id = message_id_ol.get('message_id')
#     select = db.select_message(users_id=message.from_user.id, id=mal[1])
#
#     off = '❌'
#     on = '✅'
#
#     xabar_text = f"🕑 Takroriy xabarlar\n\n"
#     for selet in select:
#         # Ma'lumotlar bazasidan kelayotgan qiymatlarni tekshirish uchun debug chiqarish
#         print(f"Holat xabarni qadash: {selet[6]}, songgi xabarni o'chirish: {selet[7]}")
#
#         # {sele[6]} va {sele[7]} qiymatlari `on` yoki `off` ekanligini tekshirish
#         xabar_qadash = on if selet[6] == 'on' else off
#         songgi_xabar_ochirish = on if selet[7] == 'on' else off
#         await message.message.answer(f"{selet}")
#         va = selet[11]
#         vaqt = va.split(':')
#
#         a = time.localtime()
#         xabar_text += f"💡 Holat: {selet[10]}\n"
#         xabar_text += f"🕑 Vaqt: {a.tm_hour}:{a.tm_min}\n"
#         xabar_text += f"🔁 Takrorlash: har {vaqt[0]}:{vaqt[1]}\n"
#         xabar_text += f"📌 Xabarni qadash: {xabar_qadash}\n"
#         xabar_text += f"♻️ So'nggi xabarni o'chirish: {songgi_xabar_ochirish}\n\n"
#
#     # Tugmalarni yaratishda to'g'ri holatni ko'rsatish
#     messagee = await bot.edit_message_text(
#         message_id=message_id,
#         chat_id=message.from_user.id,
#         text=xabar_text,
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#             [
#                 InlineKeyboardButton("✍️ Xabarni sozlash", callback_data='xabarn_sozlash'),
#             ],
#             [
#                 InlineKeyboardButton("🔄 Takrorlash", callback_data='takrorlash'),
#             ],
#             [
#                 InlineKeyboardButton("⏲ Tugash sanasi", callback_data='tugash_sanasi'),
#             ],
#             [
#                 InlineKeyboardButton(f"📌 Xabarni qadash {xabar_qadash}",
#                                      callback_data=f'xabarni_qadash:{mal[1]}:{selet[6]}'),
#             ],
#             [
#                 InlineKeyboardButton(f"♻️ So'nggi xabarni o'chirish {songgi_xabar_ochirish}",
#                                      callback_data=f'songgi_xabarni_ochirish:{mal[1]}:{selet[7]}'),
#             ],
#             [
#                 InlineKeyboardButton(text='🔙 Ortga', callback_data=f'ortga:{message.from_user.id}:{mal[1]}')
#             ]
#         ])
#     )
#
#     # Davlatni yangilash
#     await xabar_set_bol.xabar_set_bol.set()
#     await state.update_data({'chat_id': mal[1]})
#     await state.update_data({'message_id': messagee.message_id})

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
            await message.message.answer(f"{selet}")
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
                    InlineKeyboardButton("✍️ Xabarni sozlash", callback_data='xabarn_sozlash'),
                ],
                [
                    InlineKeyboardButton("🔄 Takrorlash", callback_data='takrorlash'),
                ],
                [
                    InlineKeyboardButton("⏲ Tugash sanasi", callback_data='tugash_sanasi'),
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
            await message.message.answer(f"{selet}")
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
                    InlineKeyboardButton("✍️ Xabarni sozlash", callback_data='xabarn_sozlash'),
                ],
                [
                    InlineKeyboardButton("🔄 Takrorlash", callback_data='takrorlash'),
                ],
                [
                    InlineKeyboardButton("⏲ Tugash sanasi", callback_data='tugash_sanasi'),
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
            await message.message.answer(f"{selet}")
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
                    InlineKeyboardButton("✍️ Xabarni sozlash", callback_data='xabarn_sozlash'),
                ],
                [
                    InlineKeyboardButton("🔄 Takrorlash", callback_data='takrorlash'),
                ],
                [
                    InlineKeyboardButton("⏲ Tugash sanasi", callback_data='tugash_sanasi'),
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
            await message.message.answer(f"{selet}")
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
                    InlineKeyboardButton("✍️ Xabarni sozlash", callback_data='xabarn_sozlash'),
                ],
                [
                    InlineKeyboardButton("🔄 Takrorlash", callback_data='takrorlash'),
                ],
                [
                    InlineKeyboardButton("⏲ Tugash sanasi", callback_data='tugash_sanasi'),
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
