from shutil import copyfile
import os

folder = 'validation'

scrDir = './' + folder + '/'
dstDir = './data/' + folder + '/'

if not os.path.exists(dstDir):
    os.mkdir(dstDir)

for i in range(8):
    locaDir = dstDir + str(i) + '/'
    if not os.path.exists(locaDir):
        os.mkdir(locaDir)

file = open(folder + '.txt', 'r') 
Lines = file.readlines() 
  
for line in Lines: 
    print(line.strip())
    info = line.strip().split(',')
    imgName = info[0]
    classNo = info[1]
    copyfile(scrDir + imgName, dstDir + str(classNo) + '/' + imgName)
