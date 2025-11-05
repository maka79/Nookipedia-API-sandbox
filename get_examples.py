#! /usr/bin/env python

from NookipediaToObsidianBase import NookipediaToObsidianBase
import json
from os import path

skip_tests = False

def doRESTQuery(item_type, item_name='', outfile_dir=''):
    outfile_path = ''
    if item_name:
        url = ntob.genUrl(item_type, item_name)
        if outfile_dir:
            outfile_path = path.join(outfile_dir, f"{item_type}_{item_name}.example.log")
    else:
        url = ntob.genUrl(item_type, excludedetails=True)
        if outfile_dir:
            outfile_path = path.join(outfile_dir, f"{item_type}_names_only.log")
    with open(outfile_path, "w") as log_file:
        if not log_file:
            lof_file = sys.stdout
        print(url, file=log_file)
        resp_json = ntob.getJSONObject(url, throttle=True)
        print(f"{len(resp_json)} objects returned", file=log_file)
        print(json.dumps(resp_json, indent=4), file=log_file)

if __name__ == "__main__":
    item_types = [
        'villagers',
        'fish',
        'bugs',
        'sea',
        'clothing',
        'tools',
        'gyroids',
        'art',
        'furniture',
        'interior',
        'photos',
        'items',
        'recipes',
        'fossils',
        'fossil_groups',
        'fossil_all'
    ]

    ntob = NookipediaToObsidianBase(base_folder="/Users/Matt/Develop/Projects/Obsidian Plugin Dev/ACNH Database",
                                    api_key="86c16905-70aa-4c7e-9d33-43b698691779", throttle=0.5,
                                    globalPauseOnPrint=False)
    if not skip_tests:
        for item_type in item_types:
            doRESTQuery(item_type, outfile_dir="./logs")

        # Individual villager test
        doRESTQuery('villagers', 'Beardo', outfile_dir="./logs")

        # Individual fish test
        doRESTQuery('fish', 'arowana', outfile_dir="./logs")

        # Individual bugs test
        doRESTQuery('bugs', 'scorpion', outfile_dir="./logs")

        # Individual sea critters test
        doRESTQuery('sea', 'scallop', outfile_dir="./logs")

        # Individual clothing test
        doRESTQuery('clothing', 'visual-punk dress', outfile_dir="./logs")

        # Individual tools test
        doRESTQuery('tools', 'Slingshot', outfile_dir="./logs")

        # Individual gyroids test
        doRESTQuery('gyroids', 'Crumploid', outfile_dir="./logs")

        # Individual art test
        doRESTQuery('art', 'Wistful painting', outfile_dir="./logs")

        # Individual furniture test
        doRESTQuery('furniture', 'Castle tower', outfile_dir="./logs")

        # Individual interor test
        doRESTQuery('interior', 'Spooky flooring', outfile_dir="./logs")

        # Individual photos test
        doRESTQuery('photos', 'Muffy\'s photo', outfile_dir="./logs")

        # Individual items test
        doRESTQuery('items', 'Acorn', outfile_dir="./logs")

        # Individual recipes test
        doRESTQuery('recipes', 'Pull-apart bread', outfile_dir="./logs")

        # Individual fossil test
        doRESTQuery('fossils', 'Spino skull', outfile_dir="./logs")

        # Individual fossil group test
        doRESTQuery('fossil_groups', 'Spinosaurus', outfile_dir="./logs")

        # Individual fossil group and item test
        doRESTQuery('fossil_all', 'Spinosaurus', outfile_dir="./logs")

