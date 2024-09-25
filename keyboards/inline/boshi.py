from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

boshi= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Botni guruhga qo'shish ➕",callback_data='botni_guruhga_qoshish',url=f"https://t.me/qoravul_moskava_bot?startgroup=true")
        ],

        [
            InlineKeyboardButton(text="🔧 Yordam",callback_data='yordam'),
            InlineKeyboardButton(text="Batafsil 💬",callback_data='batavsil')
        ],
        [
InlineKeyboardButton(text="Chiqish 🚪",callback_data='chiqish')
        ]
    ]
)