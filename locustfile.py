import json
from locust import TaskSet, task, HttpLocust


class ApiClientBehavior(TaskSet):
    def __init__(self, parent):
        super(ApiClientBehavior, self).__init__(parent)
        self.token = ""
        self.headers = {'Content-Type': 'application/json'}

    def on_start(self):
        self.token = self.login_user()
        self.headerz = {'Authorization': 'Bearer ' + self.token,
                        'Content-Type': 'application/json'}

    def login_user(self):
        data = self.client.post("auth/login", data=json.dumps({
            "email": "bettkevin757@gmail.com",
            "password": "Password@1"
        }),
            headers=self.headers,
            name="Login User")
        access_token = json.loads(data._content)['auth_token']
        return access_token

    @task(1)
    def login_(self):
        self.login_user()

    @task(3)
    def book_flight(self):
        data1 = {
            "number_of_tickets": "4",
            "flight_id": "1"
        }
        self.client.post("booking/flightbooking", data=json.dumps(data1),
                         headers=self.headerz,
                         name="Book Flight")


class ApiClient(HttpLocust):

    task_set = ApiClientBehavior
    host = "https://flight-api-bett.herokuapp.com/"
    min_wait = 5000
    max_wait = 10000
