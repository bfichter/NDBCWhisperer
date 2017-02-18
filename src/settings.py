MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#TODO
#MONGO_USERNAME = '<your username>'
#MONGO_PASSWORD = '<your password>'
MONGO_DBNAME = 'ndbc'

RESOURCE_METHODS = ['GET']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

users = {
    'item_title': 'user',
    
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'number'
    },
    
    'schema': {
        'number': {
            'type': 'string',
            'required': True,
            'unique': True
        }
    }
}

DOMAIN = {
    'users': users
}