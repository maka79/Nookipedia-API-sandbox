#!/usr/bin/env python

import requests
import json
import os
import time
from requests.exceptions import JSONDecodeError, RequestException

# base_folder = "/Users/Matt/Develop/Projects/Obsidian Plugin Dev/ACNH Database"
# api_url = "https://api.nookipedia.com/nh/"
# query_string = "clothing?excludedetails=true"
# headers = {"X-API-KEY":"86c16905-70aa-4c7e-9d33-43b698691779", "Accept-Version":"1.0.0"}


class NookipediaToObsidianBase:
    def printWithPause(self, string, doPause=False):
        if doPause or self.globalPauseOnPrint:
            input(string + " [ENTER]")
        else:
            print(string)

    def __init__(self, base_folder, api_key, no_clobber = True, api_url = "https://api.nookipedia.com", item_types = ['clothing', 'tools', 'gyroids'], throttle=0.1, retry_delay=5, globalPauseOnPrint=False):
        print("Creating object...")
        self.no_clobber = no_clobber
        self.base_folder = base_folder
        self.api_url = api_url
        self.item_types = item_types
        self.api_key = api_key
        self.headers = {"X-API-KEY":self.api_key, "Accept-Version":"1.0.0"}
        self.throttle = throttle
        self.retry_delay = retry_delay
        self.globalPauseOnPrint = globalPauseOnPrint


    def genUrl(self, item_type, item_name='', excludedetails=False):
        query_string = ""
        resource_path = ""
        if excludedetails:
            query_string = "?excludedetails=true"
        match item_type:
            case 'villagers':
                if item_name:
                    resource_path = "/".join([self.api_url, 'villagers'])
                    if query_string:
                        query_string += f"&name={item_name}&game=nh"
                    else:
                        query_string = f"?name={item_name}&game=nh"
                else:
                    resource_path = "/".join([self.api_url, 'villagers'])
            case 'fish' | 'bugs' | 'sea' | 'art' | 'furniture' | 'clothing' | 'interior' |'tools' | 'photos' | 'items' | 'recipes' | 'gyroids':
                if item_name:
                    resource_path = "/".join([self.api_url, 'nh', item_type, item_name])
                else:
                    resource_path = "/".join([self.api_url, 'nh', item_type])
            case 'fossils':
                if item_name:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'individuals', item_name])
                else:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'individuals'])
            case 'fossil_groups':
                if item_name:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'groups', item_name])
                else:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'groups'])
            case 'fossil_all':
                if item_name:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'all', item_name])
                else:
                    resource_path = "/".join([self.api_url, 'nh', 'fossils', 'all'])
        self.printWithPause(f"Resource path: {resource_path}")
        self.printWithPause(f"Query string:  {query_string}")
        return(f"{resource_path}{query_string}")
                      

    def getJSONObject(self, request_url, throttle=False):
        try:
            if throttle:
                time.sleep(self.throttle)
            response = requests.get(request_url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            resp_json = response.json()
        except JSONDecodeError as e:
            print(f"JSONDecodeError: Failed to decode JSON response. Error: {e}")
            self.printWithPause(f"Response content: {response.text}") # Print the raw response content for debugging
            return {}
        except RequestException as e:
            self.printWithPause(f"RequestException: An error occurred during the request. Error: {e}")
            return {}
        except Exception as e:
            self.printWithPause(f"An unexpected error occurred: {e}")
            return {}

        if response.status_code == 200:
            return resp_json        


    def getAllItems(self):
        for item_type in self.item_types:
            self.printWithPause(f"Getting {item_type} from Nookipedia REST API...")
            self.getItemsByType(item_type)


    def getItemsByType(self, item_type):
        request_url = self.genUrl(item_type, excludedetails=True)
        self.printWithPause(f"Request URL for {item_type}: {request_url}")

        resp_json = {}
        while not (resp_json := self.getJSONObject(request_url)):
            if self.retry_delay:
                time.sleep(self.retry_delay)

        for item in resp_json:
            item_name = item
            self.printWithPause(f"{item_type} item: {item}")
            file_name = os.path.join(self.base_folder, item_type, item + ".md")

            if self.no_clobber and os.path.exists(file_name):
                self.printWithPause("File exists, skipping...")
                continue

            succeeded = False
            resp_json = {}
            request_url = self.genUrl(item_type, item)
            while not (resp_json := self.getJSONObject(request_url)):
                if self.retry_delay:
                    time.sleep(self.retry_delay)

            self.printWithPause(f"Fetching data from {request_url} for item {resp_json['name']}")

            # TODO: Make a class to parse the JSON results and convert them to markdown and YAML.
            # Many of the items in the DB will work similarly to clothing where the variants have the 
            # image_url fields, but others do not have variations and will need to be handled differently
            # Art has two image urls for fake and non-fake

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

            self.printWithPause(f"Creating markdown file: {file_name}")
            try:
                file_object = open(file_name, "w")
            except FileNotFoundError:
                self.printWithPause("Could not create file -- attempting to create missing directories")
                dir_path = os.path.dirname(file_name)
                os.makedirs(dir_path, exist_ok=True)
                try: 
                    file_object = open(file_name, "w")
                except Exception as e:
                    self.printWithPause(f"Unknown error creating new file: {e}")
                    continue

            # Generate YAML frontmatter for primary .md file, then handle variations if present
            file_object.write("---\n")

            name = item_name
            url = ''
            category = ''
            variation_total = 0
            image_url = ''

            # TO-DO - look for other common and/or useful fields across different objects to
            #         extract and convert to properties

            # name and url *should* always be present, but just in case something is funky...
            # Hmmm, looks like name *isn't always present -- at least not in the top level object for photos
            # Using the item_name saved from the initial list of items saves us here
            if 'name' in resp_json:
                self.printWithPause("name field in response is clobbering...")
                name = resp_json['name']
                self.printWithPause(f"name: {name}")
                file_object.write(f"name: {name}\n")
            if 'url' in resp_json:
                url = resp_json['url']
                self.printWithPause(f"url: {url}")
                file_object.write(f"url: {url}\n")
            if 'category' in resp_json:
                category = resp_json['category']
                self.printWithPause(f"Category: {category}")
                file_object.write(f"category: {category}\n")
            if 'variation_total' in resp_json:
                variation_total = resp_json['variation_total']
                self.printWithPause(f"variation_total: {variation_total}")
                file_object.write(f"variation_total: {variation_total}\n")
            if 'colors' in resp_json:
                file_object.write("colors:\n")
                self.printWithPause(f"colors:")
                for color in resp_json['colors']:
                    self.printWithPause(f"  - {color}")
                    file_object.write(f"  - {color}\n")

            self.printWithPause(f"Outside if/else - name property is {name}, item property is {item_name}")

            if not 'variations' in resp_json:
                # some items don't have variations and have their image_url in the main object
                if 'image_url' in resp_json:
                    image_url = resp_json['image_url']
                    file_object.write(f"image_url: {'image_url'}\n")
            else:
                self.printWithPause(f"Inside else case - name property is {name}, item property is {item_name}")
                variation_table_header = "<table>\n  <tr>\n"
                variation_table_embeds = ""
                variation_table_labels = ""
                variation_table_footer = "  </tr>\n</table>\n"
                file_object.write("variations:\n")
                for item in resp_json['variations']:
                    file_object.write(f"  - \"[[{name}_{item['variation']}|{item['variation']}]]\"\n")
                    var_file_name = os.path.join(self.base_folder, item_type, name + "_" + item['variation'] + ".md")
                    self.printWithPause(f"Creating markdown file: {var_file_name}")
                    variation_file = open(var_file_name, "w")
                    variation_file.write("---\n")
                    variation_file.write(f"name: {name}\n")
                    # add an explict back link to the "parent" item
                    variation_file.write(f"parent: \"[[{item_type}/{name}|{name}]]\"\n")
                    if category:
                        variation_file.write(f"category: {category}\n")
                    if url:
                        variation_file.write(f"url: {url}\n")
                    if 'variation' in item: 
                        variation_file.write(f"variation: {item['variation']}\n")
                    if 'image_url' in item:
                        variation_file.write(f"image_url: {item['image_url']}\n")
                    variation_table_embeds += f"<td> <img src='{item['image_url']}' alt='{item['variation']}' width='100' height='100'> </td>\n"
                    variation_table_labels += f"<td> {item['variation']} </td>\n"
                    if 'colors' in item:
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

if __name__ == "__main__":
    self.printWithPause("Running script")
    ntob = NookipediaToObsidianBase(base_folder = "/Users/Matt/Develop/Projects/Obsidian Plugin Dev/ACNH Database", api_key="86c16905-70aa-4c7e-9d33-43b698691779")
    ntob.getAllItems()

