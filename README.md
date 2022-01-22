# Take screenshot from url

## Installation:

Download and decompress Geckodriver from: https://github.com/mozilla/geckodriver/releases/latest

`python3 -m venv venv`

`source venv/bin/activate`

`pip install --upgrade pip`

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
  --delayreq DELAYREQ   wait time in seconds between requests (Default 0.5s)
  --webdriver-local     use local geckodriver binary (Default)
  --webdriver-manager   use driver manager
```
## Examples:

Take screenshot of a single url:

`python3 main.py --url 'http://192.168.1.200/'`


Take screenshot of multiple urls:

`python3 main.py --urls 'http://192.168.1.200/' 'http://192.168.1.1' --outdir '/tmp/ale/'`


Take screenshot of url in net.txt file:

`python3 main.py --url-file net.txt --outdir '/tmp/ale/'`
