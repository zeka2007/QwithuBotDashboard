import requests

class Oauth:
    client_id = "768148604367536138"
    client_secret = "mSH2k8pwVI5Gm4cPkAPbzYnIcFlwWCGO"
    redirect_uri = "https://qwithubotdashboard-3e6561.us1.kinto.io/login"
    scope = "identify%20guilds%20guilds.join"
    discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"

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
