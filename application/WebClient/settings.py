import os

settings = dict(template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                static_path=os.path.join(os.path.dirname(__file__), 'static'),
                cookie_secret="MySecretCookie", #change this to an auotogeneratey thing
                login_url="/auth/",
                
                )