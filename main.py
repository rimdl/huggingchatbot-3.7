from flask import Flask,request,render_template
from hugchat import hugchat
from hugchat.login import Login

app = Flask(__name__)
cookie_path_dir = "./cookies_snapshot"
userinfo_path = "./userinfo_path"

chatbot = None

def getbot():
  try:
    email = ""
    with open(userinfo_path, 'r') as file:
      email = file.read()
    sign = Login(email, None)
    cookies = sign.loadCookiesFromDir(cookie_path_dir)
    global chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
  except Exception as e:
    print(e)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login')
def login():
  email = request.args.get("email")
  passworld = request.args.get("password")

  cookies = ""
  info = ""

  try:
    sign = Login(email, passworld)
    cookies = sign.login()
    sign.saveCookiesToDir(cookie_path_dir)
    with open(userinfo_path,'w') as file:
      file.write(email)
  except Exception as e:
    info = e
    print(e)

  if len(cookies):
    return "登录成功，cookie已保存至["+cookie_path_dir+"]"
  else:
    print(cookies)
    return "登录失败，重新登录试试 --> "+str(info)

@app.route("/refresh")
def refresh():
  try:
    email = ""
    with open(userinfo_path, 'r') as file:
      email = file.read()
    sign = Login(email, None)
    cookies = sign.loadCookiesFromDir(cookie_path_dir)
    global chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return "刷新成功"
  except Exception as e:
    print(e)
    return "刷新失败 "

@app.route('/chat')
def chat():
  message = request.args.get("message")
  query_result = chatbot.query(message)
  print(chatbot.active_model)
  return str(query_result)

@app.route('/chatstream')
def chatstream():
  message = request.args.get("message")
  for resp in chatbot.query(
          message,
          stream=True
  ):
    print(resp)
  return "stream流"

@app.route('/help')
def help():
  cmds = "/change?num=xx：切换模型，/newchat:开启新会话，/list：获取对话列表，/models：获取可用的模型列表，/alllist：从服务器获取所有回话列表"
  return cmds

@app.route("/newchat")
def newchat():
  id = chatbot.new_conversation()
  chatbot.change_conversation(id)
  return "新会话开启"

@app.route("/list")
def list():
  conversation_list = chatbot.get_conversation_list()
  return str(conversation_list)

@app.route("/models")
def models():
  models = chatbot.get_available_llm_models()
  models_str = ""
  for model in models:
    models_str += ("[" + str(model) + "] ")
  return models_str

@app.route("/alllist")
def alllist():
  conversations = chatbot.get_remote_conversations(replace_conversation_list=True)
  conversations_str = ""
  for conversation in conversations:
    conversations_str += ("[" + str(conversation) + "] ")
  return conversations_str

@app.route("/change")
def change():
  # id = chatbot.new_conversation()
  # chatbot.change_conversation(id)
  num = request.args.get("num")
  chatbot.switch_llm(int(num)-1)
  return "切换成功"

@app.route("/test")
def test():
  print(chatbot.active_model)
  return "test"

getbot()
app.run(host='0.0.0.0', port=81)
