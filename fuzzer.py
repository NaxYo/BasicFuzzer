#!/usr/bin/python

import math
import random
import string
import subprocess
import time

import glob
lFiles = []
lFiles.extend(glob.glob("imgSet/*.png"))
lFiles.extend(glob.glob("imgSet/*.jpg"))
lFiles.extend(glob.glob("imgSet/*.gif"))


oFile = "fuzz."

fFactor = 100
nParcial = 1000
fIncrement = 25
nIncrement = 10

for k in range(nIncrement):
	for i in range(nParcial):
		rFile = random.choice(lFiles);

		buff = bytearray(open(rFile, 'rb').read())
		nEscrituras = random.randrange(math.ceil(float(len(buff) / fFactor))) + 1

		for j in range(nEscrituras):
			rByte = random.randrange(256)
			rPosition = random.randrange(len(buff))
			buff[rPosition] = "%c"%(rByte)

		open(oFile+rFile[-3:],"wb").write(buff)
		process = subprocess.Popen(['eog', oFile+rFile[-3:]])

		time.sleep(1)
		crashed = process.poll()
		if not crashed:
			try:
				process.terminate()
			except:
				print 'Ha ocurrido una excepcion al intentar terminar el proceso...'
				crashed = True

		if crashed:
			fCrash = 'crashRecord/'+str(k)+'_'+str(i)+rFile[-3:]
			print 'Ha petado! guardamos el fichero chungo: '+fCrash
			open(fCrash,"wb").write(buff)

		print "Analizado: "+str(nParcial*k+i)+'/'+str(nParcial*nIncrement)

	fFactor = fFactor+fIncrement