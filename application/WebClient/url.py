from handlers.auth import LoginHandler, RegisterHandler
from handlers.DashboardHandler import DashboardHandler
from handlers.EntityHandler import EntityHandler
from handlers.EntityDimensionHandler import EntityDimensionHandler
from handlers.ErrorHandler import ErrorHandler
from handlers.TrackHandler import TrackHandler
from handlers.PinHandler import PinHandler
from handlers.PushPinHandler import PushPinHandler
from handlers.MakeGoldHandler import MakeGoldHandler
from handlers.DiscoverHandler import DiscoverHandler
from handlers.api.DimensionDistributionHandler import DimensionDistributionHandler
from handlers.api.LocationDistributionHandler import LocationDistributionHandler
from handlers.api.TimeDistributionHandler import TimeDistributionHandler

urls = [
        (r"/auth/", LoginHandler),
        (r"/dashboard/", DashboardHandler),
        (r"/entity/([A-Za-z0-9%]+)/", EntityHandler),
        (r"/entity/([A-Za-z0-9%]+)/([A-Za-z0-9%&]+)/", EntityDimensionHandler),
        (r"/track/", TrackHandler),
        (r"/register/", RegisterHandler),
        (r"/discover/", DiscoverHandler),
        (r"/pins/",PinHandler),
        (r"/pushpin/",PushPinHandler),
        (r"/makegold/",MakeGoldHandler),
        (r"/api/dimensiondistribution/", DimensionDistributionHandler),
        (r"/api/locationdistribution/", LocationDistributionHandler),
        (r"/api/timedistribution/", TimeDistributionHandler),
        (r"/404/",ErrorHandler),
        ]
