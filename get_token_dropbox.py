from os import environ, path
from dotenv import load_dotenv

from dropbox import DropboxOAuth2FlowNoRedirect

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))



APP_KEY = environ.get("APP_KEY")

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()


try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

print(f"Refresh token: {oauth_result.refresh_token}")



