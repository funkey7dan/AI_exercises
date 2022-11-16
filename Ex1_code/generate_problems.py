from Ex1_code.ways.info import SPEED_RANGES
from ways.graph import load_map_from_csv
from main import ucs

import random
import csv

TO_GENERATE = 100
SOLUTIONS_TO_RUN = 10
roads = load_map_from_csv(count = 1000)


def generate_solutions():
    with open("./results/UCSRuns.txt","w") as out:
        with open("problems.csv","r",newline = "") as f:
            reader = csv.reader(f)
            problems = list(reader)
            seen_list = []
            for _ in range(0,SOLUTIONS_TO_RUN):
                r = random.randint(0,len(problems) - 1)
                while r in seen_list:
                    r = random.randint(0,len(problems) - 1)
                seen_list.append(r)
                s = problems[r][0]
                t = problems[r][1]
                #s = "636"
                #t = "644"
                print(s+"->"+t)
                path = ucs(int(s),int(t),roads)
                sol = path.solution()
                path_time = 0
                dist = path.path_cost
                for i in range(0,len(sol)-1):
                    path_time += roads.distance_from_links(sol[i],sol[i+1]) / SPEED_RANGES[roads.get_roadtype(sol[i],sol[i+1])][1] * 1000
                out.write(' '.join(str(j) for j in path.solution())+" - "+str(dist)+"m"+" - "+str(path_time/60))
                out.write("\n")

def generate_problems():
    # f = open("problems.csv","w")
    with open("problems.csv","w",newline = "") as f:
        writer = csv.writer(f)
        problems = []
        for _ in range(0,TO_GENERATE):
            j1 = random.randint(0,len(roads) - 1)
            while len(roads[j1].links) == 0:
                j1 = random.randint(0,len(roads) - 1)
            closure = sorted(roads.return_focus(j1,max_depth = 20))
            closure_flat = list(set(map(lambda x: x.target,closure)))
            # closure_flat = set(map(lambda x: x.target,closure))
            j2 = random.randint(0,len(roads) - 1)
            while j2 not in closure_flat:
                j2 = closure_flat[random.randint(0,len(closure_flat) - 1)]
            problems.append((j1,j2))
        writer.writerows(problems)
        f.close()
        pass


if __name__ == "__main__":
    from sys import argv

    assert len(argv) == 1
    generate_problems()
    generate_solutions()
