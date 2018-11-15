"""This is users class defining the users class model constructor """

class AuthUser:
    """ """
    def __init__(self, *args):
        """This is AuthUsers class constructor"""
        self.user_id = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.email = args[3]
        self.contact = args[4]
        self.username = args[5]
        self.password = args[6]
        self.user_type = args[7]




    