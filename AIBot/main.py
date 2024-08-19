import discord
from discord.ext import commands
import uuid
from keras.preprocessing import image
from keras.models import load_model
import numpy as np

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


def get_class(model_path, labels_path, image_path):
    # load model
    model = load_model(model_path)

    # load label
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale the image


    # Inferensi
    predictions = model.predict(img_array)


    predict_idx = np.argmax(predictions, axis=1)
    predict_label = labels[predict_idx[0]]

    return predict_label





@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

# untuk check input dari user kirim attachment
@bot.command(name='upload_image')
async def upload_image(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            unique_filename = f"{uuid.uuid4()}_{attachment.filename}"
            file_path = f"images/{unique_filename}"

            await attachment.save(file_path)

            # Proses integrasi AI
            model_path = "keras_model.h5"
            labels_path = "labels.txt"
            result = get_class(model_path,labels_path, file_path)

            # Inform user the result from AI
            await ctx.send(f"Your AI Predict: {result}")


            # Inform the user that the image has been saved
            # await ctx.send(f"Image saved as {unique_filename}")
        else:
            # Inform the user that the attachment is not an image
            await ctx.send("The attached file is not an image. Please upload a .png, .jpg, .jpeg, or .gif file.")
    else:
        # Inform the user that no attachment was found
        await ctx.send("No attachment found in the message. Please upload an image.")

bot.run("MTIyMTM3NDk4NzYwOTQ0NDQwMw.Gazq2S.aq8hWOjoVa3Os6M7K-0fLtSiukdrou7Xi8K0ow")
