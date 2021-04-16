from locust import HttpUser, task, between, tag
import json

filename = 'AGEN'
token ='eyJraWQiOiJFWGJweG9JNnlaRHozT3M4M2Q4M0JlNnBYZUlLUTlaNVM2eXRpT0FqQjZNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1c2UwNzQwZG1pcWdwN2l1a2I3cGY3bHJndSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibGFiLWFwaVwvbGFtYmRhLWludm9rZSIsImF1dGhfdGltZSI6MTYxODU0ODAzMCwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMi5hbWF6b25hd3MuY29tXC91cy1lYXN0LTJfczRnYWN0Zm1vIiwiZXhwIjoxNjE4NTUxNjMwLCJpYXQiOjE2MTg1NDgwMzAsInZlcnNpb24iOjIsImp0aSI6IjI4MWI4YzQ1LWZkMjEtNGQ0MS1hZGY3LTZiZDU1M2E4MWYzOSIsImNsaWVudF9pZCI6IjVzZTA3NDBkbWlxZ3A3aXVrYjdwZjdscmd1In0.mQZ4P36-OzamwWiDZJN-hSosY1D9EugDx9O6hB-phwAVjFGi9n0nX8fIYzVbPUHB-Q0g4JvXTK8jEumbSg_icw8_ksdqoLmRAy0SoV6Ah0-3zTECrj7M7U7fEuL9owqNfSZ2QmdYToinbeaMZFH5159-_grN7wACf9KRqsGGiRKuEUYBrK7c9tIutdijax7aKVq0StfzG_NIKb0C3_s0wcnqmBMm96SFxa3qJyd2g2SCHyXZlx3yYSBh9jburs4yUNRrb-nu2TgrbqDiwHc7Y8X0ZA7M9-UHUWW3-duKgnhKZq-UNPjX9DTTD0lVUYzA3GoRIJSnO52AdHCCbA3wAw'

class Edgar_file(HttpUser):
    host='https://10.247.123.172'
    wait_time = between(0,0.1)
    headers = {
        'Authorization': 'Bearer ' + token}
    base_url = "https://9kf5kdc8w5.execute-api.us-east-2.amazonaws.com/test/Edgar/"
    url = base_url + filename

    @task(1)
    def testurl1(self):
        resp = self.client.get(self.url, headers=self.headers)

class anon_mask(HttpUser):
    host = 'https://10.247.123.173'
    wait_time = between(0,0.1)
    headers = {
        'Authorization': 'Bearer ' + token}
    url = "https://9kf5kdc8w5.execute-api.us-east-2.amazonaws.com/test/new?s3_path=s3%3A%2F%2Ftextfiles2%2Fcall_transcripts%2FAGEN&Mask_Entity=NAME&deidentify_Ent=ADDRESS"

    @task(1)
    def testurl2(self):
        resp = self.client.get(self.url, headers=self.headers)

class sentiment(HttpUser):
    host = 'https://10.247.123.174'
    headers = {
        'Authorization': 'Bearer ' + token}

    text = 'Honestly Speaking, I am unable to understand exactly what you mean to say.'
    data = json.dumps({"signature_name": "serving_default", "instances": [text]})

    @task(1)
    def testurl3(self):
        json_response = self.client.post('http://localhost:8501/v1/models/saved_model:predict', data=self.data,
                                      headers=self.headers)