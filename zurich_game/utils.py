from .parameters import *
from typing import List
from itertools import accumulate, repeat
import random


def get_next_step(params: dict, row: int, col: int, rows, cols, map, rnd: random.Random):
    ego_start = row == params['start']['ego'][0] and col == params['start']['ego'][1]
    alter_start = row == params['start']['alter'][0] and col == params['start']['alter'][1]
    moves = []
    if not ego_start:
        if row != 0 and map[row - 1][col] == 0:
            moves.append([row - 1, col, 'up'])
        if col != 0 and map[row][col - 1] == 0:
            moves.append([row, col - 1, 'left'])
    if not alter_start:
        if row != rows - 1 and map[row + 1][col] == 0:
            moves.append([row + 1, col, 'down'])
        if col != cols - 1 and map[row][col + 1] == 0:
            moves.append([row, col + 1, 'right'])
    
    if moves:
        step = rnd.choice(moves)
        return step
    return None


def get_path(params: dict, start_tile, rows, cols, path_length, map_copy, rnd: random.Random):
    path = [start_tile]
    for step in range(path_length - 1):
        next_step = get_next_step(params, path[step][0], path[step][1], rows, cols, map_copy, rnd)
        if next_step:
            map_copy[next_step[0]][next_step[1]] = -1
            path.append(next_step)
        else:
            break
    return path


def set_path_on_map(path, path_length, map_copy, steps, treasures, step_to_tile: dict):
    for s in range(path_length):
        step = path[s]
        if s < path_length - 1:
            next_step = path[s + 1]
            if step[2] == '':
                map_copy[step[0]][step[1]] = 0
            else:
                tile = step_to_tile[step[2]][next_step[2]]
                map_copy[step[0]][step[1]] = steps[tile]
        else:
            if step[2] == 'right':
                map_copy[step[0]][step[1]] = treasures['r']
            elif step[2] == 'left':
                map_copy[step[0]][step[1]] = treasures['l']
            elif step[2] == 'up':
                map_copy[step[0]][step[1]] = treasures['t']
            elif step[2] == 'down':
                map_copy[step[0]][step[1]] = treasures['b']


def trace_path(params: dict, start_tile, rows, cols, path_length, map, rnd: random.Random) -> tuple:
    tiles = params['tiles']
    map_copy = map.copy()
    map_copy[start_tile[0]][start_tile[1]] = 1
    path = get_path(params, start_tile, rows, cols, path_length, map_copy, rnd)
    if len(path) == path_length:
        set_path_on_map(path, path_length, map_copy, tiles['steps'], tiles['treasures'], step_to_tile)
        return path, map_copy
    return None, None


def reset_map(game: dict) -> int:
    game['paths']['ego'] = []
    game['paths']['alter'] = []
    game['map'] = [[0 for row in range(game['rows'])] for col in range(game['cols'])]
    return 0


def get_doors_for_game(default_doors: List[dict], rnd: random.Random) -> List[dict]:
    doors = default_doors.copy()
    rnd.shuffle(doors)
    for n, door in enumerate(doors):
        door.update(
            id=f'door_{n}', order=default_doors.index(door),
            fallen=False, closed=False, step=None
        )
    return doors


def set_start_tiles_on_map(game: dict):
    ego_start, alter_start = game['start']['ego'], game['start']['alter']
    game['map'][game['rows'] * ego_start[0] + ego_start[1]] = game['tiles']['starts']['ego']
    game['map'][game['rows'] * alter_start[0] + alter_start[1]] = game['tiles']['starts']['alter']


def set_landscape_items(game: dict, rnd: random.Random):
    for item in [k for k in list(game['tiles']['items']) if f'num_{k}' in game]:
        idx = rnd.sample([i for i, t in enumerate(game['map']) if t == 0], game[f'num_{item}'])
        for i in idx:
            game['map'][i] = game['tiles']['items'][item]


def get_zurich_prosocial_game(params: dict, trials: List[dict], trial_num: int, rnd: random.Random) -> dict:
    game = params.copy()
    game.update(trials[trial_num])
    doors = get_doors_for_game(game['doors'], rnd)
    game.update(
        map=[[0 for row in range(game['rows'])] for col in range(game['cols'])],
        paths=dict(ego=[], alter=[]),
        doors=doors,
        doors_times=sorted(door['time'] for door in doors)
#            list(
 #               accumulate(repeat(game['falling_door_interval'], game['n_doors']))
  #          ) if game['use_fixed_falling_door_interval'] else [
   #             door['time'] for door in doors
    #        ])
    )

    n = 0
    start_tiles = ['ego', 'ego', 'alter', 'alter']
    rnd.shuffle(start_tiles)
    while n < game['n_paths']:
        role = start_tiles[n]
        path, map_copy = trace_path(
            params, game['start'][role], game['rows'], game['cols'], game['paths_length'] + 1, game['map'], rnd
        )
        if path:
            n += 1
            game['paths'][role].append(path)
            game['map'] = map_copy
        else:
            n = reset_map(game)

    game['map'] = [t for row in game['map'] for t in row]

    set_start_tiles_on_map(game)
    set_landscape_items(game, rnd)
    game['alter_path'] = rnd.choice([0, 1])
    game['alter_color'] = '#%02X%02X%02X' % (rnd.randint(100, 255), rnd.randint(100, 255), rnd.randint(100, 255))
    
    return game
