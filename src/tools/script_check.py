#/usr/bin/env python

f=open('/tmp/script', 'r')
no=0
while True:
    no+=1
    id = f.readline().strip()
    id = int(id)
    if not id:
        break
    else:
        id=int(id)

    while True:
        if id > no:
            print no
            no += 1
            continue
        else:
            break;

f.close()
