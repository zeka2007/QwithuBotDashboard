from flask import Flask, request, redirect, render_template, url_for
from oauth import Oauth

app = Flask(__name__)


@app.route('/', methods = ['get'])
def index():
    return redirect(Oauth.discord_login_url)

@app.route('/login', methods = ['get'])
def login():
    try:
        code = request.args.get("code")
        at = Oauth.get_access_token(code)

        user_json = Oauth.get_user_json(at)
        guilds_json = Oauth.get_guilds_json(at)
        guilds = " "
        for guild in guilds_json:
            # if guild.get("permissions") & 0x8 == 0x8:
            if not guild.get("icon") == None:
                guilds = f"https://cdn.discordapp.com/icons/{str(guild.get('id'))}/{str(guild.get('icon'))}.png?size=1024"
        user_name = user_json.get("username")
        user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'
        return render_template("index.html", articles = user_name, avatar = user_avatar)
    except AttributeError:
        return redirect(Oauth.discord_login_url)
if __name__ == "__main__":
    app.run(debug = True)
