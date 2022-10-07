import pandas as pd
import os

def read_scr_csv(scr_dir,dataframe):
    # csvfiles = []
    # for file in os.listdir(scr_dir):
    #     if ".csv" in file:
    #         d = pd.read_csv(scr_dir+file)        
    #     csvfiles.append(d)
    df_scr = pd.concat(scr_dir+dataframe, ignore_index =True)
    return df_scr

# # check to see if the audio files in the directory match with the filenames in csv file
# def check_audio_csv_match(df_scr, audio_file_dir):
#     return audio_csv_message

# 
def prepare_scr_for_js(df_scr):
    df_scr_json = df_scr.to_json()
    return df_scr_json

