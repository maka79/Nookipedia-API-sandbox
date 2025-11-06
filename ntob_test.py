#! /usr/bin/env python

from NookipediaToObsidianBase import NookipediaToObsidianBase
import json
import argparse

skip_tests = True

def doRESTQuery(ntob, item_type, item_name=''):
    if item_name:
        url = ntob.genUrl(item_type, item_name)
    else:
        url = ntob.genUrl(item_type, excludedetails=True)
    print(url)
    resp_json = ntob.getJSONObject(url, throttle=True)
    print(f"{len(resp_json)} objects returned")
    print(json.dumps(resp_json, indent=4))


def main(base_path="/Users/Matt/Develop/Projects/Obsidian Plugin Dev/ACNH Database"):
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

    ntob = NookipediaToObsidianBase(base_folder=base_path,
                                    api_key="86c16905-70aa-4c7e-9d33-43b698691779", throttle=0.5,
                                    globalPauseOnPrint=False)
    if not skip_tests:
        for item_type in item_types:
            doRESTQuery(ntob, item_type)

        # Individual villager test
        doRESTQuery(ntob, 'villagers', 'Beardo')

        # Individual fish test
        doRESTQuery(ntob, 'fish', 'arowana')

        # Individual bugs test
        doRESTQuery(ntob, 'bugs', 'scorpion')

        # Individual sea critters test
        doRESTQuery(ntob, 'sea', 'scallop')

        # Individual clothing test
        doRESTQuery(ntob, 'clothing', 'visual-punk dress')

        # Individual tools test
        doRESTQuery(ntob, 'tools', 'Slingshot')

        # Individual gyroids test
        doRESTQuery(ntob, 'gyroids', 'Crumploid')

        # Individual art test
        doRESTQuery(ntob, 'art', 'Wistful painting')

        # Individual furniture test
        doRESTQuery(ntob, 'furniture', 'Castle tower')

        # Individual interor test
        doRESTQuery(ntob, 'interior', 'Spooky flooring')

        # Individual photos test
        doRESTQuery(ntob, 'photos', 'Muffy\'s photo')

        # Individual items test
        doRESTQuery(ntob, 'items', 'Acorn')

        # Individual recipes test
        doRESTQuery(ntob, 'recipes', 'Pull-apart bread')

        # Individual fossil test
        doRESTQuery(ntob, 'fossils', 'Spino skull')

        # Individual fossil group test
        doRESTQuery(ntob, 'fossil_groups', 'Spinosaurus')

        # Individual fossil group and item test
        doRESTQuery(ntob, 'fossil_all', 'Spinosaurus')

    # Do a get items by type on Photos -- should work like clothing, gyroids and tools
    ntob.getItemsByType(ntob, 'photos')

    # Do a get items by type on miscellaneous items -- should work like clothing, gyroids and tools
    #ntob.getItemsByType('items')

    # TO DO: add a main function with argparse for command line arguments:
    #   - Switch for base folder
    #   - Switch for item type to pull
    #   - Switch for individual item by name
    #   - Switch for debug prints
    #   - Switch for api key

    # TO DO: Look into python unit test frameworks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs queries using the Nookipedia REST API")
    parser.add_argument("-b", "--base_path", type=str, help="Path to a folder inside an Obsidian vault to store the generated" \
        "markdown files", default="")
    args = parser.parse_args()
    main(args.base_path)