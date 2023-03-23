import sys

sys.path.insert(1, '../Communication')

import RegistryServer
import Replica
import Client
import uuid
import threading
import time
import unittest

def stepsForPrimaryServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def stepsForBackupServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def stepsForClient1(IP, port):
    Client.runRegistryServer(IP, port)

def stepsForClient2(IP, port):
    Client.runRegistryServer(IP, port)
    server = ["localhost", 5000]
    unique_id1 = str(uuid.uuid1())
    fileName = "file1.txt"
    content = "coding in file1"
    # Client.write(server, unique_id1, fileName, content)


def setUp():
    registryServer = threading.Thread(target=RegistryServer.startRegistryServer)
    registryServer.start()
    time.sleep(2)
    server1 = threading.Thread(target=stepsForPrimaryServer, args=("localhost", 5000))
    server1.start()

    server2 = threading.Thread(target=stepsForBackupServer, args=("localhost", 5001))
    server2.start()
    # time.sleep(2)
    # client1 = threading.Thread(target=stepsForClient1, args=("localhost", 6000))
    # client1.start()
    time.sleep(2)
    client2 = threading.Thread(target=stepsForClient2, args=("localhost", 7000))
    client2.start()

    # client1.join()
    client2.join()
    server1.join()
    server2.join()
    registryServer.join()    
    

if __name__ == '__main__':
    setUp()
