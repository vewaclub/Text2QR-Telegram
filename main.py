import logging
import qrcode
from imgurpython import ImgurClient
from aiogram import Bot, Dispatcher, executor, types
import os 

API_TOKEN = 'telegram token here'

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

image_path = 'qr.png'
client_id = 'client id imgur'
client_secret = 'client secret imgur'

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo_message(message: types.Message):
    global filename
    # Download the photo
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
    await message.answer_photo(uploaded_image_url)
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
    uploaded_image_url = upload_image_to_imgur(image_path='qr.png', client_id=client_id, client_secret=client_secret)
    await message.answer_photo(uploaded_image_url)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
