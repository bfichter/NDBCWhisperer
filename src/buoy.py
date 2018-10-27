class Buoy: 
    # station_id: String *
    # name: String
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
    def mongoDB(self):
        return self.__dict__