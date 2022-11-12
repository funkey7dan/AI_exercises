"""
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
"""

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
from ways.tools import compute_distance
from ways.graph import load_map_from_csv
from ways.ucs import ucs


def huristic_function(lat1, lon1, lat2, lon2):
    raise NotImplementedError


def find_ucs_rout(source, target):
    "call function to find path, and return list of indices"
    roads = load_map_from_csv(count=1500)
    # print(roads[source])
    # print(roads[target])
    # lat1, lon1, lat2, lon2
    # print(compute_distance(roads[source].lat,roads[source].lon,
    #                        roads[target].lat,roads[target].lon))
    return ucs(source, target, roads)
    # raise NotImplementedError


def find_astar_route(source, target):
    "call function to find path, and return list of indices"
    raise NotImplementedError


def find_idastar_route(source, target):
    "call function to find path, and return list of indices"
    raise NotImplementedError


def dispatch(argv):
    from sys import argv

    source, target = int(argv[2]), int(argv[3])
    if argv[1] == "ucs":
        path = find_ucs_rout(source, target)
    elif argv[1] == "astar":
        path = find_astar_route(source, target)
    elif argv[1] == "idastar":
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path.solution()))


if __name__ == "__main__":
    from sys import argv

    dispatch(argv)
