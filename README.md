# DOSpaces

This is a simple Command line utility to mannagw with S3  storage from command line
mainly  for Mac OS X, but shoudl work with linux and can be ported  to windows  and python3 if necessary.

Nhecked and teste with digitalocean spaces ( http://www.digitalocean.com)

Not stable.

Mainly created in educational purposes

## config.cfg
before using  copy spaces.cfg.defaults to space.cfg  and put there your identities.

## Main usage

__python dofiles.py  -l__ lists all files

__python dofiles.py  -u <filename>__ uploads filename to storage

__python dofiles.py  -d -k <filename>__  downloads  filename to storage

