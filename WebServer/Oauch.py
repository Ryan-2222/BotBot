import requests
import os 

class Oauch:
  API_ENDPOINT = 'https://discord.com/api/v10'
  CLIENT_ID = os.getenv("CLIENT_ID")
  CLIENT_SECRET = os.getenv("CLIENT_SECRET")
  REDIRECT_URI = 'https://Nyan-Cat.snowryan2222.repl.co/OAuth2/discord'
  DISCORD_LOGIN_URL = "https://discord.com/api/oauth2/authorize?client_id=803138272398278677&redirect_uri=https%3A%2F%2FNyan-Cat.snowryan2222.repl.co%2FOAuth2%2Fdiscord&response_type=code&scope=identify%20email%20guilds"


  @staticmethod
  def get_token(code):
    data = {
      'client_id': Oauch.CLIENT_ID,
      'client_secret': Oauch.CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': Oauch.REDIRECT_URI
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    rqst = requests.post('%s/oauth2/token' % Oauch.API_ENDPOINT, data=data, headers=headers)
    rqst.raise_for_status()
    return rqst.json()['access_token']

  def get_user_guilds(token: str):
    rqst = requests.get('%s/users/@me/guilds' % Oauch.API_ENDPOINT, headers={"Authorization": f"Bearer {token}"})
    rqst.raise_for_status()
    return rqst.json()

  def get_bot_guilds():
    token = os.getenv("TOKEN")
    rqst = requests.get('%s/users/@me/guilds' % Oauch.API_ENDPOINT, headers={"Authorization": f"Bot {token}"})
    rqst.raise_for_status()
    return rqst.json()

  def get_intersect_guilds(user_guilds: list, bot_guilds: list):
    return [guild for guild in user_guilds if guild['id'] in map(lambda i: i['id'], bot_guilds) and (int(guild['permissions']) & 0x20) == 0x20]
    
    """
    intersect_guild = []
    for guild in user_guilds:
      if guild['id'] in map(lambda i: id['id'], bot_guilds):
        intersect_guild.append()
    """

  def get_guild_data(guild_id: int):
    token = os.getenv("TOKEN")
    rqst = requests.get(f'%s/guilds/{guild_id}' % Oauch.API_ENDPOINT, headers={"Authorization": f"Bot {token}"})
    rqst.raise_for_status()
    return rqst.json()