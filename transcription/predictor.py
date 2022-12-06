#1. imported whisper
#2. in transformation changed code to return text

from __future__ import print_function

import os, sys, stat
import json
import shutil
import flask
from flask import Flask, jsonify
import glob
import tempfile
import whisper
import base64
import pprint
import torch
DATA_PATH = '/tmp/data'

# in this tmp folder, audio for inference will be saved

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH, mode=0o755,exist_ok=True)
'''
os.system(f'wget https://upload.wikimedia.org/wikipedia/commons/3/32/Audio_James_Randi.wav -P {DATA_PATH}')
'''

            
# # A singleton for holding the model. This simply loads the model and holds it.
# # It has a predict function that does a prediction based on the model and the input data.
# class ClassificationService(object):

#     @classmethod
#     def get_model(cls):
#         """Get the model object for this instance."""
#         return load_learner(path=TMP_MODEL_PATH) #default model name of export.pkl 

#     @classmethod
#     def predict(cls, input):
#         """For the input, do the predictions and return them."""
        
#         learn = cls.get_model()
#         return learn.predict(input) 

# The flask app for serving predictions
app = flask.Flask(__name__)
# global model
# model = whisper.load_model("large.pt")
# print('model loaded')

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
#     health = ClassificationService.get_model() is not None  
    health = True
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transcribe():
    print('invoked')
#     global model
    model = whisper.load_model("large.pt")
    print('model loaded')
    if torch.cuda.is_available():
        model.to('cuda')
    print('on cuda')

    
    if flask.request.content_type == 'application/json':
        '''
        print("request.content_type == 'application/json'")
#         print(flask.request)
        print(flask.request.headers)
        print(flask.request.cookies)
        print(flask.request.data)
        print(flask.request.args)
        print(flask.request.form)
        print(flask.request.endpoint)
        print(flask.request.method)
        print(flask.request.remote_addr)
        request = flask.request.get_json()
        print("returning request")
        return request
        '''
        request = flask.request.get_json()
        # Unpack data and hyperparams for testing
        try:
            data = request['data']
            #'''
            ext = request['ext']
        except KeyError as e:
            print(e)
        
        audio_path = os.path.join(DATA_PATH,next(tempfile._get_candidate_names())  + ext)
        #'''
#         audio_path = os.path.join(DATA_PATH,next(tempfile._get_candidate_names())  + ".wav")
        wav_file = open(audio_path, "wb")
        decode_string = base64.b64decode(data)
        wav_file.write(decode_string)        
        wav_file.close()
    else:
        print("request.content_type not json")
        return flask.Response(response='This predictor only supports json data', status=415, mimetype='text/plain')
    
#     return {'status':'returning from transcribe'}
    try:
#         model = whisper.load_model("large",download_root=TMP_MODEL_PATH)
#         model = whisper.load_model("tiny.pt")
#         model = whisper.load_model("large.pt")
#         print('model loaded')
        
        with torch.no_grad():
            result = model.transcribe(audio_path)
            print(result)
            print('result')
    except OSError as e:
        print('OSError',e)
        print('BEFORE nvidia-smi')
        del model
        import gc;gc.collect()
        os.system(f'rm {audio_path}')
        torch.cuda.empty_cache()
        print('AFTER nvidia-smi')
        os.system('nvidia-smi')
        raise e
        
    except Exception as e:
        print(e)
        print('BEFORE nvidia-smi')
        del model
        import gc;gc.collect()
        os.system(f'rm {audio_path}')
        torch.cuda.empty_cache()
        print('AFTER nvidia-smi')
        os.system('nvidia-smi')
        raise Exception

    print('returning')
    del model
    import gc;gc.collect()
    os.system(f'rm {audio_path}')
    torch.cuda.empty_cache()
    print('FINAL nvidia-smi')
    os.system('nvidia-smi')
    return result
    

