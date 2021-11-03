import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button
import numpy as np
from collections import deque
from typing import Tuple, List

# === constants ===
NUMBER_OF_ROWS = 20
NUMBER_OF_COLUMNS = 20
COLOR_DEAD = ('black', 'white')
COLOR_ALIVE = ('white','black')
SAMPLETIME = 500 # ms

# === variables ===
initialized = False # indicates the start of life
states = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)) # keeps track of the cells states
cells_alive_now = deque() # all cells currently alive
cells_alive_tmr = deque() # cells alive next iteration
dead_cells_in_nbhd = deque() # all dead cells in the neighborhood of cells alive
change_to_dead = deque() # cells which will cange state to dead next iteration
change_to_alive = deque() # cells which will change state to alive next iteration

# === PySimpleGui stuff ===
grid = [[sg.Button('', size=(1,1), key=(i,j), pad=(0,0), button_color=COLOR_DEAD) for j in range(NUMBER_OF_COLUMNS)] for i in range(NUMBER_OF_ROWS)]
layout =  [
    grid,
    [sg.Button('start'), sg.Button('reset')]
]
window = sg.Window('Conways Game of Life',layout)

# === functions ===
def get_neighbors(cell: Tuple) -> List[Tuple]:
    neighbors = []
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if x==0 and y==0:
                continue
            x_new = cell[0] + x
            y_new = cell[1] + y
            if x_new < 0 or x_new > NUMBER_OF_COLUMNS-1:
                continue
            if y_new < 0 or y_new > NUMBER_OF_ROWS-1:
                continue
            neighbors.append((x_new, y_new))
    return neighbors

# === main loop ===
while True:
    event, values = window.read(timeout=SAMPLETIME)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'reset':
        for cell in cells_alive_now:
            window[cell].update(button_color=COLOR_DEAD)
        initialized = False
        states = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        cells_alive_now = deque()
        cells_alive_tmr = deque()
        dead_cells_in_nbhd = deque()
        change_to_dead = deque()
        change_to_alive = deque()

    if not initialized:
        if event == 'start':
            initialized = True
        elif type(event) is tuple:
            window[event].update(button_color=COLOR_ALIVE)
            cells_alive_now.append(event)
            states[event] = 1
        else:
            continue
    else:
        # evolute all cells alive
        for cell in cells_alive_now:
            neighbors = get_neighbors(cell)
            count_alive = 0
            for neighbor in neighbors:
                state = states[neighbor]
                if not state:
                    if cell not in dead_cells_in_nbhd:
                        dead_cells_in_nbhd.append(neighbor)
                else:
                    count_alive += state
            if count_alive < 2 or count_alive > 3:
                change_to_dead.append(cell)
            else:
                cells_alive_tmr.append(cell)
        # evolute all dead cells in nbhd
        while dead_cells_in_nbhd:
            cell = dead_cells_in_nbhd.popleft()
            neighbors = get_neighbors(cell)
            count_alive = 0
            for neighbor in neighbors:
                count_alive += states[neighbor]
            if count_alive == 3:
                if cell not in change_to_alive:
                    change_to_alive.append(cell)
                if cell not in cells_alive_tmr:
                    cells_alive_tmr.append(cell)

        while change_to_dead:
            cell = change_to_dead.popleft()
            states[cell] = 0
            window[cell].update(button_color=COLOR_DEAD)

        while change_to_alive:
            cell = change_to_alive.popleft()
            states[cell] = 1
            window[cell].update(button_color=COLOR_ALIVE)

        cells_alive_now = cells_alive_tmr.copy()
        cells_alive_tmr = deque()
        h = 0



            

window.close()