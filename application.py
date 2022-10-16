
from email.mime import application
from flask import Flask, render_template, request, make_response, redirect, url_for
import flask
import pandas as pd
import numpy as np
# from utils import read_scr_csv, prepare_scr_for_js
import json

HOST_NAME = '0.0.0.0'
HOST_PORT = 81
# Elastic Beanstalk doesn't accept 'app', switching to 'application'
application = Flask(__name__)
application.debug = True

@application.route("/", methods=('GET', 'POST'))
# This function renders the annotation main page
# which extends table_base.html template, and uses bootstrap-table plugin
# Currently the annotation tool can edit the transcript, and annotate some cols
# ToDo
# 1. generalize to unknown variables to be annotated
# 2. have a seperate datahandler, seperate out data directory
# 3. audio/data directories intake form
def transcript_annotator():
  df = pd.read_csv("static/data/data.csv")
  df_var = pd.read_csv("static/data/annotation_schema.csv")
  col_toannot = df.columns.to_list() # this needs to be changed to a json file
  data_all = df.to_json(orient="records")
  if flask.request.method == 'POST':
    annot_output = json.dumps(request.get_json())
    annot = pd.read_json(annot_output, orient="index")
    annot.to_csv("static/data/output.csv") # this needs to save differently
  return render_template("annotation_page.html",col_toannot= json.dumps(col_toannot), data_all = data_all )

@application.route("/results", methods=('GET', 'POST'))
def display_results():
  # df_results = 
  return render_template("results_dashboard.html")


if __name__ == "__main__":
  application.run(HOST_NAME, HOST_PORT)
