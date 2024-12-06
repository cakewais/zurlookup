import time
import requests
import csv
import json

def obfuscate_api_key(seed):
    """
    Obfuscates the API key based on the provided algorithm.
    """
    now = int(time.time() * 1000)  # Current timestamp in milliseconds
    n = str(now)[-6:]             # Last 6 digits of the timestamp
    r = str(int(n) >> 1).zfill(6) # Right-shifted value of n, padded to 6 digits
    key = ""

    # Build the first part of the key using n
    for i in range(len(n)):
        key += seed[int(n[i])]

    # Build the second part of the key using r
    for j in range(len(r)):
        key += seed[int(r[j]) + 2]

    return key, now


def authenticate_and_store_cookie(base_url, endpoint, username, password, seed):
    """
    Authenticates to the API and stores the JSESSIONID for future use.
    """
    obfuscated_key, timestamp = obfuscate_api_key(seed)
    url = f"{base_url}/{endpoint}"
    body = {
        "username": username,
        "password": password,
        "apiKey": obfuscated_key,
        "timestamp": timestamp
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        cookies = response.cookies.get_dict()
        return cookies.get("JSESSIONID")
    else:
        raise Exception(f"Authentication failed: {response.text}")


def logout(base_url, endpoint, jsessionid):
    """
    Logs out by sending a DELETE request to the authentication endpoint.
    """
    headers = {"Cookie": f"JSESSIONID={jsessionid}"}
    url = f"{base_url}/{endpoint}"

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Successfully logged out.")
        else:
            print(f"Logout failed. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred during logout: {e}")


def split_list(input_list, chunk_size):
    """
    Splits a list into chunks of a given size.
    """
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]


def lookup_urls(base_url, endpoint, jsessionid, url_list):
    """
    Sends batches of URLs to the `urlLookup` endpoint and collects responses.
    """
    headers = {"Cookie": f"JSESSIONID={jsessionid}", 'Content-Type': 'application/json', 'Accept':'application/json'}
    url = f"{base_url}/{endpoint}"
    results = []

    for chunk in split_list(url_list, 100):  # Process 100 URLs at a time
        response = requests.post(url, data=json.dumps(chunk), headers=headers)  # Send chunk directly as data
        if response.status_code == 200:
            results.extend(response.json())
            time.sleep(2)
        else:
            print(f"Request failed for chunk: {chunk}")
            print(f"Status code: {response.status_code}, Response: {response.text}")

    return results


def save_to_csv(results, output_file):
    """
    Saves the URL and classifications (including security alerts) to a CSV file.
    """
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "URL Classifications", "URL Classifications with Security Alert"])  # Header row

        for result in results:
            url = result.get("url", "")
            classifications = ", ".join(result.get("urlClassifications", []))
            security_alerts = ", ".join(result.get("urlClassificationsWithSecurityAlert", []))
            writer.writerow([url, classifications, security_alerts])

def read_urls_from_csv(csv_file):
    """
    Reads URLs from a CSV file and returns them as a list.
    """
    url_list = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row (if any)
        for row in reader:
            url_list.append(row[0])  # Assuming URLs are in the first column
    return url_list

# Example usage
if __name__ == "__main__":
    base_url = "YOUR_BASE_URL example:https://zsapi.zscalerthree.net/api/v1"
    auth_endpoint = "authenticatedSession"
    lookup_endpoint = "urlLookup"
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    your_api_key = "YOUR_API_KEY"
    input_csv_file = "YOUR_SOURCE_CSV.csv"
    output_file = "YOUR_DESTINATION_CSV.csv"

    try:
        # Read URLs from CSV
        url_list = read_urls_from_csv(input_csv_file) 
        print(f"Read {len(url_list)} URLs from {input_csv_file}")

        # Authenticate and get JSESSIONID
        jsessionid = authenticate_and_store_cookie(base_url, auth_endpoint, username, password, your_api_key)
        print("Authenticated successfully. JSESSIONID:", jsessionid)

        # Lookup URLs and get results
        results = lookup_urls(base_url, lookup_endpoint, jsessionid, url_list)
        print(f"Retrieved classifications for {len(results)} URLs.")

        # # Save results to CSV
        save_to_csv(results, output_file)
        print(f"Results saved to {output_file}.")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Ensure logout happens regardless of success or failure
        if 'jsessionid' in locals() and jsessionid:
            logout(base_url, auth_endpoint, jsessionid)
