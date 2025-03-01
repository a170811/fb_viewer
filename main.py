import os

from dotenv import load_dotenv
from loguru import logger

from src.fb_viewer import FBViewer

load_dotenv()


if "__main__" == __name__:
    viewer = FBViewer()
    
    # Optional: Login if credentials are available
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if email and password:
        viewer.login(email, password)
    else:
        logger.warning("No login credentials found. Running without login.")
        logger.warning("Set EMAIL and PASSWORD environment variables to enable login.")
    
    # View posts with default filters
    viewer.view_posts("台中租屋")
    
    # Example with custom filters:
    viewer.view_posts("台中租屋", filter_keywords=[
                "西屯", "南屯", "南區", "大里", "求租", 
                "龍井", "梧棲", "沙鹿", "售價", "3房", 
                "社宅", "社會住宅"
            ])