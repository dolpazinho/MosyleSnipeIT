import requests

class Mosyle:
    
    # Create Mosyle instance
    def __init__(self, access_token, url="https://businessapi.mosyle.com/v1/", user="", password=""):
        self.url = url
        self.user = user
        self.password = password
        self.access_token = access_token
        self.token = None
        self.request = requests.Session()
        self.login()

    def login(self):
        login_url = self.url + "/login"
        body = {
            "email": self.user,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/json",
            "accessToken": self.access_token
        }
        # Debugging: Print the headers to verify
        print("Sending headers:", headers)
        response = self.request.post(login_url, json=body, headers=headers)
        # Debugging: Print the response status and body
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()  # Raise an error for bad status codes
        self.token = response.headers.get('Authorization')  # Extract token from headers
        if self.token:
            self.request.headers["Authorization"] = self.token
            self.request.headers["accessToken"] = self.access_token

    def refresh_token(self):
        self.login()

    # Create variables requests
    def list(self, os):
        self._ensure_token()
        print("Listing devices for OS:", os)
        params = {
            "operation": "list",
            "options": {
                "os": os,
                "supervised": "true",
                "page": 1,
            }
        }
        return self.request.post(self.url + "/devices", json=params)

    def listTimestamp(self, start, end, os):
        self._ensure_token()
        params = {
            "operation": "list",
            "options": {
                "os": os,
                "enrolldate_start": start,
                "enrolldate_end": end    
            }
        }
        return self.request.post(self.url + "/devices", json=params)

    def listmobile(self):
        self._ensure_token()
        params = {
            "operation": "list",
            "options": {
                "os": "ios"
            }
        }
        return self.request.post(self.url + "/devices", json=params)

    def listuser(self, iduser):
        self._ensure_token()
        params = {
            "operation": "list_users",
            "options": { "identifiers": [iduser]
                }
        }
        return self.request.post(self.url + "/users", json=params)

    def setAssetTag(self, serialnumber, tag):
        self._ensure_token()
        params = {
            "operation": "update_device",
            "serialnumber": serialnumber,
            "asset_tag": tag
        }
        return self.request.post(self.url + "/devices", json=params)

    def _ensure_token(self):
        if not self.token:
            self.refresh_token()
