from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
	return "Wassup browski"

def run():
	app.run(host='0.0.0.0', port=8888)

def keep_alive():
	th = Thread(thread=run)
	th.start()
