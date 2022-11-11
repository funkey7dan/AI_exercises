TO_GENERATE = 100
from ways import load_map_from_csv
import random
import csv


def check_if_connected(j1,j2):
    return (j2.index in j1.links)

def generate():
    #f = open("problems.csv","w")
    with open("problems.csv",'w',newline='') as f:
        writer = csv.writer(f)
        problems = []
        roads = load_map_from_csv(count=10000)
        for _ in range(0,TO_GENERATE):
            j1 = random.randint(0,len(roads)-1)
            while len(roads[j1].links) == 0:
                j1 = random.randint(0,len(roads)-1)
            closure = roads.return_focus(j1,max_depth=20)
            closure_flat = list(set(map(lambda x: x.target,closure)))
            #closure_flat = set(map(lambda x: x.target,closure))
            j2 = random.randint(0,len(roads)-1)
            while j2 not in closure_flat:
                j2 = closure_flat[random.randint(0,len(closure_flat)-1)]
            problems.append((j1,j2))
        writer.writerows(problems)
        f.close()
        pass

if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    generate()