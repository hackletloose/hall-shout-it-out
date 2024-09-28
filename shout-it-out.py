import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from api_client import APIClient
import logging

# Konfiguration des Loggings
logging.basicConfig(filename='bot_log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Laden der Umgebungsvariablen
load_dotenv()

# Discord Bot-Konfiguration
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Einrichtung des Discord-Clients
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="!", intents=intents)
        self.api_client = APIClient(os.getenv('API_BASE_URL'), API_TOKEN)
        self.api_logged_in = False

    async def login_to_api(self):
        if not self.api_logged_in:
            self.api_client.base_url = os.getenv('API_BASE_URL')
            self.api_logged_in = await self.api_client.login(USERNAME, PASSWORD)
            if self.api_logged_in:
                print(f"API-Login erfolgreich für {self.api_client.base_url}")
            else:
                print(f"API-Login fehlgeschlagen für {self.api_client.base_url}")

    async def send_messages(self, interaction, message_to_send, filter_function=None):
        await self.login_to_api()  # Stelle sicher, dass der API-Login durchgeführt wird
        await interaction.response.defer(ephemeral=True)

        players_data = await self.api_client.get_detailed_players()

        if players_data and 'result' in players_data and 'players' in players_data['result']:
            for player_id, player_info in players_data['result']['players'].items():
                if filter_function is None or filter_function(player_info):
                    await self.api_client.do_message_player(player_info['name'], player_info['player_id'], message_to_send)
            await interaction.followup.send(f"Nachricht gesendet: {message_to_send}", ephemeral=True)
        else:
            await interaction.followup.send("Fehler beim Abrufen der Spielerliste oder keine Spieler gefunden.", ephemeral=True)


bot = MyBot(intents)

class DropdownMenu(discord.ui.Select):
    def __init__(self, message_to_send):
        self.message_to_send = message_to_send

        options = [
            discord.SelectOption(label="An alle Spieler", description="Sende Nachricht an alle Spieler"),
            discord.SelectOption(label="An Allies", description="Sende Nachricht an die Allies"),
            discord.SelectOption(label="An Axis", description="Sende Nachricht an die Axis"),
            discord.SelectOption(label="An alle Offiziere", description="Sende Nachricht an alle Offiziere"),
            discord.SelectOption(label="An Axis Offiziere", description="Sende Nachricht an die Offiziere der Axis"),
            discord.SelectOption(label="An Allies Offiziere", description="Sende Nachricht an die Offiziere der Allies"),
            discord.SelectOption(label="An alle Commander", description="Sende Nachricht an alle Commander"),
            discord.SelectOption(label="An Axis Commander", description="Sende Nachricht an die Commander der Axis"),
            discord.SelectOption(label="An Allies Commander", description="Sende Nachricht an die Commander der Allies"),
        ]

        super().__init__(placeholder="Wähle eine Option", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Speichert die Auswahl im Dropdown
        self.view.selected_option = self.values[0]
        # Zeige den OK-Button, sobald eine Auswahl getroffen wurde
        self.view.add_item(OKButton())  # Füge den OK-Button hinzu
        await interaction.response.edit_message(content=f"Ausgewählt: {self.values[0]}. Drücke OK, um zu bestätigen.", view=self.view)


class OKButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OK", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        if self.view.selected_option:
            # Die Methode handle_dropdown_select ist Teil der View-Klasse
            await self.view.handle_dropdown_select(interaction, self.view.message_to_send, self.view.selected_option)
        else:
            await interaction.response.send_message("Bitte wähle zuerst eine Option im Dropdown-Menü.", ephemeral=True)


class DropdownView(discord.ui.View):
    def __init__(self, bot, message_to_send):
        super().__init__()
        self.selected_option = None
        self.bot = bot
        self.message_to_send = message_to_send
        self.add_item(DropdownMenu(message_to_send))  # Dropdown-Menü initialisieren

    async def handle_dropdown_select(self, interaction: discord.Interaction, message_to_send, option):
        filter_map = {
            "An alle Spieler": None,
            "An Allies": lambda p: p.get('team', '').lower() == 'allies',
            "An Axis": lambda p: p.get('team', '').lower() == 'axis',
            "An alle Offiziere": lambda p: p.get('role', '').lower() in ['officer', 'spotter', 'tankcommander'],
            "An Axis Offiziere": lambda p: p.get('role', '').lower() in ['officer', 'spotter', 'tankcommander'] and p.get('team', '').lower() == 'axis',
            "An Allies Offiziere": lambda p: p.get('role', '').lower() in ['officer', 'spotter', 'tankcommander'] and p.get('team', '').lower() == 'allies',
            "An alle Commander": lambda p: p.get('role', '').lower() == 'armycommander',
            "An Axis Commander": lambda p: p.get('role', '').lower() == 'armycommander' and p.get('team', '').lower() == 'axis',
            "An Allies Commander": lambda p: p.get('role', '').lower() == 'armycommander' and p.get('team', '').lower() == 'allies'
        }

        filter_function = filter_map.get(option)
        await self.bot.send_messages(interaction, message_to_send, filter_function)


@bot.tree.command(name="message", description="Nachricht an Spieler senden")
@app_commands.describe(message="Die Nachricht, die gesendet werden soll")
async def message(interaction: discord.Interaction, message: str):
    view = DropdownView(bot, message)
    await interaction.response.send_message("Wählen Sie eine Option und bestätigen Sie mit OK:", view=view, ephemeral=True)

bot.run(TOKEN)
