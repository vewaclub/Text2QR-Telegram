import logging
import asyncio
import qrcode
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import os 
import sys
from imgurpython import ImgurClient

TOKEN = "telegram bot token"
image_path = 'qr.png'
client_id = 'imgur client id'
client_secret = 'imgur secret'

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

def upload_image_to_imgur(image_path, client_id, client_secret):
    client = ImgurClient(client_id, client_secret)
    uploaded_image = client.upload_from_path(image_path)
    return uploaded_image['link']


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЭтот бот умеет создавать QR-коды из текста и изображений. Просто отправьте мне любое сообщение и я отправлю вам QR-код")

@dp.message(F.content_type == types.ContentType.PHOTO)
async def handle_photo_message(message: types.ContentType.PHOTO):
    file_name = f"photos/{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1], destination=file_name)
    print(f"Photo {file_name} downloaded successfully")
    uploaded_image_url = upload_image_to_imgur(image_path=f'{file_name}', client_id=client_id, client_secret=client_secret)
    data = uploaded_image_url
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    uploaded_image_url = upload_image_to_imgur(image_path='qr.png', client_id=client_id, client_secret=client_secret)
    await message.answer_photo(uploaded_image_url)
    print(f"Sent QR with image {file_name}")
    if os.path.exists(file_name):
        os.remove(f"{file_name}")
        print(f"Photo named {file_name} was deleted")
    else:
        print("The file does not exist.")
   
@dp.message()
async def handle_text_message(message: types.Message):
    print(f"Text message received: {message.text}")
    data = message.text
    print(data)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    uploaded_image_url = upload_image_to_imgur(image_path='qr.png', client_id=client_id, client_secret=client_secret)
    await message.answer_photo(uploaded_image_url)


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
