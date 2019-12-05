from fly_tello import FlyTello

#
# SIMPLE EXAMPLE - SINGLE TELLO WITH MISSION PAD
#
# SETUP: Tello on Mission Pad, facing in direction of the pad - goes max 50cm left and 100cm forward - takes ~45sec
#

#
# MAIN FLIGHT CONTROL LOGIC
#

# Read all serial numbers from a serial_numbers.txt file
tello_sn_list = FlyTello.read_serial_numbers_from_file()
# Since this is a single Tello demo, we only need one Tello serial number
tello_sn_list = [tello_sn_list[0]]
# Control the flight
with FlyTello(tello_sn_list) as fly:
    fly.takeoff()
    fly.forward(dist=50)
    fly.back(dist=50)
    fly.reorient(height=100, pad='m-2')
    fly.left(dist=50)
    fly.flip(direction='right')
    fly.reorient(height=100, pad='m-2')
    fly.curve(x1=50, y1=30, z1=0, x2=100, y2=30, z2=-20, speed=60)
    fly.curve(x1=-50, y1=-30, z1=0, x2=-100, y2=-30, z2=20, speed=60)
    fly.reorient(height=100, pad='m-2')
    fly.rotate_cw(angle=360, tello=1)
    fly.straight_from_pad(x=30, y=0, z=75, speed=100, pad='m-2')
    fly.flip(direction='back')
    fly.reorient(height=50, pad='m-2')
    fly.land()
