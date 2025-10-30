import requests

class SubdomainModule:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_from_securitytrails(self, domain):
        if not self.api_key:
            print(f"Please check SECURITYTRAILS_TOKEN in .env ")
            return []

        url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
        headers = {"APIKEY": self.api_key}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            subdomains = {f"{sub}.{domain}" for sub in data.get('subdomains', [])}
            return list(subdomains)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []