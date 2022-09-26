import hashlib


def myhash(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return int(md5.hexdigest(), 16)


key = myhash("U202013894") % 20+1
if (key <= 10):
    print("A"+str(key))
else:
    print("B"+str(key-10))
