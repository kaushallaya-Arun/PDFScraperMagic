# PDF Scraper

![PDF Scraper Logo](https://example.com/your-logo.png)

PDF Scraper is a versatile Python script for crawling websites, discovering PDF links, and downloading them. It offers options to use user agents and proxies for enhanced scraping capabilities.

## Features

- Crawl a website up to a specified depth.
- Find and download PDFs from discovered links.
- Utilize user agents to mimic different browsers.
- Implement proxies for anonymous and distributed scraping.
- Concurrently download PDFs using ThreadPoolExecutor.
- User-friendly CLI with prompts for configuration.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/pdf-scraper.git
    cd pdf-scraper
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python scraper.py
    ```

## Configuration

- `scraper.py`: Main script for crawling and downloading PDFs.
- `requirements.txt`: List of Python packages required for the script.
- `README.md`: Project documentation.

## Usage

Follow the prompts to enter the target URL, choose proxy settings, and set the depth and number of iterations.

## Examples

### Basic Usage

```bash
python scraper.py


Using a Proxy: python scraper.py --proxy http://your-proxy-ip:your-proxy-port
