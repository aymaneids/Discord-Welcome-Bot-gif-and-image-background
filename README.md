# Discord-Welcome-Bot-gif-and-image-background

# Discord Welcome Bot

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

4. in the last line in the code replace the bot token with your token

## Usage

1. Use the following commands in your Discord server to configure the bot:
   - `!set_welcome_channel`: Set the channel for welcome messages
   - `!set_background`: Set the background image (local file or URL)
   - `!set_welcome_format`: Set the welcome message format
   - `!toggle_welcome`: Toggle welcome messages on/off
   - `!set_font_size`: Set the font size for welcome messages
   - `!set_font_color`: Set the font color (RGB values)
   - `!set_background_size`: Set the background image size
   - `!set_avatar_size`: Set the size of the avatar in welcome images
   - `!set_text_position`: Set the position of the welcome text
   - `!set_avatar_position`: Set the position of the avatar
   - `!test_welcome`: Test the welcome message for a specific member
   - `!show_config`: Display the current configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
