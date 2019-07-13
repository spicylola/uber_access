import json
from urllib.parse import unquote
import requests
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_rides.auth import AuthorizationCodeGrant





class UberAccess:

    def __init__(self, contents=None):
     self.contents = self._get_contents()
     self.server_token = self.contents["server_token"]
     self.uber_session = Session(server_token=self.server_token)
     self.uber_client = UberRidesClient(self.uber_session)

    def _get_contents(self):
        # TODO: You can make this configurable later and move to setup.py, hardcoded ish for now
        infile = open("./lib/credentials.txt", "r")
        contents = infile.readline()
        contents = json.loads(contents)
        return contents

    def get_available_products(self, lat, long):
        # ------------------Available products at clients location---------#
        response = self.uber_client.get_products(lat, long)
        products = response.json.get('products')
        return products

    def get_price_estimates(self, start_lat, start_long, end_lat, end_long, seat_count):
        response = self.uber_client.get_price_estimates(start_lat, start_long, end_lat, end_long, seat_count)
        estimate = response.json.get('prices')
        return estimate

    def uber_profile_exists(self):
        ### ----- Check if user has Uber Profile -----------#

        contents = self.content
        client_id = contents['client_id']
        scopes =set(contents['scopes'])
        client_secret =contents['client_secret']
        redirect_uri = contents['redirect_uri']
        code = contents['code']

        auth_flow = AuthorizationCodeGrant(
        client_id,
        scopes,
        client_secret,
        redirect_uri
        )
        auth_url = auth_flow.get_authorization_url()
        r = requests.get(auth_url, allow_redirects=True)
        encodedStr = r.url
        # Get rid of Url encoding
        decoded_url= unquote(encodedStr)
        idx = decoded_url.index("state=")
        state_str = decoded_url[idx:]

        # TODO: FIGURE OUT Whats going on with redirect URI
        new_redirect_url = redirect_uri+"?"+code+"&"+state_str

        # TODO: Figure this out for new session
        session = auth_flow.get_session(new_redirect_url)
        client = UberRidesClient(session, sandbox_mode=True)
        credentials = session.oauth2credential
        response = client.get_user_profile()
        profile = response.json
        email = profile.get('email')
        #THIS Is all a guess:
        has_uber_profile = True if email is None else False
        return has_uber_profile

if __name__ == '__main__':
    ub_instance = UberAccess()
    print(ub_instance.get_available_products(37.77, -122.41))
    print(ub_instance.get_price_estimates(start_lat=37.770, start_long=-122.411, end_lat=37.791,
                                          end_long=-122.405, seat_count=2))

