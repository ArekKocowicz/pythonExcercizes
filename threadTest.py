#!/usr/bin/env python

from threading import Thread
from queue import Queue
from queue import Empty

import logging, time, sys


logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout, level=logging.DEBUG)

def funThread1(threadname, q):
    while True:
        logging.info("here is thread1")
        time.sleep(5)


def funThread2(threadname, q):
    while True:
        logging.info("here is thread2")
        time.sleep(4)


if __name__ == "__main__":
   logging.info("starting")
   queue = Queue()
   thread1 = Thread( target=funThread1, args=("Thread-1", queue) )
   thread2 = Thread( target=funThread2, args=("Thread-2", queue) )

   thread1.start()
   thread2.start()
   thread1.join()

