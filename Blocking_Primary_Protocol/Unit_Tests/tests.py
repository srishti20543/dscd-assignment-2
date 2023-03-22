import unittest
from multiprocessing import Process
import sys
sys.path.insert(1, '../Communication')
import RegistryServer
import Replica
import time

def setUp():
    registryServer = Process(target=RegistryServer.startRegistryServer)
    registryServer.start()
    time.sleep(2)
    server = Process(target=Replica.connectToRegistry, args=("localhost", 5555))
    server.start()


if __name__ == '__main__':
    setUp()
