"""
Configuration module for loading and managing settings from TOML files.
This module is independent of the FB Viewer implementation to avoid tight coupling.
"""
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

import tomli


class ViewerMode(str, Enum):
    """Enum for viewer modes."""
    BY_URL = "by_url"
    BY_SEARCH = "by_search"


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class Config:
    """Configuration manager that loads settings from TOML files."""
    
    def __init__(self, config_path: Union[str, Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the TOML configuration file.
                         If None, looks for config.toml in the current directory.
        """
        if config_path is None:
            # Default to config.toml in the current directory
            config_path = Path("config.toml")
        elif isinstance(config_path, str):
            config_path = Path(config_path)
        
        self.config_path = config_path
        self.configs = {}
        self.default_config = None
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from the TOML file."""
        if not self.config_path.exists():
            raise ConfigError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomli.load(f)
            
            # Load default configuration name
            self.default_config = config_data.get("default")
            
            # Load configurations
            configs_data = config_data.get("configs", {})
            for name, config in configs_data.items():
                self.configs[name] = config
            
            if not self.configs:
                raise ConfigError("No configurations found in the config file")
            
            if self.default_config and self.default_config not in self.configs:
                raise ConfigError(f"Default configuration '{self.default_config}' not found")
            
            # If no default is specified, use the first configuration
            if not self.default_config:
                self.default_config = next(iter(self.configs))
        
        except tomli.TOMLDecodeError as e:
            raise ConfigError(f"Error parsing TOML file: {e}")
    
    def get_config_names(self) -> List[str]:
        """Get a list of available configuration names."""
        return list(self.configs.keys())
    
    def get_config(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a configuration by name.
        
        Args:
            name: Name of the configuration to get.
                  If None, returns the default configuration.
        
        Returns:
            The configuration dictionary.
        
        Raises:
            ConfigError: If the configuration is not found or is invalid.
        """
        if name is None:
            name = self.default_config
        
        if name not in self.configs:
            raise ConfigError(f"Configuration '{name}' not found. Available configs: {self.get_config_names()}")
        
        config = self.configs[name]
        
        # Validate the configuration
        mode = config.get("mode")
        if not mode:
            raise ConfigError(f"Configuration '{name}' is missing 'mode'")
        
        try:
            mode = ViewerMode(mode)
        except ValueError:
            raise ConfigError(f"Invalid mode '{mode}' in configuration '{name}'. Valid modes: {[m.value for m in ViewerMode]}")
        
        if mode == ViewerMode.BY_URL and not config.get("url"):
            raise ConfigError(f"Configuration '{name}' is missing 'url' required for mode '{mode}'")
        
        if mode == ViewerMode.BY_SEARCH and not config.get("search_key"):
            raise ConfigError(f"Configuration '{name}' is missing 'search_key' required for mode '{mode}'")
        
        return config
    
    def get_viewer_args(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get arguments for the FB Viewer from a configuration.
        
        Args:
            name: Name of the configuration to use.
                  If None, uses the default configuration.
        
        Returns:
            A dictionary of arguments for the FB Viewer.
        
        Raises:
            ConfigError: If the configuration is not found or is invalid.
        """
        config = self.get_config(name)
        mode = ViewerMode(config.get("mode"))
        
        args = {
            "mode": mode,
            "filter_keywords": config.get("filter_keywords", [])
        }
        
        if mode == ViewerMode.BY_URL:
            args["url"] = config.get("url")
        elif mode == ViewerMode.BY_SEARCH:
            args["search_key"] = config.get("search_key")
        
        return args
