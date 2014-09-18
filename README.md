eg-pyms-lan
===========

A Python controller class for Energenie EG-PMS-LAN device. Reverse engineered and does not require third party libraries. Though pretty limited at the moment and does not support anything other than switching socket states.

Usage
-----
  - Can be used as a Python class.
  - Can be used from command line.

        ./pyms-socket.py hostname password 1:0 3:1
 
   Connect to 'hostname' using 'password' (fixed port 5000), turn off socket 1 and turn on socket 3.

   A 2-3 seconds delay is required between calls because the device cannot process requests any faster. On the contrary, requests through Web interface (forging a POST request) are processed without delay. Kinda makes you wonder, huh.
