from locust import HttpUser, task, between


comp = ['asm','a','aa']
# Creating an API User class inheriting from Locust's HttpUser class
class APIUser(HttpUser):
    # Setting the host name and wait_time
    host = 'http://localhost:8000'
    wait_time = between(3, 5)
    # Defining the post task using the JSON test data
    @task()
    def company(self):
        for c in comp:
            self.client.get('/Company/'+c+'?access_token=1234567asdfgh')
