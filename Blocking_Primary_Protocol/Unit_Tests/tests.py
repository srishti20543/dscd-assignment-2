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

    def test_case(self):
        setUp()
        Client.runRegistryServer("localhost", 7000)
        server = ["localhost", 5001]
        unique_id1 = str(uuid.uuid1())
        fileName = "file1.txt"
        content = "coding in file1"
        unique_id2 = str(uuid.uuid1())

        self.assertEqual(Client.write(server, unique_id1, fileName, content), ["SUCCESS", unique_id1])
        self.assertEqual(Client.write(server, unique_id2, fileName, content), ["FAIL, FILE WITH THE SAME NAME ALREADY EXISTS", ""])
        self.assertEqual(Client.write(server, unique_id1, "abc.txt", content), ["FAIL, CANNOT HAVE TWO DIFFERENT FILES WITH SAME UUID", ""])

        server = ["localhost", 5000]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1"])
        server = ["localhost", 5001]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1"])
        server = ["localhost", 5002]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1"])

        content = "coding in file1 again"
        self.assertEqual(Client.write(server, unique_id1, fileName, content), ["SUCCESS", unique_id1])

        server = ["localhost", 5000]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1 again"])
        server = ["localhost", 5001]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1 again"])
        server = ["localhost", 5002]
        self.assertEqual(Client.read(server, unique_id1), ["SUCCESS", "file1.txt", "coding in file1 again"])

        self.assertEqual(Client.delete(server, unique_id1), "SUCCESS")

        server = ["localhost", 5000]
        self.assertEqual(Client.read(server, unique_id1), ["FAIL, FILE ALREADY DELETED", "", ""])
        server = ["localhost", 5001]
        self.assertEqual(Client.read(server, unique_id1), ["FAIL, FILE ALREADY DELETED","", ""])
        server = ["localhost", 5002]
        self.assertEqual(Client.read(server, unique_id1), ["FAIL, FILE ALREADY DELETED", "", ""])

        unique_id3 = str(uuid.uuid1())
        self.assertEqual(Client.read(server, unique_id3), ["FAIL, FILE DOESNOT EXIST", "", ""])

        self.assertEqual(Client.write(server, unique_id1, fileName, content), ["FAIL, DELETED FILE CANNOT BE UPDATED", ""])

        self.assertEqual(Client.delete(server, unique_id3), "FAIL, FILE DOES NOT EXIST")

        self.assertEqual(Client.delete(server, unique_id1), "FAIL, FILE ALREADY DELETED")

        

