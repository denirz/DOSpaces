# DOSpaces

This is a simple Command line utility to mannagw with S3  storage from command line
mainly  for Mac OS X, but shoudl work with linux and can be ported  to windows  and python3 if necessary.

Nhecked and teste with digitalocean spaces ( http://www.digitalocean.com)

Not stable.

Mainly created in educational purposes

## config.cfg
before using  copy spaces.cfg.defaults to space.cfg  and put there your identities.

##Main usage

_python dofiles.py  -l_ lists all files

_python dofiles.py  -u <filename>_ uploads filename to storage

_python dofiles.py  -d -k <filename>_  downloads  filename to storage

