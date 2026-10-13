# Project 1A

## Instructions
To start this program, type `python3 client.py <host> <port>`

Enter a player name, and proceed to enter a number to fill out a box on the grid. The boxes are numbered 1-9, left to right, top to bottom.
Moves are validated client side. If packets are lost, they are retried four times with 1/2/4/8 s timeouts.
