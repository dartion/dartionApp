FROM python:3.8
RUN mkdir /dartionApp

WORKDIR /dartionApp

RUN pip install --upgrade pip

COPY . /dartion-app
RUN pip install -r /dartion-app/requirements.txt
RUN apt-get update

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN echo "en_AU.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen en_AU.UTF-8

ENV TZ=Australia/Sydney
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8000
RUN sed -i 's/MinProtocol = TLSv1.2/MinProtocol = TLSv1.0/' /etc/ssl/openssl.cnf

#CMD python wsgi.py runserver -h 0.0.0.0

#RUN locale-gen en_AU.utf8
ENV LANG en_AU.UTF-8
ENV LANGUAGE en_AU:en
ENV LC_ALL en_AU.UTF-8


CMD tail -f /dartionApp/requirements.txt
