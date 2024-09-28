# Discord Welcome Bot
![welcome_test](https://github.com/user-attachments/assets/8ac232fc-4b96-4aa6-a785-f2a1636bd708)

![image](https://github.com/user-attachments/assets/5516a723-41d0-4822-9745-425b2229b109)


A customizable Discord bot that sends welcome messages with personalized images when new members join a server.

## Features

- Customizable welcome messages and images
- Support for GIF backgrounds
- Configurable text position, font size, and color
- Adjustable avatar size and position
- Option to use local or URL-based background images
- Easy configuration through Discord commands

## Requirements

- Python 3.8+
- discord.py
- Pillow
- requests

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `config.json` file in the project root directory with the following structure:
   ```json
   {
     "background_type": "url",
     "background_path": "https://example.com/background.gif",
     "background_width": 500,
     "background_height": 232,
     "font_path": "./font.ttf",
     "font_size": 30,
     "font_color": [255, 255, 255],
     "avatar_size": 64,
     "avatar_position": [50, 84],
     "text_position": [250, 180],
     "welcome_format": "Welcome {display_name}! to the server!",
     "welcome_enabled": true,
     "welcome_channel_id": null
   }
   ```

## Usage

1. Use the following commands in your Discord server to configure the bot:

   - `!set_welcome_channel [#channel]`: Set the channel for welcome messages
     Example: `!set_welcome_channel #welcome`

   - `!set_background <type> <path>`: Set the background image (local file or URL)
     Example: `!set_background url https://example.com/background.gif`
     Example: `!set_background local ./images/background.png`

   - `!set_welcome_format <format>`: Set the welcome message format
     Example: `!set_welcome_format Welcome {display_name} to {server_name}!`

   - `!toggle_welcome`: Toggle welcome messages on/off
     Example: `!toggle_welcome`

   - `!set_font_size <size>`: Set the font size for welcome messages
     Example: `!set_font_size 36`

   - `!set_font_color <r> <g> <b>`: Set the font color (RGB values)
     Example: `!set_font_color 255 255 255`

   - `!set_background_size <width> <height>`: Set the background image size
     Example: `!set_background_size 800 400`

   - `!set_avatar_size <size>`: Set the size of the avatar in welcome images
     Example: `!set_avatar_size 128`

   - `!set_text_position <x> <y>`: Set the position of the welcome text
     Example: `!set_text_position 400 300`

   - `!set_avatar_position <x> <y>`: Set the position of the avatar
     Example: `!set_avatar_position 100 150`

   - `!test_welcome [@user]`: Test the welcome message for a specific member
     Example: `!test_welcome @JohnDoe`
     Note: If no user is specified, it will test with the command user.

   - `!show_config`: Display the current configuration
     Example: `!show_config`

## Command Permissions

All configuration commands require administrator permissions in the Discord server.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
