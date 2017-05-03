This is a small test suite for OpenAM implemented in Python(3)

Prior to executing the tests you will need to update config.py with the correct details for the 

To execute these tests you will need to:

1. Create a virtual environment, with something like `virtualenv --python=python3 venv`
2. Install the dependencies from PyPi with `pip install -r requirements.txt`
3. Go ahead and run them with `nosetests3 test_authenticate.py`

All 7 tests should pass.
