from fly_tello import FlyTello

my_tellos = list()

#
# SIMPLE EXAMPLE - MOST BASIC FLIGHT TO SHOW STATUS MESSAGES
#
# SETUP: Any number of Tellos
#


#
# MAIN FLIGHT CONTROL LOGIC
#

# Read all serial numbers from a serial_numbers.txt file
tello_sn_list = FlyTello.read_serial_numbers_from_file()
# Control the flight
with FlyTello(tello_sn_list, get_status=True) as fly:
    fly.print_status(sync=True)
    fly.takeoff()
    fly.print_status(sync=True)
    fly.land()
    fly.print_status(sync=True)
