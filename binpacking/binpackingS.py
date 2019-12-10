#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys
import copy
import time


class BinPacking(Problem):

    def successor(self, state):
        ret = []
        swappable = [True]*len(state.items)
        for bin in range(len(state.bins)):
            for item in state.bins[bin]:
                swappable[int(item)-1] = False
                ret.extend(swap(bin, item, swappable, state))
        return ret

    def value(self, state):
        return self.fitness(state)

    def fitness(self, state):
        sum = 0
        for c in state.fullness:
            sum += (c/state.capacity)**2
        return 1-sum/len(state.bins)

class State:

    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.fullness = []
        self.bins = self.build_init()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        init = []
        for ind in self.items: # sorted(self.items.keys(), key=self.items.get):
            size = self.items[ind]
            if len(init) == 0:
                init.append({ind: size})
                self.fullness.append(size)
            elif not self.can_fit(init[-1], size):
                init.append({ind: size})
                self.fullness.append(size)
            else:
                init[-1][ind] = size
                self.fullness[-1] += size
        return init

    def can_fit(self, bin, itemsize):
        return sum(list(bin.values())) + itemsize <= self.capacity

    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(list(self.bins[i].keys())) + '\n'
        return s


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
    at_step = limit
    at_time = 0
    startTime = time.perf_counter()

    for step in range(limit):
        if callback is not None:
            callback(current)

        l = list(current.expand())
        if len(l) != 0:
            current = minvalues(l, 1)[0]
            if current.value() < best.value():
                best = current
                at_step = step
                at_time = time.perf_counter() - startTime
        else:
            break
    return (best, best.step, at_time)
    # return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    at_step = limit
    at_time = 0
    startTime = time.perf_counter()

    for step in range(limit):
        if callback is not None:
            callback(current)

        l = list(current.expand())
        if len(l) != 0:
            current = random.choice(minvalues(l, 5))
            if current.value() < best.value():
                best = current
                at_step = step
                at_time = time.perf_counter() - startTime
        else:
            break
    return (best, best.step, at_time)
    # return best

def minvalues(successors, n):
    n = min(n, len(successors)) # in case len(successors) < n
    values = [float('inf')]*n
    states = [None]*n
    for state in successors:
        eval = state.value()
        max_index = max(range(len(values)), key=values.__getitem__)
        if eval < values[max_index]:
            values[max_index] = eval
            states[max_index] = state
    return states

def swap(binA, itemA, swappable, state):
    nextStates = []
    for bin in range(len(state.bins)):
        if bin != binA:
            for item in state.bins[bin]:
                if swappable[int(item)-1]:
                    if state.bins[bin][item] !=  state.bins[binA][itemA] \
                       and state.fullness[bin] - state.bins[bin][item] + state.bins[binA][itemA] <= state.capacity \
                       and state.fullness[binA] - state.bins[binA][itemA] + state.bins[bin][item] <= state.capacity :
                        nextStates.append(swapItems(binA, itemA, bin, item, state))

            if state.fullness[bin] + state.bins[binA][itemA] <= state.capacity :
                nextStates.append(swapItems(binA, itemA, bin, None, state))
    return nextStates

def swapItems(binA, itemA, binB, itemB, state):
    nextstate = copy.deepcopy(state)
    if itemB == None: #move
        sizeA = nextstate.bins[binA].pop(itemA)
        nextstate.bins[binB][itemA] = sizeA
        nextstate.fullness[binB] += sizeA
        nextstate.fullness[binA] -= sizeA
        if (nextstate.fullness[binA] == 0):
            nextstate.fullness.pop(binA)
            nextstate.bins.pop(binA)
        return (None, nextstate)
    else: # swap items
        sizeA = nextstate.bins[binA].pop(itemA)
        sizeB = nextstate.bins[binB].pop(itemB)
        nextstate.bins[binA][itemB] = sizeB
        nextstate.bins[binB][itemA] = sizeA
        diff = sizeA - sizeB
        nextstate.fullness[binA] -= diff
        nextstate.fullness[binB] += diff
        return (None, nextstate)


#####################
#       Launch      #
#####################

'''

if __name__ == '__main__':
    files = ['instances/i01.txt'] #, 'instances/i02.txt', 'instances/i03.txt', 'instances/i04.txt', 'instances/i05.txt', 'instances/i06.txt', 'instances/i07.txt', 'instances/i08.txt', 'instances/i09.txt', 'instances/i10.txt']
    for file in files:
        info = read_instance(file)
        res = []
        v = []
        t = []
        s = []
        n = 1
        for i in range(n):
            init_state = State(info[0], info[1])
            bp_problem = BinPacking(init_state)
            step_limit = 100
            (node, steps, duration) = maxvalue(bp_problem, step_limit)
            res.append(len(node.state.fullness))
            v.append(node.value())
            s.append(steps)
            t.append(duration)

        print(sum(res)/n)
        print(sum(v)/n)
        print(sum(t)/n)
        print(sum(s)/n)
        
'''

if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1])
    bp_problem = BinPacking(init_state)
    step_limit = 100
    (node, step, time) = maxvalue(bp_problem, step_limit)
    state = node.state
    print(state)