import json
import os
import tempfile
import base64
from timeit import default_timer as timer
def send_request(audio_path,url):
    print('using',audio_path)
    #=====================================================================
    audio_base64 = base64.b64encode(open(audio_path, "rb").read())
    ext = audio_path.split('.')[-1]
    payload = audio_base64
    request_dict ={
        'data':payload.decode(),
        'ext':ext}

    with tempfile.NamedTemporaryFile(mode='w+',suffix='.json',delete=True) as f:
        json.dump(request_dict,f)    
        f.seek(0)
        os.system(f'bash predict.sh {url} {f.name} "application/json"')

# audio_path = '/home/ec2-user/SageMaker/Audio_James_Randi.wav'
# audio_path = '/home/ec2-user/SageMaker/Audio_James_Randi_Long_Version.ogg'
audio_path = '/home/ec2-user/SageMaker/thecantervilleghostversion2_01_wilde_128kb.mp3'
start = timer()
send_request(audio_path,'127.0.0.1:5000')

# your code here    
print(timer() - start)

