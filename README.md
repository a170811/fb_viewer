# FB Viewer

A tool for viewing and filtering Facebook posts from groups or search results.

## Features

- View posts from Facebook groups by URL
- View posts from Facebook search results
- Filter posts by keywords
- Configurable settings using TOML files for different use cases (rental, badminton, etc.)
- Login support with cookies persistence

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fb_viewer.git
cd fb_viewer

# Install dependencies
pip install -e .
```

## Usage

### Basic Usage

```bash
# Run with default configuration
python main.py

# Run with a specific configuration
python main.py --config rental

# Use a different configuration file
python main.py --config-file /path/to/your/config.toml

# List available configurations
python main.py --list-configs
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
EMAIL=your_facebook_email@example.com
PASSWORD=your_facebook_password
```

### Configuration File

The configuration file uses TOML format and should be structured as follows:

```toml
# Default configuration to use if not specified
default = "badminton"

# Badminton configuration
[configs.badminton]
mode = "by_url"
url = "https://www.facebook.com/groups/191628104570229/"  # 台中羽球同好版
filter_keywords = ["沙鹿", "西屯"]

# Rental configuration
[configs.rental]
mode = "by_search"
search_key = "台中租屋"
filter_keywords = ["西屯", "南屯", "南區", "大里"]
```

### Available Configurations

The default configuration file includes:

- `badminton`: View posts from the 台中羽球同好版 Facebook group
- `badminton_alt`: View posts from the 台中羽球揪團版 Facebook group
- `rental`: Search for "台中租屋" and filter results

## Creating Custom Configurations

You can create custom configurations by:

1. Editing the `config.toml` file directly
2. Creating a new TOML file with your configurations and using the `--config-file` option

### Configuration Structure

Each configuration must include:

- `mode`: Either "by_url" or "by_search"
- For "by_url" mode: `url` (the Facebook group URL)
- For "by_search" mode: `search_key` (the search term)
- `filter_keywords`: A list of keywords to filter posts (optional)

Example:

```toml
[configs.my_custom_config]
mode = "by_url"
url = "https://www.facebook.com/groups/your_group_id/"
filter_keywords = ["keyword1", "keyword2"]
```
