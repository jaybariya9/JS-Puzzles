import pandas as pd
import numpy as np
from collections import deque
import itertools

# define a function to compute factors of a positive integer
def factors(num):
    if num <= 0:
        print("number is non-positive")
    else:
        factor_list = [1]
        divisor = 2
        while divisor <= num:
            if num%divisor == 0:
                factor_list.append(divisor)
            divisor += 1
    return factor_list

# define a function to compute combinations of a n distinct positive integer
def combos(num,n,non_fact,thres):
    fact_list = factors(num) + non_fact
    all_combos = list(set(itertools.permutations(fact_list, n)))
    return [c for c in all_combos if sum(c) < thres]

# define a dictionary to map A,B,C (distinct positive integer) to a dictionary based on x,y co-ordinates
def puzzle_dict(A,B,C):
    puzz_dic = {(1,1):A, (1,2):A, (1,3):A, (1,4):A, (1,5):A, (1,6):A,
                (2,1):A, (2,2):A, (2,3):A, (2,4):A, (2,5):B, (2,6):B,
                (3,1):A, (3,2):A, (3,3):B, (3,4):B, (3,5):B, (3,6):B,
                (4,1):B, (4,2):B, (4,3):B, (4,4):B, (4,5):C, (4,6):C,
                (5,1):B, (5,2):B, (5,3):C, (5,4):C, (5,5):C, (5,6):C,
                (6,1):C, (6,2):C, (6,3):C, (6,4):C, (6,5):C, (6,6):C}
    return puzz_dic

# define a dictionary to map coordinates to a string 
def puzzle_map():
    puzz_map = {(1,1):'a1', (1,2):'a2', (1,3):'a3', (1,4):'a4', (1,5):'a5', (1,6):'a6',
                (2,1):'b1', (2,2):'b2', (2,3):'b3', (2,4):'b4', (2,5):'b5', (2,6):'b6',
                (3,1):'c1', (3,2):'c2', (3,3):'c3', (3,4):'c4', (3,5):'c5', (3,6):'c6',
                (4,1):'d1', (4,2):'d2', (4,3):'d3', (4,4):'d4', (4,5):'d5', (4,6):'d6',
                (5,1):'e1', (5,2):'e2', (5,3):'e3', (5,4):'e4', (5,5):'e5', (5,6):'e6',
                (6,1):'f1', (6,2):'f2', (6,3):'f3', (6,4):'f4', (6,5):'f5', (6,6):'f6'}
    return puzz_map

# define a function to get valid moves from a given x,y co-ordinates
def get_valid_moves(x, y):
    moves = [(x+1, y+2), (x-1,y+2), (x+1,y-2), (x-1,y-2), (x+2,y+1), (x+2,y-1), (x-2,y+1), (x-2,y-1)]
    return [(x, y) for x, y in moves if 1 <= x <= 6 and 1 <= y <= 6]

# define a function to get all valid paths 
def find_paths(start_x, start_y, end_x, end_y, max_moves):
    queue = deque([(start_x, start_y, [(start_x, start_y)], set([(start_x, start_y)]))])
    paths = []

    while queue:
        x, y, path, visited = queue.popleft()
        if (x, y) == (end_x, end_y) and len(path) <= max_moves:
            paths.append(path)
        if len(path) < max_moves:
            for new_x, new_y in get_valid_moves(x, y):
                if (new_x, new_y) not in visited:
                    new_visited = visited.copy()
                    new_visited.add((new_x, new_y))
                    queue.append((new_x, new_y, path + [(new_x, new_y)], new_visited))
    
    return paths

# define a function to compute score for a valid path
def compute_score(A,B,C,path):
    val = puzzle_dict(A,B,C)[path[0]]
    cum_score = puzzle_dict(A,B,C)[path[0]]
    for p in path[1:]:
        score = puzzle_dict(A,B,C)[p]
        if score == val:
            cum_score += score
        else: 
            cum_score = cum_score * score
        val = score
    return cum_score

# define a function to extract all paths where total points matches required score
def valid_path(A,B,C,route,req_score):
    valid_paths = []
    for path in route:
        if compute_score(A,B,C, path) == req_score:
            valid_paths.append(path)
    return valid_paths

# define a function to find valid solution to puzzle
def puzzle_solution(A,B,C, r1,r2, pt):
    vpath1 = valid_path(A,B,C,r1, req_score=pt)
    vpath2 = valid_path(A,B,C,r2, req_score=pt)
    if len(vpath1) > 0 and len(vpath2) > 0:
        return vpath1, vpath2
    else:
        print("No solution found")
        return None
    
route1 = find_paths(start_x = 1, start_y = 1, end_x = 6, end_y = 6, max_moves = 7)
route2 = find_paths(start_x = 1, start_y = 6, end_x = 6, end_y = 1, max_moves = 7)

solution = []
vpaths1 = []
vpaths2 = []
for A,B,C in combos(num=2024,n=3,non_fact=[3,7],thres=50):
    vp1 = valid_path(A,B,C,route=route1,req_score=2024)
    vp2 = valid_path(A,B,C,route=route2,req_score=2024)
    if len(vp1) > 0 and len(vp2) > 0:
        s = (A,B,C,A+B+C)
        vpaths1.append(vp1)
        vpaths2.append(vp2)
        solution.append(s)

