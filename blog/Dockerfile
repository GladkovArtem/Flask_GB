FROM python:3.7.9

WORKDIR /app

COPY requirements.txt requirements.txt
#RUN pip install --no-cache --user -r requirements.txt
RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py
COPY blog ./blog

EXPOSE 5000

CMD ["python", "wsgi.py"]
