import urllib
import http.cookiejar as cookielib
import getopt
import sys
import os

appleId = 'appleId'
password = 'password'
outputDirectory = ''
debug = False


class Options:
    def __getattr__(self, attrname):
        if attrname == 'appleId':
            return appleId
        elif attrname == 'password':
            return password
        elif attrname == 'outputDirectory':
            return outputDirectory
        elif attrname == 'debug':
            return debug
        else:
            raise AttributeError(attrname)


def usage():
    print ('''usage: %s [options]
Options and arguments:
-h     : print this help message and exit (also --help)
-a uid : your apple id (also --appleId)
-p pwd : your password (also --password)
--debug : debug output, default is off''' % sys.argv[0])


def process_cmd_args():
    global appleId
    global password
    global outputDirectory
    global debug

    # Check for command line options. The command line options
    # override the globals set above if present.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:p:Po:uvd:D:f:n', ['help', 'appleId=', 'password=', 'outputDirectory=', 'debug'])
    except getopt.GetoptError as err:
        # print help information and exit
        print(str(err))  # will print something like "option -x not recongized"
        usage()
        return 2

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            return 2
        elif o in ('-a', '--appleId'):
            appleId = a
        elif o in ('-p', '--password'):
            password = a
        elif o in '--debug':
            debug = True
        else:
            assert False, 'unhandled option'

    return 0


def show_cookies(cj):
    for index, cookie in enumerate(cj):
        print(index, ' : ', cookie)


def read_file(opener, url):
    request = urllib.request.Request(url)
    print(url)
    url_handle = opener.open(request)
    html = url_handle.read().decode('utf-8')
    f = open(os.path.join('./result.csv'), 'w')
    try:
        f.write(html)
    finally:
        f.close()


def download_file(options):

    if options.outputDirectory != '' and not os.path.exists(options.outputDirectory):
        os.makedirs(options.outputDirectory)

    urlITCBase = 'https://itunesconnect.apple.com%s'

    handlers = []

    cj = cookielib.CookieJar();
    cj.set_policy(cookielib.DefaultCookiePolicy(rfc2965=True))
    cjhdr = urllib.request.HTTPCookieProcessor(cj)
    handlers.append(cjhdr)
    opener = urllib.request.build_opener(*handlers)

    if options.debug:
        print('Signing into iTunes Connect web site.')

    # Go to the iTunes Connect website and retrieve the
    # form action for logging into the site.
    urlWebsite = 'https://idmsa.apple.com/appleauth/auth/signin'
    body = '{"accountName":"bingu.shim@netmarble.com","rememberMe":false,"password":"Dmasi89#"}'

    req = urllib.request.Request(urlWebsite, data=body.encode("utf-8"))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Accept-Language', 'ko,en;q=0.9')
    req.add_header('X-Apple-Widget-Key', 'e0b80c3bf78523bfe80974d320935bfa30add02e1bff88ec2166c6bd5a706c42')
    response = opener.open(req, timeout=1000)
    show_cookies(cj)

    result = response.read().decode('utf-8')
    price_matrix_url = 'https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/apps/982502769/pricing/matrix/export?iapType=consumable'

    read_file(opener, price_matrix_url)
    show_cookies(cj)

    return 'result'


def main():
    if process_cmd_args() > 0:    # Will exit if usgae requested or invalid argument found.
        return 2

    # Set report options.
    options = Options()
    options.appleId = appleId
    options.password = password
    options.outputDirectory = outputDirectory
    options.debug = debug

    # Download the file.
    download_file(options)


if __name__ == '__main__':
  sys.exit(main())
