import argparse
import requests
import take_pic as take_pic
from pathlib import Path

def get_site_response_code(site):
    try:
        # could add allow_redirects=True to follow through.
        r = requests.head(str(site))
        return r.status_code

    except requests.ConnectionError as e:
        print("Connection Error:", e)
        return 0

def get_site_redirect(site):
    try:
        response = requests.head(site, allow_redirects=True)
        if response.history:
            print("Request was redirected")
            for resp in response.history:
                print("  ", resp.status_code, resp.url)
            print("  ","Final destination:", response.status_code, response.url)
            return {"response_code": response.status_code, "url": response.url}
        else:
            print("Response was not redirected")
            return {"response_code": 000, "url": ""}
    except requests.ConnectionError as e:
        print("Connection Error: ", e)
        return {"response_code": 000, "url": ""}

def domain_to_http_url(domain):
    site = "http://" + str(domain)
    return site

def domain_to_https_url(domain):
    site = "https://" + str(domain)
    return site

# Argument parsing
parser = argparse.ArgumentParser(prog='up_image', description='Detects sites that are available over http(s) in a list and takes an image of each one')
parser.add_argument('filename')

args = parser.parse_args()
print("Analyzing sites listed in", args.filename)

action_name = input('Name this operation: ').replace(" ", "_").replace("..","").replace("/","").lstrip("/")
Path(action_name+"/200").mkdir(parents=True, exist_ok=True)
Path(action_name+"/400").mkdir(parents=True, exist_ok=True)
Path(action_name+"/500").mkdir(parents=True, exist_ok=True)

domains_all = []
domains_200 = set()
domains_400 = set()
domains_500 = set()
domains_redirect = []

# Extract all domains from the file
with open(args.filename) as file:
    domains_all = [line.rstrip() for line in file]

# TODO: Add checks as needed for IP addresses and CIDr + ranges.

# Find all of the domains that resolve to 2xx, 3xx, or 4xx
for domain in domains_all:
    if domain != "":
        print("Checking domain", domain)
        http_domain = domain_to_http_url(domain)
        http_code = get_site_response_code(http_domain)
        if str(http_code).startswith('2'):
            domains_200.add(http_domain)
        elif str(http_code).startswith('3'):
            domains_redirect.append(http_domain)
        elif str(http_code).startswith('4'):
            domains_400.add(http_domain)
        elif str(http_code).startswith('5'):
            domains_500.add(http_domain)

        https_domain = domain_to_https_url(domain)
        https_code = get_site_response_code(https_domain)
        if str(https_code).startswith('2'):
            domains_200.add(https_domain)
        elif str(https_code).startswith('3'):
            domains_redirect.append(https_domain)
        elif str(https_code).startswith('4'):
            domains_400.add(https_domain)
        elif str(https_code).startswith('5'):
            domains_500.add(https_domain)

print(domains_all)

for domain in domains_redirect:
    print("Checking redirection of domain", domain)
    redirect = get_site_redirect(domain)
    if str(redirect["response_code"]).startswith('2'):
        domains_200.add(redirect["url"].rstrip('/'))
    if str(redirect["response_code"]).startswith('4'):
        domains_400.add(redirect["url"].rstrip('/'))
    if str(redirect["response_code"]).startswith('5'):
        domains_500.add(redirect["url"].rstrip('/'))

print("\nURLs to analyze")
print("  200:", domains_200)
print("  400:", domains_400)
print("  500:", domains_500)

print("\nAnalyzing URLs with 2xx response codes...")
take_pic.list(domains_200, action_name + "/200/")
print("Complete")
print("\nAnalyzing URLs with 4xx response codes...")
take_pic.list(domains_400, action_name + "/400/")
print("Complete")
print("\nAnalyzing URLs with 5xx response codes...")
take_pic.list(domains_500, action_name + "/500/")
print("Complete")