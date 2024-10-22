import requests
import json

# URLs to fetch data from
# urls = [
#     "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2021/JSON/if_2021.js",
#     "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2022/JSON/if_2022.js",
#     "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2023/JSON/if_2023.js",
#     "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2024/JSON/if_2024.js"
# ]
urls_rc = [
    "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2024/JSON/if_2024.js"
]

class ResourceEprint:

    def __init__(self, link_urls):
        self.urls = link_urls
        self.all_data = []

    def fetch(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # check for errors in response
            data = response.text
            json_data = json.loads(data)
            return json_data
        except Exception as e:
            print(f"Error fetching data from {self.urls}: {e}")
            return None

    def process(self):
        items=[]
        for url in self.urls:
            data = self.fetch(url)
            if data:
                self.all_data.append(data)

        # Process the combined data (example: print the titles of each entry)
        for year_data in self.all_data:
            for entry in year_data:
                parsed_data = self.parse_json(entry)
                # items.append(str(parsed_data['title']).lower())
                items.append({
                    'title': str(parsed_data['title']).lower(),  # Ensure title is a string before applying lower()
                    'date': parsed_data['date'],  # Assuming date is in correct format
                    'author': str(parsed_data['creator']).lower(),  # Ensure author is a string before applying lower()
                    'nim': parsed_data['nim'],
                    'supervisor': ', '.join([str(name).lower() for name in parsed_data['contributors_name']])
                    # Ensure contributors' names are strings
                })
                # print(f"Title: {parsed_data['title']}")
                # print(f"Date: {parsed_data['date']}")
                # print(f"Creator: {parsed_data['creator']}")
                # print(f"Nim: {parsed_data['nim']}")
                # print(f"Supervision: {', '.join(parsed_data['contributors_name'])}")
        return items

    def parse_json(self,data):
        title = data.get("title", "No title available")
        date = data.get("date", "No date available")

        creators = data.get("creators", [])
        creator = creators[0]
        student_name = creator.get("name", {})
        student_full_name = f"{student_name.get('given', '')} {student_name.get('family', '')}".strip()
        nim = creator.get("nim", "No NIM available")

        # Extracting contributor names
        contributors = data.get("contributors", [])
        contributor_names = []
        for contributor in contributors:
            name = contributor.get("name", {})
            full_name = f"{name.get('given', '')} {name.get('family', '')}".strip()
            contributor_names.append(full_name)

        return {
            "title": title.replace("\r\n", " "),  # Cleaning up the title formatting
            "date": date,
            "contributors_name": contributor_names,
            "creator":student_full_name,
            "nim":nim
        }


