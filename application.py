from flask import Flask, render_template, request, make_response, redirect, url_for
import flask
import pandas as pd
import numpy as np
# from utils import read_scr_csv, prepare_scr_for_js
import json

# HOST_NAME = '0.0.0.0'
# HOST_PORT = 81
# Elastic Beanstalk doesn't accept 'app', switching to 'application'
application = Flask(__name__)
application.debug = True
@application.route("/", methods=('GET', 'POST'))


@application.route("/annotation", methods=('GET', 'POST'))
# This function renders the annotation main page
# which extends table_base.html template, and uses bootstrap-table plugin
# Currently the annotation tool can edit the transcript, and annotate some cols
def transcript_annotator():
  df = pd.read_csv("static/data/data.csv").fillna("None")
  data_all = df.to_json(orient="records")
  if flask.request.method == 'POST':
    annot_output = json.dumps(request.get_json())
    annot = pd.read_json(annot_output, orient="index")
    annot.to_csv("static/data/output.csv") # this needs to save differently
  return render_template("annotation_page.html", data_all = data_all )

@application.route("/results", methods=('GET', 'POST'))
def display_results():
  df_results = pd.read_csv("static/data/output.csv")
  return render_template("results_dashboard.html")


if __name__ == "__main__":
  application.run()
