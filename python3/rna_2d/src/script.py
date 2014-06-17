#!/usr/bin/env python3
"""parallel map """
from shapedistance import *
from utility import *


CHUNK_SIZE = 50  # size of process jobs
NPROC = 4  # amount of processors available
THRESHOLD = 6  # amount of errors tolerated
SUBOPT_FILE = "result2.txt"  # input file


# parallel part (pretty coarse grained)
# ref: http://stackoverflow.com/questions/8329974/
import multiprocessing


def split_jobs(array):
    """creates an array of arrays for the positions over which to start"""
    num_of_jobs = len(array) // CHUNK_SIZE
    residual = len(array) % CHUNK_SIZE
    result = [[i for i in range(
        CHUNK_SIZE * x, CHUNK_SIZE * x + CHUNK_SIZE)] for x in range(
            0, num_of_jobs)]
    if residual != 0:
        result.append([i for i in range(num_of_jobs * CHUNK_SIZE, len(array))])
    return result


def calculate_centrality(positions, array, queue):
    """launch the unlabeled_distance conditional sum"""
    # the array has (dot_bracket, (Node, qt))
    result = []  # (position, cumulative_quantity)
    for position in positions:
        tree_1 = array[position][1][0]
        length_1 = len(array[position][0])
        result.append(-array[position][1][1])
        for (dot_bracket, (tree_2, qt)) in array:
            # only break if at the upper end
            length_2 = len(dot_bracket)
            #if(length_2 - length_1 < (-(THRESHOLD))):
            #    continue
            #elif(length_2 - length_1 < (THRESHOLD * 2)):
            #    break
            if(unlabeled_distance(tree_1, tree_2) < THRESHOLD):
                result[-1] += qt
    print("process at position {0} - {1} done".format(
          positions[0], positions[-1]))
    queue.put(list(zip(positions, result)))


if __name__ == '__main__':
    # fetch data
    data = fastaRead(SUBOPT_FILE)
    allData = []
    for (name, subopts) in data:
        allData += subopts

    allData = allData[1:10000]  # TODO change after confirmed it works
    S = ShapeSet()

    # add the subopts and transform into trees
    # (annotated with the number of times it was seen)
    for subopt in allData:
        S.add(subopt)
    print("number of abstract shapes = "+str(len(S)))
    # get back the array (dot_bracket, (tree, quantity))
    # organized by len(dot_bracket), increasing
    array = S.get_keys()

    # multiprocessing setup
    result_queue = multiprocessing.Queue()
    job_arrays = split_jobs(array)
    jobs = [multiprocessing.Process(target=calculate_centrality,
            args=(positions, array, result_queue)) for positions in job_arrays]

    # start the processes
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    results = []
    for i in [result_queue.get() for _ in jobs]:
        for j in i:
            results.append(j)

    # store the results
    #for (index, (dot_bracket, (_, qt))) in enumerate(S.get_keys()):
    #    print(str(index) + " " + dot_bracket+ " " + str(qt))
    #print(results)
    results.sort(key=lambda x: x[1], reverse=True)
    for (index, qt) in results:
        print(array[index][0]+ " " + str(qt))