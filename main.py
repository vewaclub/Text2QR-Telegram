import logging
import qrcode
from aiogram import Bot, Dispatcher, executor, types
import os 

API_TOKEN = 'telegram token'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЭтот бот умеет создавать QR-коды из текста и изображений. Просто отправьте мне любое сообщение и я отправлю вам QR-код")

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo_message(message: types.Message):
    photo = await message.photo[-1].download()
    photo = str(photo)
    filename = photo.split("'")[1] 
    filename = filename.replace("'", "")
    print(f"Photo {filename} downloaded successfully")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(open('qr.png', 'rb'))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    await message.answer_photo(open('qr.png', 'rb'))
    print(f"Sent QR with image {filename}")
    if os.path.exists(filename):
        os.remove(f"{filename}")
        print(f"Photo named {filename} was deleted")
    else:
        print("The file does not exist.")
    
    
   
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def handle_text_message(message: types.Message):
    print(f"Text message received: {message.text}")
    data = message.text
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    await message.answer_photo(open('qr.png', 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
