
from flask import Flask, render_template, request, make_response, redirect, url_for
import pandas as pd
import numpy as np
# from utils import read_scr_csv, prepare_scr_for_js
import json

HOST_NAME = '0.0.0.0'
HOST_PORT = 81
app = Flask(__name__)
app.debug = True

@app.route("/", methods=('GET', 'POST'))
# This function renders the annotation main page
# which extends table_base.html template, and uses bootstrap-table plugin
# Currently the annotation tool can edit the transcript, and annotate some cols
# ToDo
# 1. generalize to unknown variables to be annotated
# 2. have a seperate datahandler, seperate out data directory
# 3. audio/data directories intake form
# 4. Also need to figure out how to save data remotely
def TranscriptAnnotator():
  df = pd.read_csv("static/data/data.csv")
  df_var = pd.read_csv("static/data/annotation_schema.csv")
  col_toannot = ["record", "filename","utterances"] + df_var.columns.to_list()
  df_toannot = df[col_toannot]
  data_all = df_toannot.to_json(orient="records")
  return render_template("annotation_page.html",col_toannot= json.dumps(col_toannot), data_all = data_all )

@app.route("/", methods=['POST'])
def table():
  return render_template("table_boot2.html")

@app.route("/index")
def index():
  return render_template("index.html")


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
