FROM python:3.10
ADD . /back
WORKDIR /back
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD python app.py