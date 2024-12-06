import csv

def generate_test_urls_csv(filename, num_urls):
    """
    Generates a CSV file with test URLs in the format test0.com, test1.com, etc.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(num_urls):
            url = f"test{i}.com"
            writer.writerow([url])

if __name__ == "__main__":
    filename = "test_urls.csv"  # Name of the CSV file to create
    num_urls = 1024  # Number of test URLs to generate
    generate_test_urls_csv(filename, num_urls)
    print(f"Generated {num_urls} test URLs in {filename}")