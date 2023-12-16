FROM python:3.10-alpine3.18

ADD src .
ADD requirements.txt .
RUN pip install
CMD [“python”, “./src/app.py”] 