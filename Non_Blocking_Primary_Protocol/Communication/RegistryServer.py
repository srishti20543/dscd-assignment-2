import sys
sys.path.insert(1, '../Protos')

from concurrent import futures

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import logging
import grpc
import threading

PR_details = {}
Replicas = {}


def addReplicas(name, ip, port):

    if name == 'replica_1':
        PR_details['name'] = name
        PR_details['ip'] = ip
        PR_details['port'] = port

    for replica in Replicas.keys():
        addr = Replicas[replica][0] + str(Replicas[replica][1])
        check_addr = ip + str(port)
        if addr == check_addr:
            return 1

    Replicas[name] = [ip, port]
    return 0


class CommWithRegistryServerServicer(CommWithRegistryServer_pb2_grpc.CommWithRegistryServerServicer):

    def Register(self, request, context):
        print("REGISTRY SERVER: JOIN REQUEST FROM " + request.ip + ":" + str(request.port) + "\n")
        nextcount = len(Replicas) + 1
        name = 'replica_' + str(nextcount)
        result = addReplicas(name, request.ip, request.port)
        if result == 0:
            if request.port != PR_details["port"]:
                addr=PR_details["ip"]+":"+str(PR_details["port"])
                with grpc.insecure_channel(addr) as channel:
                    stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
                    request = CommWithReplica_pb2.Address(name=name, ip=request.ip, port=request.port)
                    stub.SendDetailsOfPR(request)
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="SUCCESS", primaryServerAddress=CommWithReplica_pb2.Address(name=PR_details['name'], ip=PR_details['ip'], port=PR_details['port']), selfName=name)
        else:
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="FAIL", primaryServerAddress=None, selfName=None)


    def getReplicaList(self, request, context):
        print("REGISTRY SERVER: REPLICA LIST REQUEST FROM CLIENT " + request.ip + ":" + str(request.port) + "\n")
        for replica in Replicas.keys():
            ip = Replicas[replica][0]
            port = Replicas[replica][1]
            yield CommWithRegistryServer_pb2.ReplicaListResponse(replicaServer= CommWithReplica_pb2.Address(name=replica, ip=ip, port=port))


def startRegistryServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithRegistryServer_pb2_grpc.add_CommWithRegistryServerServicer_to_server(CommWithRegistryServerServicer(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
