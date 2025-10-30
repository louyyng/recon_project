import sys
from database import DatabaseManager
from subdomain_module import SubdomainModule
from dotenv import load_dotenv
import os 

load_dotenv()

if len(sys.argv) < 2:
    print("Usage: python main.py <domain>")
    sys.exit(1)

target_domain = sys.argv[1]

SECURITYTRAILS_API_KEY = os.getenv("SECURITYTRAILS_API_KEY")

db = DatabaseManager("recon.db")
recon_module = SubdomainModule(SECURITYTRAILS_API_KEY)

target_id = db.get_or_create_target(target_domain)

old_subs = db.get_active_subdomains(target_id)
new_subs = set(recon_module.fetch_from_securitytrails(target_domain))

db.update_subdomains(target_id, new_subs, old_subs)

