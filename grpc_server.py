import grpc
from concurrent import futures
import greet_pb2
import greet_pb2_grpc

class GreeterService(greet_pb2_grpc.GreeterServicer):
    def Greet(self, request, context):
        name = request.name if request.name else 'Guest'
        return greet_pb2.GreetResponse(message=f'Hello, {name}')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('gRPC server is running on port 50051')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()