# Simple recon tool

A simple subdomain discovery and monitoring tool. In the first stage, it uses the SecurityTrails API to find subdomains for a specified domain and stores them in a local SQLite database, tracking changes over time.

## Features

-   Fetches subdomains from SecurityTrails.
-   Stores results in a SQLite database (`recon.db`).
-   Tracks new and removed subdomains between scans.
-   Accepts a target domain via command-line arguments.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key:**
    -   Create a file named `.env` in the project root.
    -   Add your SecurityTrails API key to the `.env` file like this:
        ```
        SECURITYTRAILS_API_KEY="your_api_key_here"
        ```

## Usage

To run a scan, provide a domain name as a command-line argument:

```bash
python main.py <domain_to_scan>
```

### Example

```bash
python main.py example.com
```

The tool will create a `recon.db` file to store the results.


# Docker
```
docker-compose build
docker-compose run --rm recon-app python main.py example.com
```