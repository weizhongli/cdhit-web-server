# cdhit-web-server


Steps to install cdhit-web-server

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

3) download most up to date cd-hit and compile
4) download NCBI blast+ package
5) Edit cgi-bin/server-config
6) READ output.README 
   to create a symbolic to a job dir (e.g. ln -s /path_to_job_dir output) 
7) some perl modules maybe no longer standard for some Linux 
   e.g. Switch.pm. try
   sudo apt-get install libswitch-perl
