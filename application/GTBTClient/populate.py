import os

def populate():

def add_notification(user, entity, message):
    = Notifications.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]



# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
    from app.models import Category, Page
    populate()