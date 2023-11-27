from flask import Flask,request,render_template
from hugchat import hugchat
from hugchat.login import Login

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login')
def login():
  email = request.args.get("email")
  passworld = request.args.get("password")

  cookie_path_dir = "./cookies_snapshot"

  cookies = ""
  info = ""

  try:
    sign = Login(email, passworld)
    cookies = sign.login()
    sign.saveCookiesToDir(cookie_path_dir)
  except Exception as e:
    info = e
    print(e)

  if len(cookies):
    return "登录成功，cookie已保存至["+cookie_path_dir+"]"
  else:
    print(cookies)
    return "登录失败，重新登录试试 --> "+str(info)

app.run(host='0.0.0.0', port=81)
