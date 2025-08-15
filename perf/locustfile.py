from locust import HttpUser, task, between
import time

class RailsUser(HttpUser):
    # Short think time so we drive concurrency
    wait_time = between(0.05, 0.2)

    @task(5)
    def health(self):
        self.client.get("/health", name="/health")

    @task(3)
    def slow_200ms(self):
        self.client.get("/slow?s=0.2", name="/slow?s=0.2")

    @task(1)
    def slow_1s(self):
        self.client.get("/slow?s=1.0", name="/slow?s=1.0")

    # Simulate a slow-reading client on the stream endpoint.
    # This is where async / non-blocking servers shine.
    @task(1)
    def stream_slow_reader(self):
        # Stream=True yields an iterator; read slowly to emulate a "slow consumer".
        with self.client.get("/stream", stream=True, name="/stream(slow-read)", timeout=30) as r:
            try:
                # Read a few small chunks slowly.
                for chunk in r.iter_content(chunk_size=128):
                    # emulate a user/connection that reads at ~2 chunks/sec
                    time.sleep(0.5)
            except Exception:
                pass

