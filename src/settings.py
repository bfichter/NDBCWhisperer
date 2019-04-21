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

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

users = {
    # Allow user creation to happen w/o auth
    'public_methods': ['POST'],
    'resource_methods': ['POST'],
    # Only allow for registration, no querying of users
    'item_methods': [],
    'schema': {
        'user_id': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'password': {
            'type': 'string',
            'required': True
        }
    }
}

devices = {
    'resource_methods': ['POST'],
    'item_methods': ['DELETE'],
    # Allow lookup by token (not just the mongo _id)
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
    # Allow notifications to be created w/o auth (to make reg easier on client)
    'public_methods': ['POST'],
    'resource_methods': ['POST'],
    'item_methods': ['GET', 'PUT'],
    # Allow lookup by user_id (not just the mongo _id)
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

# We need auth here (maybe the user id specific auth, only touch alerts you have)
alerts = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['DELETE', 'PUT'], 
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

readings = {
    'resource_methods': [],
    'item_methods': ['GET'],
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
        'wind_direction': {'type': 'number'},
        'wind_speed': {'type': 'number'},
        'wave_height': {'type': 'number'},
        'dominant_period': {'type': 'number'},
        'wave_direction': {'type': 'number'},
        'swell_height': {'type': 'number'},
        'swell_period': {'type': 'number'},
        'swell_direction': {'type': 'number'},
        'datetime': {'type': 'string'}
    }
}

buoys = {
    'resource_methods': [],
    'item_methods': ['GET'],
    # allow lookup by station_id
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
