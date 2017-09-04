from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn as TMI
import ssl, urllib, threading
import sys, os, shutil, base64, posixpath

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


#3-2 stuff
#if python_version.startswith('3'):
    #from urllib.parse import parse_qs
    #from http.server import BaseHTTPRequestHandler


#Info!
#A mostly simple HTTP server, now with features!
###########################
#Features working:NOTHING! First to fix are parseURI and
#To Fix: Webserver without serving your drive, adds Basic Auth, SSL(with OpenSSL),
#Todo: multi-page director, digest auth, do_POST() all the things, log request, log error
###########################

#Notes:
#Methods starting with "do_" are overrides or expanded header functions
#self.wfile is inherited way to write data to client



LPORT = 443
CERTFILE_PATH = "localhost.pem"    
        
class TestHandler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    key = ''
    SrvObject = None
    EnableFileRead = True
    indexhtml = None
    home = None
    about = None
    news = None
    blog = None
    contact = None
    pages = {}#registered pages; eventually a .cfg maybe
    
#content type examples
#self.send_header('Content-type', 'text/html')
#self.send_header("Content-type", 'text/plain')
#self.send_header("Content-type", 'application/octet-stream')
    
    def do_AuthenticateHeader(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()#Sends a blank line, indicating the end of the HTTP headers in the response

    def do_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Serve a GET request."""
        self.logic(head=False)
        
    def do_HEAD(self):
        """Serve a HEAD request."""
        self.logic()

    def parseURI(self):
        i = {}
        #parse URI
        print(self.path)
        o = urlparse(self.path)
        #choose page    
        if o.path.lower():# in self.pages and self.EnableFileRead == True:
            if o.path.lower() == '/' or o.path.lower() == '/index.html':
                i = self.pages['index'],0
            elif o.path.lower() == '/home':
                i = self.pages['home'],1
            elif o.path.lower() == '/about':
                i = self.pages['about'],0
            elif o.path.lower() == '/news':
                i = self.pages['news'],0
            elif o.path.lower() == '/blog':
                i = self.pages['blog'],0
            elif o.path.lower() == '/contact': #complaints page with picture upload
                i = self.pages['contact'],0
            else:
                return None,None
        return i #return tuple of page,challenge

    def logic(self, head=True):
        page = None
        page,challenge = self.parseURI()
        
        if challenge == 1:
            if self.headers.getheader('Authorization') == None:
                self.do_AuthenticateHeader()
                self.send_error(404, "File not found")
                return
            elif self.headers.getheader('Authorization') == 'Basic '+key:
                pass
            else:#likely failed password
                self.do_AuthenticateHeader()
                self.send_error(404, "File not found")
                return

        #Give 200 OK
        self.do_200()
        
        #Write data to client
        if page != None and head == False:
            self.do_200()
            print(page)
            self.wfile.write(page)
        return

    def copyfile(self, source, outputfile): #not used now but may be later
        shutil.copyfileobj(source, outputfile)

class ThreadedHTTPServer(TMI, HTTPServer):
    """Handle requests in a separate thread."""

#Make dict from files
def BuildPageCache():
    odict = {}
    blobs = []
    pages = []
    
    with open("index.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('index')
        
    with open("home.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('home')
        
    with open("about.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('about')
        
    with open("news.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('news')
        
    with open("blog.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('blog')
         
    with open("contact.html","rb") as ifile:
        blobs.append(ifile.read())
        pages.append('contact')
    
    odict = dict(zip(pages,blobs))
    return odict

#content type examples
#self.send_header('Content-type', 'text/html')
#self.send_header("Content-type", 'text/plain')
#self.send_header("Content-type", 'application/octet-stream')

if __name__ == '__main__':
    key = base64.b64encode(b"cookie:cookie")#sys.argv[1])
    TH = TestHandler
    TH.key = key
    TH.pages = BuildPageCache()
    #httpd = HTTPServer(('localhost', 80), TH)
    httpd = ThreadedHTTPServer(('localhost', 80), TH)
    #httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='server1.key', certfile='server1.cert', server_side=True)
    print("serving!")
    httpd.serve_forever()
    
    
