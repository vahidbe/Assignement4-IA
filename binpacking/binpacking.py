#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys
import heapq
import random

successorDict = {}
fitnessDict = {}

class BinPacking(Problem):

    def successor(self, state):
        key = hash(state)
        value = successorDict.get(key, None)
        if(value!=None):
            return value

        action_statelist = []
        #print(state.bins)

        for i in range(state.bins.__len__()):
            #print("keys: "+str(state.bins[i].keys()))
            for j in state.bins[i].keys():
                for k in range(state.bins.__len__()):
                    if state.can_fit(state.bins[k], state.bins[i].get(j, None)):
                        #print("move object "+str(j)+" from "+str(i)+" to "+str(k))
                        action = "move object "+str(j)+" from "+str(i)+" to "+str(k)
                        newstate = state.copy()
                        newstate.move(i,j,k)
                        action_statelist.append((action, newstate))

        result = action_statelist
        successorDict[key] = result
        return result

    def value(self, state):
        return self.fitness(state)

    def fitness(self, state):
        """
        :param state:
        :return: fitness value of the state in parameter
        """
        key = hash(state)
        value = fitnessDict.get(key, None)
        if(value!=None):
            return value

        sum = 0
        for i in range(state.bins.__len__()):
            sum = sum + math.pow(self.fullness(state, i)/state.capacity,2)

        result = 1 - sum/state.bins.__len__()

        fitnessDict[key] = result
        return result
    
    def fullness(self, state, i):
        sum = 0
        for ind,size in state.bins[i].items():
            sum = sum + size
        return sum


class State:

    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.bins = self.build_init()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        init = []
        for ind, size in self.items.items():
            if len(init) == 0 or not self.can_fit(init[-1], size):
                init.append({ind: size})
            else:
                if self.can_fit(init[-1], size):
                    init[-1][ind] = size
        return init

    def can_fit(self, bin, itemsize):
        return sum(list(bin.values())) + itemsize <= self.capacity

    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(str(list(self.bins[i].keys()))) + '\n'
        return s
    
    def copy(self):
        newstate = State(self.capacity, self.items.copy())
        newstate.bins.clear()
        for b in self.bins:
            newstate.bins.append(b.copy())
        return newstate

    def move(self, i, j, k):
        item = self.bins[i].pop(j, None)
        self.bins[k][j] = item




def read_instance(instanceFile):
    file = open(instanceFile)
    capacitiy = int(file.readline().split(' ')[-1])
    items = {}
    line = file.readline()
    while line:
        items[line.split(' ')[0]] = int(line.split(' ')[1])
        line = file.readline()
    return capacitiy, items

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    bestEstimation = problem.value(current.state)
    for i in range(limit):
        for neighbour in current.expand():
            estimate = problem.value(neighbour.state)
            if estimate < bestEstimation:
                bestEstimation = estimate
                best = neighbour
        current = best
    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    minusBestEstimation = problem.value(current.state)
    counter = 0
    for i in range(limit):
        heap = []
        for neighbour in current.expand():
            counter = counter + 1
            estimate = problem.value(neighbour.state)
            if len(heap) >= 5:
                if estimate < minusBestEstimation:
                    heap[-1] = (estimate, counter, neighbour)
                    heapq.heapify(heap)
                    minusBestEstimation = heap[-1][0]
            else:
                heapq.heappush(heap, (estimate, counter, neighbour))
                minusBestEstimation = heap[-1][0]
        best = heap[random.randint(0, 4)][2]
        current = best

    return best

def hash(state):
    return state.__str__()


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    for i in range(1, sys.argv.__len__()):
        info = read_instance(sys.argv[i])
        init_state = State(info[0], info[1])
        bp_problem = BinPacking(init_state)
        step_limit = 100
        node1 = maxvalue(bp_problem, step_limit)
        state1 = node1.state
        #print("maxvalue")
        #print(state1)
        node2 = randomized_maxvalue(bp_problem, step_limit)
        state2 = node2.state
        #print("randomized_maxvalue")
        #print(state2)
        print("===Instance "+str(i)+"===")
        print("Number of bins:\n  maxvalue: "+str(state1.bins.__len__())+"\n  randomized_maxvalue: "+str(state2.bins.__len__())+"\n")
