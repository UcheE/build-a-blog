# import os
# import webapp2
# import jinja2
#
# from google.appengine.ext import db
#
#
# template_dir = os.path.join(os.path.dirname(__file__), "templates")
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
#                                autoescape = True)
#
#
# class Handler(webapp2.RequestHandler):
#     def write(self, *a, **kw):
#         self.response.write(*a, **kw)
#
#     def render_str(self, template, **params):
#         t = jinja_env.get_template(template)
#         return t.render(params)
#
#     def render(self, template, **kw):
#         self.write(self.render_str(template, **kw))
#
#
# class Blogpost(db.Model):
#     title = db.StringProperty(required = True)
#     blogpost = db.TextProperty(required = True)
#     created = db.DateTimeProperty(auto_now_add = True)
#
#
# class FrontPage(Handler):
#     def render_form(self, title="", blogpost="", error=""):
#         blogp= db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 5")
#
#         self.render("newpost.html", title=title, blogpost=blogpost, error=error,
#                     blogp = blogp)
#
#     def get(self):
#         self.redirect("/mainblog")
#         # Landing page appears.
#
#
# class Blog(Handler):
#     def get(self):
#         query = Blogpost.all().order("created")
#         writenew_posts = query.fetch(limit = 5)
#
#         self.render("blog.html", blogp = writenew_posts)
#
# class Newpost(Handler):
#     def get(self):
#         self.render("Newpost.html")
#
#     def post(self):
#         write_title = self.request.get("title")
#         write_blogpost = self.request.get("blogpost")
#
#         if write_title and write_blogpost:
#             b = Blogpost(title = write_title, blogpost = write_blogpost)
#             b.put()
#
#             self.redirect('/')
#         else:
#             error = " Please fill in both title and post entry, they are required!"
#
#             self.render("Newpost.html", new_title = write_title,
#                         new_blogpost = write_blogpost, error=error)
#
# class ViewPostHandler(Handler):
#     def get(self, id):
#         key = db.Key.from_path("Blogpost", int(id))
#         blogpost = db.get(key)
#
#         if not blogpost:
#             self.error(404)
#             return
#
#         self.render("permalink.html", blogpost=blogpost)
#
# app = webapp2.WSGIApplication([
#     ('/', FrontPage),
#     ('/newpost', Newpost),
#     ('/blog', Blog),
#     webapp2.Route('/viewposthandler/<id:\d+>', ViewPostHandler)],
#     debug=True)
#
#
# ##################################
# import webapp2
# import cgi
# import jinja2
# import os
# from google.appengine.ext import db
#
# template_dir = os.path.join(os.path.dirname(__file__), "templates")
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
#                                autoescape = True)
#
# class Handler(webapp2.RequestHandler):
#     def write(self, *a, **kw):
#         self.response.out.write(*a, **kw)
#
#     def render_str(self, template, **params):
#         t = jinja_env.get_template(template)
#         return t.render(params)
#
#     def render(self, template, **kw):
#         self.write(self.render_str(template, **kw))
#
# class Entry(db.Model):
#     title = db.StringProperty(required = True)
#     entry = db.TextProperty(required = True)
#     created = db.DateTimeProperty(auto_now_add = True)
#
# class BlogPage(Handler):
#     # handles the '/' webpage
#     def get(self):
#         self.render("base.html")
#
# class NewPost(Handler):
#     # handles new-entry form submissions
#     def render_entry_form(self, title="", body="", error=""):
#         self.render("newpost.html", title=title, body=body, error=error)
#
#     def get(self):
#         self.render_entry_form()
#
#     def post(self):
#         title = self.request.get("title")
#         body = self.request.get("body")
#
#         if title and entry:
#             e = Entry(title=title, body=bidt)
#             e.put()
#
#             self.redirect("/blog/"+ str(e.key().id()))
#         else:
#             error = "We need both a title and entry content!"
#             self.render_entry_form(title, entry, error)
#
# class Blog(Handler):
#     #for the '/blog' webpage
#     def render_entries(self, title="", blogpost="", error=""):
#         blogs= db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 5")
#         self.render("newpost.html", title=title, blogpost=blogpost, error=error, blogs=blogs)
#
#     def get(self):
#         self.redirect("/mainblog")
#
# class ViewPostHandler(Handler):
#     #handle viewing single post by entity id
#     def render_single_entry(self, id, title="", entry="", error=""):
#         single_entry = Entry.get_by_id(int(id), parent=None)
#         self.render("single-entry.html", title=title, entry=entry, error=error, single_entry=single_entry)
#     def get(self, id):
#         if id:
#             self.render_single_entry(id)
#         else:
#             self.render_single_entry(id, title = "nothing here!",
#                         post = "there is no post with id "+ str(id))
#
# app = webapp2.WSGIApplication([
#     ('/', MainPage),
#     ('/blog', Blog),
#     ('/newpost', NewPost),
#     webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
# ], debug=True)
