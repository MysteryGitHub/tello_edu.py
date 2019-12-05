# tello_edu.py

## Introduction
After coming across the Tello EDU drone in Nov 2019, I decided to get a few and mess with some simple swarm programming.
I came across [this repo](), and I liked it better than [the official Tello Python SDK](https://github.com/TelloSDK/Multi-Tello-Formation).
See upstream repo for motivation, etc.

## Getting Started
From the root of the project, run the following commands:

**OPTIONAL FIRST STEP**: Create a Python virtual environment (via [`virtualenv`](https://virtualenv.pypa.io/en/stable/)) before installing the Python libraries
, and activate the new environment:
    ```shell script
    virtualenv venv
   source venv/bin/activate
    ```

1. Install the needed Python libraries:
    ```shell script
    pip install -r requirements.txt
    ```
1. If you have not connected your Tello EDU to your main WiFi network yet, you need to do so for swarming support. First, connect directly to the ad-hoc network
 created by your Tello EDU, then update the `connect_to_wifi.py` file, replacing `MY_SSID` and `MY_PASSWORD` with your main WiFi network credentials, then
  run the file:
   ```shell script
   python connect_to_wifi.py
   ```
1. Create a `serial_numbers.txt` file in the root directory with a list of all your Tello serial numbers, one-per-line. Lines that are blank or start with
 `#` will be ignored. In this example, the 4th drone (and all of the labels, i.e. "1-Yellow") will not be included in the detected list of serial numbers. You can
  find the serial number for your Tello(s) on a tiny sticker inside the battery compartment. If you ran the previous step, the `connect_to_wifi.py` should
   have printed the serial number to the console.
    ```text
    # 1-Yellow
   0TQDFC6EDBBX03

   # 2-Blue
   0TQDFC6EDB4398

   # 3-Green
   0TQDFC6EDBH8M8
   
   # 4-Red
   #0TQDFC7EDB4874 
    ```
1. Run any of the demos (see [Demos](#demos) section below)

## Project Structure
 * There are three key files in the project:
   * `fly_tello.py` - The `FlyTello` class is intended to be the only one that a typical user needs to use.  It contains functions enabling all core
    behaviours of one or more Tellos, including some complex behaviour such as searching for Mission Pads.  This should always be the starting point.
   * `comms_manager.py` - The `CommsManager` class performs all of the core functions that communicate with the Tellos, sending and receiving commands and status messages, and ensuring they are acted on appropriately.  If you want to develop new non-standard behaviours, you'll probably need some of these functions.
   * `tello.py` - The `Tello` class stores key parameters for each Tello, enabling the rest of the functionality.  The `TelloCommand` class provides the structure for both queued commands, and logs of commands which have already been sent.
 * All demos are included in the `demos` directory

## FlyTello

Using `FlyTello` provides the easiest route to flying one or more Tellos.  A simple demonstration would require the following code:
```
from fly_tello import FlyTello      # Import FlyTello

my_tellos = list()
my_tellos.append('0TQDFCAABBCCDD')  # Replace with your Tello Serial Number
my_tellos.append('0TQDFCAABBCCEE')  # Replace with your Tello Serial Number

with FlyTello(my_tellos) as fly:    # Use FlyTello as a Context Manager to ensure safe landing in case of any errors
    fly.takeoff()                   # Single command for all Tellos to take-off
    fly.forward(50)                 # Single command for all Tellos to fly forward by 50cm
    with fly.sync_these():          # Keep the following commands in-sync, even with different commands for each Tello
        fly.left(30, tello=1)       # Tell just Tello1 to fly left
        fly.right(30, tello=2)      # At the same time, Tello2 will fly right
    fly.flip(direction='forward')   # Flips are easy to perform via the Tello SDK
    fly.land()                      # Finally, land
```

It is suggested to browse through `fly_tello.py` for full details of the available methods which you can use - all are fully commented and explained in the code.  A few worth mentioning however include:
* Every function listed in the Tello SDK v2.0 (available to download from https://www.ryzerobotics.com/tello-edu/downloads) is implemented as a method within FlyTello; though some have been renamed for clarity.
* `reorient()` - a simplified method which causes the Tello to centre itself over the selected (or any nearby) Mission Pad.  This is really helpful for long-running flights to ensure the Tellos remain exactly in the right positions.
* `search_spiral()` - brings together multiple Tello SDK commands to effectively perform a search for a Mission Pad, via one very simple Python command.  It will stop over the top of the Mission Pad if it finds it, otherwise returns to its starting position.
* `search_pattern()` - like search_spiral, but you can specify any pattern you like for the search via a simple list of coordinates.
* `sync_these()` - when used as a Context Manager (as a `with` block), this ensures all Tellos are in sync before any functions within the block are executed.

`FlyTello` also provides a simple method of programming individual behaviours, which allow each Tello to behave and follow its own independent set of instructions completely independently from any other Tello.  For full details read the comments in `fly_tello.py`, but key extracts from an example of this are also shown below:
```
# independent() is used to package up the FlyTello commands for the independent phase of the flight
def independent(tello, pad):
    found = fly.search_spiral(dist=50, spirals=2, height=100, speed=100, pad=pad, tello=tello)
    if found:
        print('[Search]Tello %d Found the Mission Pad!' % tello)
        fly.land(tello=tello)

with FlyTello(my_tellos) as fly:
    with fly.individual_behaviours():
        # individual_behaviours() is a Context Manager to ensure separate threads are setup and managed for each Tello's
        # own behaviour, as defined in the independent() function above.
        # run_individual() actually initiates the behaviour for a single Tello - in this case both searching, but each
        # is searching for a different Mission Pad ('m1' vs 'm2').
        fly.run_individual(independent, tello_num=1, pad_id='m1')
        fly.run_individual(independent, tello_num=2, pad_id='m2')
```

## Demos
All demos are in the `demos` directory. The first two listed also include YouTube video demos:
 * Tello EDU Capabilities Demo (`demos/all_functions.py`) - https://youtu.be/F3rSW5VKsW8
 * Simple Searching Demo (`demos/search.py`) - https://youtu.be/pj2fJe7cPTE
 * Single Tello Demo (`demos/single.py`)
 * Status Reading Demo (`demos/status.py`)
You can run any of these demos by executing the Python file:
```shell script
python demos/DEMO_NAME.py
```

## Limitations
There are some limitations of what can be done with this project and the Tello EDU:
 * No Video Stream.  The Tello is capable of sending its video stream, but only when connected directly to the in-build WiFi of a single Tello.  The video is
  not accessible when the Tellos are connected to a separate WiFi network, as required for swarming behaviour.  There is a workaround, which is to have multiple
  WiFi dongles connected to a single computer, one per Tello, but that hasn't been a focus for me.
* Limited Status Messages.  The Tello does broadcast a regular (multiple times per second) status message, however this seems to be of limited value as many of the values do not seem to correspond with the Tello's behaviour, and others are rather erratic.  This requires further investigation to determine which are useful.

## Further Work/Recommendations (from upstream repo)
The project as it is currently is enough to fly one or more Tello EDU drones via a simple yet sophisticated set of controls.  Expanding its capabilities is easy, with layers of modules which expose increasingly more detailed / low-level functionality.  I'd suggest adding or changing:
* Position Tracking.  By tracking the relative position of each Tello from when it launches, this will enable behaviours such as "return to start", and will e.g. allow Mission Pad locations to be shared with other Tellos in the swarm - a pre-requisite for collaborative swarm behaviour.  Clearly accuracy will decrease over time, but could be regularly restored using the `reorient()` method described above.
* Better Error Checking.  Some error checking is already implemented, but it's incomplete.  Getting the arc radius correct for a curve is sometimes difficult, and this project could be more helpful in identifying the errors and suggesting valid alternative values.
* Implement `on_error` alternative commands for Flips and Curves, which can easily fail due to e.g. battery low or incorrect curve radius values.  This will ensure Tello is less likely to end up in an unexpected location.
* Command Stream & Logging.  Currently all commands either sent or received are printed to the Python Console.  These would be better saved in a detailed log file, so that only key information is presented to the user in the Console.

## Random Notes
 * You can reset your drone by holding the power button down for 5-10 seconds.