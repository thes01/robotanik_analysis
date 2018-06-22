import urllib.request
from os import mkdir
from shutil import rmtree

def getLink(id):
    return "https://tutor.fi.muni.cz/include/a_data_file.php?instance_id=" + str(id)

def parseIds():
    ids = []
    with open("data/Robotanik_mapping.txt") as mapping:
        ids = [line.split(';')[0] for line in mapping.readlines() if len(line) > 0]

    return ids

rmtree("data/current")
mkdir("data/current")

ids = parseIds()

for id in ids:
    id = id.zfill(4)
    print("Downloading", id)
    urllib.request.urlretrieve(getLink(id), "data/current/{}.txt".format(id))
