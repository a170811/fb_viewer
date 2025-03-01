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
    
    viewer.view_posts_by_url(
        "https://www.facebook.com/groups/191628104570229/", # 台中羽球同好版
        # "https://www.facebook.com/groups/737214643034696/", # 台中羽球揪團版
        filter_keywords=['沙鹿', '西屯']
    )

    # Example with custom filters:
    # viewer.view_posts_by_search("台中租屋", filter_keywords=[
    #             "西屯", "南屯", "南區", "大里", "求租", 
    #             "龍井", "梧棲", "沙鹿", "售價", "3房", 
    #             "社宅", "社會住宅"
    #         ])