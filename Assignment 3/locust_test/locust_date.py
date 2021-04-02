from locust import HttpUser, task, between

d = '2016-06-29'
# Creating an API User class inheriting from Locust's HttpUser class
class APIUser(HttpUser):
    # Setting the host name and wait_time
    host = 'http://localhost:8000'
    wait_time = between(3, 5)
    # Defining the post task using the JSON test data

    @task()
    def company(self):
        self.client.get('/Date/'+ d+'?ETFS_STOCKS=ETF&access_token=1234567asdfgh')