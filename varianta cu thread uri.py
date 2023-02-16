import csv
import requests
import re
from concurrent.futures import ThreadPoolExecutor, wait
import os

# compile regular expression to match furniture keywords
furniture_regex = re.compile(
    r'\b(?:sofa|armchair|recliner|loveseat|sectional|ottoman|chaise|rocker|stool|bench|table|desk|bookcase|cabinet|dresser|wardrobe|bed|mirror|shelf|hutch)\b',
    re.IGNORECASE)
num_cpus = os.cpu_count()

# set the maximum number of workers to use with ThreadPoolExecutor
max_workers = num_cpus * 2  # you can adjust this multiplier to see what works best for your use case

# define function to process each URL
def process_url(url):
    try:
        # send HTTP GET request to URL
        response = requests.get(url)
        if response.status_code == 200:
            # extract product name from URL using regular expressions
            product_name_match = re.search(r'/products/([a-z0-9-]+)', url)
            if product_name_match:
                product_name = product_name_match.group(1)

                # search for furniture keywords in product name
                match = furniture_regex.search(product_name)
                if match:
                    # if furniture keyword found, return the furniture name and URL
                    furniture_name = match.group(0)
                    return (furniture_name, url)
    except requests.exceptions.RequestException as e:
        # if there is an error with the request, print the error message
        print(f"Error processing link: {url}. {str(e)}")

    # if no furniture keyword found or there was an error, return None
    return None
if __name__ == '__main__':
    # initialize dictionary to keep track of furniture counts and URLs
    furniture_counts = {}

    # read URLs from CSV file and sort them alphabetically
    with open('furniture stores pages.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        urls = sorted([row[0] for row in reader])

    # use ThreadPoolExecutor to process URLs in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        # wait for all tasks to complete
        wait(futures)
        for future in futures:
            result = future.result()
            if result is not None:
                # if furniture name is already in the dictionary, update count and add URL
                furniture_name, url = result
                if furniture_name in furniture_counts:
                    furniture_counts[furniture_name]['count'] += 1
                    furniture_counts[furniture_name]['links'].append(url)
                else:
                    # if furniture name is not in the dictionary, add it and set count to 1
                    furniture_counts[furniture_name] = {'count': 1, 'links': [url]}

    # sort the furniture counts in ascending order by count
    sorted_furniture_counts = {k: v for k, v in sorted(furniture_counts.items(), key=lambda item: item[1]['count'])}

    # print the furniture counts
    for furniture_name, count_info in sorted_furniture_counts.items():
        print(f"{furniture_name}: {count_info['count']} ({', '.join(count_info['links'])})")