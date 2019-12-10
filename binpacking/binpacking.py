#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys
import copy
import heapq
import random
import time

successorDict = {}
fitnessDict = {}

class BinPacking(Problem):

    def successor(self, state):
        key = hash(state)
        value = successorDict.get(key, None)
        if(value!=None):
            return value

        result = []
        already_used = [False]*len(state.items)
        for i in range(state.bins.__len__()):
            for j in state.bins[i]:
                already_used[int(j)-1] = True
                result.extend(possibilities(i, j, state, already_used))
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
            sum = sum + math.pow(state.fullness(i)/state.capacity, 2)

        result = 1 - sum/state.bins.__len__()

        fitnessDict[key] = result
        return result


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

    def can_exchange(self, bin, item, other_bin, other_item):
        if item is None:
            return self.fullness(bin)  + self.bins[other_bin][other_item] <= self.capacity
        return self.fullness(bin) - self.bins[bin][item] + self.bins[other_bin][other_item] <= self.capacity

    def can_fit(self, bin, itemsize):
        return sum(list(bin.values())) + itemsize <= self.capacity

    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(list(self.bins[i].keys())) + '\n'
        return s
    
    def copy(self):
        #newstate = State(self.capacity, self.items.copy())
        #newstate.bins.clear()
        #for b in self.bins:
        #    newstate.bins.append(b.copy())
        #return newstate
        return copy.deepcopy(self)

    def move(self, i, j, k):
        item = self.bins[i].pop(j, None)
        self.bins[k][j] = item

    def fullness(self, bin):
        sum = 0
        for ind,size in self.bins[bin].items():
            sum = sum + size
        return sum




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
    best_solution = current
    best_estimation = problem.value(current.state)
    steps_until_best = 0
    for i in range(limit):
        if callback is not None:
            callback(current)
        best = None
        bestEstimation = 1.0
        for neighbour in current.expand():
            estimate = problem.value(neighbour.state)
            if estimate < bestEstimation:
                bestEstimation = estimate
                best = neighbour
            if estimate < best_estimation:
                best_estimation = estimate
                best_solution = best
                steps_until_best = i
        current = best
    return best_solution, steps_until_best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    bestEstimation = problem.value(current.state)
    counter = 0
    steps_until_best = 0
    for i in range(limit):
        minusBestEstimation = 1.0
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
        current = heap[random.randint(0, 4)][2]
        currentEstimation = problem.value(current.state)
        if (bestEstimation>currentEstimation):
            bestEstimation = currentEstimation
            best = current
            steps_until_best = i

    return best, steps_until_best

def hash(state):
    return state.__str__()

def possibilities(bin, item, state, already_used):
    result = []
    for other_bin in range(state.bins.__len__()):
        if other_bin != bin:
            for other_item in state.bins[other_bin]:
                if not already_used[int(other_item)-1]:
                    if state.bins[bin][item] != state.bins[other_bin][other_item]:
                        if state.can_exchange(bin, item, other_bin, other_item) and state.can_exchange(other_bin, other_item, bin, item):
                            other = state.copy()
                            other.bins[bin][other_item] = other.bins[other_bin].pop(other_item)
                            other.bins[other_bin][item] = other.bins[bin].pop(item)
                            action = "exchange object " + str(item) + " from bin" + str(bin) + " with object " + str(other_item) + " from bin " + str(other_bin)
                            result.append((action, other))
            if state.can_exchange(other_bin, None, bin, item):
                other = state.copy()
                other.bins[other_bin][item] = other.bins[bin].pop(item)
                action = "move object " + str(item) + " from bin" + str(bin) + " to bin " + str(other_bin)
                result.append((action, other))
    return result





#####################
#       Launch      #
#####################

'''

if __name__ == '__main__':
    for i in range(1, sys.argv.__len__()):
        info = read_instance(sys.argv[i])
        init_state = State(info[0], info[1])
        bp_problem = BinPacking(init_state)
        step_limit = 100
        start0 = time.time()
        print("très passé")
        node0, steps0 = maxvalue(bp_problem, step_limit)
        end0 = time.time()
        time0 = end0 - start0
        state0 = node0.state
        bins0 = state0.bins.__len__()
        value0 = bp_problem.value(state0)
        time1 = 0
        value1 = 0
        steps1 = 0
        bins1 = 0
        print("passé")
        for j in range(10):
            start1 = time.time()
            print("Step : " + str(j))
            node1, steps = random_walk(bp_problem, step_limit)
            steps1 = steps1 + steps
            end1 = time.time()
            state1 = node1.state
            bins1 = bins1 + state1.bins.__len__()
            value1 = value1 + bp_problem.value(state1)
            time1 = time1 + end1 - start1            
        time1 = time1/10
        value1 = value1/10
        steps1 = steps1/10
        bins1 = bins1/10
        time2 = 0
        value2 = 0
        steps2 = 0        
        bins2 = 0
        print("présent")
        for j in range(10):
            start2 = time.time()
            print("Step : " + str(j))
            node2, steps = randomized_maxvalue(bp_problem, step_limit)
            steps2 = steps2 + steps
            end2 = time.time()
            state2 = node2.state
            bins2 = bins2 + state2.bins.__len__()
            value2 = value2 + bp_problem.value(state2)
            time2 = time2 + end2 - start2
        time2 = time2/10
        value2 = value2/10
        steps2 = steps2/10
        bins2 = bins2/10
        start2 = time.time()
        print("futur")
        print("===Instance "+str(i)+"===")
        print("Maxvalue - Random_walk - Randomized_maxvalue")
        print("Times: "+str(time0)+" - "+str(time1)+" - "+str(time2))
        print("Bins: "+str(bins0)+" - "+str(bins1)+" - "+str(bins2))
        print("Values: "+str(value0)+" - "+str(value1)+" - "+str(value2))
        print("Steps: "+str(steps0)+" - "+str(steps1)+" - "+str(steps2))

'''

if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1])
    bp_problem = BinPacking(init_state)
    step_limit = 100
    (node, step) = maxvalue(bp_problem, step_limit)
    state = node.state
    print(state)