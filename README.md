# gRPC vs HTTP Benchmark

This project benchmarks the performance of HTTP and gRPC servers by comparing their request-handling capacity and response times.

## Prerequisites

- **Python 3.7+**
- **Docker**
- **`protoc` compiler** (for generating gRPC code from `.proto` files)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd grpcHttpBenchmark
```

### 2. Set Up Virtual Environment

Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install Python Dependencies

Within the activated virtual environment, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Generate gRPC Code from Proto File

Ensure that `protoc` is installed on your system. To generate the `greet_pb2.py` and `greet_pb2_grpc.py` files, run:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greet.proto
```

This will generate the `greet_pb2.py` and `greet_pb2_grpc.py` files in the project directory.

### 5. Run Docker Containers

Use Docker Compose to start the HTTP and gRPC servers:

```bash
docker compose up --build
```

The HTTP server will be available at `http://127.0.0.1:50050`, and the gRPC server will listen on `127.0.0.1:50051`.

### 6. Run the Benchmark Script

With Docker running the servers, you can run the benchmark script in the host environment:

```bash
python benchmark.py
```

The script will output the results for the HTTP and gRPC servers, including request counts and average response times.

## Docker Setup

### Dockerfile for HTTP and gRPC Servers

Both servers have Dockerfiles (`DockerfileHTTP` and `DockerfileGRPC`), and Docker Compose configuration is in `docker-compose.yml`. Ensure that Docker is running before starting the benchmark.

## Example Results

The benchmark script will print results similar to:

```
HTTP Server: <requests> requests in <duration>s, Avg response time: <avg_response_time>s
gRPC Server: <requests> requests in <duration>s, Avg response time: <avg_response_time>s
```

## Troubleshooting

- **`curl: (52) Empty reply from server`**: Make sure the HTTP server is running on the correct port (`50050` in this setup).
- **Python or gRPC errors**: Ensure `greet_pb2.py` and `greet_pb2_grpc.py` are generated as described above.
