from collections import namedtuple

GameCoord = namedtuple("GameCoord", ["last_round", "board_value", "placement"])


def convert_game_to_coords(game_dict):

    return GameCoord(
        last_round=game_dict['lastRound'],
        board_value=get_board_value(game_dict['units']),
        placement=game_dict['placement']
    )


def get_board_value(unit_list):

    return 0
