import os
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType

bot = Bot(token='7024550646:AAET34-ZY8H6bI_Bb30JhY7wOF2_AYcsLPY')
dp = Dispatcher(bot)

IMG_DIR, VID_DIR = 'images/', 'videos/'
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VID_DIR, exist_ok=True)

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Rasm yoki video yuboring!')

@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.VIDEO])
async def handle_media(message: types.Message):
    if message.content_type == ContentType.PHOTO:
        file_id, ext, folder = message.photo[-1].file_id, 'jpg', IMG_DIR
    elif message.content_type == ContentType.VIDEO:
        file_id, ext, folder = message.video.file_id, 'mp4', VID_DIR

    unique_name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(folder, unique_name)
    await bot.download_file_by_id(file_id, path)
    await message.reply(f"Fayl saqlandi: {path}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
