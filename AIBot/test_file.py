import discord
from discord.ext import commands
import os
import uuid

# Set up intents and initialize the bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Create a folder to save images if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

# Command to handle image uploads
@bot.command(name='upload_image')
async def upload_image(ctx):
    # Check if the message contains any attachments
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        
        # Check if the attachment is an image by checking its extension
        if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Generate a unique filename
            unique_filename = f"{uuid.uuid4()}_{attachment.filename}"
            file_path = f"images/{unique_filename}"
            
            # Save the image
            await attachment.save(file_path)
            
            # Inform the user that the image has been saved
            await ctx.send(f"Image saved as {unique_filename}")
        else:
            # Inform the user that the attachment is not an image
            await ctx.send("The attached file is not an image. Please upload a .png, .jpg, .jpeg, or .gif file.")
    else:
        # Inform the user that no attachment was found
        await ctx.send("No attachment found in the message. Please upload an image.")

# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")
