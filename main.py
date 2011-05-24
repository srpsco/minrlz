import cgi
import base64

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MyURL(db.Model):
  LongURL = db.LinkProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)

# need to pull the view out of this file and use a template
class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/shorten" method="post">
			<div><label for="LongURL">Enter a URL to shorten:</label>
            <div><input type="text" name="LongURL" style="width:750px" ></div>
            <div><input type="submit" value="Shorten"></div>
          </form>
		<script type="text/javascript">
		var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
		document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
		</script>
		<script type="text/javascript">
		try {
			var pageTracker = _gat._getTracker("UA-7254144-1");
			pageTracker._trackPageview();
		} catch(err) {}</script>
        </body>
      </html>""")
  #added the following to prevent amsu getting 404 error on checking if site is up	  
  def head(self):
    self.response.out.write("""
	""")



class Short(webapp.RequestHandler):
  def post(self):
	myurl = MyURL(LongURL=self.request.get('LongURL'))
	myurl.put()	
	self.response.out.write('<html><body>You wrote:<pre>')
	self.response.out.write(cgi.escape(self.request.get('LongURL')))
	self.response.out.write('<br />')
	self.response.out.write(myurl.key().id())
	self.response.out.write('<br />')
	self.response.out.write('http://www.minrlz.com/')	
	#we need to change the meethod of shortening the url to optimize efficiency
	self.response.out.write(base64.urlsafe_b64encode(str(myurl.key().id())))
	self.response.out.write('<br />')	
	self.response.out.write(base64.urlsafe_b64decode(base64.urlsafe_b64encode(str(myurl.key().id()))))
	self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/shorten', Short)],
                                     debug=False)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
