# Build an image that can do inference in SageMaker
# This is a Python 2 image that uses the nginx, gunicorn, flask stack

FROM ubuntu:20.04
# https://anonoz.github.io/tech/2020/04/24/docker-build-stuck-tzdata.html
RUN apt-get -y update && \
         DEBIAN_FRONTEND=noninteractive \
         TZ=Asia/Singapore \
         apt-get install -y --no-install-recommends \
         wget \
         python \
         python3-pip \
         nginx \
         ca-certificates \
         build-essential \
         git \
         curl \
#          python-qt4 &&\
         ffmpeg &&\
         rm -rf /var/lib/apt/lists/*
		 
RUN apt-get clean

# ENV PYTHON_VERSION=3.6



RUN pip3 install --upgrade pip 
# Here we install the extra python packages to run the inference code
RUN pip3 install setuptools
RUN pip3 install flask gevent gunicorn && \
        rm -rf /root/.cache
RUN pip3 install torch torchvision torchaudio
RUN pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
RUN pip3 install ffmpeg-python    
RUN pip3 install transformers
#RUN cp libopenh264-2.1.1-linux64.6.so ~/anaconda3/envs/pytorch_p38/lib/libopenh264.so.5
# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
# ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/program:${PATH}"
# our work is gpu bound, so we can only serve 1 request at a time?
ENV MODEL_SERVER_WORKERS=1 
# Set up the program in the image
COPY transcription /opt/program

RUN chmod 755 /opt/program
WORKDIR /opt/program
# for inputting dummy audio
RUN wget https://upload.wikimedia.org/wikipedia/commons/3/32/Audio_James_Randi.wav
RUN chmod 755 serve
RUN chmod 755 train
