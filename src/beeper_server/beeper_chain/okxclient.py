import json
import warnings
from datetime import datetime, timezone

import httpx
from httpx import Client
from datetime import datetime, timezone

from . import consts as c, util

class OkxClient(Client):

    def __init__(self, project_id='-1', api_key='-1', api_secret_key='-1', passphrase='-1', debug=False, base_api=c.API_URL, proxy=None):
        super().__init__(base_url=base_api, http2=True, proxy=proxy)
        self.PROJECT_ID = project_id
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.use_server_time = False
        self.domain = base_api
        self.debug = debug

    def _request(self, method, request_path, params):
        if method == c.GET:
            request_path = request_path + util.parse_params_to_str(params)
        timestamp = util.get_timestamp()
        body = json.dumps(params) if method == c.POST else ""
        if self.API_KEY != '-1':
            sign = util.sign(util.pre_hash(timestamp, method, request_path, str(body), self.debug), self.API_SECRET_KEY)
            header = util.get_header(self.PROJECT_ID, self.API_KEY, sign, timestamp, self.PASSPHRASE, self.debug)

        response = None
        if self.debug == True:
            print(f'domain: {self.domain}')
            print(f'url: {request_path}')
            print(f'body:{body}')
        if method == c.GET:
            response = self.get(request_path, headers=header)
        elif method == c.POST:
            response = self.post(request_path, data=body, headers=header)
        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _get_timestamp(self):
        request_path = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = self.get(request_path)
        if response.status_code == 200:
            ts = datetime.fromtimestamp(int(response.json()['data'][0]['ts']) / 1000.0, tz=timezone.utc)
            return ts.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        else:
            return ""
