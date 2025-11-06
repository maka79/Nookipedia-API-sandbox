#! /usr/bin/env python

from NookipediaToObsidianBase import NookipediaToObsidianBase
import json

skip_tests = True

def doRESTQuery(item_type, item_name=''):
    if item_name:
        url = ntob.genUrl(item_type, item_name)
    else:
        url = ntob.genUrl(item_type, excludedetails=True)
    print(url)
    resp_json = ntob.getJSONObject(url, throttle=True)
    print(f"{len(resp_json)} objects returned")
    print(json.dumps(resp_json, indent=4))


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
            doRESTQuery(item_type)

        # Individual villager test
        doRESTQuery('villagers', 'Beardo')

        # Individual fish test
        doRESTQuery('fish', 'arowana')

        # Individual bugs test
        doRESTQuery('bugs', 'scorpion')

        # Individual sea critters test
        doRESTQuery('sea', 'scallop')

        # Individual clothing test
        doRESTQuery('clothing', 'visual-punk dress')

        # Individual tools test
        doRESTQuery('tools', 'Slingshot')

        # Individual gyroids test
        doRESTQuery('gyroids', 'Crumploid')

        # Individual art test
        doRESTQuery('art', 'Wistful painting')

        # Individual furniture test
        doRESTQuery('furniture', 'Castle tower')

        # Individual interor test
        doRESTQuery('interior', 'Spooky flooring')

        # Individual photos test
        doRESTQuery('photos', 'Muffy\'s photo')

        # Individual items test
        doRESTQuery('items', 'Acorn')

        # Individual recipes test
        doRESTQuery('recipes', 'Pull-apart bread')

        # Individual fossil test
        doRESTQuery('fossils', 'Spino skull')

        # Individual fossil group test
        doRESTQuery('fossil_groups', 'Spinosaurus')

        # Individual fossil group and item test
        doRESTQuery('fossil_all', 'Spinosaurus')

    # Do a get items by type on Photos -- should work like clothing, gyroids and tools
    ntob.getItemsByType('photos')

    # Do a get items by type on miscellaneous items -- should work like clothing, gyroids and tools
    #ntob.getItemsByType('items')

    # TO DO: add a main function with argparse for command line arguments:
    #   - Switch for base folder
    #   - Switch for item type to pull
    #   - Switch for individual item by name
    #   - Switch for debug prints
    #   - Switch for api key

    # TO DO: Look into python unit test frameworks

