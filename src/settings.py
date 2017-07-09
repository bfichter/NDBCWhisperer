MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#TODO
#MONGO_USERNAME = '<your username>'
#MONGO_PASSWORD = '<your password>'
MONGO_DBNAME = 'ndbc'
#DEBUG = True

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

users = {
    #'item_title': 'user',
    
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'number'
    },
    
    'schema': {
        'number': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'token': {
            'type': 'string',
        }       
    }
}

rangeType = {
    'type': 'dict',
    'schema': {
        'clockwise_start': {'type': 'double'},
        'clockwise_end': {'type': 'double'}
    }
}

alerts = {
    'schema': {
        'number': {
             'type': 'string',
             'required': True,
        },
        'wind_direction_range': rangeType,
        'wave_direction_range': rangeType,
        'swell_direction_range': rangeType,
        'wind_speed_max': {'type': 'int32'},
        'wave_height_min': {'type': 'double'},
        'wave_period_min': {'type': 'int32'},
        'swell_height_min': {'type': 'double'},
        'swell_period_min': {'type': 'int32'}
    }
}

# TODO, disable put post etc
buoys = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'station_id'
    },
    
    'schema': {
        'station_id': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'name': {'type': 'string'}       
    }
}

DOMAIN = {
    'users': users,
    'alerts': alerts,
    'buoys': buoys
}
