from copy import deepcopy
from random import shuffle
from itertools import permutations
import time

# коды перемещений колец:
# куда  0  1  2
# из 0     0  1
# из 1  2     3
# из 2  4  5  
CODE_TABLE = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

EMPTY_LIST = [] # пустой лист
RINGS = 5 # количество колец

# сортированные башни
SORTED_TOWER = [list(range(i, 0, -1)) for i in range(0, RINGS+1)]

s_moves_history = [] # временно хранит промежуточные истории ходов
limites = [] # временно хранит накладываемые на расчеты ограничения

def get_sample(rings=5):
    """
    Создает новую  несортированную раскладку
    """
    first_tower = list(range(rings, 0, -1))
    shuffle(first_tower)
    return [first_tower, [], []]

def last_index(history, towers):
    """
    Возвращает индекс последнего вхождения towers в history или -1, 
    если элемент отсутсвует в истории
    """
    index = -1
    while True:
        try:
            index = history.index(towers, index+1, len(history) - 1)
        except ValueError:
            return index

def is_solved(towers, rings):
    """
    Возвращает True, если задача решена
    """
    sorted_l = SORTED_TOWER[rings]
    return ((towers[0] == EMPTY_LIST) and 
             (towers[1] == sorted_l) and (towers[2] == EMPTY_LIST))

def get_available_moves(towers):
    """
    Возвращает лист возможный ходов
    """
    available_moves = []
    for i, move_code in enumerate(CODE_TABLE):
        from_, to_ = move_code
        if (towers[from_] != EMPTY_LIST):
            if ((towers[to_] == EMPTY_LIST) or 
                (towers[from_][-1] < towers[to_][-1])):
                available_moves.append(i)
    return available_moves

def get_bad_moves(towers, towers_history, moves_history, rings=0):
    """
    Возвращает лист плохих ходов
    """
    global RINGS
    sorted_l = SORTED_TOWER[rings]
    bad_moves = []
    n_in_history = last_index(towers_history, towers)
    if n_in_history != -1:
        bad_moves.append(moves_history[n_in_history])
    if (towers[1] == sorted_l[:len(towers[1])]) and (towers[1] != EMPTY_LIST):
        bad_moves.append(2)
        bad_moves.append(3)
    return bad_moves

def get_good_moves(towers, available_moves, ring):
    """
    Возвращает лист хороших ходов
    """
    good_moves = []
    sorted_l = SORTED_TOWER[ring]
    for m in available_moves:
        from_, to_ = CODE_TABLE[m]  
        if (to_ != 1) and (towers[1] == []) and (len(towers[from_]) > 1):
            if (towers[from_][-2] == ring):
                good_moves.append(m)
                break
        if ((ring > 2) and 
            (to_ == 2) and
            (from_ == 0) and
            (len(towers[to_]) == 1) and
            (towers[to_][0] == ring - 1) and 
            (towers[from_][-1] == ring - 2)):
            good_moves.append(m)
            break  
        if (towers[to_] == EMPTY_LIST): 
            if ((towers[from_][-1] == ring) and (to_ == 1)): 
                good_moves.append(m)
                break
        if ((to_ == 2) and 
            (towers[from_][-1] == ring - 1) and 
            (towers[to_] == [])):
            good_moves.append(m)
            break          
    return good_moves

def move(towers, move_code):
    """
    Производит указанное перемещение
    """
    from_, to_ = CODE_TABLE[move_code]
    towers[to_].append(towers[from_].pop())           

def get_tasks():
    """
    Возвращает список всех возможных задач
    """
    global RINGS
    tasks_list = []
    for i in permutations(range(1, RINGS + 1)):
        tasks_list.append([list(i), [], []])
    return tasks_list

def get_solution_helper(towers, ring, 
                        towers_history=[], moves_history=[], start=0):
    """
    Записывает решение в s_moves_history
    """
    global limites
    is_done = False
    h_1 = []
    if (start < limites[ring]):
        bad_moves = get_bad_moves(towers, towers_history, moves_history, ring)
        available_moves_wb = [move for move in get_available_moves(towers)
                                      if move not in bad_moves]
        good_moves = get_good_moves(towers, available_moves_wb, ring)
        
        for m in good_moves if len(good_moves) > 0 else available_moves_wb:
            clone_t = deepcopy(towers)        
            move(clone_t, m)
            clone_m = deepcopy(moves_history)
            clone_m.append(m)
            clone_h = deepcopy(towers_history)
            clone_h.append(clone_t)
            if len(clone_t[1]) == 1:
                if clone_t[1][0] == ring:
                    global s_moves_history
                    s_moves_history = clone_m
                    clone_t[1] = []
                    limites[ring] = start
                    return True, clone_t
            is_d, h = get_solution_helper(clone_t, 
                                          ring, 
                                          clone_h, 
                                          clone_m, 
                                          start + 1)
            if is_d:
                is_done = True
                h_1 = h
        if not is_done:
            return False, []
    return is_done, h_1

def get_solution(task):
    """
    Записывает решение задачи
    """  
    begin = time.time()
    global limites, s_moves_history
    ind_of_largest = 1
    try:
        ind_of_largest = task[0].index(RINGS) + 1
    except:
        pass
    limites = [0,]
    for i in range (RINGS - 1):
        limites.append(2 ** i)
    limites.append(2 ** (RINGS - ind_of_largest))
    moves_history = []
    h = deepcopy(task)
    for i in range (RINGS):
        b, h = get_solution_helper(h, RINGS - i)
        if not b:
            raise Exception(i, h)
        moves_history += s_moves_history
    end = time.time()
    print(f"Task: {task}, time: {end - begin:.2f}")
    return moves_history

def get_training_data():
    """
    Возвращает обучающий набор (tasks, targets)
    """
    targets = []
    tasks = get_tasks()
    for task in tasks:
        targets.append(get_solution(task))
    return tasks, targets

get_training_data()

