FROM ubuntu:18.04

WORKDIR /opt

#### get necessary packages
RUN apt-get -y update && apt-get install -y wget build-essential zlib1g zlib1g-dev apache2 git rsync \
    libcgi-pm-perl libswitch-perl


#### download and compile cd-hit 4.8.1
RUN wget https://github.com/weizhongli/cdhit/releases/download/V4.8.1/cd-hit-v4.8.1-2019-0228.tar.gz && \
    tar xvf cd-hit-v4.8.1-2019-0228.tar.gz && \
    mv cd-hit-v4.8.1-2019-0228 cd-hit && \
    cd /opt/cd-hit && \
    make && \
    cd /opt/cd-hit/cd-hit-auxtools && \
    make 


#### get NCBI BLAST+ 2.8.1
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.8.1/ncbi-blast-2.8.1+-x64-linux.tar.gz && \
    tar xvf ncbi-blast-2.8.1+-x64-linux.tar.gz && \
    rm -f ncbi-blast-2.8.1+-x64-linux.tar.gz

#### get cd-hit webserver
RUN git clone https://github.com/weizhongli/cdhit-web-server.git && \
    mkdir www && \
    mv cdhit-web-server www && \
    cd /opt/www/cdhit-web-server && \
    cp -f Docker/server-config-docker.pl cgi-bin/server-config.pl && \
    ln -sf /opt/data output && \
    cd /opt && \
    mkdir -p data && \
    chmod -R a+rwx data && \
    rsync -av www/cdhit-web-server/etc/apache2 /etc && \
    cd /etc/apache2/mods-enabled && \
    ln -s ../mods-available/cgid* . 

#### or maybe a2enmod cgi

#### set system PATH
ENV PATH="/opt/cd-hit:/opt/cd-hit/cd-hit-auxtools:/opt/cd-hit/psi-cd-hit:/opt/ncbi-blast-2.8.1+/bin:${PATH}"

#### set apache2 ENVs
## ENV APACHE_RUN_USER root
## ENV APACHE_RUN_GROUP root
## ENV APACHE_RUN_USER www-data
## ENV APACHE_RUN_GROUP www-data
## ENV APACHE_LOG_DIR /var/log/apache2
## ENV APACHE_PID_FILE /var/run/apache2.pid
## ENV APACHE_RUN_DIR /var/run/apache2
## ENV APACHE_LOCK_DIR /var/lock/apache2

#### maybe need php
## apt-get install -y php libapache2-mod-php php-mcrypt php-mysql
## a2enmod php7.0


EXPOSE 80 443

#### make it run foreground
CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]

#### to build docker image
# docker build --tag cdhit-server https://raw.githubusercontent.com/weizhongli/cdhit-web-server/master/Docker/Dockerfile
#### to start a container
# docker run -d -h cdhit-server --name cdhit-server -p 8088:80                    cdhit-server
#### to access local cdhit-server
# go to http://localhost:8088/cdhit-web-server/


#### optional
# docker run -d -h cdhit-server --name cdhit-server -p 8088:80 -v `pwd`:/opt/data cdhit-server
# docker run -it -p 8088:80                    cdhit-server bash

