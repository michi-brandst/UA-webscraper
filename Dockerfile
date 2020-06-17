FROM python:3.8

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/ 

RUN apt update && apt upgrade -y && apt install firefox-esr -y

RUN pip install pipenv
COPY Pipfile* insttmp/
RUN cd insttmp && pipenv lock --requirements > requirements.txt
RUN pip install -r insttmp/requirements.txt
COPY *.py app/

CMD python app/main.py
