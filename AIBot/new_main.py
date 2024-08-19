import discord
from discord.ext import commands
import uuid
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Load the model and labels (adjust paths as needed)
def get_class(model_path, labels_path, image_path):
    # Load the model
    model = load_model(model_path)

    # Load labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale the image

    # Inference
    predictions = model.predict(img_array)

    # Get the label with the highest score
    predicted_idx = np.argmax(predictions, axis=1)
    predicted_label = labels[predicted_idx[0]]

    return predicted_label

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
            unique_filename = f"images/{uuid.uuid4()}_{attachment.filename}"
            file_path = unique_filename

            await attachment.save(file_path)

            # Use the AI model to classify the image
            model_path = 'path/to/your/model.h5'
            labels_path = 'path/to/your/labels.txt'
            result = get_class(model_path, labels_path, file_path)

            # Inform the user of the classification result
            await ctx.send(f"The model predicts: {result}")
        else:
            # Inform the user that the attachment is not an image
            await ctx.send("The attached file is not an image. Please upload a .png, .jpg, .jpeg, or .gif file.")
    else:
        # Inform the user that no attachment was found
        await ctx.send("No attachment found in the message. Please upload an image.")

bot.run("MTIyMTM3NDk4NzYwOTQ0NDQwMw.Gazq2S.aq8hWOjoVa3Os6M7K-0fLtSiukdrou7Xi8K0ow")
