import logging
import qrcode
from aiogram import Bot, Dispatcher, executor, types
import os 
from imgurpython import ImgurClient

API_TOKEN = 'telegram token'
image_path = 'qr.png'
client_id = 'imgur client id'
client_secret = 'imgur secret'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def upload_image_to_imgur(image_path, client_id, client_secret):
    # authenticate with the Imgur API
    client = ImgurClient(client_id, client_secret)
    # upload the image to Imgur
    uploaded_image = client.upload_from_path(image_path)
    # return the URL of the uploaded image
    return uploaded_image['link']


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
    uploaded_image_url = upload_image_to_imgur(image_path=f'{filename}', client_id=client_id, client_secret=client_secret)
    data = uploaded_image_url
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    uploaded_image_url = upload_image_to_imgur(image_path='qr.png', client_id=client_id, client_secret=client_secret)
    await message.answer_photo(open('qr.png', 'rb'))
    print(f"Sent QR with image {filename}")
    if os.path.exists(filename):
        os.remove(f"{filename}")
        print(f"Photo named {filename} was deleted")
    else:
        print("The file does not exist.")
   
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def handle_text_message(message: types.Message):
    # Print the text to console
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
