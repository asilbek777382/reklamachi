from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def sozlamalar_klaviaturasi():
    keyboard = InlineKeyboardMarkup(row_width=3)

    keyboard.add(
        InlineKeyboardButton("📜 Qoidalar", callback_data='qoidalar'),
        InlineKeyboardButton("🛡 Anti-Spam", callback_data='anti_spam'),

    )

    keyboard.add(
        InlineKeyboardButton("🛡 Anti-Flood", callback_data='anti_flood'),
        InlineKeyboardButton("💬 Salomlashish", callback_data='salomlashish'),

    )

    keyboard.add(
        InlineKeyboardButton("👋 Xayrlashuv", callback_data='xayrlashuv'),
        InlineKeyboardButton("🔠 Alifbolar", callback_data='alifbolar')

    )

    keyboard.add(
        InlineKeyboardButton("🤖 Captcha", callback_data='captcha'),
        InlineKeyboardButton("🛠 Tekshiruvlar", callback_data='tekshiruvlar'),

    )

    keyboard.add(
        InlineKeyboardButton("🆘 @admin", callback_data='blok'),
        InlineKeyboardButton("🚫 Blok", callback_data='blok'),


    )

    keyboard.add(
    InlineKeyboardButton("🎥 Media", callback_data='media'),
    InlineKeyboardButton("🔞 Porno", callback_data='porno'),


    )

    keyboard.add(
    InlineKeyboardButton("🌙 Tun", callback_data='tun'),
        InlineKeyboardButton("❗ Ogohlantirish", callback_data='ogohlantirish'),


    )
    keyboard.add(
        InlineKeyboardButton("🏷 Belgilash", callback_data='belgilash'),
        InlineKeyboardButton("🔗 Guruh havolasi", callback_data='guruh_havolasi')

    )

    keyboard.add(
        InlineKeyboardButton("ℹ Tasdiqlash rejimi", callback_data='tasdiqlash_rejimi'),
    )

    keyboard.add(InlineKeyboardButton("🗑 Xabarlarni o‘chirish", callback_data='xabar_ochirish')
)

    keyboard.add(

    InlineKeyboardButton("🇺🇿 Lang", callback_data='lang'),
    InlineKeyboardButton("✅ Yopish", callback_data='yopish'),
    InlineKeyboardButton("🔧 Boshqalar", callback_data='boshqalar')
    )


    return keyboard



