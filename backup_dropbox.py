import dropbox
from os import environ, path
import pathlib
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


APP_KEY = environ.get("APP_KEY")
APP_SECRET = environ.get("APP_SECRET")
REFRESH_TOKEN = environ.get("REFRESH_TOKEN")

dbx = dropbox.Dropbox(
            app_key = APP_KEY,
            app_secret = APP_SECRET,
            oauth2_refresh_token = REFRESH_TOKEN
        )


local_file_path = pathlib.Path("app.db") 

with local_file_path.open("rb") as f:
    meta = dbx.files_upload(f.read(), "/app1.db", mode=dropbox.files.WriteMode("overwrite"))
