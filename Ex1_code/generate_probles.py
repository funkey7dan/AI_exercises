TO_GENERATE = 100
from ways import load_map_from_csv
import random


def check_if_connected(j1,j2):
    return (j2.index in j1.links)

def generate():
    f = open("problems.csv","w+")
    problems = []
    roads = load_map_from_csv(count=100)
    for _ in range(0,TO_GENERATE+1):
        j1 = random.randint(0,len(roads)-1)
        j2 = roads.return_focus(j1)
        problems.append((j1,j2))
    pass

if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    generate()