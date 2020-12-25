# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)
    invaderDist=99999
    evaluateActions=[]
    bestAction=actions[0]
    for action in actions:
      successor = gameState.generateSuccessor(self.index, action)
      if successor.isOnRedTeam(self.index):
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        ghosts = [a for a in enemies if (not a.isPacman) and a.getPosition() != None]
        #if pacman on our side, eat him
        if len(invaders)>0:
          invaderDistances = [self.getMazeDistance(successor.getAgentPosition(self.index), a.getPosition()) for a in invaders]
          if min(invaderDistances)<invaderDist:
            bestAction = action
            invaderDist = min(invaderDistances)
        else:
          ghostDistances = [self.getMazeDistance(successor.getAgentPosition(self.index), a.getPosition()) for a in ghosts]
          ghostDistance = sum(ghostDistances)
          blueFoods = successor.getBlueFood().asList()
          foodDistances = [self.getMazeDistance(successor.getAgentPosition(self.index), food) for food in blueFoods]
          foodDistance = sum(foodDistances)
          print(foodDistance, ghostDistance)
          me = successor.getAgentState(self.index)
          if me.isPacman:
            #if I am pacman, eat food and avoid ghosts
            evaluateActions.append((action,(1/(foodDistance))*ghostDistance))
          else:
            #else food ke paas jao
            evaluateActions.append((action,1/foodDistance))

    if invaderDist != 99999 and bestAction != Directions.STOP:
      print(invaderDist, bestAction)
      print("han")
      return bestAction
    else:
      print("what")
      bestValue=-99999
      print(evaluateActions)
      for evaluateAction in evaluateActions:
        if evaluateAction[1]>bestValue:
          bestAction = evaluateAction[0]
          bestValue = evaluateAction[1]
      return bestAction


    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)

