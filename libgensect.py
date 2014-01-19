#!/usr/bin/python

import random
import sys

random.seed()

# mode, in all cases, refers to:
#   0 for default sector generation
#   1 for space opera sector generation
#     more crap atmospheres and less water
#   2 for hard science sector generation
#     as space opera, plus population varies with atmo
#     and starport varies with pop
# bitmasked flags

def gensize():
  return random.randint(0,5) + random.randint(0,5)

def genatmo(size, mode):
  base = random.randint(1,6) + random.randint(1,6) - 7 + size
  if base < 0 or (mode & 1 and size < 2):
    return 0
  if mode & 1 and size <= 4:
    if base <= 2:
      return 0
    if base <= 5:
      return 1
    else:
      return 10
  if base > 15:
    return 15
  return base

def gentemp(atmo):
  base = random.randint(1,6) + random.randint(1,6)
  if atmo <= 1:
    return 0
  elif atmo <= 3:
    base -= 2
  elif atmo <= 5 or atmo == 14:
    base -= 1
  elif atmo >= 11:
    base += 6
  elif atmo >= 10:
    base += 2
  elif atmo >= 8:
    base += 1
  return base

def genhydro(size, atmo, temp, mode):
  if size <= 1:
    return 0
  base = random.randint(1,6) + random.randint(1,6) - 7 + size
  if atmo <= 1 or atmo == 10 or atmo == 11 or atmo == 12:
    base -= 4
  if atmo != 13:
    if temp >= 10:
      base -= 2
      if temp >= 12:
        base -= 4
  if mode & 1:
    if atmo <= 1:
      base -= 6
    elif atmo <= 3 or atmo == 11 or atmo == 12:
      base -= 4
    if atmo == 10 and (size == 3 or size == 4):
      base -=6
  if base < 0:
    return 0
  if base > 10:
    return 10
  return base

def genpop(size, atmo, mode):
  base = random.randint(1,6) + random.randint(1,6) -2
  if mode & 2:
    if size <= 2 or size >= 10:
      base -= 1
    if atmo == 5 or atmo == 6 or atmo == 8:
      base += 1
    else:
      base -= 1
  if base < 0:
    return 0
  return base

def gengov(pop):
  if pop == 0:
    return 0
  base = random.randint(1,6) + random.randint(1,6) -7 + pop
  if base < 0:
    return 0
  if base > 13:
    return 13
  return base

def genll(pop, gov):
  if pop == 0:
    return 0
  base = random.randint(1,6) + random.randint(1,6) -7 + gov
  if base < 0:
    return 0
  return base

def genport(pop, mode):
  base = random.randint(1,6) + random.randint(1,6)
  if mode > 1:
    base += pop - 7
  if base <= 2:
    return 'X'
  elif base <= 4:
    return 'E'
  elif base <= 6:
    return 'D'
  elif base <= 8:
    return 'C'
  elif base <= 10:
    return 'B'
  else:
    return 'A'

#TODO genculture, genfrags, genzones/doomed

def genbases(port):
  portmap = {\
    'A':[('N',8,1),('S',10,2),('R',8,3),('T',4,4),('I',6,5)],\
    'B':[('N',8,1),('S',8,2),('R',10,3),('T',6,4),('I',8,5),('P',12,6)],\
    'C':[('S',8,2),('R',10,3),('T',10,4),('I',10,5),('P',10,6)],\
    'D':[('S',7,2),('P',12,6)], 'E':[('P',12,6)], 'X':[] }
  l = portmap[port]
  acc = []
  for i in range(0,7):
    acc.append(" ")
  s = random.randint(1,6)
  if s != 1:
    acc[0] = 'G'
  for (b,p,ind) in l:
    s = random.randint(1,6) + random.randint(1,6)
    if s >= p:
      acc[ind] = b
  return "".join(acc)

def gencodes(size, atmo, hydro, pop, gov, law, tech):
  traitslist = [\
    ("Ag",[("Atmo",4,9),("Hydro",4,8),("Pop",5,7)]),\
    ("As",[("Size",0,0),("Atmo",0,0),("Hydro",0,0)]),\
    ("Ba",[("Pop",0,0),("Gov",0,0),("LL",0,0)]),\
    ("De",[("Atmo",2,100),("Hydro",0,0)]),\
    ("Fl",[("Atmo",10,100),("Hydro",1,10)]),\
    ("Ga",[("Size",5,10),("Atmo",4,9),("Hydro",4,8)]),\
    ("Hi",[("Pop",9,100)]),\
    ("Ht",[("Tech",12,100)]),\
    ("IC",[("Atmo",0,1),("Hydro",1,100)]),\
    ("In",[("Atmo",0,2,4,4,7,7,9,9),("Pop",9,100)]),\
    ("Lo",[("Pop",1,3)]),\
    ("Lt",[("Tech",0,5),("Pop",1,100)]),\
    ("Na",[("Atmo",0,3),("Hydro",0,3),("Pop",6,100)]),\
    ("NI",[("Pop",4,6)]),\
    ("Po",[("Atmo",2,5),("Hydro",0,3)]),\
    ("Ri",[("Atmo",6,6,8,8),("Pop",6,8)]),\
    ("Va",[("Atmo",0,0)]),\
    ("Wa",[("Hydro",10,100)])]
  accum = ""
  traits = {}
  traits["Size"] = size
  traits["Atmo"] = atmo
  traits["Hydro"] = hydro
  traits["Pop"] = pop
  traits["Gov"] = gov
  traits["LL"] = law
  traits["Tech"] = tech
  for (trait, params) in traitslist:
    j=0
    posssat = True
    while j < len(params) and posssat:
      v = params[j]
      key = v[0]
      val = traits[key]
      i = 1
      sat = False
      while i < len(v) and not sat:
        if val >= v[i] and val <= v[i+1]:
          sat = True
        i += 2
      if not sat:
        posssat = False
      j += 1
    if posssat:
      accum += trait + " "
  return accum
          
def gentl(size, atmo, hydro, pop, gov, port):
  if pop == 0:
    return 0
  portmap = {'A':6, 'B':4, 'C':2, 'X':-4}
  base = random.randint(1,6)
  if size <= 1:
    base += 2
  elif size <= 4:
    base += 1
  if atmo <= 3 or atmo >= 10:
    base += 1
  if hydro == 0 or hydro >= 9:
    base += 1
    if hydro == 10:
      base += 1
  if pop < 5:
    base += 1
  if pop > 8:
    base += pop - 8
  if gov == 0 or gov == 5:
    base += 1
  if gov == 7:
    base += 2
  if gov == 13 or gov == 14:
    base -= 2
  if port in portmap:
    base += portmap[port]
  if base < 0:
    return 0
  return base

def genalerts(atmo, pop, gov, ll, tl):
  acc = ""
  if atmo >= 10 or (gov == 0 and pop > 0) or gov == 7 or \
    gov == 10 or (ll == 0 and pop > 0) or ll >= 10:
    acc += "Amb "
  mintls = [8,8,5,5,3,0,0,3,0,3,8,9,10,5,5,8]
  if tl < mintls[atmo] and pop > 0:
    acc += "Doomed "
  return acc

def hxp(a):
  if a >= 10:
    return chr(ord("A")+a-10)
  return str(a)

def genplanet(mode=0):
  size = gensize()
  atmo = genatmo(size, mode)
  temp = gentemp(atmo)
  hydro = genhydro(size, atmo, temp, mode)
  pop = genpop(size, atmo, mode)
  gov = gengov(pop)
  ll = genll(pop, gov)
  port = genport(pop, mode)
  bases = genbases(port)
  tl = gentl(size, atmo, hydro, pop, gov, port)
  trade = gencodes(size, atmo, hydro, pop, gov, ll, tl)
  alerts = genalerts(atmo, pop, gov, ll, tl)
  sys.stdout.write(port + '-' + hxp(size) + hxp(atmo) + hxp(hydro))
  sys.stdout.write(hxp(pop) + hxp(gov) + hxp(ll) + '-' + hxp(tl) + ' ')
  sys.stdout.write(bases + ' ' + trade + alerts + '\n')


def gensect(width, height, density, mode=0):
  wlen = len(str(width-1))
  hlen = len(str(height-1))
  for i in range(width):
    for j in range(height):
      if random.random() < density:
        sys.stdout.write('(' + str(i).zfill(wlen) + ',' + str(j).zfill(hlen) + '): ')
        genplanet(mode)

