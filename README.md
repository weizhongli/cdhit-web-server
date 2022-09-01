# cdhit-web-server

## Installation of cdhit-web-server through Docker
cdhit-web-server can be installed on your local computer through Docker.
1) install Docker on your system
2) run the latest cdhit-web-serverdocker image: 
```
docker run -d -h cdhit-server --name cdhit-server -p 8088:80 weizhongli1987/cdhit-server:latest
```
3) Now you can access the cdhit web server from
> http://localhost:8088/cdhit-web-server

And you can upload files to the local cdhit server, the same way as using the public cdhit web server.

4) It is suggested to learn a bit more docker commands about how to start/stop/delete the docker container and how to manage the docker image.


## Manual installation of cdhit-web-server

1) enable apache server on Linux system

2) configure apache server
The cdhit-web-server code need to be copied under Apache's DocumentRoot 
(e.g. /home/home/oasis/data/www/cdhit-web-server). Then the cgi-bin directory
within /home/home/oasis/data/www/cdhit-web-server need to be added to Apache 
config file so that cgi scripts can be executed.

text like below need to be added to Apache config file. Different version of
Apache, the location of config file is different. for example 
/etc/apache2/sites-available, 
/etc/apache2/sites-enabled/000-default

        <Directory "/home/oasis/data/www/home/cdhit-web-server/cgi-bin">
            AddHandler cgi-script .cgi .pl
            Options FollowSymLinks +ExecCGI
            AllowOverride None
        </Directory>

for some version of Apache2, you may need to 
   cd /etc/apache2/mods-enabled; 
   ln -s ../mods-available/cgid* . 

or to use command: a2enmod cgid

3) download most up to date cd-hit and compile
4) download NCBI blast+ package
5) Edit cgi-bin/server-config
6) READ output.README 
   to create a symbolic to a job dir (e.g. ln -s /path_to_job_dir output) 
7) some perl modules maybe no longer standard for some Linux 
   e.g. Switch.pm. try
   sudo apt-get install libswitch-perl
