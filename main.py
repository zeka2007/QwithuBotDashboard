from flask import Flask, request, redirect, render_template, url_for, make_response
from oauth import Oauth

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
@app.route('/exit')
def exit():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', '0', max_age=0)
    return resp
if __name__ == "__main__":
    app.run(host='0.0.0.0')
