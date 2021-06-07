FROM python:3.9
RUN mkdir /dartion-app

WORKDIR /dartion-app

RUN pip install --upgrade pip

COPY ./ /dartion-app
RUN pip install -r /dartion-app/requirements.txt
RUN apt-get update -y
RUN pip install psycopg2-binary
#RUN apt-get install npm  -y

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN echo "en_AU.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen en_AU.UTF-8

ENV TZ=Australia/Sydney
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8000
EXPOSE 5000
RUN touch /sample.txt
RUN sed -i 's/MinProtocol = TLSv1.2/MinProtocol = TLSv1.0/' /etc/ssl/openssl.cnf



#RUN locale-gen en_AU.utf8
ENV LANG en_AU.UTF-8
ENV LANGUAGE en_AU:en
ENV LC_ALL en_AU.UTF-8
#CMD python baseApp/wsgi.py runserver -h 0.0.0.0
WORKDIR /dartion-app
CMD python /dartion-app/manage.py runserver 0.0.0.0:5000 --noreload

#CMD gunicorn baseApp.wsgi:application --bind 0.0.0.0:8000

#CMD tail -f /sample.txt
#CMD tail -f /dartion-app/requirements.txt


