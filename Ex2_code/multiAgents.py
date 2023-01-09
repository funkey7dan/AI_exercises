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
import gameUtil as u

def generate_switch(game_state,action):
    next_state = game_state.generateSuccessor(game_state.turn,action)
    next_state.turn = next_state.switch_turn(game_state.turn)
    return next_state
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

        def minMax_Value(depth,game_state):

            if depth == 0 or game_state.is_terminal():
                return self.evaluationFunction(game_state)
            # if the agent for whom we are building the tree(the maximizer) is now evaluated
            if game_state.turn == u.AI:
                value = -math.inf
                values = (minMax_Value(depth - 1,generate_switch(game_state,a)) for a in game_state.getLegalActions())
                return max(value,max(values))
                # for a in game_state.getLegalActions(game_state.turn):
                #     next_state = game_state.generateSuccessor(game_state.turn,a)
                #     next_state.turn = next_state.switch_turn(game_state.turn)
                #     value = max(value,minMax_Value(depth - 1,next_state))
                # return value
            #minimizing
            else:
                value = math.inf
                values = (minMax_Value(depth - 1,generate_switch(game_state,a)) for a in
                          game_state.getLegalActions(game_state.turn))
                return min(value,min(values))
                # for a in game_state.getLegalActions(game_state.turn):
                #     next_state = game_state.generateSuccessor(game_state.turn,a)
                #     next_state.turn = next_state.switch_turn(game_state.turn)
                #     value = min(value,minMax_Value(depth - 1,next_state))
                # return value
        results = {}
        for act in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(gameState.turn,act)
            next_state.turn = next_state.switch_turn(gameState.turn)
            results[act] = minMax_Value(self.depth-1,next_state)
        print(results)
        return max(results,key = lambda x: (results[x],x))
        # return max(gameState.getLegalActions(0),key = lambda x: minMax_Value(self.depth,
        # gameState))

class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self,gameState):
        """
            Your minimax agent with alpha-beta pruning (question 2)
        """
        def alpha_beta_minimax(depth,game_state,alpha,beta):
            if depth == 0 or game_state.is_terminal():
                return self.evaluationFunction(game_state)

            # maximizing player
            if game_state.turn == u.AI:
                value = -math.inf
                for a in game_state.getLegalActions():
                    # next_state = game_state.generateSuccessor(game_state.turn,a)
                    # next_state.turn = next_state.switch_turn(game_state.turn)
                    value = max(value,alpha_beta_minimax(depth - 1,generate_switch(game_state,a),alpha,beta))
                    if value > beta:
                        break
                    alpha = max(alpha,value)

            # minimizing player
            else:
                value = math.inf
                for a in game_state.getLegalActions():
                    # next_state = game_state.generateSuccessor(game_state.turn,a)
                    # next_state.turn = next_state.switch_turn(next_state.turn)
                    value = min(value,alpha_beta_minimax(depth - 1,generate_switch(game_state,a),alpha,beta))
                    if value < alpha:
                        break
                    beta = min(beta,value)
            return value

        results = {}
        for act in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(gameState.turn,act)
            next_state.turn = next_state.switch_turn(gameState.turn)
            results[act] = alpha_beta_minimax(self.depth-1,next_state,alpha = -math.inf,
                                                      beta = math.inf)
        print(results)
        return max(results,key = lambda x: (results[x],x))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self,gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def expectiminimax(depth,game_state):
            if depth == 0 or game_state.is_terminal():
                if game_state.turn == u.AI:
                    return self.evaluationFunction(game_state)
                else:
                    return self.evaluationFunction(game_state)

            if game_state.turn == u.AI:
                value = -math.inf
                values = (expectiminimax(depth - 1,generate_switch(game_state,a)) for a in game_state.getLegalActions())
                return max(value,max(values))
            else:
                p = 1 / len(game_state.getLegalActions())
                value = sum(p *expectiminimax(depth - 1,generate_switch(game_state,a)) for a in game_state.getLegalActions())
            return value

        results = {}
        for act in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(gameState.turn,act)
            next_state.turn = next_state.switch_turn(gameState.turn)
            results[act] = expectiminimax(self.depth-1,next_state)
        print(results)
        return max(results,key = lambda x: results[x])
        # return max(gameState.getLegalActions(0),
        #            key = lambda x: expectiminimax(self.depth,gameState.generateSuccessor(u.AI,x)))
