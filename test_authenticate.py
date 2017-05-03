import json
import requests
import testtools

from testtools.matchers import (
    Equals,
    KeysEqual,
)

from .config import (
    OPENAM_URI,
    PASSWORD,
    USERNAME,
)

AUTHENTICATE_URI = OPENAM_URI + "/authenticate"
OPENAM_USERNAME_HEADER = "X-OpenAM-Username"
OPENAM_PASSWORD_HEADER = "X-OpenAM-Password"

class TestAuthenticateZeroPage(testtools.TestCase):

    def test_authenticate_default(self):
        """
        Verify that the correct username and password combination
        gives a succesful response with the correct fields.
        """
        headers = {
            OPENAM_USERNAME_HEADER: USERNAME,
            OPENAM_PASSWORD_HEADER: PASSWORD,
            "Content-Type": "application/json",
        }
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(200))
        # verify that the response has the right fields
        self.assertThat(response.json(), KeysEqual(
            {
                "successUrl": "",
                "tokenId": "",
            }
        ))

    def test_authenticate_invalid_username(self):
        """
        Verify that when an invalid username is provided, the response
        is 401 Unauthorised.
        """
        headers = {
            OPENAM_USERNAME_HEADER: "invalid",
            OPENAM_PASSWORD_HEADER: PASSWORD,
            "Content-Type": "application/json",
        }
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(401))

    def test_authenticate_invalid_password(self):
        """
        Verify that when an invalid password is provided, the response
        is 401 Unauthorised.
        """
        headers = {
            OPENAM_USERNAME_HEADER: USERNAME,
            OPENAM_PASSWORD_HEADER: "invalid",
            "Content-Type": "application/json",
        }
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(401))


class TestAuthenticateCallbacks(testtools.TestCase):

    def test_authenticate_default(self):
        """
        Verify that when we send a POST request to the authenticate endpoint
        with no username and password specified, we get a callback response,
        then when we respond to that with the callback filled in with the
        correct username and password, a response is returned with the tokenId
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(200))
        data = response.json()
        for idx, callback in enumerate(data['callbacks']):
            if callback['type'] == 'NameCallback':
                data['callbacks'][idx]['input'][0]['value'] = USERNAME
            if callback['type'] == 'PasswordCallback':
                data['callbacks'][idx]['input'][0]['value'] = PASSWORD
        response = requests.post(
            AUTHENTICATE_URI,
            data=json.dumps(data),
            headers=headers,
        )
        self.assertThat(response.status_code, Equals(200))
        self.assertThat(response.json(), KeysEqual(
            {
                "successUrl": "",
                "tokenId": "",
            }
        ))

    def test_authenticate_invalid_username(self):
        """
        Verify that when we send a POST request to the authenticate endpoint
        with no username and password specified, we get a callback response,
        then when we respond to that with the callback filled in with the
        incorrect username and correct password, a 401 response is returned.
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(200))
        data = response.json()
        for idx, callback in enumerate(data['callbacks']):
            if callback['type'] == 'NameCallback':
                data['callbacks'][idx]['input'][0]['value'] = 'invalid'
            if callback['type'] == 'PasswordCallback':
                data['callbacks'][idx]['input'][0]['value'] = PASSWORD
        response = requests.post(
            AUTHENTICATE_URI,
            data=json.dumps(data),
            headers=headers,
        )
        self.assertThat(response.status_code, Equals(401))

    def test_authenticate_invalid_password(self):
        """
        Verify that when we send a POST request to the authenticate endpoint
        with no username and password specified, we get a callback response,
        then when we respond to that with the callback filled in with the
        correct username and incorrect password, a 401 response is returned.
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(200))
        data = response.json()
        for idx, callback in enumerate(data['callbacks']):
            if callback['type'] == 'NameCallback':
                data['callbacks'][idx]['input'][0]['value'] = USERNAME
            if callback['type'] == 'PasswordCallback':
                data['callbacks'][idx]['input'][0]['value'] = 'invalid'
        response = requests.post(
            AUTHENTICATE_URI,
            data=json.dumps(data),
            headers=headers,
        )
        self.assertThat(response.status_code, Equals(401))

    def test_authenticate_no_session(self):
        """
        Verify that when we send a POST request to the authenticate endpoint
        with no username and password specified, we get a callback response,
        then when we respond to that with the callback filled in with the
        correct username and correct password and the noSession parameter set
        to true, then a response is returned without the tokenId
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(AUTHENTICATE_URI, headers=headers)
        self.assertThat(response.status_code, Equals(200))
        data = response.json()
        for idx, callback in enumerate(data['callbacks']):
            if callback['type'] == 'NameCallback':
                data['callbacks'][idx]['input'][0]['value'] = USERNAME
            if callback['type'] == 'PasswordCallback':
                data['callbacks'][idx]['input'][0]['value'] = PASSWORD
        response = requests.post(
            AUTHENTICATE_URI,
            data=json.dumps(data),
            headers=headers,
            params={'noSession': True},
        )
        self.assertThat(response.status_code, Equals(200))
        self.assertThat(response.json(), KeysEqual(
            {
                "successUrl": "",
                "message": "",
            }
        ))
