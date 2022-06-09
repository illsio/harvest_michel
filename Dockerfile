FROM python:3.9-alpine
WORKDIR /project
ENV DOCKER=True
ADD . /project
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","main.py"]

#docker build -t smasho/harvest-michael .
#docker push smasho/harvest-michael

#curl builder-back-end-44b495.appfleet.net:80/test