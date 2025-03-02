#!/usr/bin/env python
"""
Command-line interface for FB Viewer.
"""
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from .config import Config, ViewerMode, ConfigError
from . import FBViewer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Facebook Viewer")
    parser.add_argument(
        "--config", "-c",
        help="Configuration to use"
    )
    parser.add_argument(
        "--config-file", "-f",
        help="Path to the configuration file (default: config.toml)"
    )
    parser.add_argument(
        "--list-configs", "-l",
        action="store_true",
        help="List available configurations"
    )
    return parser.parse_args()


def main():
    """Main entry point for the console script."""
    load_dotenv()
    args = parse_args()
    
    # Load configuration
    try:
        config_manager = Config(args.config_file)
        logger.info(f"Loaded configuration from {config_manager.config_path}")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # List available configurations if requested
    if args.list_configs:
        print("Available configurations:")
        for name in config_manager.get_config_names():
            config = config_manager.get_config(name)
            mode = ViewerMode(config.get("mode"))
            mode_str = "URL" if mode == ViewerMode.BY_URL else "Search"
            
            if mode == ViewerMode.BY_URL:
                target = config.get("url")
            else:
                target = config.get("search_key")
                
            print(f"  - {name}: {mode_str} mode, Target: {target}")
            print(f"    Filter keywords: {', '.join(config.get('filter_keywords', []))}")
        
        if config_manager.default_config:
            print(f"\nDefault configuration: {config_manager.default_config}")
        
        sys.exit(0)
    
    # Get the selected configuration
    try:
        viewer_args = config_manager.get_viewer_args(args.config)
        config_name = args.config or config_manager.default_config
        logger.info(f"Using configuration: {config_name}")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Initialize the viewer
    viewer = FBViewer()
    
    # Optional: Login if credentials are available
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if email and password:
        viewer.login(email, password)
    else:
        logger.warning("No login credentials found. Running without login.")
        logger.warning("Set EMAIL and PASSWORD environment variables to enable login.")
    
    # Run the viewer with the selected configuration
    mode = viewer_args["mode"]
    filter_keywords = viewer_args.get("filter_keywords", [])
    
    if mode == ViewerMode.BY_URL:
        viewer.view_posts_by_url(viewer_args["url"], filter_keywords=filter_keywords)
    elif mode == ViewerMode.BY_SEARCH:
        viewer.view_posts_by_search(viewer_args["search_key"], filter_keywords=filter_keywords)


if __name__ == "__main__":
    main()
