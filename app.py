
from flask import Flask, render_template, request, make_response, redirect, url_for
# import pandas as pd
# import numpy as np
import json

HOST_NAME = '0.0.0.0'
HOST_PORT = 81
app = Flask(__name__)
app.debug = True


@app.route("/")
def TranscriptAnnotator():
  return render_template("audio_annotator.html")


# @app.route("/")
# def index():
#   df = pd.read_csv("dummy.csv")

#   return render_template("csv_table.html", tables=[df.to_html(classes='data', header=False, index = False)])

# @app.route("/edited")
# def edited():
#   return render_template("editable.html")


# @app.route("/table")
# def edit_table():
#   audio_names = [
#     {'row_id':1, 'fname':"Code", 'lname':"With Mark", 'email':"mark@codewithmark.com", 'audio':"010512-4.wav"}, 
#     {'row_id':2, 'fname':"Mary", 'lname':"Moe", 'email':"mary@gmail.com",'audio':"010512-165.wav"},
#     ]
#   return render_template("table.html",audio_names=audio_names)
#   #

# @app.route('/posts/', methods=('GET', 'POST'))
# def postmessage():
#   if request.method == "POST":
#     title = request.form["title"]
#     content = request.form["content"]
#     return redirect(url_for("index"))
#   return render_template('post_message.html')



# (C) START
if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)
