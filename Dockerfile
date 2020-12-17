FROM python:3.8-slim
WORKDIR /app
COPY . .
EXPOSE 8888
RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn lxml
CMD uvicorn main:app --host 0.0.0.0 --port 8888