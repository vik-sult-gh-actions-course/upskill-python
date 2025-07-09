import os
from dotenv import load_dotenv
from sites_api.clients.sites_api_client import SitesAPIClient
from sites_api.db import SessionLocal
from sites_api.models import Sites

load_dotenv()

session = SessionLocal()

sites_api_url = os.getenv("SITES_API_URL", "")

# Initialize client
client = SitesAPIClient(base_url=sites_api_url)

# Sign up
client.signup("Testina Testowa", "testina.testowa@test.com", "mypassword")

# Get first 5 sites
# sites = client.get_list_of_sites(page=0, limit=5)

# Get all sites (warning: might be a lot of data!)
all_sites = client.get_all_sites()

for site in all_sites:
    source_id = site["id"]

    site_model = session.query(Sites).filter_by(source_id=source_id).first()

    # Common fields to update
    site_attributes = {
        "name": site["name"],
        "cid": site["cid"],
        "manager": site["manager"],
        "submanager": site["submanager"],
        "state": site["state"],
        "host": bool(site["host"]),
        "devteam": site["devteam"],
        "lifetime": site["lifetime"],
        "url": site["url"],
    }

    if site_model is None:
        # Create new site with all attributes including source_id
        site_model = Sites(source_id=source_id, **site_attributes)
    else:
        # Update existing site
        for attr, value in site_attributes.items():
            setattr(site_model, attr, value)

    session.add(site_model)
    session.commit()

session.close()
print("End collect sites process")
