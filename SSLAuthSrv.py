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
#Features working:NOTHING!
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
    EnableFileRead = False
    indexhtml = None
    home = None
    about = None
    news = None
    blog = None
    contact = None
    pages = ['/index', '/home', '/about', '/news', '/blog', '/contact']#registered pages; eventually a .cfg maybe
    
    def do_AuthenticateHeader(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()#Sends a blank line, indicating the end of the HTTP headers in the response

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Serve a GET request."""
        self.logic()
        

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.logic(head=True)

    def parseURI(self):
        #parse URI
        #Use cache not disk
        o = urlparse(self.path)
        if o.path.lower() == '/' or o.path.lower() == '/index.html' or o.path.lower() == '/index.htm':#preloaded main index
            if self.indexhtml != None:
                i = self.indexhtml
                pass
            else:
                self.send_error(404, "File not found")
                return None
            
        #choose page    
        if o.path.lower() in pages and self.EnableFileRead == True:
            if o.path.lower() == '/home':
                i = home,1
            elif o.path.lower() == '/about':
                i = about,0
            elif o.path.lower() == '/news':
                i = news,0
            elif o.path.lower() == '/blog':
                i = blog,0
            elif o.path.lower() == '/contact': #complaints page with picture upload
                i = contact,0
            else:
                self.send_error(404, "File not found")
                return None
            return i #return tuple of page,challenge

    def logic(self, head=False):
        page = None
        
        page,challenge = self.parseURI()
        
        if challenge == 1:
            if self.headers.getheader('Authorization') == 'Basic '+self.key: #if valid pass else return auth header
                pass
        else:
            self.do_AUTHEDHEADER() #Failz
            return None
        
        #Write data to client
        if page and head == True:
            self.copyfile(f, self.wfile)#wfile Contains the output stream for writing a response back to the client. Proper adherence to the HTTP protocol must be used when writing to this stream.
            f.close()
        
        self.do_HEAD()
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

    def BuildPageCache():
        blobs = []
        for page in self.pages: #internal registered pages; eventually a .cfg maybe
            pagename = page.strip('/')
            dirlist = os.listdir()
            for filename in dirlist:
                if pagename in filename:
                    with open(filename,'rb') as file:
                        out = file.read()
                        TupleOut = pagename,out
                        blobs.append(TupleOut)
                else:
                    pass
        #tuple filling here
        self.indexhtml = None
        self.home = None
        self.about = None
        self.news = None
        self.blog = None
        self.contact = None
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
    TH.BuildPageCache
    #httpd = HTTPServer(('localhost', 80), TH)
    httpd = ThreadedHTTPServer(('localhost', 80), TH)
    #httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='server1.key', certfile='server1.cert', server_side=True)
    print("serving!")
    httpd.serve_forever()
    
    
