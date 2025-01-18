import requests
import json
from fake_useragent import UserAgent
from urllib.parse import urlparse

def get_subdomains(domain, retries=3):
    """
    Fetch subdomains for the given domain using crt.sh
    Use a fake user agent to bypass restrictions.
    """
    url = f'https://crt.sh/?q=%25.{domain}&output=json'
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                subdomains = set()
                for entry in data:
                    name_value = entry.get("name_value")
                    if name_value:
                        subdomains.update(name_value.split("\n"))
                return sorted(subdomains)
            elif response.status_code == 503:
                print(f"Server unavailable (503). Retrying... (Attempt {attempt}/{retries})")
        except requests.RequestException as e:
            print(f"Error: {e}")
    print("Failed to fetch data after retries.")
    return []

if __name__ == "__main__":
    print("Reverse Subdomain Finder")
    file_path = input("Enter the path to the file containing domains: ").strip()

    try:
        with open(file_path, "r") as file:
            domains = [line.strip() for line in file if line.strip()]

        with open("subdo.txt", "w") as output_file:
            for domain in domains:
                print(f"Fetching subdomains for: {domain}\n")
                subdomains = get_subdomains(domain)

                if subdomains:
                    output_file.write("\n".join(subdomains) + "\n")
                    print(f"Found {len(subdomains)} subdomains for {domain}. Results saved to subdo.txt.\n")
                else:
                    print(f"No subdomains found for {domain}.\n")

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")
