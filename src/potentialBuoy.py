class PotentialBuoy: 
    # station_id: String *
    # buoy_name: String
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
    def mongoDB(self):
        return self.__dict__