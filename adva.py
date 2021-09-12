import numpy as np

def bullen():
    for i in range(10):
        gopher = yield np.random.randint(1000)
        yield gopher ** 2

buller2 = (np.random.randint(1000) for i in range(10))
buller3 = (i for i in (6, 2, 3, 7, 9, 1, 7))

def buller():
    bulgen = bullen()
    count = 0
    for bul in bulgen:
        print(bul)
        if count == 5:
            break
        count += 1
    print(f"Got one more: {next(bulgen)}")

def ispali(num):
    numstr = str(num)
    revnumstr = numstr[::-1]
    revnum = int(revnumstr)
    return num == revnum

def add_to_database():
    try:
        while True:
            try:
                row = yield
                print('INSERT INTO mytable VALUES(?, ?, ?)', row)
            except Exception:
                print('COMMIT')
    finally:
        print('ABORTFINAL')
