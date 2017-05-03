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

class TestAuthenticate(testtools.TestCase):

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
