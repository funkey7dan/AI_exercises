from . import PriorityQueue,Node,RoutingProblem
from Ex1_code.ways.info import SPEED_RANGES
import sys

# def dfs_contour(problem,f_limit,f_function):
#     frontier = [(Node(problem.s_start))]
#     while frontier:
#         node = frontier.pop()
#         if f_function(node) > f_limit:
#             return None,f_function(node)
#         if problem.is_goal(node.state):
#             return node.solution(),f_limit
#         if node.depth < f_limit:
#             frontier.extend(node.expand(problem))
#     return None

def dfs_contour(node,problem,f_limit,f_function):
    successors = node.expand(problem)
    if f_function(node) > f_limit:
        return None,f_function(node)
    if problem.is_goal(node.state):
        return node,f_limit
    next_f = sys.maxsize
    for child in successors:
        result,new_f = dfs_contour(child,problem,f_limit,f_function)
        if result:
            return result,f_limit
        next_f = min(new_f,next_f)
    return None,next_f

# def ida_star(s,t,G,heuristic):
#     problem = RoutingProblem(s,t,G)
#     def g(node):
#         if node.state == s:
#             return 0
#         return node.path_cost  #l = list(filter(lambda x: x.source == s and x.target == node.state,links))
#     def h(node):
#         return heuristic(G[node.state].lat,G[node.state].lon,G[t].lat,G[t].lon)/(max(SPEED_RANGES,key = lambda x: x[1]))[1]
#
#     f_limit = h(Node(problem.s_start))
#     for depth in range(1,1000):
#         result,f_limit = dfs_contour(problem,f_limit,f_function = lambda x: g(x) + h(x))
#         if result:
#             return result
#     return None
def ida_star(s,t,G,heuristic):
    problem = RoutingProblem(s,t,G)
    def g(node):
        if node.state == s:
            return 0
        return node.path_cost  #l = list(filter(lambda x: x.source == s and x.target == node.state,links))
    def h(node):
        return heuristic(G[node.state].lat,G[node.state].lon,G[t].lat,G[t].lon)/(max(SPEED_RANGES,key = lambda x: x[1]))[1]


    initial = Node(problem.s_start)
    f_limit = h(initial)
    while True:
        result,f_limit = dfs_contour(initial,problem,f_limit,f_function = lambda x: g(x) + h(x))
        if result:
            return result
        if f_limit == sys.maxsize:
            return None
    return None

def bfgs(problem,f_function):
    frontier = PriorityQueue(f_function)
    frontier.append(Node(problem.s_start))
    closed_list = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        closed_list.add(node.state)
        for child in node.expand(problem):
            if child.state not in closed_list and child.state not in frontier:
                frontier.append(child)
            elif child in frontier and f_function(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)
    return None

def ucs(s,t,G):
    """ Accept the start target junction indices, and the Roads graph"""
    problem = RoutingProblem(s,t,G)

    def g(node):
        if node.state == s:
            return 0
        cost = node.path_cost
        return cost  #l = list(filter(lambda x: x.source == s and x.target == node.state,links))

        #return compute_distance(G[s].lat,G[s].lon,G[node.state].lat,G[node.state].lon)

    return bfgs(problem = problem,f_function = g)

def a_star(s,t,G,heuristic):
    """ Accept the start target junction indices, and the Roads graph"""
    problem = RoutingProblem(s,t,G)

    #links = list(G.iterlinks())

    def g(node):
        if node.state == s:
            return 0
        return node.path_cost  #l = list(filter(lambda x: x.source == s and x.target == node.state,links))
    def h(node):
        return heuristic(G[node.state].lat,G[node.state].lon,G[t].lat,G[t].lon) / \
               (max(SPEED_RANGES,key = lambda x: x[1]))[1]

    return bfgs(problem = problem,f_function = lambda x: g(x) + h(x))

