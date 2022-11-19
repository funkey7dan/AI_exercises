""" Daniel Bronfman 315901173"""
'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple,Counter
from ways import load_map_from_csv

        
def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    links_map = list(map(lambda x: len(x.links),roads.values()))
    #for each junction, map the list of its link distances
    distance_map = list(map(lambda x: list(map(lambda y: y.distance,x.links)),roads.values()))
    distance_map = [item for list in distance_map for item in list]
    highway_types = (list(map(lambda x: list(map(lambda y: y.highway_type,x.links)),roads.values())))
    highway_types = [item for list in highway_types for item in list]
    return {
        'Number of junctions' : len(roads),
        'Number of links' : sum(links_map),
        'Outgoing branching factor' : Stat(max=max(links_map),
                                           min=min(links_map),
                                           avg=sum(links_map)/len(links_map)),
        'Link distance' : Stat(max=max(distance_map), min=min(distance_map), avg=sum(distance_map)/len(distance_map)),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : dict(Counter(highway_types).most_common()),
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

