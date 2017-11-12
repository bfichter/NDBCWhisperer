MONGO_HOST = 'localhost'
MONGO_PORT = 27017
#TODO
#MONGO_USERNAME = '<your username>'
#MONGO_PASSWORD = '<your password>'
MONGO_DBNAME = 'ndbc'
#DEBUG = True
IF_MATCH = False

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

users = {
    #'item_title': 'user',
    
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'user_id'
    },
    
    'schema': {
        'user_id': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'token': {
            'type': 'list'
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
        'user_id': {
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

directionType = {
    'type': 'dict',
    'schema': {
        'compass': {'type': 'string'},
        'angle': {'type': 'number'}
    }
}

readings = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'station_id'
    },
    
    'schema': {
        'station_id': {
            'type': 'string',
            'required': True
        },
        'buoy_name': {
            'type': 'string',
            'required': True
        },
        'wind_direction': directionType,
        'wind_speed': {'type': 'number'},
        'wind_gust': {'type': 'number'},
        'wind_height': {'type': 'number'},
        'wave_height': {'type': 'number'},
        'dominant_period': {'type': 'number'},
        'average_period': {'type': 'number'},
        'wave_direction': directionType,
        'air_temperature': {'type': 'number'},
        'significant_wave_height': {'type': 'number'},
        'swell_height': {'type': 'number'},
        'swell_period': {'type': 'number'},
        'swell_direction': {'type': 'string'},
        'wind_wave_height': {'type': 'number'},
        'wind_wave_period': {'type': 'number'},
        'wind_wave_direction': {'type': 'string'},
        'average_wave_period': {'type': 'number'},
        'first_time': {'type': 'string'},
        'second_time': {'type': 'string'}
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
    'readings': readings,
    'buoys': buoys
}
