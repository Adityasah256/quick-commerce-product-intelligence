import requests
import json

url = "https://blinkit.com/v1/layout/search"

params = {
    "offset": 0,
    "limit": 12,
    "actual_query": "milk",
    "q": "milk",
    "search_method": "basic",
    "search_type": "type_to_search",
    "page_index": 1
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    params=params,
    headers=headers
)

print(response.status_code)
print(response.text[:500])