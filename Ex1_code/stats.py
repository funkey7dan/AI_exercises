'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv

        
def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : len(roads),
        'Number of links' : sum(map(lambda x: len(x.links),roads.values())),
        'Outgoing branching factor' : Stat(max=avg(map(lambda x: len(x.links),roads.values())), min=None, avg=None),
        'Link distance' : Stat(max=None, min=None, avg=None),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : None,  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv(count=9999)).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

