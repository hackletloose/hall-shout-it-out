# Discord Bot with RCON API Integration
This Discord bot allows sending messages to players in a game via the RCON API, with role-based and team-based filtering using a dropdown menu. 
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
**2. Set Up a Virtual Environment (optional but recommended)**
   Create and activate a Python virtual environment to isolate dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
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
**4. Configure Environment Variables**
   ```
   DISCORD_BOT_TOKEN=<your-discord-bot-token>
   USERNAME=<rcon-username>
   PASSWORD=<rcon-password>
   API_TOKEN=<rcon-api-token>
   API_BASE_URL=<rcon-url-example: http://127.0.0.1>
   ```
**5. Run the Bot**
   ```
   python bot.py
   ```
## Commands
/message <message>: Send a message to players with the ability to filter by teams or roles using a dropdown menu.
## Logging
Logs are stored in a file named bot_log.txt. You can configure the logging level and format in the bot.py file.
## License
This project is licensed under the MIT License.
