import httpx
from config import API_KEY, REDIRECT_URI, SECRET, TOKEN_PATH
from log_setup import logger
from schwab import auth

# Login process
try:
    c = auth.client_from_token_file(
        TOKEN_PATH, API_KEY, SECRET, enforce_enums=False)
except FileNotFoundError:
    c = auth.client_from_manual_flow(
        API_KEY, SECRET, REDIRECT_URI, TOKEN_PATH, enforce_enums=False)

# Grabbing account number for login check
resp = c.get_account_numbers()

# Grabbing response code
assert resp.status_code == httpx.codes.OK

# If good response code then login successful
if resp.status_code == 200:
    logger.info("Login Successful\n")
    print("Login Successful")
else:
    logger.error("Login NOT Successful\n")
    print("Login NOT Successful")

# Grabbing account hash
accountHash = c.get_account_numbers().json()[0]["hashValue"]

# Assigning client to cline to use in main
cline = c
