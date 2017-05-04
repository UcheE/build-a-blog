#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blogpost(db.Model):
    title = db.StringProperty(required = True)
    blogpost = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class FrontPage(Handler):
    def render_form(self, title="", blogpost="", error=""):
        blogp= db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 5")

        self.render("newpost.html", title=title, blogpost=blogpost, error=error,
                    blogp = blogp)
#redirect to the blog handle once post
    def get(self):
        self.response.write("blog")


class Blog(Handler):
    def get(self):
        query = Blogpost.all().order("created")
        writenew_posts = query.fetch(limit = 5)

        self.render("blog.html", blogp = writenew_posts)

class Newpost(Handler):
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        write_title = self.request.get("title")
        write_blogpost = self.request.get("body")

        if write_title and write_blogpost:
            b = Blogpost(title = write_title, blogpost = write_blogpost)
            b.put()

            self.redirect('/blog/')
        else:
            error = " Please fill in both title and post entry, both are required!"
            t = jinja_env.get_template("newpost.html")
            content = t.render( title = write_title,
                                entry = write_blogpost,
                                error=error)
            self.response.write(content)

class ViewPostHandler(Handler):
    def get(self, id):
        post = Blogpost.get_by_id(int(id))
        if post:
            t = jinja_env.get_template("permalink.html")
            content = t.render(post=post)
            self.response.write(content)
        else:
            self.response.write("No post here.")

app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/blog/newpost', Newpost),
    ('/blog/newpost/', Newpost),
    ('/blog', Blog),
    ('/blog/', Blog),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)],
    debug=True)
