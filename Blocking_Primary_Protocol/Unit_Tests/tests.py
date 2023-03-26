import sys

sys.path.insert(1, '../Communication')

import RegistryServer
import Replica
import Client
import uuid
from multiprocessing import Process
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
    server = ["localhost", 5001]
    unique_id1 = str(uuid.uuid1())
    fileName = "file1.txt"
    content = "coding in file1"
    Client.write(server, unique_id1, fileName, content)
    server = ["localhost", 5005]
    Client.read(server, unique_id1)
    server = ["localhost", 5003]
    Client.read(server, unique_id1)
    server = ["localhost", 5000]
    Client.read(server, unique_id1)
    content = "coding in file1 again"
    Client.write(server, unique_id1, fileName, content)
    # time.sleep(3)
    Client.read(server, unique_id1)
    server = ["localhost", 5001]
    Client.read(server, unique_id1)
    server = ["localhost", 5002]
    Client.read(server, unique_id1)
    server = ["localhost", 5003]
    Client.read(server, unique_id1)
    server = ["localhost", 5004]
    Client.read(server, unique_id1)
    server = ["localhost", 5005]
    Client.read(server, unique_id1)
    Client.delete(server, unique_id1)

    # time.sleep(3)
    Client.read(server, unique_id1)
    server = ["localhost", 5001]
    Client.read(server, unique_id1)
    server = ["localhost", 5000]
    Client.read(server, unique_id1)


def setUp():
    registryServer = Process(target=RegistryServer.startRegistryServer)
    registryServer.start()
    time.sleep(1)
    server1 = Process(target=stepsForPrimaryServer, args=("localhost", 5000))
    server1.start()
    time.sleep(1)
    server2 = Process(target=stepsForBackupServer, args=("localhost", 5001))
    server2.start()
    time.sleep(1)
    server3 = Process(target=stepsForBackupServer, args=("localhost", 5002))
    server3.start()
    time.sleep(1)
  
class Testing(unittest.TestCase):

    def test_write1(self):
        setUp()
        Client.runRegistryServer("localhost", 7000)
        server = ["localhost", 5001]
        unique_id1 = str(uuid.uuid1())
        fileName = "file1.txt"
        content = "coding in file1"
        unique_id2 = str(uuid.uuid1())
        self.assertEqual(Client.write(server, unique_id1, fileName, content), ["SUCCESS", unique_id1])
        self.assertEqual(Client.write(server, unique_id2, fileName, content), ["FAIL, FILE WITH THE SAME NAME ALREADY EXISTS", ""])
        self.assertEqual(Client.write(server, unique_id1, fileName, content), ["FAIL, FILE WITH THE SAME NAME ALREADY EXISTS", ""])


    
if __name__ == '__main__':
    setUp()
