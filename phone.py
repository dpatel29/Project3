"""
    Phone Class Starter Code

    This code defines the basic functionality that you need from a phone.
    When these functions are called they should communicate with the
    switchboards to find a path
"""


class Phone:
    def __init__(self, number, switchboard):
        """
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        """
        self.number = number
        self.switchboard = switchboard
        self.connection = ()
        # you will need more parameters/attributes

    def get_number(self):
        return self.number
    
    def is_connected(self):
        return len(self.connection)


    def connect(self, area_code, other_phone_number):
        """
        :param area_code: the area code of the other phone number
        :param other_phone_number: the other phone number without the area code
        :return: **this you must decide in your implementation**
        """
        self.connection = (area_code, other_phone_number)

    def disconnect(self):
        """
        This function should return the connection status to disconnected.  You need
        to use new members of this class to determine how the phone is connected to
        the other phone.

        You should also make sure to disconnect the other phone on the other end of the line.
        :return: **depends on your implementation**
        """
        self.connection = ()

