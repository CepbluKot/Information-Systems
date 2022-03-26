FROM python:latest

WORKDIR /Users/igormalysh/Documents/codes/dockus

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./

CMD [ "python3", "./main.py"]