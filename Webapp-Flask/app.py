import re
from datetime import datetime
from flask import render_template
import time

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
     return render_template("home.html")
    
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

def sendString():
    recyclables = ["cardboard", "paper", "plastic", "aluminum", "glass"]
    nonRecyclable = "not recyclable"
    
    for x in recyclables:
        print(x)
        time.sleep(5)
        
    print (nonRecyclable)

    
