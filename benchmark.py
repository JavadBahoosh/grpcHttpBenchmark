import requests
import grpc
import greet_pb2
import greet_pb2_grpc
import threading
import time

# Configuration
HTTP_SERVER_URL = "http://localhost:50050/greet"
GRPC_SERVER_ADDRESS = "127.0.0.1:50051"
DURATION = 10  # Benchmark duration in seconds

# Results storage
http_results = []
grpc_results = []

def benchmark_http():
    start_time = time.time()
    while time.time() - start_time < DURATION:
        try:
            response = requests.post(HTTP_SERVER_URL, json={"name": "Alice"})
            if response.status_code == 200:
                http_results.append(response.elapsed.total_seconds())
        except Exception as e:
            print("HTTP request failed:", e)

def benchmark_grpc():
    start_time = time.time()
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        while time.time() - start_time < DURATION:
            try:
                request_start = time.time()
                stub.Greet(greet_pb2.GreetRequest(name="Alice"))
                grpc_results.append(time.time() - request_start)
            except Exception as e:
                print("gRPC request failed:", e)

# Run benchmarks concurrently
http_thread = threading.Thread(target=benchmark_http)
grpc_thread = threading.Thread(target=benchmark_grpc)

http_thread.start()
grpc_thread.start()

http_thread.join()
grpc_thread.join()

# Calculate metrics
def calculate_metrics(results):
    total_requests = len(results)
    avg_response_time = sum(results) / total_requests if total_requests > 0 else 0
    return total_requests, avg_response_time

http_requests, http_avg_response = calculate_metrics(http_results)
grpc_requests, grpc_avg_response = calculate_metrics(grpc_results)

print(f"HTTP Server: {http_requests} requests in {DURATION}s, Avg response time: {http_avg_response:.4f}s")
print(f"gRPC Server: {grpc_requests} requests in {DURATION}s, Avg response time: {grpc_avg_response:.4f}s")

if http_requests > grpc_requests:
    print("HTTP server can handle more requests.")
elif grpc_requests > http_requests:
    print("gRPC server can handle more requests.")
else:
    print("Both servers handled an equal number of requests.")
