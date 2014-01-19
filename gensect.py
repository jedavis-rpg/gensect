#!/usr/bin/python2

import libgensect
import argparse

parser = argparse.ArgumentParser(description="Generate a sector for Mongoose Traveller")
parser.add_argument("-w","--width",type=int,default=8,help="width of sector in parsecs")
parser.add_argument("-g","--height",type=int,default=10,\
  help="height of sector in parsecs")
parser.add_argument("-s","--science",action="store_true",help="Hard Science Mode")
parser.add_argument("-o","--opera",action="store_true",help="Space Opera Mode")
parser.add_argument("-d","--density",type=float,default=0.5,help=\
  "Density of inhabited systems")
args = parser.parse_args()
mode = 0
if args.science:
  mode |= 2
elif args.opera:
  mode |= 1
libgensect.gensect(args.width,args.height,args.density,mode)
