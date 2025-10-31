import requests
import os
import subprocess

class SubdomainModule:
    def __init__(self, api_key):
        self.api_key = api_key
        self.found_subdomains = set()

    def _fetch_from_securitytrails(self, domain):
        print(f"INFO: Finding subdomains on securitytrails ...")
        if not self.api_key:
            print(f"Please check SECURITYTRAILS_TOKEN in .env ")
            return 

        url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
        headers = {"APIKEY": self.api_key}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            subdomains = {f"{sub}.{domain}" for sub in data.get('subdomains', [])}
            self.found_subdomains.update(subdomains)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        
    def _fetch_from_crtsh(self, domain):
        print(f"INFO: Finding subdomains on crtsh ...")
        url = f"https://crt.sh/?q=%.{domain}&output=json"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            if not response.text:
                print("WARNING: crt.sh return empty")
                return

            data = response.json()

            subdomains = set()
            for entry in data:
                name = entry.get('name_value')
                if name:
                    names = name.split('\n')
                    for sub_name in names:
                        if '*' not in sub_name and sub_name.endswith(domain):
                            subdomains.add(sub_name)
            print(f"INFO: Found {len(subdomains)} subdomains")
            self.found_subdomains.update(subdomains)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
    def _fetch_with_subfinder(self, domain):
        print(f"INFO: Running subfinder ...")
        command = ['subfinder', '-d', domain, '-silent']
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=300
            )
            subdomains = {line for line in process.stdout.strip().split('\n') if line}
            print(f"INFO: Found {len(subdomains)}")
            self.found_subdomains.update(subdomains)
        except Exception as e:
            print(f"{e}")

    def run(self, domain):
        self._fetch_from_securitytrails(domain)
        self._fetch_with_subfinder(domain)
        self._fetch_from_crtsh(domain)
        return list(self.found_subdomains)