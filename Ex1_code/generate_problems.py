from Ex1_code.ways.algorithms import ida_star
from Ex1_code.ways.draw import plot_path
from Ex1_code.ways.info import SPEED_RANGES
from ways.graph import load_map_from_csv
from main import ucs,a_star,huristic_function

import random
import csv
import matplotlib.pyplot as plt

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
                for i in range(0,len(sol)-1):
                    path_time += ((roads.distance_from_links(sol[i],sol[i+1])/1000) / SPEED_RANGES[roads.get_roadtype(sol[i],sol[i+1])][1])
                out.write(' '.join(str(j) for j in path.solution())+" - "+str(path_time*60))
                out.write("\n")
    with open("./results/AStarRuns.txt","w") as out:
        with open("problems.csv","r",newline = "") as f:
            reader = csv.reader(f)
            problems = list(reader)
            seen_list = []
            x_values = []
            y_values = []
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
                path = a_star(int(s),int(t),roads,huristic_function)
                sol = path.solution()
                path_time = 0
                s = int(s)
                t = int(t)
                h_time = huristic_function(roads[s].lat,roads[s].lon,roads[t].lat,roads[t].lon) / (max(SPEED_RANGES,key = lambda x: x[1]))[1]
                for i in range(0,len(sol)-1):
                    path_time += ((roads.distance_from_links(sol[i],sol[i+1])/1000) / SPEED_RANGES[roads.get_roadtype(sol[i],sol[i+1])][1])
                out.write(' '.join(str(j) for j in path.solution())+" - "+str(path_time*60)+" - "+str(h_time*60))
                out.write("\n")
                x_values.append(h_time*60)
                y_values.append(path_time*60)
    #plt.xlabel("Heuristic time ")
    #plt.ylabel("a_star time")
    #plt.plot(x_values,y_values,marker='o',linestyle='dashed')
    #plt.savefig('a_star_graph.png')
    plt.clf()
    with open("problems.csv","r",newline = "") as f:
        out = open("./results/IDAStarRuns.txt","w")
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
            print(s + "->" + t)
            path = ida_star(int(s),int(t),roads,huristic_function)
            sol = path.solution()
            plot_path(roads,sol)
            plt.savefig(f'map{_}.png')
            plt.clf()
            path_time = 0
            s = int(s)
            t = int(t)
            h_time = huristic_function(roads[s].lat,roads[s].lon,roads[t].lat,roads[t].lon) / \
                     (max(SPEED_RANGES,key = lambda x: x[1]))[1]
            for i in range(0,len(sol) - 1):
                path_time += ((roads.distance_from_links(sol[i],sol[i + 1]) / 1000) /
                              SPEED_RANGES[roads.get_roadtype(sol[i],sol[i + 1])][1])
            out.write(
                ' '.join(str(j) for j in path.solution()) + " - " + str(path_time * 60) + " - " + str(h_time * 60))
            out.write("\n")
        out.close()

def generate_problems():
    # f = open("problems.csv","w")
    with open("problems.csv","w",newline = "") as f:
        writer = csv.writer(f)
        problems = []
        for _ in range(0,TO_GENERATE):
            j1 = random.randint(0,len(roads) - 1)
            while len(roads[j1].links) == 0:
                j1 = random.randint(0,len(roads) - 1)
            closure = sorted(roads.return_focus(j1,max_depth = 25))
            closure_flat = list(set(map(lambda x: x.target,closure)))
            # closure_flat = set(map(lambda x: x.target,closure))
            j2 = random.randint(0,len(roads) - 1)
            while j2 not in closure_flat and j2 != j1:
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
