# F. E. T. C. H.
Flight Enabled Transportation & Collection of Hardware.

Fetch is a drone equipped with sensors and magnets that conveys sensor devices
to user specified locations. It uses A Pixhawk, Raspberry Pi, and Electro-permanent 
magnets to fly, locate, and deploy/collect sensors.

## Pixhawk
This flight controller solves the waypoint and control of drone problems out of the box.

## Raspberry Pi
The raspberry pi (rpi) is the brains of the drone assembly. The rpi will control the computer vision and magnetic
components of the drone.

## Computer Vision
The rpi uses computer vision to locate the payloads. Their circular shape and specific coloring scheme make
the payloads easy to locate. The computer vision information can be used to intuit the position and distance
of a given payload relative to the drone.
