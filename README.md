# README

## Running the Demo App

This demo compares Puma and Falcon web servers. Follow these steps to run both servers and benchmark them using Locust:

> **Note:** Each of the following commands should be run in its own terminal window/tab.

### 1. Launch the Puma server (port 3001)

```
./bin/puma-3001
```

### 2. Launch the Falcon server (port 3002)

```
./bin/falcon-3002
```

### 3. Run Locust against Puma (port 3001)

```
locust -f perf/locustfile.py --host=http://127.0.0.1:3001
```

This will start the Locust web UI at http://localhost:8089 by default.

### 4. Run Locust against Falcon (port 3002, web UI on port 8090)

```
locust -f perf/locustfile.py --host=http://127.0.0.1:3002 --web-port 8090
```

This will start the Locust web UI at http://localhost:8090.

---

You can now use the Locust web UI to start load tests and compare the performance of Puma and Falcon.