# Discord Bot with RCON API Integration
This Discord bot allows sending messages to players in a game via the RCON API, with role-based and team-based filtering using a dropdown menu.

ToDo:
Execute the following commands after downloading:
1. Copy the `.env.dist` file to `.env` and enter your values.
2. Run the command `pip install python-dotenv`.
3. Copy `shout-it-out.service.dist` to `/etc/systemd/system/shout-it-out.service`
4. Activate and start the service with `sudo systemctl enable shout-it-out.service` and `sudo systemctl start shout-it-out.service`.

## Requirements
- Python 3.8+
- A Discord Bot Token (can be created from [Discord Developer Portal](https://discord.com/developers/applications))
- RCON API with valid credentials (username, password, and token)

## Mandatory CRCON Permissions
Whichever account you use must have at least these permissions:
- api|rcon user|Can message players

## Mandatory Discord Bot Permissions
- Manage Message
- Read Massage History
- Send Message
- Use Slash Commands
- View Channel

**under Bot (Privileged Gateway Intents)**
- Presence Intent
- Server Members Intent
- Message Content Intent
  
## Installation
**1. Clone the Repository**
   First, clone the repository to your local machine:

   ```
   bash
   git clone https://github.com/hackletloose/hall-shout-it-out.git
   cd hall-shout-it-out
   ```
**2. Edit the environment config file**
   Now, you're going to create and edit an `.env` file. 
   Here we'll use `nano`, a simple text editor that runs in text mode.  
  *You can use any other tool you're used to, either local or getting the file from a SFTP connection.*

> [!CAUTION]
> Do not edit `.env.dist`.  
> The file you're about to create must be named `.env`.  

Make a copy of the environnement config file template :

```shell
cp .env.dist .env
```

Install the `nano` text editor (debian-based command) :

```shell
apt update && apt install nano
```

Launch `nano` to edit the `.env` file :

```shell
nano .env
```

> [!TIP]
> In `nano`, you can move the cursor with the arrow keys.

**2.1 Configure Environment Variables**
   ```
   DISCORD_BOT_TOKEN=<your-discord-bot-token>
   USERNAME=<rcon-username>
   PASSWORD=<rcon-password>
   API_TOKEN=<rcon-api-token>
   API_BASE_URL=<rcon-url-example: http://127.0.0.1>
   ```

> [!IMPORTANT]
> - save the changes with `Ctrl`+`o` (then press the `[ENTER]` key to validate)  
> - exit nano with `Ctrl`+`x`

**3. Install Dependencies**
   Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```
   Ensure you have the following packages in requirements.txt:
   ```
   discord.py
   python-dotenv
   logging
   ```
**5. Run the Bot**
   ```
   python3 shout-it-out.py
   ```
## Commands
/message <message>: Send a message to players with the ability to filter by teams or roles using a dropdown menu and OK button.
## Logging
Logs are stored in a file named bot_log.txt. You can configure the logging level and format in the bot.py file.
## License
This project is licensed under the MIT License.
