from . import PriorityQueue, Node, RoutingProblem
from ways.tools import compute_distance


def bfgs(problem, f_function):
    frontier = PriorityQueue(f_function)  # Priority Queue
    frontier.append(Node(problem.s_start))
    closed_list = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        closed_list.add(node.state)
        for child in node.expand(problem):
            if child.state not in closed_list and child not in frontier:
                frontier.append(child)
            elif child in frontier and f_function(child) < frontier[child]:
                del frontier[child]
            frontier.append(child)
    return None


def ucs(s, t, G):
    ''' Accept the start traget junction indices, and the Roads graph'''
    problem = RoutingProblem(s, t, G)

    def g(node):
        return compute_distance(G[s].lat, G[s].lon,
                                G[node.state].lat, G[node.state].lon)

    return bfgs(problem=problem, f_function=g)
