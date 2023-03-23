import unittest
from multiprocessing import Process
import sys
sys.path.insert(1, '../Communication')
import RegistryServer
import Replica
import Client
import time

def stepsForPrimaryServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def stepsForBackupServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def stepsForClient(IP, port):
    Client.runRegistryServer(IP, port)


def setUp():
    registryServer = Process(target=RegistryServer.startRegistryServer)
    registryServer.start()

    server1 = Process(target=stepsForPrimaryServer, args=("localhost", 5000))
    server1.start()
    server2 = Process(target=stepsForBackupServer, args=("localhost", 5001))
    server2.start()

    client1 = Process(target=stepsForClient, args=("localhost", 6000))
    client1.start()
    

if __name__ == '__main__':
    setUp()
