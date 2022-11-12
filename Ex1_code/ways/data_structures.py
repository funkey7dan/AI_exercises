import heapq


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        # remove duplicates while preserving order
        return list(
            dict.fromkeys(
                [
                    self.child_node(problem, action)
                    for action in problem.actions(self.state)
                ]
            )
        )

    def child_node(self, problem, action):
        next_state = problem.succ(self.state, action)
        next_node = Node(
            next_state,
            self,
            action,
            self.path_cost + problem.step_cost(self.state, action),
        )
        return next_node

    def solution(self):
        return [node.state for node in self.path()]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.state)


# Using Ram's pq implementation
class PriorityQueue:
    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        for item in items:
            self.append(item)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception("Trying to pop from empty PriorityQueue.")

    def __len__(self):
        return len(self.heap)

    def __contains__(self, key):
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

    def __repr__(self):
        return str(self.heap)


class RoutingProblem:
    def __init__(self, s_start, goal, G):
        self.s_start = s_start
        self.goal = goal
        self.G = G

    def actions(self, s):
        """Applicable actions from state s"""
        actions = [x.target for x in self.G[s].links if x.source == s]
        return actions

    def succ(self, s, a):
        closure = sorted(self.G.return_focus(s, max_depth=0))
        closure_flat = list(set(map(lambda x: x.target, closure)))
        """the state that results from doing action a in state s"""
        if a in closure_flat:
            return a
        raise ValueError(f"No route from {s} to {a}")

    def is_goal(self, s):
        return s == self.goal

    def step_cost(self, s, a):
        link = list(filter(lambda x: x.target == a, self.G[s].links))[0]
        return link.distance

    def state_str(self, s):
        return s

    def __repr__(self):
        return {"s_start": self.s_start, "goal": self.goal, "graph": self.G}
