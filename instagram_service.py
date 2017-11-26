import requests
import json

class InstagramApi:
    """Reaches out to the Instagram Proxy API for infos"""
    endpoint = "https://igpi.ga/"
    headers = {'referer': 'https://github.com/whizzzkid/instagram-proxy-api'}
    next_url = None

    def __init__(self, account=None):
        self.account = account

    def user_url(self, action):
        """Returns the full url"""
        return self.endpoint + self.account + '/' + action

    def get(self, url):
        """Sends a get request and parses the response"""
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)

        if 'next' in data:
            self.next_url = data['next']
        else:
            self.next_url = None

        return data

    def info(self):
        """Fetches user information"""
        url = self.user_url("?__a=1")
        return self.get(url)

    def media(self, count=10):
        """Fetches up to X posts"""
        url = self.user_url("media?count={}".format(count))
        return self.get(url)

    def has_next(self):
        return self.next_url != None

    def next(self):
        """fetches the next round of results"""
        if self.next_url:
            return self.get(self.next_url)
        else:
            return None