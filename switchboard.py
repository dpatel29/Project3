"""
    Switchboard class

"""

from phone import Phone


class Switchboard:
    def __init__(self, area_code):
        """
        :param area_code: the area code to which the switchboard will be associated.
        """
        self.area_code = area_code
        self.trunks = []
        self.phones = []
        # you will probably need more data here.

    def get_area_code(self):
        """
        Return the area code of the switch
        return: self.area_code
        """
        return self.area_code

    def get_trunk_connection(self):
        """
        Return the area code of the switch
        return: self.area_code
        """
        return self.trunks

    def get_phones(self):
        """
        Return the area code of the switch
        return: self.area_code
        """
        return self.phones

    def get_phone_numbers(self):
        return [p.get_number() for p in self.phones ]

    def add_phone(self, phone_number):
        """
        This function should add a local phone connection by creating a phone object
        and storing it in this class.  How you do that is up to you.

        :param phone_number: phone number without area code
        :return: depends on implementation / None
        """
        for phone in self.phones:
            if phone.get_number() == phone_number:
                return False
        self.phones.append(Phone(phone_number, self))
        return True

    def add_trunk_connection(self, switchboard):
        """
        Connect the switchboard (self) to the switchboard (switchboard)

        :param switchboard: should be either the area code or switchboard object to connect.
        :return: success/failure, None, or it's up to you
        """
        if switchboard in self.trunks:
            return False
        
        self.trunks.append(switchboard)
        return True

    def connect_call(self, area_code, number, previous_codes):
        """
        This must be a recursive function.

        :param area_code: the area code to which the destination phone belongs
        :param number: the phone number of the destination phone without area code.
        :param previous_codes: you must keep track of the previously tracked codes
        :return: Depends on your implementation, possibly the path to the destination phone.
        """
        pass
