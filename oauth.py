import requests
import json
import os
class Oauth:
    bot_token = os.environ.get('BOT_TOKEN')
    client_id = "768148604367536138"
    client_secret = os.environ.get('CLIENT_SECRET') 
    redirect_uri = "https://qwithubotdashboard.zeet.app/login"
    scope = "identify%20guilds%20guilds.join"
    discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api/v6"

    discord_bot_redirect_uri = "http%3A%2F%2F127.0.0.1%3A5000%2Flogin"
    discord_bot_scope = "8"
    discord_bot_oauth_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={discord_bot_scope}&redirect_uri={discord_bot_redirect_uri}&scope=bot'
    # &guild_id=775650720761774111

    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id": Oauth.client_id,
            "client_secret": Oauth.client_secret,
            "grant_type":"authorization_code",
            "code": code,
            "redirect_uri": Oauth.redirect_uri,
            "scope": Oauth.scope
        }

        access_token = requests.post(url = Oauth.discord_token_url, data = payload).json()
        return access_token.get("access_token")
    @staticmethod
    def get_user_json(access_token):
        url = f"{Oauth.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_object = requests.get(url = url, headers = headers).json()
        return user_object
    @staticmethod
    def get_guilds_json(access_token):
        url = f"{Oauth.discord_api_url}/users/@me/guilds"
        headers = {"Authorization": f"Bearer {access_token}"}

        guilds_object = requests.get(url = url, headers = headers).json()
        return guilds_object
    @staticmethod
    def get_guild_members_json(guild_id, user_id):
        url = f"{Oauth.discord_api_url}/guilds/{guild_id}/members/{user_id}"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        member = requests.get(url = url, headers = headers).json()
        return member
    @staticmethod
    def get_guild_by_id_json(guild_id):
        url = f"{Oauth.discord_api_url}/guilds/{guild_id}"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        guild = requests.get(url = url, headers = headers).json()
        return guild

    @staticmethod
    def get_guild_channels_json(guild_id):
        url = f"{Oauth.discord_api_url}/guilds/{guild_id}/channels"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        channels = requests.get(url = url, headers = headers).json()
        return channels

    @staticmethod
    def send_message(channel_id, title, message):
        url = f"{Oauth.discord_api_url}/channels/{channel_id}/messages"
        headers = {'content-type': 'application/json',
                    "Authorization": f"Bot {Oauth.bot_token}"}
        send = {"embed": {
                "color": 0x0c0c0,
                "title": title,
                "description": message
               }
             }

        message = requests.post(url = url, data=json.dumps(send), headers = headers)
