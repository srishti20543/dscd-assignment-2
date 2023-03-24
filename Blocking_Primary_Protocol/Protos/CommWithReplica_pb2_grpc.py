# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import CommWithReplica_pb2 as CommWithReplica__pb2


class CommWithReplicaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendDetailsOfPR = channel.unary_unary(
                '/CommWithReplica/SendDetailsOfPR',
                request_serializer=CommWithReplica__pb2.Address.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )
        self.Write = channel.unary_unary(
                '/CommWithReplica/Write',
                request_serializer=CommWithReplica__pb2.WriteRequest.SerializeToString,
                response_deserializer=CommWithReplica__pb2.WriteResponse.FromString,
                )
        self.Read = channel.unary_unary(
                '/CommWithReplica/Read',
                request_serializer=CommWithReplica__pb2.ReadRequest.SerializeToString,
                response_deserializer=CommWithReplica__pb2.ReadResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/CommWithReplica/Delete',
                request_serializer=CommWithReplica__pb2.DeleteRequest.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )
        self.ConnectToPRforWrite = channel.unary_unary(
                '/CommWithReplica/ConnectToPRforWrite',
                request_serializer=CommWithReplica__pb2.WriteRequest.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )
        self.ConnectToPRforDelete = channel.unary_unary(
                '/CommWithReplica/ConnectToPRforDelete',
                request_serializer=CommWithReplica__pb2.DeleteRequest.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )
        self.ConnectToReplicaforWrite = channel.unary_unary(
                '/CommWithReplica/ConnectToReplicaforWrite',
                request_serializer=CommWithReplica__pb2.Request.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )
        self.ConnectToReplicaforDelete = channel.unary_unary(
                '/CommWithReplica/ConnectToReplicaforDelete',
                request_serializer=CommWithReplica__pb2.DeleteRequestToReplica.SerializeToString,
                response_deserializer=CommWithReplica__pb2.StatusRepReq.FromString,
                )


class CommWithReplicaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendDetailsOfPR(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectToPRforWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectToPRforDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectToReplicaforWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectToReplicaforDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CommWithReplicaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendDetailsOfPR': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDetailsOfPR,
                    request_deserializer=CommWithReplica__pb2.Address.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=CommWithReplica__pb2.WriteRequest.FromString,
                    response_serializer=CommWithReplica__pb2.WriteResponse.SerializeToString,
            ),
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=CommWithReplica__pb2.ReadRequest.FromString,
                    response_serializer=CommWithReplica__pb2.ReadResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=CommWithReplica__pb2.DeleteRequest.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
            'ConnectToPRforWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectToPRforWrite,
                    request_deserializer=CommWithReplica__pb2.WriteRequest.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
            'ConnectToPRforDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectToPRforDelete,
                    request_deserializer=CommWithReplica__pb2.DeleteRequest.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
            'ConnectToReplicaforWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectToReplicaforWrite,
                    request_deserializer=CommWithReplica__pb2.Request.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
            'ConnectToReplicaforDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectToReplicaforDelete,
                    request_deserializer=CommWithReplica__pb2.DeleteRequestToReplica.FromString,
                    response_serializer=CommWithReplica__pb2.StatusRepReq.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CommWithReplica', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CommWithReplica(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendDetailsOfPR(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/SendDetailsOfPR',
            CommWithReplica__pb2.Address.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/Write',
            CommWithReplica__pb2.WriteRequest.SerializeToString,
            CommWithReplica__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/Read',
            CommWithReplica__pb2.ReadRequest.SerializeToString,
            CommWithReplica__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/Delete',
            CommWithReplica__pb2.DeleteRequest.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectToPRforWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/ConnectToPRforWrite',
            CommWithReplica__pb2.WriteRequest.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectToPRforDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/ConnectToPRforDelete',
            CommWithReplica__pb2.DeleteRequest.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectToReplicaforWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/ConnectToReplicaforWrite',
            CommWithReplica__pb2.Request.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectToReplicaforDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CommWithReplica/ConnectToReplicaforDelete',
            CommWithReplica__pb2.DeleteRequestToReplica.SerializeToString,
            CommWithReplica__pb2.StatusRepReq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
