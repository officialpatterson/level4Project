mongod & >> "Datastore-"date
python services/data-service.py & >> "Dataservice-"date
python GTBTClient/manage.py runserver & >> "Webclient-"date
python feed-enrichment/live-classification.py & >> "Feedenrichment-"date