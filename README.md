# Take screenshot from url

## Installation:
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python3 main.py -h`


## Usage:
```
usage: use "python main.py --help" for more information

Get screenshot of URL.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL to screenshot
  --urls URLS [URLS ...]
                        URLS list to screenshot
  --url-file URL_FILE   URL or URLS list file to screenshot
                        example generate list ip with nmap:
                        	nmap -sL -n 192.168.1.0/24 | awk '/Nmap scan report/{print "http://"$NF"/"}'
  --enable-js           enable js
  --disable-js          disable js
  --outdir OUTDIR       output directory where screenshots will saved
  --delayreq DELAYREQ   wait time in seconds between requests
  --webdriver-local     use local geckodriver binary
  --webdriver-manager   use driver manager
```
