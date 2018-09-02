FROM python:2.7

ENV TWILIO_SID ''
ENV TWILIO_TOKEN ''
EXPOSE 5000

WORKDIR /app

RUN apt-get update > /dev/null && \
	apt-get install -y wget > /dev/null && \
	wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-214.0.0-linux-x86_64.tar.gz > /dev/null && \
	tar zxvf google-cloud-sdk-214.0.0-linux-x86_64.tar.gz google-cloud-sdk && \
	mv /app/google-cloud-sdk /google-cloud-sdk && \
	/google-cloud-sdk/install.sh && \
	/google-cloud-sdk/bin/gcloud components install cloud-datastore-emulator app-engine-go  --quiet

COPY . /app

RUN pip install -r requirements.txt

RUN export PATH=$PATH:/google-cloud-sdk/bin/

CMD python /google-cloud-sdk/bin/dev_appserver.py app.yaml --host=0.0.0.0 --port=5000 --runtime python27

