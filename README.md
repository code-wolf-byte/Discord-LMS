# Discord LMS

## Problem
This project was inspired to move [City Montessori School](https://www.cmseducation.org/) from a Google-based LMS solution to a custom one over Discord. The primary idea was to use a bunch of common services offered by Google Classroom and Google Meet widely used in the Classroom and move their features to Discord with the help of Bots.

## Features
The bot provides the following functionalities to manage school-related tasks:

### Utility Commands
- `send`: Send a direct message to a member.
- `send_dm`: Send a direct message with attachment information to a member.
- `verify`: Verify a user and update their nickname.
- `nuke`: Clone and delete a text channel.
- `info`: Get information about a user.
- `assignment`: Create new assignment channels for submission and issue.
- `check`: Check the status of something (currently not fully implemented).
- `status`: Check the status of assignment submission channels.
- `move`: Move members with a specific role to a different voice channel.
- `attendance`: Log attendance for members with a specific role in a voice channel.

### Event Listeners
- `on_ready`: Change the bot's presence when it is ready.
- `on_guild_channel_update`: Update control panel when channels are created, deleted, or moved.
- `on_reaction_add`: Handle reactions for moving members between channels.

### Helper Functions
- `_get_channel`: Get a voice channel by name.
- `_mbr_helper`: Move members with a specific role from one channel to another.
- `_get_role`: Get a role by name.
- `_any_null`: Check if any arguments are null.
- `error`: Print an error message.
- `reaction_add_check`: Check requirements for adding a reaction.

## Archival
This project was set as an archive after an MSP was declined to be used by the school's administration as it would be too much work in training staff and more to make viable use of this service.

## Installation
To set up the bot, follow these steps:
1. Clone the repository.
2. Install the required packages using pip:
   ```sh
   pip install discord.py
   ```
3. Add your bot token in the client.run("YOUR_BOT_TOKEN_HERE") section of the code.
4. Run the bot:
```sh
python main.py
```

## Usage
Once the bot is running, use the following commands in your Discord server:
- `!send @member message`: Send a direct message to a member.
- `!send_dm @member message`: Send a direct message with attachment information to a member.
- `!verify`: Verify a user and update their nickname.
- `!nuke #channel`: Clone and delete a text channel.
- `!info username`: Get information about a user.
- `!assignment name`: Create new assignment channels for submission and issue.
- `!move role_name dst_channel_name`: Move members with a specific role to a different voice channel.
- `!attendance role_name channel_name`: Log attendance for members with a specific role in a voice channel.

Feel free to contribute to this project by submitting a pull request. Please ensure your changes are well-tested and documented.

License
This project is licensed under the MIT License.
