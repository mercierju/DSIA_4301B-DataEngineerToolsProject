FROM python:3.10
ADD . /front
WORKDIR /front
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD python dashboard.py