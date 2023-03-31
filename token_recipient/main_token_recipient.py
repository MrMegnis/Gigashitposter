from dotenv import load_dotenv
from flask import Flask
import token_recipient
import sys
import os
sys.path.append('../app')
directory = os.getcwd()

print(directory)
print(os.listdir())

from data import db_session
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mega_secret_key'

@app.route('/')
def index():
  return "aboba"


if __name__ == "__main__":
    load_dotenv('.env')
    db_session.global_init()
    app.register_blueprint(token_recipient.blueprint)
    app.run()

