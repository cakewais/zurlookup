# Zurlookup

Zurlookup is a Python tool designed to automate the process of looking up URL classifications in Zscaler using their API. It's particularly useful for bulk lookups, saving you time and effort compared to manual checks.

**Key Features:**

* **Bulk URL Lookups:** Process large lists of URLs efficiently by sending requests in batches to the Zscaler API.
* **Authentication Handling:** Securely authenticates to the Zscaler API using your credentials and the required obfuscation algorithm.
* **CSV Support:** Reads URLs from a CSV file and outputs the results, including classifications and security alerts, to another CSV file for easy analysis.
* **Logout Functionality:** Ensures proper logout from the API after the process is completed.
* **Reference URL Generator:** Includes a separate script (`url_gen.py`) to quickly generate a CSV file with test URLs.

**Requirements:**

* Python 3.6 or higher
* `requests` library

**How to Use:**

1. **Install the `requests` library:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update `url_lookup.py`:**
   * Replace placeholders for `base_url`, `auth_endpoint`, `lookup_endpoint`, `username`, `password`, `your_api_key`, `input_csv_file`, and `output_file` with your actual Zscaler API details and file paths.

3. **Prepare your URL list:**
   * Create a CSV file containing the URLs you want to look up. Each URL should be on a separate line. You can use the provided `url_gen.py` script to generate a test CSV.

4. **Run the script:**
   ```bash
   python url_lookup.py
   ```

**How it Works:**

* **Authentication:** The script first authenticates to the Zscaler API using your provided credentials. It handles the API key obfuscation as required by Zscaler.
* **URL Lookup:** It reads URLs from your input CSV file and sends them to the Zscaler API's `urlLookup` endpoint in batches.
* **Result Processing:** The script retrieves the classification information and any associated security alerts for each URL.
* **Output:** Finally, it saves the results in a new CSV file, making it easy to review and analyze the classifications.

**Important Notes:**

* The provided code is designed to work with the Zscaler API. Ensure you have the necessary API access and credentials.
* The `url_gen.py` script is for generating test URLs. Modify or replace it as needed for your specific URL generation requirements.
* Remember to update the placeholders in `url_lookup.py` with your actual Zscaler API details and file paths.
