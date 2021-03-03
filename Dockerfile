FROM ubuntu:18.04
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==2.2.1 && pip3 install -U spacy==2.3.5
ADD . /app/
ENV LC_ALL=C.UTF-8 
ENV LANG=C.UTF-8
RUN pip3 install /app/gujarati_model_fastText/guj_model-0.0.1.tar.gz && python3 -m spacy link gu_model gu
RUN pip3 install PyYAML
RUN mkdir /app/models && chmod +x /app/start_services.sh
RUN cd /app && rasa train
CMD /app/start_services.sh