"""This is orders class defining the orders class model constructor """

class Orders:
    """ """
    def __init__(self, *args):
        """This is orders class constructor"""
        self.user_id = args[0]
        self.order_id = args[1]
        self.order_name = args[2]
        self.senders_names = args[3]
        self.senders_contact = args[4]
        self.parcel_pickup_address = args[5]
        self.parcel_destination_address = args[6]
        self.receivers_names = args[7]
        self.receivers_contact = args[8]
        self.parcel_weight = args[9]
        self.price = args[10]
        self.date = args[11]
        self.order_status = args[12]




    