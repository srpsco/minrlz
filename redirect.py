import cgi
import base64

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MyURL(db.Model):
  LongURL = db.LinkProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class Redirect(webapp.RequestHandler):
  def get(self):
	self.response.out.write('<html><body>The URL is <br />')
	mypath = self.request.path.strip()
	self.response.out.write(mypath)
	mypath = mypath[1:(len(self.request.path))]
	self.response.out.write(mypath)
	
	self.response.out.write("<br />")
	self.response.out.write("<br />")
	
	mypath = str(mypath.replace('%3D', '='))
	self.response.out.write(mypath)
	mypath = base64.urlsafe_b64decode(mypath)
	
	self.response.out.write("<br />")
	self.response.out.write("<br />")
	self.response.out.write("<br />")
	self.response.out.write("<br />")
	self.response.out.write("<br />")

	d = MyURL.get_by_id(int(mypath))

	self.response.out.write(d.LongURL)
	self.redirect(d.LongURL)

	
	self.response.out.write('</body></html>')
  
application = webapp.WSGIApplication([('/.*', Redirect)],debug=False)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()