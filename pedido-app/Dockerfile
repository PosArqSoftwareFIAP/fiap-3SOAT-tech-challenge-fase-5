FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

# RUN  python app.py

# CMD ["tail", "-f", "/dev/null"]


ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]