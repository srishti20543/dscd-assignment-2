import unittest
from multiprocessing import Process
import sys
sys.path.insert(1, '../Communication')
import RegistryServer
import Replica
import time

def stepsForPrimaryServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def setUp():
    registryServer = Process(target=RegistryServer.startRegistryServer)
    registryServer.start()
    # time.sleep(2)
    server1 = Process(target=stepsForPrimaryServer, args=("localhost", 5555))
    server1.start()
    server2 = Process(target=Replica.connectToRegistry, args=("localhost", 6555))
    server2.start()
    

if __name__ == '__main__':
    setUp()
