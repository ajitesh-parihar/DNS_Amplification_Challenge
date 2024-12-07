from urllib.request import Request, urlopen
from random import choice, randint
from time import sleep
import random

challenge_host = "http://64.23.208.78"
file_path = 'commoncrawl.txt'

record_types = [
    6,   # SOA
    2,   # NS
    15,  # MX
    16,  # TXT
    33,  # SRV
    35,  # NAPTR
    46,  # RRSIG
]

dns_resolver_ips = [
    "8.8.8.8", 
    "1.1.1.1",    # Cloudflare
    "9.9.9.9",    # Quad9
    "208.67.222.222",  # OpenDNS
    "64.6.64.6",  # Verisign
    "84.200.69.80",  # DNS.WATCH
    "8.26.56.26",  # Comodo Secure DNS
    "77.88.8.8",  # Yandex.DNS
    "156.154.70.1",  # Neustar DNS
    "198.101.242.72",  # Alternate DNS
    "176.103.130.130", # AdGuard DNS
    "114.114.114.114",  # 114DNS
    "180.76.76.76",     # Baidu DNS
    "119.29.29.29",     # DNSPod
    "101.226.4.6",      # ChinaNetCenter
    "140.207.198.6",    # Tencent DNS
    "1.2.4.8",          # CNNIC
    "4.2.2.4",

]

agents = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 OPR/114.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.65',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
]

# Extract the domain from the line and then reverse it (tld after second-level domain)
def process_line(line):
    parts = line.split()
    if len(parts) >= 2:
        domain_parts = parts[1].split('.')
        domain = '.'.join(reversed(domain_parts))
        return domain

# Create a request object with headers
def create_request(url):
    headers = {
        'User-Agent': choice(agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    req = Request(url, headers=headers)
    return req

# Generic fetch function to make a request to the api
def fetch(url):
    try:
        res = urlopen(create_request(url), timeout=15)
        if res.getcode() == 200:
            html = res.read()
            return html
        else:
            return None
    except:
        return None

# Call the api with the domain, resolver and record type
def call_api(domain, resolver, record_type):
    api_url = f"{challenge_host}/api_query?resolver={resolver}&port=53&domain={domain}&qtype={record_type}&studentno=300352269"
    response = fetch(api_url)
    return response

def submit_request(domain):
    resolver = choice(dns_resolver_ips)
    # check if the domain is active and has an A record, else no point checking other record types
    initial_response = call_api(domain, "1.1.1.1", 1)
    if not initial_response:
        print(f"Didnt find A record for {domain}")
        return
    for record_type in record_types:
        try:
            sleep(1)
            response = call_api(domain, resolver, record_type)
            if response: # colorful output to make my serial console look cool
                print(f"\033[{randint(31,37)}mSuccesful for URL: {domain} with resolver: {resolver} and record type: {record_type}\033[0m")
            else:
                print(f"\033[{randint(31,37)}mNo response for URL: {domain} with resolver: {resolver} and record type: {record_type}\033[0m")
        except Exception as e:
            print(f"Error occurred for URL: {domain} with resolver: {resolver} and record type: {record_type} - {e}")


def main():
    # host vertices data from the latest crawl by commoncrawl
    

    with open(file_path, 'r') as file:
        lines = file.readlines()

    while True:
        # pick a random line from the file and process it
        random_line = random.sample(lines, 1)[0]
        domain = process_line(random_line)
        if domain:
            submit_request(domain)

if __name__ == '__main__':
    main()

