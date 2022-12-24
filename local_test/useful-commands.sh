docker rm localserve;nvidia-docker run -p 5000:8080 --name localserve -it dummy-whisper-async:latest bash
docker exec -it localserve bash
