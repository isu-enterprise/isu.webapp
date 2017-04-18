# Installation as Apache mod_wsgi application

 1. Change dir to `src/isu/webapp`
 2. Run `install-admin-lte[-git].sh` check if `nasm` compiler exists on the path.
 3. Return here.
 4. Edit `.sh` and `.conf` files to suit the directory structure of the project.
 4. Run college-wsgiapp-aliases-gen.sh
 5. Place links from apache config directory to the *.conf in this one
 6. Include college-applicatio.conf in a Virtual host conf.
 7. Installation of `mod_wsgi` read (here)[http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/modwsgi/].
 
 Hope everything will work.
 
