"""
Introduction to Artificial Intelligence, 89570, Bar Ilan University, ISRAEL

Student name:
Student ID:

"""

# multiAgents.py
# --------------
# Attribution Information: part of the code were created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# http://ai.berkeley.edu.
# We thank them for that! :)


import random,util,math

from connect4 import Agent

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent is another abstract class.
    """

    def __init__(self,evalFn = 'scoreEvaluationFunction',depth = '2'):
        self.index = 1  # agent is always index 1
        self.evaluationFunction = util.lookup(evalFn,globals())
        self.depth = int(depth)

class BestRandom(MultiAgentSearchAgent):

    def getAction(self,gameState):
        return gameState.pick_best_move()

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self,gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Which means - returns the actions the agent should do according to the minMax algorithm

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.isWin():
        Returns whether or not the game state is a winning state for the current turn player

        gameState.isLose():
        Returns whether or not the game state is a losing state for the current turn player

        gameState.is_terminal()
        Return whether or not that state is terminal
        """

        "*** YOUR CODE HERE ***"
        action_values = {}

        def minMax_Value(depth,game_state,agent_id):
            if depth == 0:
                return self.evaluationFunction(game_state)

            # if the agent for whom we are building the tree(the maximizer) is now evaluated
            if agent_id == self.index:
                if game_state.isWin():
                    return math.inf
                if game_state.isLose():
                    return -math.inf
                value = -math.inf
                leg_acts = game_state.getLegalActions(agent_id)
                for a in leg_acts:
                    value = max(value,
                                minMax_Value(depth - 1,game_state.generateSuccessor(agent_id,a),(agent_id + 1) % 2))
                    if value == math.inf:
                        return value
            else:
                if game_state.isWin():
                    return math.inf
                if game_state.isLose():
                    return -math.inf
                value = math.inf
                leg_acts = game_state.getLegalActions(agent_id)
                #states = (minMax_Value(depth-1,game_state.generateSuccessor(agent_id,a),(agent_id + 1) % 2) for a in leg_acts)
                for a in leg_acts:
                    value = min(value,minMax_Value(depth - 1,game_state.generateSuccessor(agent_id,a),(agent_id + 1) % 2))
            return value

        leg_acts = gameState.getLegalActions(self.index)
        # for a in leg_acts:
        #     if a == 5:
        #         print('foo')
        #     action_values[a] = minMax_Value(self.depth,gameState,self.index)
        #action_values[4] = minMax_Value(self.depth,gameState.generateSuccessor(0,4),self.index)
        value = minMax_Value(self.depth,gameState,self.index)
        return max(gameState.getLegalActions(0),key = lambda x: minMax_Value(self.depth,gameState.generateSuccessor(0,x),self.index))

class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self,gameState):
        """
            Your minimax agent with alpha-beta pruning (question 2)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self,gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
