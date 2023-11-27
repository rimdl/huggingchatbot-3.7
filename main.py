from flask import Flask,request,render_template
from hugchat import hugchat
from hugchat.login import Login

app = Flask(__name__)
cookie_path_dir = "./cookies_snapshot"
userinfo_path = "./userinfo_path"

chatbot = None
try:
  email = ""
  with open(userinfo_path,'r') as file:
    email = file.read()
  sign = Login(email, None)
  cookies = sign.loadCookiesFromDir(cookie_path_dir)
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

@app.route('/chat')
def chat():
  message = request.args.get("message")
  query_result = chatbot.query(message)
  print(query_result)
  return "success"

@app.route('/chatstream')
def chatstream():
  message = request.args.get("message")
  for resp in chatbot.query(
          message,
          stream=True
  ):
    print(resp)
  return "success"

@app.route('/menu')
def menu():
  option = request.args.get("option")
  print(option)
  if option == "/newchat":
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
  elif option == "/list":
    conversation_list = chatbot.get_conversation_list()
    print(conversation_list)
  elif option == "/models":
    models = chatbot.get_available_llm_models()
    print(models[0])
  elif option == "/alllist":
    conversations = chatbot.get_remote_conversations(replace_conversation_list=True)
    print(conversations)
  return "success"


app.run(host='0.0.0.0', port=81)
