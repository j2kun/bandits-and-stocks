import os
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("provide one argument: the directory name.")

theDir = sys.argv[-1]
for filename in os.listdir(theDir):
   with open(theDir + '/' + filename, 'r') as theFile:
      lines = theFile.readlines()

   header = lines[0]
   data = lines[1:]
   data.reverse()

   with open(theDir + '/' + filename, 'w') as theFile:
      theFile.write(header)
      for line in data:
         theFile.write(line)

