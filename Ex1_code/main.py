"""
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
"""
# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
from ways.tools import compute_distance,timed
from ways.graph import load_map_from_csv
from ways.algorithms import ucs,a_star,ida_star

roads = None

def huristic_function(lat1, lon1, lat2, lon2):
    return compute_distance(lat1, lon1, lat2, lon2)

def find_ucs_rout(source, target):
    "call function to find path, and return list of indices"
    return ucs(source, target, roads)


def find_astar_route(source, target):
    "call function to find path, and return list of indices"

    return a_star(source,target,roads,huristic_function)


def find_idastar_route(source, target):
    "call function to find path, and return list of indices"
    return ida_star(source,target,roads,huristic_function)


@timed
def dispatch(argv):
    global roads
    roads = load_map_from_csv()
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == "ucs":
        path = find_ucs_rout(source, target)
    elif argv[1] == "astar":
        path = find_astar_route(source, target)
    elif argv[1] == "idastar":
        path = find_idastar_route(source, target)
    if path != None:
        print(' '.join(str(j) for j in path.solution()))
    else:
        print("No path found!")

if __name__ == "__main__":
    from sys import argv

    dispatch(argv)
