#!/usr/bin/env python

import requests
import json
import os
from requests.exceptions import JSONDecodeError, RequestException

no_clobber = True

base_folder = "/Users/Matt/Develop/Projects/Obsidian Plugin Dev/ACNH Database/Clothing"
api_url = "https://api.nookipedia.com/nh/"
#query_string = "clothing?category=Socks&excludedetails=true"
query_string = "clothing?excludedetails=true"
headers = {"X-API-KEY":"86c16905-70aa-4c7e-9d33-43b698691779", "Accept-Version":"1.0.0"}

try:
    response = requests.get(api_url + query_string, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    resp_json = response.json()
except JSONDecodeError as e:
    print(f"JSONDecodeError: Failed to decode JSON response. Error: {e}")
    print(f"Response content: {response.text}") # Print the raw response content for debugging
    quit()
except RequestException as e:
    print(f"RequestException: An error occurred during the request. Error: {e}")
    quit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    quit()

for item in resp_json:
    print(f"Clothing item: {item}")
    file_name = os.path.join(base_folder, item + ".md")

    if no_clobber and os.path.exists(file_name):
        print("File exists, skipping...")
        continue

    try:
        response = requests.get(api_url + "clothing/" + item, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        resp_json = response.json()
    except JSONDecodeError as e:
        print(f"JSONDecodeError: Failed to decode JSON response. Error: {e}")
        print(f"Response content: {response.text}") # Print the raw response content for debugging
        # throttle and try again?
    except RequestException as e:
        print(f"RequestException: An error occurred during the request. Error: {e}")
        # throttle and try again?
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # throttle and try again?


    # To Do: Error handling here
    resp_json = response.json()
    #print(json.dumps(response.json(), indent=4))
    
    print(f"Fetching data from {response.url} for item {resp_json['name']}")

    # Make a new .md file for use in Obsidian using frontmatter to generate properties
    #
    # Name of file and title immediately after frontmatter should match the name of the item
    #
    # Basic format for frontmatter:
    #
    # ---
    # name: {name}
    # url: {url}
    # category: {category}
    # variation_total: {variation_total}
    # variations:
    #   - {variation1}
    # ---

    name = resp_json['name']
    url = resp_json['url']
    category = resp_json['category']
    variation_total = resp_json['variation_total']

    print(f"Creating markdown file: {file_name}")
    file_object = open(file_name, "w")
    file_object.write("---\n")
    file_object.write(f"name: {name}\nurl: {url}\ncategory: {category}\nvariation_total: {variation_total}\nvariations:\n")
    variation_table_header = "<table>\n  <tr>\n"
    variation_table_embeds = ""
    variation_table_labels = ""
    variation_table_footer = "  </tr>\n</table>\n"
    for item in resp_json['variations']:
        file_object.write(f"  - \"[[{name}_{item['variation']}|{item['variation']}]]\"\n")
        var_file_name = os.path.join(base_folder, name + "_" + item['variation'] + ".md")
        print(f"Creating markdown file: {var_file_name}")
        variation_file = open(var_file_name, "w")
        variation_file.write("---\n")
        variation_file.write(f"name: {name}\ncategory: {category}\nurl: {url}\nvariation: {item['variation']}\nimage_url: {item['image_url']}\n")
        variation_table_embeds += f"<td> <img src='{item['image_url']}' alt='{item['variation']}' width='100' height='100'> </td>\n"
        variation_table_labels += f"<td> {item['variation']} </td>\n"
        if item['colors']:
            variation_file.write("colors:\n")
            for color in item['colors']:
                variation_file.write(f"  - {color}\n")
        variation_file.write("owned: false\n")
        variation_file.write("---\n")
        variation_file.close()
    file_object.write("---\n")
    file_object.write("# Variations\n")
    file_object.write(variation_table_header)
    file_object.write(variation_table_embeds + "  </tr>\n  <tr>\n")
    file_object.write(variation_table_labels)
    file_object.write(variation_table_footer)
    file_object.close()

