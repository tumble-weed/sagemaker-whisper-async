import json
import os
import tempfile
import base64
def send_request(audio_path,url):
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
audio_path = '/home/ec2-user/SageMaker/Audio_James_Randi_Long_Version.ogg'
send_request(audio_path,'127.0.0.1:5000')

# docker run -p 5000:80 --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidia-caps:/dev/nvidia-caps --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm --device /dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools --name localserve -it dummy-whisper-async:latest bash