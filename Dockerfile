FROM python:3.6.1-alpine
WORKDIR /project
ENV DOCKER=True
ADD . /project
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","main.py"]

#docker build -t harvest-michael .
#docker run -d -p 5000:5000 harvest-michael