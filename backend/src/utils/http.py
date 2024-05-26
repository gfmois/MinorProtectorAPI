import requests

class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None, headers=None):
        response = self.session.get(url, params=params, headers=headers)
        return response

    def post(self, url, data=None, headers=None):
        response = self.session.post(url, data=data, headers=headers)
        return response

    def put(self, url, data=None, headers=None):
        response = self.session.put(url, data=data, headers=headers)
        return response

    def delete(self, url, headers=None):
        response = self.session.delete(url, headers=headers)
        return response