import os                                                                                                                                                                                                                       
import sys    
import time    
import argparse, textwrap    
from urllib.parse import urlparse    
from selenium import webdriver    
from selenium.webdriver.firefox.service import Service as FirefoxService    
from selenium.webdriver.firefox.options import Options as FirefoxOptions    
    
parser = argparse.ArgumentParser(description="Get screenshot of URL.",    
                                usage='use "python %(prog)s --help" for more information',    
                                formatter_class=argparse.RawTextHelpFormatter)    
parser.add_argument("--url", type=str,    
                    help="URL to screenshot")    
parser.add_argument("--urls", nargs="+",    
                    help="URLS list to screenshot")    
parser.add_argument("--url-file", type=str,    
                    help=textwrap.dedent('''\    
                        URL or URLS list file to screenshot    
                        example generate list ip with nmap:    
                        \tnmap -sL -n 192.168.1.0/24 | awk '/Nmap scan report/{print "http://"$NF"/"}'    
                        '''))    
parser.add_argument("--enable-js", dest="js", action="store_true",    
                    help="enable js")    
parser.add_argument("--disable-js", dest="js", action="store_false",    
                    help="disable js")    
parser.add_argument("--outdir", type=str,    
                    help="output directory where screenshots will saved")    
parser.add_argument("--delayreq", type=float,    
                    help="wait time in seconds between requests")    
parser.add_argument("--webdriver-local", dest="webdrivertype", action="store_true",    
                    help="use local geckodriver binary (Default)")    
parser.add_argument("--webdriver-manager", dest="webdrivertype", action="store_false",    
                    help="use driver manager")    
    
parser.set_defaults(js=True)    
parser.set_defaults(outdir='OUT')    
parser.set_defaults(delayreq=0.5)    
parser.set_defaults(webdrivertype=True)    
    
args = parser.parse_args()

def show_message(message, status=None):    
    CRED = '\033[31m'    
    CLRED = '\033[91m'    
    CGREEN = '\033[92m'    
    CLGREEN = '\033[4m'    
    CDGREEN = '\033[32m'    
    CGRAY = '\033[90m'    
    CWGRAY = '\033[7m'
    CWBLU = '\033[44m'
    CLBLU = '\033[94m'
    CDBLU = '\033[34m'
    CWHITE = '\033[1m'
    CORANGE = '\033[33m'
    CEND = '\033[0m'
    
    if status == "success":
        print(CGREEN + message + CEND)
    elif status == "error":
        print(CRED + message + CEND)
    elif status == "info":
        print(CWBLU + message + CEND)
    elif status == "decoration":
        print(CORANGE + message + CEND)
    else:
        print(CWHITE + message + CEND)

def url_to_filename(url):
    show_message("Output Dir: {}".format(args.outdir))
    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)
    path = args.outdir
    if path[-1] != '/':
        path = path + '/'
    domain = path + urlparse(url).netloc + '.png'
    return domain

def parse_url(url):
    show_message("Taking screenshot from url: {}".format(str(url)))

    options = FirefoxOptions()
    options.add_argument("--headless")
    options.set_preference("javascript.enabled", args.js)
    
    if args.webdrivertype == True:
        # GECKODRIVER ON
        # https://github.com/mozilla/geckodriver/releases/latest
        geckodriver_path = os.path.dirname(os.path.abspath(__file__)) + "/geckodriver"
        if not os.path.isfile(geckodriver_path):
            show_message("ERROR! Local geckodriver binary does not exist: {}".format(geckodriver_path), "error")
            show_message("Download binary at https://github.com/mozilla/geckodriver/releases/latest", "error")
            sys.exit()

        #firefox_binary_path = '/usr/bin/firefox'
        #options.binary_location = firefox_binary_path
        service = FirefoxService(geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)

    if args.webdrivertype == False:
        # WEBDRIVER MANAGER ON
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    try:
        driver.get(url)
        screenshot_filename = url_to_filename(url)
        show_message("Saving screenshot to: {}".format(screenshot_filename), "success")
        screenshot = driver.save_screenshot(screenshot_filename)
    except:
        show_message("ERROR! Something wrong parsing url: {}".format(url), "error")

    show_message("Waiting {} seconds ...".format(str(args.delayreq)), "info")
    time.sleep(args.delayreq)
    show_message("-------------------------------------", "decoration")
    driver.quit()

if args.url is not None:
    parse_url(args.url)

if args.urls is not None:
    count = 0
    for url in args.urls:
        show_message("URL item[{}]: {}".format(str(count), url))
        parse_url(url)
        count += 1

if args.url_file is not None:
    if os.path.isfile(args.url_file):
        count = 0
        show_message("Read url from file: {}".format(args.url_file))

        url_file = open(args.url_file, 'r')
        url_file_lines = url_file.readlines()
        for url in url_file_lines:
            show_message("URL file item[{}]: {}".format(str(count), url))
            if not url:
                break
            parse_url(url)
            count += 1
        url_file.close()
    else:
        show_message("ERROR! URL file does not exist: {}".format(args.url_file), "error")
        sys.exit()
