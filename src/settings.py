from config import config

mongoConfig = config['mongo']
MONGO_HOST = mongoConfig['host']
MONGO_PORT = mongoConfig['port']
if not config['general']['debug']:
    MONGO_USERNAME = mongoConfig['username']
    MONGO_PASSWORD = mongoConfig['password']
# Should maybe split this into two DBs
# 'ndbc' for buoy stuff and 'users' for other stuff 
MONGO_DBNAME = 'ndbc'
#DEBUG = True
IF_MATCH = False

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

users = {
    'additional_lookup': {
        'url': 'regex("\w+(?:-\w+)+")',
        'field': 'user_id'
    },
    
    'schema': {
        'user_id': {
            'type': 'string',
            'required': True,
            'unique': True
        }
    }
}

devices = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'token'
    },
    'schema': {
        'token': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'user_id': {
            'type': 'string',
            'required': True
        }
    }
}

notifications = {
    'additional_lookup': {
        'url': 'regex("\w+(?:-\w+)+")',
        'field': 'user_id'
    },
    'schema': {
        'user_id': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'frequency': {'type': 'string'}
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
             'required': True
        },
        'station_id': {
            'type': 'string',
            'required': True
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
        'wave_height': {'type': 'number'},
        'dominant_period': {'type': 'number'},
        'wave_direction': directionType,
        'swell_height': {'type': 'number'},
        'swell_period': {'type': 'number'},
        'swell_direction': directionType,
        'datetime': {'type': 'string'}
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
    'devices': devices,
    'notifications': notifications,
    'alerts': alerts,
    'readings': readings,
    'buoys': buoys
}
