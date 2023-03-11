from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
import random

N = 10 #numero de elementos que consume cada consumidor
K = 10 #tamaño del array de cada pruductor
NPROD = 4
NCONS = 1  

def delay(factor = 3):
    sleep(random.random()/factor)


def add_data(storage, prod, index, pid, data, mutex):
    mutex.acquire()
    try:
        storage[prod][index.value] = data
        index.value = index.value + 1
        delay(6)
    finally:
        mutex.release()


def get_data(storage, mutex):
    mutex.acquire()
    try:
        (elem_min, min, min_prod) = minimo(storage)
        storage[min_prod][min] = -2 #vaciamos donde hallemos el minimo
        delay(6)
    finally:
        mutex.release()
    return elem_min, min_prod


def producer(storage, prod, indexi, empty, non_empty, mutex):
    i = 0
    data = random.randint(-1, 25);
    while i < K and not data == -1:
        print (f"producer {current_process().name} produciendo")
        delay(6)
        empty.acquire()
        band = random.randint(-1, 10)
        if data == -1:
            pass
        else:
            data = data + 1
            add_data(storage, prod, indexi, int(current_process().name.split('_')[1]),
                 data, mutex)
        #print ("almacen inicial", storage[:], "indice", index.value)
        non_empty.release()
        i = i + 1
        print (f"producer {current_process().name} almacenado {data}")

def consumer(L, storage, index2, empty, non_empty, mutex):
    v = 0
    dato = 0
    while v < N and not dato == -2:
        for prod in range(NPROD):
            non_empty[prod].acquire()
            print (f"consumer {current_process().name} desalmacenando")
            (dato, prod_min) =get_data(storage, mutex)

            L[index2.value] = dato
            index2.value = index2.value + 1
            
            empty[prod].release()
            print (f"consumer {current_process().name} consumiendo {dato}")
            v = v + 1
            delay(6)

def minimo(storage):
    min = -1
    prod_min = -1
    elem_min = -2
    for prod in range(NPROD):
        for i in range(K):
            if (elem_min == -2) and (storage[prod][i] >= 0):
                prod_min = prod
                min = i
                elem_min = storage[prod][min]
            elif storage[prod][i] < elem_min and storage[prod][i] >= 0:
                prod_min = prod
                min = i
                elem_min = storage[prod][min]

    return elem_min, min, prod_min

def main():
    
    L = Array('i', K*NPROD)
    storage = [Array('i', K) for i in range(NPROD)]

    index = [Value('i', 0) for i in range(NPROD)]
    index2 = Value('i', 0)

    for prod in range(NPROD):
        for i in range(K):
            storage[prod][i] = -2
            L[prod*K + i] = -2
    

    non_empty = [Semaphore(0) for i in range(NPROD)]
    empty = [BoundedSemaphore(K) for i in range(NPROD)]
    mutex = Lock() 

    prodlst = [ Process(target=producer,
                     name=f'prod_{i}',
                     args=(storage, i, index[i], empty[i], non_empty[i], mutex))
                for i in range(NPROD) ]

    conslst = [ Process(target=consumer,
                   name=f"cons_{i}",
                   args=(L, storage, index2, empty, non_empty, mutex))
                for i in range(NCONS) ]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

    """
    for i in range(NPROD):
        for j in range(K):
            print(storage[i][j])
    """
    print(L[:])
   

if __name__ == '__main__':
    main()



