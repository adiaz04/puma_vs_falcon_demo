# perf/locustfile.py
from locust import HttpUser, task, between
import time

class RailsUser(HttpUser):
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

    @task(1)
    def stream_slow_reader(self):
        r = None
        try:
            r = self.client.get(
                "/stream",
                stream=True,                 # yield chunks as they arrive
                name="/stream(slow-read)",
                timeout=30,                  # generous timeout for demo
                allow_redirects=False,
            )

            # If something odd happened, bail out quietly
            if r is None or getattr(r, "raw", None) is None:
                return

            # Read small chunks slowly => emulate a slow consumer
            # Keep it short so the task completes within timeout.
            chunks_read = 0
            for chunk in r.iter_content(chunk_size=128):
                # Some servers send keepalive/heartbeat lines; guard against empty chunks
                if chunk:
                    chunks_read += 1
                    time.sleep(0.5)  # ~2 chunks/sec
                if chunks_read >= 20:  # don't loop forever in the demo
                    break
        except Exception:
            pass
        finally:
            try:
                if r is not None:
                    r.close()
            except Exception:
                pass
