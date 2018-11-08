"""This is orders class defining the orders class model constructor """

class Orders:
    
    def __init__(self, user_id, order_id, order_name, senders_names, senders_contact, parcel_pickup_address, parcel_destination_address, receivers_names, receivers_contact, parcel_weight, price, date, order_status):
        """This is orders class constructor"""
        self.user_id = user_id
        self.order_id = order_id
        self.order_name = order_name
        self.senders_names = senders_names
        self.senders_contact = senders_contact
        self.parcel_pickup_address = parcel_pickup_address
        self.parcel_destination_address = parcel_destination_address
        self.receivers_names = receivers_names
        self.receivers_contact = receivers_contact
        self.parcel_weight = parcel_weight
        self.price = price
        self.date = date
        self.order_status = order_status

    # attributes_of_an_order = {
    #     #     self.user_id = user_id
    #     self.order_id = order_id
    #     self.order_name = order_name
    #     self.senders_names = senders_names
    #     self.senders_contact = senders_contact
    #     self.parcel_pickup_address = parcel_pickup_address
    #     self.parcel_destination_address = parcel_destination_address
    #     self.receivers_names = receivers_names
    #     self.receivers_contact = receivers_contact
    #     self.parcel_weight = parcel_weight
    #     self.price = price
    #     self.date = date
    #     self.order_status = order_status
    # }
    # class Bar:
    # def __init__(self,params):
    # for key,val in params.iteritems():
    #     self[key] = val
    # """This is orders class"""
    # def __init__(self, **kwargs):
    #     self.args = args


    