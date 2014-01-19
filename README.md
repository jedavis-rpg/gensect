gensect
Traveller sector generation tool

To run: gensect.py $ARGS

Command-line options:
* -w : specify sector width in 1-parsec hexes.  Default 8 (standard subsector width)
* -g : specify sector height in 1-parsec hexes.  Default 10 (standard subsector height)
* -s : enable Hard Science Mode.  Reduces population on worlds with crap atmospheres, makes population influence starport size.
* -o : enable Space Opera Mode.  Produces more crap atmospheres, less water.

TBD:
* Auto-generate trade and communications routes
* Shift trade classifications out of program text and into config file (extensible)
* Shift bases and gas giants out of program text and into config file
* Hex map generation?
