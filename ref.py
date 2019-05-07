from multiprocessing import Process
from datetime import datetime
asdf = []
def f(name):
	global asdf
	for i in range (2000):
		print('hello', name)
	asdf.append(str(datetime.now())) 
	print(str(datetime.now()))

def d(name):
	global asdf
	for i in range (2000):
		print('bye', name)
	print(str(datetime.now()))
	asdf.append(str(datetime.now())) 

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    q = Process(target=d, args=('bob',))
    q.start()
    q.join()
    r = Process(target=d, args=('bob',))
    r.start()
    r.join()
    print(asdf)


a = input("Finished")