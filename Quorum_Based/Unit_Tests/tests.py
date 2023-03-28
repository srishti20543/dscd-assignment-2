import sys

sys.path.insert(1, '../Communication')

import RegistryServer
import Replica
import Client
import uuid
from multiprocessing import Process
import time
import unittest


N = 5
N_R = 3
N_W = 3

def stepsForServer(IP, port):
    Replica.connectToRegistry(IP, port)
    Replica.ConnectToReplica(IP, port)

def stepsForClient1(IP, port):
    Client.runRegistryServer(IP, port)


def setUp():
    global N, N_R, N_W
    registryServer = Process(target=RegistryServer.startRegistryServer, args=(N,N_R,N_W))
    registryServer.start()
    time.sleep(1)

    for i in range(N):
        server = Process(target=stepsForServer, args=("localhost", 5000 + i))
        server.start()
        time.sleep(1)

  
class Testing(unittest.TestCase):

    def test_case(self):
        global N, N_R, N_W
        # A. & B. Setup registry server, and run N replicas
        print("=================== SET UP REGISTRY SERVER & REPLICAS ======================")
        setUp()

        # C. Create a client, and check all replicas are running in console
        print("=================== SET UP CLIENT ======================")
        Client.runRegistryServer("localhost", 7000)

        # D. Client performs a write operation
        print("=================== CLIENT PERFORMS WRITE ======================")

        unique_id1 = str(uuid.uuid1())
        fileName = "file1.txt"
        content = "Testing file 1"

        print("=================== CHECK SUCCESSFUL WRITE ======================")
        print("Writing UUID: ", unique_id1, " filename: ", fileName)
        writeStatus = Client.write(unique_id1, fileName, content)
        time.sleep(1)
        element = ["SUCCESS", unique_id1]
        self.assertEqual(writeStatus, [element] * N_W)

        print("=================== CHECK FAILED WRITE 1 ======================")
        unique_id2 = str(uuid.uuid1())

        print("Writing UUID: ", unique_id2, " filename: ", fileName)
        writeStatus = Client.write(unique_id2, fileName, content)
        time.sleep(1)
        # element = ["FAIL, FILE WITH THE SAME NAME ALREADY EXISTS", ""]
        # self.assertEqual(writeStatus, [element] * N_W)

        print("=================== CHECK FAILED WRITE 2 ======================")
        print("Writing UUID: ", unique_id1, " filename: ", "abc.txt")

        writeStatus = Client.write(unique_id1, "abc.txt", content)
        time.sleep(1)
        # element = ["FAIL, CANNOT HAVE TWO DIFFERENT FILES WITH SAME UUID", ""]
        # self.assertEqual(writeStatus, [element] * N_W)
        # self.assertEqual(Client.write(unique_id1, "abc.txt", content), ["FAIL, CANNOT HAVE TWO DIFFERENT FILES WITH SAME UUID", ""])

        # E. Client performs a read operation
        print("=================== CLIENT AGAIN PERFORMS READ ======================")
        # We test this in the console
        print("Reading UUID: ", unique_id1)
        Client.read(unique_id1)

        # F. Client performs a write operation
        print("=================== CLIENT AGAIN PERFORMS WRITE ======================")
        content = "coding in file1 again"
        print("Writing UUID: ", unique_id1, " filename: ", fileName)
        Client.write(unique_id1, fileName, content)
        time.sleep(1)

        # G. Client performs a read operation
        print("=================== CLIENT AGAIN PERFORMS READ ======================")
        # We test this in the console
        print("Reading UUID: ", unique_id1)
        Client.read(unique_id1)


        # H. Client performs a delete operation
        print("=================== CLIENT PERFORMS DELETE ======================")
        print("Deleting UUID: ", unique_id2)

        Client.delete(unique_id2)

        # I. Client performs a read operation
        print("=================== CLIENT PERFORMS READ ======================")
        print("Reading UUID: ", unique_id2)
        Client.read(unique_id2)
        

