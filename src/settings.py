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
        'clockwise_start': {'type': 'number'},
        'clockwise_end': {'type': 'number'}
    }
}

alerts = {
    'schema': {
        'number': {
             'type': 'string',
             'required': True,
        },
        'station_id': {
            'type': 'string',
            'required': True,
        },
        'wind_direction_range': rangeType,
        'wave_direction_range': rangeType,
        'swell_direction_range': rangeType,
        'wind_speed_max': {'type': 'integer'},
        'wave_height_min': {'type': 'number'},
        'wave_period_min': {'type': 'integer'},
        'swell_height_min': {'type': 'number'},
        'swell_period_min': {'type': 'integer'}
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
