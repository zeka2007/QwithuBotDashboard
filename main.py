from flask import Flask, request, redirect, render_template, url_for, make_response
from oauth import Oauth
import json
app = Flask(__name__)


@app.route('/', methods = ['get'])
def index():
    global url
    global user_name
    global user_avatar
    if request.cookies.get('token') == None:
        user_avatar = url_for("static", filename = "img/none_user.png")
        user_name = "войти"
        url = Oauth.discord_login_url
        return render_template("index_no_login.html",
        user_btn_url = url,
        articles = user_name,
        avatar = user_avatar,
        bot_redirect = Oauth.discord_bot_oauth_url)
    else:
        at = request.cookies.get('token')

        print(at)
        url = 'https://discord.com'
        user_json = Oauth.get_user_json(at)
        guilds_json = Oauth.get_guilds_json(at)
        guilds = " "
        # for guild in guilds_json:
        #     if guild.get("permissions") & 0x8 == 0x8:
        #     if not guild.get("icon") == None:
        #         guilds = f"https://cdn.discordapp.com/icons/{str(guild.get('id'))}/{str(guild.get('icon'))}.png?size=1024"
        user_name = user_json.get("username")
        user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'
        return render_template("index.html", user_btn_url = url, articles = user_name, avatar = user_avatar, bot_redirect = Oauth.discord_bot_oauth_url)
@app.route('/login', methods = ['get'])
def login():
    global user_name
    global user_avatar
    try:
        if request.cookies.get('token') == None:
            print("bub")
            resp = make_response(redirect(url_for("login")))
            code = request.args.get("code")
            print(code)
            at = Oauth.get_access_token(code)
            print(at)
            resp.set_cookie('token', at)
            return resp
        at = request.cookies.get('token')

        print(at)

        user_json = Oauth.get_user_json(at)
        guilds_json = Oauth.get_guilds_json(at)
        guilds = " "
        # for guild in guilds_json:
        #     if guild.get("permissions") & 0x8 == 0x8:
        #     if not guild.get("icon") == None:
        #         guilds = f"https://cdn.discordapp.com/icons/{str(guild.get('id'))}/{str(guild.get('icon'))}.png?size=1024"
        user_name = user_json.get("username")
        user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'
        return render_template("index.html", articles = user_name, avatar = user_avatar, bot_redirect = Oauth.discord_bot_oauth_url)
    except Exception as e:
        print(e)
        return redirect(Oauth.discord_login_url)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", articles = user_name, avatar = user_avatar, bot_redirect = Oauth.discord_bot_oauth_url)
@app.route('/servers')
def servers():
    if request.cookies.get('token') == None:
        return redirect(Oauth.discord_login_url)
    else:
        global members_json
        global user
        members = []
        guilds = []
        guilds_icon = []
        members_list = []
        counter = [0]

        at = request.cookies.get('token')

        user_json = Oauth.get_user_json(at)
        user_name = user_json.get("username")
        user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'
        guilds_json = Oauth.get_guilds_json(at)
        global members_json
        for guild in guilds_json:

            if guild.get("permissions") & 0x8 == 0x8:
                if Oauth.get_guild_members_json(guild.get("id"), Oauth.client_id) == {'message': 'Missing Access', 'code': 50001}:
                    g = {
                    'name': guild.get("name"),
                    'id': guild.get("id"),
                    'icon': guild.get("icon"),
                    'redirect': f'{Oauth.discord_bot_oauth_url}&guild_id={guild.get("id")}',
                    'bot_in': False
                    }
                    guilds.append(g)
                else:
                    g = {
                    'name': guild.get("name"),
                    'id': guild.get("id"),
                    'icon': guild.get("icon"),
                    'redirect': f'/{guild.get("id")}',
                    'bot_in': True
                    }
                    guilds.append(g)
        # return str(guilds)
        return render_template("server.html", servers = guilds, articles = user_name, avatar = user_avatar, bot_redirect = Oauth.discord_bot_oauth_url,
        url = Oauth.discord_bot_oauth_url)

@app.route("/<int:server_id>")
def server_settings(server_id):

    if request.cookies.get('token') == None:
        return redirect(Oauth.discord_login_url)
    else:
        at = request.cookies.get('token')

        user_json = Oauth.get_user_json(at)
        user_name = user_json.get("username")
        user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'
        guilds_json = Oauth.get_guild_by_id_json(server_id)
        # Oauth.send_message(766620925981753364) # отправка сообщений
        return render_template("dashboard.html", articles = user_name, avatar = user_avatar, bot_redirect = Oauth.discord_bot_oauth_url,
        server_id = server_id)
@app.route("/<int:server_id>/embed_message",  methods = ['POST', 'GET'])
def embed_message(server_id):
        if request.cookies.get('token') == None:
            return redirect(Oauth.discord_login_url)
        else:
            channels_json = Oauth.get_guild_channels_json(server_id)

            at = request.cookies.get('token')

            user_json = Oauth.get_user_json(at)
            user_name = user_json.get("username")
            user_avatar = f'https://cdn.discordapp.com/avatars/{user_json.get("id")}/{user_json.get("avatar")}.png?size=1024'

        if request.method == 'POST':
            text  = request.form['message']
            choose = request.form['channels']
            title = request.form['title']
            Oauth.send_message(choose, title, text)
            return render_template("embeds.html", articles = user_name, avatar = user_avatar,
            channels = channels_json, bot_redirect = Oauth.discord_bot_oauth_url)

        else:

                return render_template("embeds.html", articles = user_name, avatar = user_avatar,
                server_id = server_id,
                channels = channels_json, bot_redirect = Oauth.discord_bot_oauth_url)
@app.route('/exit')
def exit():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', '0', max_age=0)
    return resp
if __name__ == "__main__":
    app.run(debug = True)
client.run('NzY4MTQ4NjA0MzY3NTM2MTM4.X48QIg.FfL0oSJUx7BV1KUi6FpwFXgyW9E')
