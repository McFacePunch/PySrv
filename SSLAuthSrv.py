from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl, urllib, threading
from socketserver import ThreadingMixIn as TMI
from urllib.parse import urlparse
import sys, os, shutil, base64, posixpath

#2-3 or 3-2?
#if python_version.startswith('3'):
    #from urllib.parse import parse_qs
    #from http.server import BaseHTTPRequestHandler


#Info!
#A mostly simple HTTP server, now with features!
###########################
#Features working:NOTHING!
#To Fix: Webserver without serving your drive, adds Basic Auth, SSL(with OpenSSL),
#Todo: multi-page director, digest auth, do_POST() all the things
###########################

LPORT = 443
CERTFILE_PATH = "localhost.pem"    
        
class TestHandler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    key = ''
    SrvObject = None
    EnableFileRead = False
    home = None
    about = None
    news = None
    blog = None
    contact = None
    
    def __init__(self):
        #uses, ready base webpage and prepare crypto
        with open('index.html', 'rb') as f:
            self.indexhtml = f.read()
        
    
    def do_AuthenticateHeader(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()#Sends a blank line, indicating the end of the HTTP headers in the response

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.SrvObject)#THIS IS WHERE THE HMTL/DATA IS ACTUALLY SENT TO CLIENT!!!!
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def GetPageData():
        return

    def parseURI():
        #parse URI
        #Use cache not disk
        o = urlparse.urlparse(self.path)
        if o.path.lower() == '/' or o.path.lower() == '/index.html' or o.path.lower() == '/index.htm':#preloaded main index
            if self.indexhtml != None:
                f = self.indexhtml
                pass
            else:
                self.send_error(404, "File not found - C")
                return None
        #choose index    
        if o.path.lower() in pages and self.EnableFileRead == True:
            if o.path.lower() == '/home':
                i = home
            elif o.path.lower() == '/about':
                i = about
            elif o.path.lower() == '/news':
                i = news
            elif o.path.lower() == '/blog':
                i = blog
            elif o.path.lower() == '/contact': #complaints page with picture upload
                i = contact
            else:
                self.send_error(404, "File not found")
                return None
            return i

    def send_head(self):
        f = None
        pages = ['/home', '/about', '/news', '/blog', '/contact']
        print(self.headers())
        if self.headers.getheader('Authorization') == 'Basic '+self.key: #if valid pass else return auth header
            pass
        else:
            self.do_AUTHEDHEADER() #Failz
            return None

        #former parse URI
        self.parseURI()

        #Create index file object
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        return f
    
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)"""
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def buildcache():
        return

class ThreadedHTTPServer(TMI, HTTPServer):
    """Handle requests in a separate thread."""

#content type examples
#self.send_header('Content-type', 'text/html')
#self.send_header("Content-type", 'text/plain')
#self.send_header("Content-type", 'application/octet-stream')

if __name__ == '__main__':
    key = base64.b64encode(b"cookie:cookie")#sys.argv[1])
    TH = TestHandler
    TH.key = key
    #httpd = HTTPServer(('localhost', 80), TH)
    httpd = ThreadedHTTPServer(('localhost', 80), TH)
    #httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='server1.key', certfile='server1.cert', server_side=True)
    print("serving!")
    httpd.serve_forever()
    
    
