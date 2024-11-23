import os

from dotenv import load_dotenv

from src.fb_viewer import FBViewer

load_dotenv()


email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
if email is None or password is None:
    raise Exception("Please enter email and password")


if "__main__" == __name__:
    viewer = FBViewer(email, password)
    viewer.view_posts("台中租屋")
