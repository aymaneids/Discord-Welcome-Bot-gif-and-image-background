import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io
import requests
import os
import json
import logging
import asyncio
from typing import Tuple, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "background_type": "url",
    "background_path": "https://example.com/background.gif",
    "background_width": 500,
    "background_height": 232,
    "font_path": "./font.ttf",
    "font_size": 30,
    "font_color": [255, 255, 255],
    "avatar_size": 64,
    "avatar_position": [50, 84],
    "text_position": [250, 180],  # New default text position
    "welcome_format": "Welcome {display_name}! to the server!",
    "welcome_enabled": True,
    "welcome_channel_id": None
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Error decoding {CONFIG_FILE}. Using default configuration.")
    else:
        logging.info(f"{CONFIG_FILE} not found. Creating with default configuration.")
    
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        logging.info(f"Configuration saved to {CONFIG_FILE}")
    except IOError:
        logging.error(f"Error saving configuration to {CONFIG_FILE}")

config = load_config()


def get_background() -> Image.Image:
    try:
        if config['background_type'] == 'local':
            return Image.open(config['background_path'])
        else:  # URL
            response = requests.get(config['background_path'])
            return Image.open(io.BytesIO(response.content))
    except Exception as e:
        logging.error(f"Error loading background image: {e}")
        raise
#fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
def create_welcome_image(member: discord.Member, welcome_text: str, config: dict) -> io.BytesIO:
    try:
        background = get_background()  # Ensure this function is defined

        # Download and open the user's avatar
        avatar_url = str(member.display_avatar.url)
        avatar_response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(avatar_response.content)).convert("RGBA")

        # Resize and create circular mask for avatar
        avatar = avatar.resize((config['avatar_size'], config['avatar_size']), Image.LANCZOS)
        mask = Image.new("L", avatar.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, config['avatar_size'], config['avatar_size']), fill=255)

        # Prepare font
        font = ImageFont.truetype(config['font_path'], config['font_size'])

        # Create new GIF with frames
        frames = []
        for frame in ImageSequence.Iterator(background):
            frame = frame.copy().convert("RGBA")
            frame = frame.resize((config['background_width'], config['background_height']), Image.LANCZOS)
            frame.paste(avatar, tuple(config['avatar_position']), mask)

            # Add the user's name and "Welcome" text to the background
            draw = ImageDraw.Draw(frame)
            welcome_message = f"Welcome {member.display_name}"

            # Get text position from the config
            text_position = tuple(config['text_position'])
            draw.text(text_position, welcome_message, font=font, fill=tuple(config['font_color']))
            frames.append(frame)

        result = io.BytesIO()
        frames[0].save(
            result, 
            format='GIF', 
            save_all=True, 
            append_images=frames[1:], 
            loop=0, 
            duration=background.info.get('duration', 100),
            disposal=2
        )
        result.seek(0)
        return result
    except Exception as e:
        logging.error(f"Error creating welcome image: {e}")
        raise

# Helper function to handle and center multiline text
def draw_multiline_text_centered(draw, text, font, image_size, text_color):
    image_width, image_height = image_size

    # Split the text into multiple lines if necessary
    lines = text.split('\n')

    # Find the max line width to center horizontally
    max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)

    # Calculate the total height of all lines combined to center vertically
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)

    # Starting Y position (vertically centered)
    y = (image_height - total_text_height) // 2

    # Draw each line centered horizontally
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2]
        line_height = bbox[3]
        x = (image_width - line_width) // 2  # Center the text horizontally
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height  # Move down for the next line

#ffffffffffffffffffffffffffffffffffffffffffffffff
@bot.event
async def on_ready():
    logging.info(f'Bot is ready. Logged in as {bot.user.name}')
    await setup_welcome_channel()

async def setup_welcome_channel():
    if config['welcome_channel_id']:
        channel = bot.get_channel(config['welcome_channel_id'])
        if channel:
            bot.welcome_channel = channel
            logging.info(f"Welcome channel set to: {channel.name}")
        else:
            logging.error(f"Could not find channel with ID {config['welcome_channel_id']}")
    else:
        logging.warning("Welcome channel not set. Use !set_welcome_channel to set it.")

@bot.event
async def on_member_join(member: discord.Member):
    if not config['welcome_enabled']:
        return

    logging.info(f"New member joined: {member.name}")
    if hasattr(bot, 'welcome_channel'):
        try:
            welcome_text = config['welcome_format'].format(
                display_name=member.display_name,  # User's display name
                user_name=member.name,             # Actual user name
                user_mention=member.mention,       # Mention for tagging the user
                server_name=member.guild.name      # Server name
            )
            welcome_image = create_welcome_image(member, welcome_text, config)
            
            await bot.welcome_channel.send(
                content=welcome_text,
                file=discord.File(fp=welcome_image, filename="welcome.gif")
            )
            logging.info(f"Welcome message sent for {member.name}")
        except Exception as e:
            logging.error(f"Error sending welcome message: {e}")
    else:
        logging.error("Welcome channel not set. Use !set_welcome_channel to set it.")



@bot.command()
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel = None):
    """Set the welcome channel"""
    if channel is None:
        # If no channel is specified, use the current channel
        channel = ctx.channel

    bot.welcome_channel = channel
    config['welcome_channel_id'] = channel.id
    save_config(config)
    
    # Send a test message to verify the channel is set correctly
    try:
        test_message = await channel.send(f"This channel has been set as the welcome channel. (Test message)")
        await asyncio.sleep(5)  # Wait for 5 seconds
        await test_message.delete()  # Delete the test message
    except discord.errors.Forbidden:
        await ctx.send(f"Error: I don't have permission to send messages in {channel.mention}. Please check my permissions and try again.")
        return

    await ctx.send(f"Welcome channel successfully set to: {channel.mention}")
    logging.info(f"Welcome channel set to: {channel.name} (ID: {channel.id})")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_background(ctx, background_type: str, path: str):
    """Set the background image (local file or URL)"""
    if background_type not in ['local', 'url']:
        await ctx.send("Invalid background type. Use 'local' or 'url'.")
        return
    
    config['background_type'] = background_type
    config['background_path'] = path
    save_config(config)
    await ctx.send(f"Background set to {background_type}: {path}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_welcome_format(ctx, *, format_string: str):
    """Set the welcome message format"""
    config['welcome_format'] = format_string
    save_config(config)
    await ctx.send(f"Welcome format set to: {format_string}")

@bot.command()
@commands.has_permissions(administrator=True)
async def toggle_welcome(ctx):
    """Toggle welcome messages on/off"""
    config['welcome_enabled'] = not config['welcome_enabled']
    save_config(config)
    status = "enabled" if config['welcome_enabled'] else "disabled"
    await ctx.send(f"Welcome messages are now {status}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_font_size(ctx, size: int):
    """Set the font size for welcome messages"""
    if size < 1:
        await ctx.send("Font size must be a positive number.")
        return
    config['font_size'] = size
    save_config(config)
    await ctx.send(f"Font size set to: {size}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_font_color(ctx, r: int, g: int, b: int):
    """Set the font color for welcome messages (RGB values)"""
    if not all(0 <= c <= 255 for c in (r, g, b)):
        await ctx.send("RGB values must be between 0 and 255.")
        return
    config['font_color'] = [r, g, b]
    save_config(config)
    await ctx.send(f"Font color set to RGB: ({r}, {g}, {b})")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_background_size(ctx, width: int, height: int):
    """Set the background image size"""
    if width < 1 or height < 1:
        await ctx.send("Width and height must be positive numbers.")
        return
    config['background_width'] = width
    config['background_height'] = height
    save_config(config)
    await ctx.send(f"Background size set to: {width}x{height}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_avatar_size(ctx, size: int):
    """Set the size of the avatar in the welcome image"""
    if size < 1:
        await ctx.send("Avatar size must be a positive number.")
        return
    config['avatar_size'] = size
    save_config(config)
    await ctx.send(f"Avatar size set to: {size}px")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_text_position(ctx, x: int, y: int):
    """Set the position of the welcome text in the image"""
    config['text_position'] = [x, y]
    save_config(config)
    await ctx.send(f"Text position set to: ({x}, {y})")

@bot.command()
@commands.has_permissions(administrator=True)
async def test_welcome(ctx, member: discord.Member = None):
    """Test the welcome message for a specific member or the command user"""
    if member is None:
        member = ctx.author

    if not hasattr(bot, 'welcome_channel'):
        await ctx.send("Welcome channel is not set. Use !set_welcome_channel to set it first.")
        return

    try:
        welcome_text = config['welcome_format'].format(
            display_name=member.display_name,
            user_name=member.name,
            user_mention=member.mention,
            server_name=ctx.guild.name
        )
        welcome_image = create_welcome_image(member, welcome_text, config)  # Ensure 3 arguments are passed
        
        await bot.welcome_channel.send(
            content=f"**TEST MESSAGE**\n{welcome_text}",
            file=discord.File(fp=welcome_image, filename="welcome_test.gif")
        )
        await ctx.send(f"Test welcome message sent in {bot.welcome_channel.mention}")
    except Exception as e:
        logging.error(f"Error sending test welcome message: {e}")
        await ctx.send(f"Error sending test welcome message: {e}")




@bot.command()
@commands.has_permissions(administrator=True)
async def set_avatar_position(ctx, x: int, y: int):
    """Set the position of the avatar in welcome images"""
    config['avatar_position'] = [x, y]
    save_config(config)
    await ctx.send(f"Avatar position set to: ({x}, {y})")

@bot.command()
@commands.has_permissions(administrator=True)
async def show_config(ctx):
    """Show the current configuration"""
    config_display = dict(config)
    if hasattr(bot, 'welcome_channel'):
        config_display['welcome_channel'] = bot.welcome_channel.name
    await ctx.send(f"```json\n{json.dumps(config_display, indent=2)}\n```")

bot.run('your bot token')
