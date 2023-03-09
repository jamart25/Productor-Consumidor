from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
import random

M = 1 #numero maximo de elementos que produce cada productor
N = 3 #numero de elementos que consume cada consumidor
K = 10
NPROD = 4
NCONS = 1  

def delay(factor = 3):
    sleep(random.random()/factor)


def add_data(storage, index, pid, data, mutex):
    mutex.acquire()
    try:
        storage[index.value] = data
        index.value = index.value + 1
        delay(6)
    finally:
        mutex.release()


def get_data(storage, mutex):
    mutex.acquire()
    try:
        (elem_min, min) = minimo(storage)
        storage[min] = -2 #vaciamos donde hallemos el minimo
        delay(6)
    finally:
        mutex.release()
    return elem_min


def producer(storage, index, empty, non_empty, mutex):
    i = 0
    data = random.randint(-1, 25);
    while i < M and not storage[index.value] == -1:
        print (f"producer {current_process().name} produciendo")
        delay(6)
        empty.acquire()
        band = random.randint(-1, 10)
        if band == -1:
            data = band
        else:
            data = data + 1
        add_data(storage, index, int(current_process().name.split('_')[1]),
                 data, mutex)
        #print ("almacen inicial", storage[:], "indice", index.value)
        non_empty.release()
        i = i + 1
        print (f"producer {current_process().name} almacenado {data}")

def consumer(L, storage, index2, empty, non_empty, mutex):
    v = 0
    dato = 0
    while v < N and not dato == -2:
        non_empty[v].acquire()
        print (f"consumer {current_process().name} desalmacenando")
        dato =get_data(storage, mutex)

        L[index2.value] = dato
        index2.value = index2.value + 1
        
        empty[v].release()
        print (f"consumer {current_process().name} consumiendo {dato}")
        v = v + 1
        delay(6)

def minimo(storage):
    min = 0
    elem_min = -2
    for i in range(K):
        if (elem_min == -2) and (storage[i] >= 0):
            min = i
            elem_min = storage[min]
        elif storage[i] < elem_min and storage[i] >= 0:
            min = i
            elem_min = storage[min]

    return elem_min, min

def main():
    
    L = Array('i', K)
    storage = Array('i', K)

    index = Value('i', 0)
    index2 = Value('i', 0)

    for i in range(K):
        storage[i] = -2
        L[i] = -2
    print ("almacen inicial", storage[:], "indice", index.value)

    non_empty = [Semaphore(0) for i in range(NPROD)]
    empty = [BoundedSemaphore(K) for i in range(NPROD)]
    mutex = Lock() 

    prodlst = [ Process(target=producer,
                     name=f'prod_{i}',
                     args=(storage, index, empty[i], non_empty[i], mutex))
                for i in range(NPROD) ]

    conslst = [ Process(target=consumer,
                   name=f"cons_{i}",
                   args=(L, storage, index2, empty, non_empty, mutex))
                for i in range(NCONS) ]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

    print(L[:])
   

if __name__ == '__main__':
    main()



