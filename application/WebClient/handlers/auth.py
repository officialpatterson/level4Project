#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler

class LoginHandler(RequestHandler):
    client = MongoClient()
    users = client.gtbt.users
    
    def get(self):
        if self.get_secure_cookie("user"):
            print "logging user out"
            self.clear_cookie("user")
            self.render("auth.html")
        else:
            print "logging user in"
            self.render("auth.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        
        users= self.users.find_one({"username":username, "password":password})
        
        if users:
            self.set_secure_cookie("user", username)
            self.redirect("/dashboard/")
        else:
            self.redirect("/auth/")

class RegisterHandler(RequestHandler):
    client = MongoClient()
    users = client.gtbt.users
    def get(self):
        self.render("Register.html", registered=None)
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        if not username or not password or not email:
            return
        self.users.insert({"username":username, "password":password, "email":email})
        self.redirect("/auth/")
