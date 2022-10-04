
from flask import Flask, render_template, request, make_response, redirect, url_for
import pandas as pd
import numpy as np

HOST_NAME = '0.0.0.0'
HOST_PORT = 81
app = Flask(__name__)
app.debug = True



@app.route("/")
def index():
  df = pd.read_csv("dummy.csv")

  return render_template("csv_table.html", tables=[df.to_html(classes='data', header=False, index = False)])
  # with open("s1_dummy.csv") as file:
  #   return render_template("s3_csv_table.html", csv=file)

@app.route("/table")
def edit_table():
  return render_template("table.html")
  #

@app.route('/posts/', methods=('GET', 'POST'))
def postmessage():
  if request.method == "POST":
    title = request.form["title"]
    content = request.form["content"]
    return redirect(url_for("index"))
  return render_template('post_message.html')



# (C) START
if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)
