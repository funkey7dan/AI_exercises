""" Daniel Bronfman 315901173"""
import time
from ways.algorithms import ida_star
from ways.draw import plot_path
from ways.info import SPEED_RANGES
from ways.graph import load_map_from_csv
from main import ucs,a_star,huristic_function

import random
import csv
import matplotlib.pyplot as plt
import numpy as np

TO_GENERATE = 90
SOLUTIONS_TO_RUN = 100
roads = load_map_from_csv()


def generate_solutions():
    with open("problems.csv","r",newline = "") as f:
        reader = csv.reader(f)
        problems = list(reader)

        #### UCS ####
        with open("./results/UCSRuns.txt","w") as out:
            ucs_solutions = []
            times = []
            times_dict = {}
            for _ in range(0,SOLUTIONS_TO_RUN):
                #r = random.randint(0,len(problems) - 1)

                r = _
                s = problems[r][0]
                t = problems[r][1]
                start = time.perf_counter()
                path = ucs(int(s),int(t),roads)
                #if _ < 10:
                ti = time.perf_counter() - start
                times_dict[(int(s),int(t))] = ti
                sol = path.solution()
                path_time = 0
                for i in range(0,len(sol)-1):
                    path_time += ((roads.distance_from_links(sol[i],sol[i+1])/1000) / SPEED_RANGES[roads.get_roadtype(sol[i],sol[i+1])][1])
                ucs_solutions.append([n for n in path.solution()])
                out.write(' '.join(str(j) for j in path.solution())+" - "+str(round(path_time*360,4)))
                out.write("\n")
            ucs_solutions.sort(key = len,reverse = True)
            for i in range(0,10):
                times.append(times_dict[(ucs_solutions[i][0],ucs_solutions[i][-1])])
            print("UCS: ",round(np.mean(times),7))
            times.clear()
            times_dict = {}

        #### A* ####

        with open("./results/AStarRuns.txt","w") as out:
            x_values = []
            y_values = []
            for _ in range(0,SOLUTIONS_TO_RUN):
                r = _
                s = problems[r][0]
                t = problems[r][1]
                #s = "636"
                #t = "644"
                #print(s+"->"+t)
                start = time.perf_counter()
                path = a_star(int(s),int(t),roads,huristic_function)
                ti = time.perf_counter() - start
                times_dict[(int(s),int(t))] = ti
                sol = path.solution()
                path_time = 0
                s = int(s)
                t = int(t)
                h_time = huristic_function(roads[s].lat,roads[s].lon,roads[t].lat,roads[t].lon) / (max(SPEED_RANGES,key = lambda x: x[1]))[1]
                for i in range(0,len(sol)-1):
                    path_time += ((roads.distance_from_links(sol[i],sol[i+1])/1000) / SPEED_RANGES[roads.get_roadtype(sol[i],sol[i+1])][1])
                out.write(' '.join(str(j) for j in path.solution())+" - "+str(round(path_time*360,4))+" - "+str(round(h_time*360,4)))
                out.write("\n")
                x_values.append(h_time*60)
                y_values.append(path_time*60)
            for i in range(0,10):
                times.append(times_dict[(ucs_solutions[i][0],ucs_solutions[i][-1])])
            print("A*: ",round(np.mean(times),7))
            times.clear()
        plt.xlabel("Heuristic time ")
        plt.ylabel("a_star time")
        plt.plot(x_values,y_values,marker='o',linestyle='none')
        plt.savefig('a_star_graph.png')
        plt.clf()

        #### IDA* ####

        out = open("./results/IDAStarRuns.txt","w")
        for _ in range(0,10):
            #print(_)
            r = _
            #s = problems[r][0]
            #t = problems[r][1]
            s = ucs_solutions[r][0]
            t = ucs_solutions[r][-1]
            start = time.perf_counter()
            path = ida_star(int(s),int(t),roads,huristic_function)
            times.append(time.perf_counter() - start)
            sol = path.solution()
            if _ < 10:
                plot_path(roads,sol)
                plt.savefig(f'img_sulotions/map{_}.png')
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
                ' '.join(str(j) for j in path.solution()) + " - " + str(round(path_time * 360,4)) + " - " + str(round(h_time*360,4)))
            out.write("\n")
        out.close()
        print("IDA*: ",round(np.mean(times),7))
        #plt.savefig(f'map.png')

def generate_problems():
    # f = open("problems.csv","w")
    with open("problems.csv","w",newline = "") as f:
        writer = csv.writer(f)
        problems = []
        for _ in range(0,TO_GENERATE):
            j1 = random.randint(0,len(roads) - 1)
            while len(roads[j1].links) == 0:
                j1 = random.randint(0,len(roads) - 1)
            closure = sorted(roads.return_focus(j1,max_depth = 15))
            closure_flat = list(set(map(lambda x: x.target,closure)))
            j2 = random.randint(j1+1,len(roads) - 1)
            while j2 not in closure_flat or j2 == j1:
                j2 = closure_flat[random.randint(0,len(closure_flat) - 1)]
            problems.append((j1,j2))
        # add problems that do not result in loops for ida* to run (allowed by Osnat in the forum)
        problems+=[(145001,145018),(5542,38730),(5542,38730),(72661,72675),
                         (31943,31944),(4024,87868),(911910,911974),(750758,907704),(522028,522021),(530433,530440)]

        # sort by difference in indices
        problems.sort(key = lambda x: abs(int(x[0]) - int(x[1])),reverse = True)
        writer.writerows(problems)
        f.close()


if __name__ == "__main__":
    from sys import argv
    #assert len(argv) == 1
    if "--no_gen" not in argv:
        generate_problems()
    if "--no_sol" not in argv:
        generate_solutions()
