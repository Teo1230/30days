import csv
import requests

# list of common furniture keywords
furniture_keywords=['sofa', 'armchair', 'recliner', 'loveseat', 'sectional', 'ottoman', 'chaise', 'rocker', 'stool', 'bench', 'table', 'desk', 'bookcase', 'cabinet', 'dresser', 'wardrobe', 'bed', 'mirror', 'shelf', 'hutch']

furniture_counts = {}

with open('furniture stores pages.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        url = row[0]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                product_text = url.split('products/', 1)[-1].lower()

                if any(keyword in product_text for keyword in furniture_keywords):
                    furniture_name = next(keyword for keyword in furniture_keywords if keyword in product_text)
                    if furniture_name in furniture_counts:
                        furniture_counts[furniture_name]['count'] += 1
                        furniture_counts[furniture_name]['links'].append(url)
                    else:
                        furniture_counts[furniture_name] = {'count': 1, 'links': [url]}

        except requests.exceptions.RequestException as e:
            print(f"Error processing link: {url}. {str(e)}")

# sort the furniture counts in ascending order by count
sorted_furniture_counts = {k: v for k, v in sorted(furniture_counts.items(), key=lambda item: item[1]['count'])}

# print the furniture counts
for furniture_name, count_info in sorted_furniture_counts.items():
    print(f"{furniture_name}: {count_info['count']} ({', '.join(count_info['links'])})")
