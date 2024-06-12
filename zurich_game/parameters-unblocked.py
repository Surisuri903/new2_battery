step_to_tile = dict(
    up=dict(
        up='v', right='tr', left='tl'
    ),
    left=dict(
        left='h', up='br', down='tr'
    ),
    down=dict(
        down='v', right='br', left='bl'
    ),
    right=dict(
        right='h', up='bl', down='tl'
    )
)

game_parameters = {
    'rows': 15,
    'cols': 15,
    'atlas': 'atlas.png',
    'atlas_transparent': 'atlas_transparent.png',
    'players': ['ego', 'alter'],
    'start': {'ego': [7, 0, ''], 'alter': [7, 14, '']},  # TODO: fix inversion of rows and cols coordinate
    'ego_position': 0,
    'alter_position': 0,
    'tiles': {
        'steps': {'h': 1, 'v': 2, 'tr': 3, 'tl': 4, 'br': 5, 'bl': 6},
        'first_steps': {'ego': {'h': 15, 'v': 16}, 'alter': {'h': 17, 'v': 18}},
        'treasures': {'r': 7, 'l': 8, 't': 9, 'b': 10},
        'items': {'stones': 12, 'stone': 11, 'trees': 14, 'tree': 13},
        'starts': {'ego': 19, 'alter': 20}
    },
    'paths_length': 26,
    'n_paths': 4,
    'path_status': [True, False],
    'n_doors': 6,
    'n_doors_per_row': 3,
    'door_types': ['red', 'blue'],
    'use_fixed_falling_door_interval': True,
    'falling_door_interval': 10,
    'seconds_to_open_door': 30,
    'sounds': ['door_falling', 'door_opening', 'crying', 'dying', 'winning'],
    'sec_per_trial': 30
}

game_status_default = dict(
    timestamp=None,
    ego_path=-1,
    ego_position=0,
    ego_helped=0,
    ego_lost=False,
    alter_position=0,
    ego_num_doors_open=0,
    keys=dict(ego=[], alter=[]),  # each list with sequence of 'red'/'blue'
    death_timers_start=dict(ego=[], alter=[]),
    dead_players=[],
    timeout=False
)

trials = [
    {
        'type':       'instructions',
        'doors':      [{'time': 5, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 10, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 15, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 20, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 25, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 30, 'color': 'red', 'player': 'alter', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': []},
        'help_other': 'no_help_needed'
    },
    {
        'type':       'instructions',
        'doors':      [{'time': 5, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 10, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 15, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 20, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 25, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 30, 'color': 'red', 'player': 'ego', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': []},
        'help_other': 'no_help_needed'
    },
    {
        'type':       'practice',
        'doors':      [{'time': 7, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 10, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 18, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 22, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 27, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 29, 'color': 'blue', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'help'
    },
    {
        'type':       'practice',
        'doors':      [{'time': 3, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 10, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 13, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 16, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 20, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 25, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'defect'
    },
     {
        'type':       'practice',
        'doors':      [{'time': 2, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 8, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 15, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 20, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 33, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 25, 'color': 'red', 'player': 'alter', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'no_help_needed'
    },
    {
        'type':       'practice',
        'doors':      [{'time': 10, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 15, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 20, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 25, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 27, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 31, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'defect'
    },
{
        'type':       'reciprocity', # 7
        'doors':      [{'time': 4, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 12, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 21, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 32, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 37, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 41, 'color': 'blue', 'player': 'ego', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
{
        'type':       'reciprocity', # 12
        'doors':      [{'time': 3, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 11, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 22, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 28, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 32, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 39, 'color': 'red', 'player': 'ego', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
{
        'type':       'reciprocity', # 8
        'doors':      [{'time': 2, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 12, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 22, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 31, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 37, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 40, 'color': 'blue', 'player': 'ego', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
{
        'type':       'reciprocity', # 9
        'doors':      [{'time': 3, 'color': 'red', 'player': 'ego', 'active': True},
                       {'time': 11, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 21, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 25, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 29, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 33, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
{
        'type':       'reciprocity', # 11
        'doors':      [{'time': 4, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 14, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 23, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 33, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 38, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 42, 'color': 'red', 'player': 'alter', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
    {
        'type':       'reciprocity', # 10
        'doors':      [{'time': 2, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 9, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 18, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 23, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 28, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 32, 'color': 'blue', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'tit_for_tat'
    },
{
        'type':       'baseline', # 1
        'doors':      [{'time': 2, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 11, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 16, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 22, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 25, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 31, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    },
{
        'type':       'baseline', # 2
        'doors':      [{'time': 3, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 11, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 19, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 23, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 28, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 31.5, 'color': 'blue', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    },
{
        'type':       'baseline', # 6
        'doors':      [{'time': 3, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 8, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 13, 'color': 'red', 'player': 'alter', 'active': False},
                       {'time': 19, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 23, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 30, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    },
{
        'type':       'baseline', # 4
        'doors':      [{'time': 2, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 5, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 13, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 18, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 24, 'color': 'red', 'player': 'alter', 'active': True},
                       {'time': 31, 'color': 'red', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    },
{
        'type':       'baseline', # 3
        'doors':      [{'time': 4, 'color': 'red', 'player': 'ego', 'active': False},
                       {'time': 10, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 15, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 21, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 28, 'color': 'blue', 'player': 'ego', 'active': True},
                       {'time': 31.5, 'color': 'blue', 'player': 'ego', 'active': False}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    },
    {
        'type':       'baseline', # 5
        'doors':      [{'time': 3, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 7, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 12, 'color': 'blue', 'player': 'ego', 'active': False},
                       {'time': 18, 'color': 'blue', 'player': 'alter', 'active': False},
                       {'time': 24, 'color': 'blue', 'player': 'alter', 'active': True},
                       {'time': 31, 'color': 'blue', 'player': 'ego', 'active': True}],
        'keys':       {'ego': ['blue', 'red'], 'alter': ['blue', 'red']},
        'help_other': 'dies_if_helped'
    }
]
