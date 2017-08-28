from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl, urllib, urlparse
import sys, os, shutil, base64, posixpath


#Info!
#A mostly simple HTTP server, now with features!
###########################
#Features working: Webserver without serving your drive, Basic Auth, SSL(with OpenSSL),
#Todo: multi-page deliver (host header director), digest auth, do_POST() all the things
###########################

LPORT = 443
CERTFILE_PATH = "localhost.pem"    
        
class TestHandler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    key = ''
    index = None
    indexhtml = None
    FileObject = None
    EnableFileRead = False
    
    #def __init__(self):
        #'''Class Constructor'''
        #uses, ready base webpage and prepare crypto
       # with open('index.html', 'rb') as f:
            #self.indexhtml = f.read()
        #return
    
    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()     

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.FileObject)#THIS IS WHERE THE HMTL/DATA IS ACTUALLY SENT TO CLIENT!!!!
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def parseURI():
        #parse URI
        o = urlparse.urlparse(self.path)
        if o.path.lower() == '/' or o.path.lower() == '/index.html' or o.path.lower() == '/index.htm':#preloaded main index
            if self.indexhtml != None
                f = self.indexhtml
                pass
            else:
                self.send_error(404, "File not found - C")
                return Nonem
            
        if o.path.lower() in pages and self.EnableFileRead == True:
            if o.path.lower() == '/home':
                i = 'home.html'
            elif o.path.lower() == '/about':
                i = 'about.html'
            elif o.path.lower() == '/news':
                i = 'news.html'
            elif o.path.lower() == '/blog':
                i = 'blog.html'
            elif o.path.lower() == '/contact': #complaints page with picture upload
                i = 'contact.html'
            try:
                f = self.GetFile(i, 'r')
                pass
            except IOError:
                self.send_error(404, "File not found - B") #needed because open I/O errors may happen even when file exists
                return None
            return f

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.  """
        ''' Present frontpage with user authentication. '''
        f = None
        pages = ['/home', '/about', '/news', '/blog', '/contact']
        #if self.headers.getheader('Authorization') == None: #send auth, first connect usually
        if self.headers.getheader('Authorization') == 'Basic '+self.key: #Found basic auth header, if valid pass else return auth header
            pass
        else:
            self.do_AUTHEDHEADER()
            return None

        #former parse URI


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

def FindSecondaryIndex(inpath): #if not none, file path returned
    out = None
    #Select index.html file
    path = self.translate_path(inpath)
    if os.path.isdir(path):
        for index in "index.html", "index.htm":
            index = os.path.join(path, index)
            if os.path.exists(index):
                out = index
    return out

#content type examples
#self.send_header('Content-type', 'text/html')
#self.send_header("Content-type", 'text/plain')
#self.send_header("Content-type", 'application/octet-stream')

if __name__ == '__main__':
    key = base64.b64encode("cookie:cookie")#sys.argv[1])
    TH = TestHandler
    TH.key = key
    with open('index.html', 'rb') as f:
        TH.indexhtml = f.read()
    #TH.EnableFileRead = True
    #httpd = HTTPServer(('localhost', 80), TestHandler)
    httpd = HTTPServer(('localhost', 80), TH)
    #httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='server1.key', certfile='server1.cert', server_side=True)
    httpd.serve_forever()
    
    
