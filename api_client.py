import aiohttp
import logging

class APIClient:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.session = None

    async def create_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def login(self, username, password):
        await self.create_session()
        url = f'{self.base_url}/api/login'
        data = {'username': username, 'password': password}
        async with self.session.post(url, json=data) as response:
            if response.status != 200:
                text = await response.text()
                logging.error(f"Fehler beim Login: {response.status}, Antwort: {text}")
                return False
            return True

    async def get_players_fast(self):
        url = f'{self.base_url}/api/get_players_fast'
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logging.error(f"Error fetching fast players data: {e}")
            return None

    async def do_message_player(self, player_name, player_id, message):
        url = f'{self.base_url}/api/message_player'
        data = {
            "player_name": player_name,
            "player_id": player_id,
            "message": message
        }
        try:
            async with self.session.post(url, json=data) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logging.error(f"Error sending message to player {player_name}: {e}")
            return None

    async def get_detailed_players(self):
        url = f'{self.base_url}/api/get_detailed_players'
        logging.info(f"API-Anfrage an URL: {url}")
        try:
            async with self.session.get(url) as response:
                logging.info(f"API-Antwort Status: {response.status}")
                if response.status == 200:
                    try:
                        # Versuche, die JSON-Antwort zu verarbeiten
                        data = await response.json()
                        logging.info(f"API-Antwort Inhalt: {data}")  # Logge die Antwort
                        
                        # Überprüfe, ob die Antwort valide ist
                        if data and 'result' in data and 'players' in data['result']:
                            return data
                        else:
                            logging.error("API hat keine gültigen Daten zurückgegeben oder die Struktur fehlt.")
                            return None
                    except Exception as json_error:
                        # Fehler beim Verarbeiten des JSON-Formats
                        logging.error(f"Fehler beim Verarbeiten der JSON-Antwort: {json_error}")
                        return None
                else:
                    logging.error(f"API-Fehler: HTTP {response.status}. Antworttext: {await response.text()}")
                    return None
        except Exception as e:
            logging.error(f"Fehler beim Abrufen der detaillierten Spielerdaten: {e}")
            return None