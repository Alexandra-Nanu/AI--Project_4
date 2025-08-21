# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

"""MOLDOVAN PAULA"""

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) # se genereaza starea curenta, adica starea care rezulta dupa aplicarea actiunii
        newPos = successorGameState.getPacmanPosition() # se obt pozitia curenta a lui pacman in starea succesoare
        newFood = successorGameState.getFood() # se obt harta cu mancarea din starea succesoare
        newGhostStates = successorGameState.getGhostStates() # se obt starile strigoilor din starea succesoare
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # se obt timpii in care un strigoi se sperie in starea succesoare
        bigFood = successorGameState.getCapsules() # mancarea mare care permite ca pacman sa manance un strigoi; se obt ac din starea succesoare

        "** YOUR CODE HERE **" 
          
        '''MOLDOVAN PAULA'''

        # daca starea succesoare e o stare de castig, adica pacman a castigat
        if successorGameState.isWin():
            return float("inf") # se returneaza un scor ft mare, adica infinit

        # se initializeaza scorul cu scorul curent al jocului
        score = successorGameState.getScore()

        # se incurajeaza colectarea mancarii prin min dist fata de cea mai apropiata mancare
        # se verif lista de mancare si se calc dist manhattan pana la fiecarea mancare
        foodList = newFood.asList() # se extrage lista de mancare
        if foodList:
            closestFoodDistance = min(manhattanDistance(newPos, food) for food in foodList)
            # se imbunatateste scorul pe masura ce pacman se apropie de mancare (cu cat dist e mai mica, cu atat mai bine)
            score = score + 10 / (closestFoodDistance + 1) # se ad o val invers prop cu dist
            
        # daca se poate sa manance o mancare mare (capsula)
        # daca exista, sa se cal dist fata de cea mai aproape
        if bigFood:
            closestCapsuleDistance = min(manhattanDistance(newPos, capsule) for capsule in bigFood)
            # cu cat pacman se apropie mai mult de o capsula, cu atat mai mult creste scorul
            score = score + 50 / (closestCapsuleDistance + 1)

        # se evita strigoii activi
        # se verif fiecare strigoi si se cal dist pana la pacman
        for ghost, scaredTime in zip(newGhostStates, newScaredTimes): # zip combina 2 sau mai multe liste intr-o lista de tuple
            ghostDistance = manhattanDistance(newPos, ghost.getPosition())
            if scaredTime > 0:
                # daca strigoiul e speriat, pacman merge spre el sa il manance
                score = score + 200 / (ghostDistance + 1)
            else:
                # daca strigoiul nu e speriat, adica e activ, pacman se indeparteaza
                if ghostDistance < 2:
                    # daca strigoiul e ft aproape, penalizare
                    score = score - 1000  # dist periculoase au scor negativ
                else:
                    # daca strigoiul e departe, scorul scade usor in functie de dist
                    score = score - 5 / (ghostDistance + 1)

        # se penalizeaza pacman cand se opreste pt ca vr sa se miste mereu
        if action == Directions.STOP:
            score = score - 20 # ca sa fie incurajat sa se miste mereu

        # se penalizeaza mancarea ramasa pt a il face sa o ia rapid
        score = score - 4 * len(foodList) # cu cat e mai multa mancare ramase, penalizarea e mai mare

        return score # se returneaza scorul final dupa parcurgerea tuturor pasilor
        
def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You do not need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "** YOUR CODE HERE **"

        '''MOLDOVAN PAULA'''

        def minimax(agentIndex, depth, state):
            # daca a ajuns intr-o stare de castig sau de pierdere sau la adncimea dorita, se eval starea curenta
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            # se obt nr de agenti
            numAgents = state.getNumAgents()
            # se det agentul urm care va actiona
            nextAgent = (agentIndex + 1) % numAgents
            # daca urm agent e zero, se scade adancimea de cautare
            nextDepth = depth - 1 if nextAgent == 0 else depth

            # se obt actiunile pe care le poate face agentul curent
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            # se genereaza succesorii pt fiecare act
            successors = [state.generateSuccessor(agentIndex, action) for action in legalActions]
            # se calc scorurile pt fiecare succesor util minimax
            scores = [minimax(nextAgent, nextDepth, successor) for successor in successors]

            # daca agentul curent este 0, se cauta max (pt a max castigurile)
            # daca agentul curent nu e 0, se cauta min (pt a min castigul adversarului)
            return max(scores) if agentIndex == 0 else min(scores)

        # se gaseste cea mai buna actiune
        legalActions = gameState.getLegalActions(0)
        # se alege actiunea care produce cel mai mare scor
        bestAction = max(legalActions, key=lambda action: minimax(1, self.depth, gameState.generateSuccessor(0, action)))

        return bestAction # se returneaza actiunea aleasa

# @Author: Alexandra Nanu

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
         - inițializez limita maximului cu o valoare mică 
         - initializez limita minimului cu o valoare mare
         - valorile se vor modifica dupa compararea cu nodurile copii
        """
        alpha = float('-inf')
        beta = float('inf')
        """
        - pornesc de la un nod max și voi returnam actiunea
        """
        actions = gameState.getLegalActions(0)
        if not actions:
            return None # dacă nu sunt acțiuni disponibile, returnăm None
        best_score = float ('-inf') # inițializez cel mai bun scor cu -infinit
        best_action = None # inițializez cea mai bună acțiune


        for action in actions:
            val = self.value(gameState.generateSuccessor(0,action), self.depth, alpha, beta, 1)
            if val > best_score:
                best_score = val
                best_action = action
            if best_score > beta: # pruning: dacă valoarea depășește beta, ma oprim
                return best_action
            alpha = max(alpha, best_score)
        return best_action
    
    # noduri max -> Pacman
    def max_value(self, gameState, depth, alpha, beta, index):
        v = float('-inf') # initializez v cu -infinit 
        actions = gameState.getLegalActions(index) # obtin succesorul of state

        #in cazul in care nu mai sunt succesori si sunt pe un nod frunza
        if not actions:
            return self.evaluationFunction(gameState)
        
        for action in actions:
            # calculez valoarea succesorului folosind value
            val = self.value(gameState.generateSuccessor(index, action), depth, alpha, beta, 1)
            v = max(v, val) # actualizez valorea maxima
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v 
    
    # noduri min -> Strigoi
    def min_value(self, gameState, depth, alpha, beta, index):
        
        nextIndex = (index + 1) % gameState.getNumAgents() # obtinem indexul urmatorului jucator
        if nextIndex == 0: # daca urmatorul jucator este Pacman urc in arbore
            depth -= 1
        v = float('inf') # initializez v cu infinit
        actions = gameState.getLegalActions(index)
        if not actions:
            return self.evaluationFunction(gameState)
    
        for action in actions:
           
            val = self.value(gameState.generateSuccessor(index, action), depth, alpha, beta, nextIndex)
            v = min(v, val)
            if v < alpha: # pruning: dacă valoarea este mai mică decât alpfa, se opreste
                return v
            beta = min(beta, v)
        return v
    
    def value(self, gameState, depth, alpha, beta, index):
        # nod frunza
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        # nod Pacman (max)
        elif index == 0:
            return self.max_value(gameState, depth, alpha, beta, index)
        # nod strigoi (min)
        else:
            return self.min_value(gameState, depth, alpha, beta, index)

# @Author: Alexandra Nanu
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # pornim de la un nod max 
        # functioneaza ca si max_value, insa acum returnam o actiune
        actions = gameState.getLegalActions(0)

        if not actions:
            return None
        
        best_score = float('-inf')
        best_action = None

        for action in actions:
            v = self.value(gameState.generateSuccessor(0, action), self.depth, 1)

            if v > best_score:
                best_score = v
                best_action = action
        return best_action

    # noduri max -> Pacman
    def max_value(self, gameState, depth, index):
        # initializam v
        v = float('-inf')
        actions = gameState.getLegalActions(index)
        
        if not actions: # caz nod frunza
            return self.evaluationFunction(gameState)

        for action in actions:
            val = self.value(gameState.generateSuccessor(index, action), depth, 1) # calculez valoarea succesorului 
            v = max(v, val)
        
        return v

    # noduri sansa -> Strigoi
    def exp_value(self, gameState, depth, index):
        actions = gameState.getLegalActions(index)
        nextIndex = (index + 1) % gameState.getNumAgents()

        # daca urmatorul jucator e pacman, urcam in arbore
        if nextIndex == 0:
            depth -= 1
        v = 0
        for action in actions:
            # folosim aceeasi probabilitate pentru toate nodurile
            p = 1.0 / len (actions) * 1.0   
            val = self.value(gameState.generateSuccessor(index, action), depth, nextIndex) 
            v += p * val
        return v

    def value(self, gameState, depth, index):
        # nod frunza
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # nod Pacman 
        elif index == 0:
            return self.max_value(gameState, depth, index)
        # nod Strigoi 
        else:
            return self.exp_value(gameState, depth, index)
        
# @Author: Alexandra Nanu
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    max_num = float('inf')
    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    evaluation = currentGameState.getScore()

    # distanta pana la bucatile de mancare
    """
    - obiectivul lui pacman este sa manance toate bucatile de mancare
    - astfel, calculam distanta pana la cea mai apropiata bucata
    - daca nu se gaseste nicio bucata de mancare inseamna ca am terminat jocul
    - la final adaugam inversul valorii pentru a favoriza bucatile apropiate
    - daca puteam evalua si actiuni s-ar fi putut elimina opririle lui pacman cand strigoii sunt departe de el
    """
    f = max_num
    if foods:
        for food in foods:
            val = manhattanDistance(position, food)
            f = min(f, val)
    evaluation += 1.0 / f * 10

    # distanta pana la bucatile mari de mancare
    # procedez la fel ca la bucatile normale, dar acord o importanta mai mica bucatilor mari
    c = max_num
    if capsules:
        for capsule in capsules:
            val = manhattanDistance(position, capsule)
            c = min(c, val)
    evaluation += 1.0 / c * 0.7
    return evaluation 

# Abbreviation
better = betterEvaluationFunction
