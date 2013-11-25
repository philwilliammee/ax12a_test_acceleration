GUI.py runs the main program GUI 

this program requires the user to be a member of the dialout group to access the serial connections
or it must be ran as super user. 

As the start click on AX-ID to enter the ID of the motor you want to use.

the function generator class uses a self.speed_coef = 0.47776 to adjust the slope of the curve to the actual acceleration. This may need to be adjusted. There are other variables all over that are not well organized that should be used to adjust the motor. You just have to play around with it.

Data is aquired at 0.1s so you cant run the output to the dymixel much faster than .15 max because there isnt enough time.

This program has a lot of bugs and I dont guarantee anything about it use at your own risk.

Thanks for looking feel free to comment, I will try and fix any errors you finb.
