"""
network.py is both the definition file for the Network class as well as the driver for the program.

In network you need to implement the functions which the driver will call for the all the different commands.
"""

from phone import Phone
from switchboard import Switchboard
import json

"""
import csv (you can do either if you choose, or just use the regular file io)

Some constants below are for the driver, don't remove them unless you mean to.  
"""

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'


class Network:
    def __init__(self):
        """
            Construct a network by creating the switchboard container object

            You are free to create any additional data/members necessary to maintain this class.
        """
        self.switchboards = []
        pass

    def load_network(self, filename):
        """
        :param filename: the name of the file to be loaded.  Assume it exists and is in the right format.
                If not, it's ok if your program fails.
        :return: success?
        """
        with open(filename, 'r') as f:
            data = json.load(f)

            # create switches first
            for s in data.keys():
                # convert the keys to int as json keys are string only
                switchboard = self.add_switchboard(int(s))
                if 'phones' in data[s].keys():
                    for p in data[s]['phones']:
                        switchboard.add_phone(p)
                if 'trunks' in data[s].keys():
                    for t in data[s]['trunks']:
                        self.connect_switchboards(switchboard, self.add_switchboard(t))
                        
        

    def save_network(self, filename):
        """
        :param filename: the name of your file to save the network.  Remember that you need to save all the
            connections, but not the active phone calls (they can be forgotten between save and load).
            You must invent the format of the file, but if you wish you can use either json or csv libraries.
        :return: success?
        """

        """
        swithces:
          410:
            trunks:
              - 510
              - 610
            phones:
              - 1231111
              - 1232222
          510:
            trunks:
              - 410
              - 610
        """
        output = {}
        for switch in self.switchboards:
            output[switch.get_area_code()] = {}
            if len(switch.get_trunk_connection()):
                output[switch.get_area_code()] = []
            trunks = []
            for trunk in switch.get_trunk_connection():
                trunks.append(trunk.get_area_code())
            if len(trunks):
                output[switch.get_area_code()] = {'trunks' : trunks}
            phones = []
            for phone in switch.get_phones():
                phones.append(phone.get_number())
            if len(phones):
                output[switch.get_area_code()]['phones'] = phones
        
        with open(filename, 'w') as f:
            json.dump(output, f, sort_keys = True, indent=2)

    def add_switchboard(self, area_code):
        """
        add switchboard should create a switchboard and add it to your network.

        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return:
        """
        for switch in self.switchboards:
            if switch.get_area_code() == area_code:
                return switch
        switch = Switchboard(area_code)
        self.switchboards.append(switch)
        return switch

    def connect_switchboards(self, area_1, area_2):
        """
            Connect switchboards should connect the two switchboards (creates a trunk line between them)
            so that long distance calls can be made.

        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: success/failure
        """

        if area_1 == area_2:
            return False
        numbers = [area_1, area_2]
        connected = []

        i = 0
        while len(numbers) and i < len(self.switchboards):
            switchboard = self.switchboards[i]
            if switchboard.get_area_code() in numbers:
                numbers.remove(switchboard.get_area_code())
                connected.append(switchboard)
            i += 1
            
        if len(connected) == 2:
            connected[0].add_trunk_connection(connected[1])
            connected[1].add_trunk_connection(connected[0])
        else:
            return False

    def find_switchboard(self, area_code):
        for switchboard in self.switchboards:
            if switchboard.get_area_code() == area_code:
                return switchboard
        return None

    def find_connection(self, s1, s2, start = 0, t='\t'):

        print(t + '{}'.format(s1.get_area_code()))
        if s2 in s1.get_trunk_connection():
            return True
        if start >= len(s1.get_trunk_connection()):
            return False


        return self.find_connection(s1.get_trunk_connection()[start], s2, start+1, 2*t)
 
    def connect_call(self, area_code1, phone_number1, area_code2, phone_number2):
        
        s1 = self.find_switchboard(area_code1)
        if not s1:
            return False

        s2 = self.find_switchboard(area_code2)
        if not s2:
            return False

        if self.find_connection(s1, s2):
            p1 = p2 = None
            for phone in s1.get_phones():
                if phone.get_number() == phone_number1:
                    p1 = phone
                    break
            if not p1:
                print("The phone number {} not found in the switchboard {}".format(phone_number1, s1.get_area_code()))
                return False
            for phone in s2.get_phones():
                if phone.get_number() == phone_number2:
                    p2 = phone
                    break
            if not p2:
                print("The phone number {} not found in the switchboard {}".format(phone_number2, s2.get_area_code()))
                return False            
            print ("Start a Call")
            p1.connect(s2.get_area_code(), phone_number2)
            p2.connect(s1.get_area_code(), phone_number1)
            return True
        else:
            print ("No Connection, can't start a call")
            return False

    def display(self):
        """
            Display should output the status of the phone network as described in the project.
        """
        for switch in self.switchboards:
            print("Switchboard with area code: {0}".format(switch.get_area_code()))
            print("\tTrunk lines are:")
            for trunk in switch.get_trunk_connection():
                print("\t\tTrunk line connection to: {0}".format(trunk.get_area_code()))
            print("\tLocal phone numbers are:")
            for phone in switch.get_phones():
                if not phone.is_connected():
                    print("\t\tPhone with number: {0} is not in use".format(phone.get_number()))
                else:
                    con_area = phone.connection[0]
                    con_number = phone.connection[1]
                    print("\t\tPhone with number: {0} is connected to {1}-{2}".format(
                        phone.get_number(), con_area, con_number))


if __name__ == '__main__':
    the_network = Network()
    the_network.add_switchboard(410)
    the_network.add_switchboard(510)
    the_network.add_switchboard(610)
    the_network.add_switchboard(710)
    the_network.add_switchboard(810)
    # the board is not connected to anyother board
    the_network.add_switchboard(910)
    
    the_network.connect_switchboards(410, 510)
    the_network.connect_switchboards(410, 610)
    the_network.connect_switchboards(510, 710)
    the_network.connect_switchboards(510, 810)

               
    for area_code in [410, 510, 610, 710]:
        s = the_network.find_switchboard(area_code)
        if s:
            for phone_number in [1231111, 1232222, 1233333, 1239999]:
                if not s.add_phone(phone_number):
                    print('ERROR: Phone number exist {0}'.format(phone_number))
        else:
            print('ERROR: The switchboard with {0} does not exist. Add the board first'.format(area_code))

    s = the_network.find_switchboard(810)
    s.add_phone(1239999)
    s = the_network.find_switchboard(910)
    s.add_phone(1239999)


    src_area = 410
    dst_number = src_number = 1239999
    dst_area = 810
    the_network.connect_call(src_area, src_number, dst_area, dst_number)
    # can't connect, the switchboard is not connected to anything
    the_network.connect_call(src_area, src_number, 910, dst_number)

    # save and load functions
    the_network.save_network('blah')
    # clear out the network object to load in the saved file
    the_network = Network()
    the_network.load_network('blah')
    # show the loaded file
    the_network.display()



# if __name__ == '__main__':
#     the_network = Network()
#     s = input('Enter command: ')
#     while s.strip().lower() != QUIT:
#         split_command = s.split()
#         if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
#             area_1 = int(split_command[1])
#             area_2 = int(split_command[2])
#             the_network.connect_switchboards(area_1, area_2)
#         elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
#             the_network.add_switchboard(int(split_command[1]))
#         elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
#             number_parts = split_command[1].split(HYPHEN)
#             area_code = int(number_parts[0])
#             phone_number = int(''.join(number_parts[1:]))
#             """
#                 here is a pass, you must replace it with your code for this driver to work
#             """
#             s = the_network.find_switchboard(area_code)
#             if s:
#                 if not s.add_phone(phone_number):
#                     print('ERROR: Phone number exist {0}'.format(split_command[1]))
#             else:
#                 print('ERROR: The switchboard with {0} does not exist. Add the board first'.format(area_code))


#         elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
#             the_network.save_network(split_command[1])
#             print('Network saved to {}.'.format(split_command[1]))
#         elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
#             the_network.load_network(split_command[1])
#             print('Network loaded from {}.'.format(split_command[1]))
#         elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
#             src_number_parts = split_command[1].split(HYPHEN)
#             src_area_code = int(src_number_parts[0])
#             src_number = int(''.join(src_number_parts[1:]))

#             dest_number_parts = split_command[2].split(HYPHEN)
#             dest_area_code = int(dest_number_parts[0])
#             dest_number = int(''.join(dest_number_parts[1:]))
#             """
#                 here is a pass, you must replace it with your code for this driver to work
#             """

#             pass

#         elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
#             number_parts = split_command[1].split('-')
#             area_code = int(number_parts[0])
#             number = int(''.join(number_parts[1:]))
#             """
#                 here is a pass, you must replace it with your code for this driver to work
#             """
#             pass
#         elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
#             the_network.display()

#         s = input('Enter command: ')

