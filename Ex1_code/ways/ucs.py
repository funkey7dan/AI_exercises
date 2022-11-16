from . import PriorityQueue,Node,RoutingProblem
from ways.tools import compute_distance

def bfgs(problem,f_function):
    frontier = PriorityQueue(f_function)  # Priority Queue
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
    links = list(G.iterlinks())

    def g(node):
        if node.state == s:
            return 0
        cost = node.path_cost
        return cost
        #l = list(filter(lambda x: x.source == s and x.target == node.state,links))

        #return compute_distance(G[s].lat,G[s].lon,G[node.state].lat,G[node.state].lon)


    return bfgs(problem = problem,f_function = g)
