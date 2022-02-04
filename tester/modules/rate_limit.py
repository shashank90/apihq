import json

from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def read_from_file(self):
        with open('/home/kali/Desktop/rate_limit_input.json') as f:
            self.data = json.load(f)

    def on_start(self):
        print("Locust started")
        self.read_from_file()

    @task
    def get_request(self):
        self.client.get("/static/assets.js")

    @task
    def post_request(self):
        self.client.post(url="/about/", headers=None)
