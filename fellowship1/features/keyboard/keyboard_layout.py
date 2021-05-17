import os
import json
import numpy as np
from typing import Tuple


EMPTY_LETTER = "X"
KEYBOARD_LAYOUT_QWERTY = [["`", "1!", "2@", "3#", "4$", "5%", "6^", "7&", "8*", "9(", "0)", "-_", "=+"],
                          [EMPTY_LETTER, "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[{", "]}"],
                          [EMPTY_LETTER, "a", "s", "d", "f", "g", "h", "j", "k", "l", ";:", "'\"", "\\|"],
                          [EMPTY_LETTER, "z", "x", "c", "v", "b", "n", "m", ",<", ".>", "/?", EMPTY_LETTER, EMPTY_LETTER],
                          [EMPTY_LETTER, EMPTY_LETTER, " ", " ", " ", " ", " ", " ", " ", EMPTY_LETTER, EMPTY_LETTER, EMPTY_LETTER, EMPTY_LETTER]]

KEYBOARD_LAYOUT_QWERTY = np.asarray(KEYBOARD_LAYOUT_QWERTY)


def create_distance_key_layout_dict(keyboard_layout: np.ndarray, empty_letter: str = EMPTY_LETTER) -> dict:
    """
    Creates dictionary for every letter as a key. Values for keys are dictionaries
    with keys as letters and value as manhattan distance between key from main
    dictionary and key in sub dictionary.

    Parameters
    ----------
    keyboard_layout: np.ndarray
        Keyboard layout as array. Row should be equal, if there is empty space
        is should be filled with empty_letter.
    empty_letter: str
        Value which fill up empty spaces in keyboard_layout. It can't be one
        of the letters in keyboard_layout

    Returns
    -------
    out: dict
        Dictionary with values as dictionary
        e.g For QWERTY: {'q': {'w': 1,
                               'e': 2,}}
    """
    layout_dict = dict()
    for main_idx, main_letter in np.ndenumerate(keyboard_layout):
        single_letter_dict = dict()
        for row in range(keyboard_layout.shape[0]):
            for column in range(keyboard_layout.shape[1]):
                sub_letter = keyboard_layout[row, column]
                if sub_letter == empty_letter:
                    continue

                dist = abs(main_idx[0] - row) + abs(main_idx[1] - column)
                if main_letter == " ":
                    dist = helper_distance_for_space((row, column))
                elif sub_letter == " ":
                    dist = helper_distance_for_space(main_idx)

                if len(sub_letter) >= 2:
                    single_letter_dict[sub_letter[0]] = dist
                    single_letter_dict[sub_letter[1]] = dist
                else:
                    single_letter_dict[sub_letter] = dist

        if len(main_letter) >= 2:
            layout_dict[main_letter[0]] = single_letter_dict
            layout_dict[main_letter[1]] = single_letter_dict
        else:
            layout_dict[main_letter] = single_letter_dict

    return layout_dict


def helper_distance_for_space(not_space_letter_idx: Tuple[int, int]) -> int:
    """
    Helper function for create_distance_key_layout_dict.

    Compute distances between not_space_letter_idx and space " "
    and return the smallest distance.

    Parameters
    ----------
    not_space_letter_idx: Tuple[int, int]
        Index of letter fot compute distance

    Returns
    -------
    out: int
        The smallest distnce between not_space_letter_idx and space.

    Examples
    --------
    >>> dist = create_distance_key_layout_dict((1,5)) # letter "t" for QWERTY
    >>> print(dist)
    3
    """
    space_idx = [[4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8]]
    space_idx = np.asarray(space_idx)

    letter_idx = np.asarray([not_space_letter_idx]*7)
    distance_array = np.sum(abs(space_idx-letter_idx), axis=1)
    min_dist = min(distance_array)
    return min_dist

def create_neighbors_key_layout_dict(keyboard_layout: np.ndarray, empty_letter="X") -> dict:
    """
    Creates 8 lists were every one is pointed in other direction. Every direction
    is at multiples of 45 trigonometric degrees. Lists contain neighbouring letters
    in a given direction grouped in pairs.

    Parameters
    ----------
    keyboard_layout: np.ndarray
        Keyboard layout as array. Row should be equal, if there is empty space
        is should be filled with empty_letter.
    empty_letter: str
        Value which fill up empty spaces in keyboard_layout. It can't be one
        of the letters in keyboard_layout

    Returns
    -------
    out: dict
        Keys are the directions and values are list with pairs.
        Keys: ["list_left", "list_right", "list_down", "list_up", "list_45_degree",
               "list_135_degree", "list_225_degree", "list_315_degree"]

    """
    list_dict = dict()

    list_dict["list_left"] = []
    list_dict["list_right"] = []
    list_dict["list_down"] = []
    list_dict["list_up"] = []
    list_dict["list_45_degree"] = []
    list_dict["list_225_degree"] = []
    list_dict["list_135_degree"] = []
    list_dict["list_315_degree"] = []

    list_moves = [[0, -1], [0, 1], [1, 0], [-1, 0],         # left, right, down, up,
                  [-1, 1], [1, -1], [1, 1], [-1, -1]]       # 45, 135, 225, 315 degree

    def add_next_neighbor(current_idx: Tuple[int, int], current_letter: str, nei_row: int, nei_column: int,
                          key_layout: np.ndarray, direction_list: list, empty_letter: str):
        neighbor = key_layout[current_idx[0] + nei_row, current_idx[1] + nei_column]
        if neighbor == empty_letter:
            return
        if current_letter == " " and neighbor == " ":
            return
        for cl in current_letter:
            for nb in neighbor:
                direction_list.append(cl + nb)

    for idx, letter in np.ndenumerate(keyboard_layout):
        for move, direction_list_name in zip(list_moves, list_dict.keys()):
            try:
                add_next_neighbor(idx, letter, move[0], move[1], keyboard_layout,
                                  list_dict[direction_list_name], empty_letter)
            except IndexError:
                continue

    return list_dict


def save_to_json(dictionary_object, path: str = None, name: str = "key_layout_dist_qwerty.json"):
    """
    Save keyboard feature to json

    Parameters
    ----------
    dictionary_object:dict,list
        Object which should be saved as json
    path: str
        Path where json shoould be saved
    name: str
        Name of the saved file. Should end with ".json"

    Returns
    -------
    """
    if path is None:
        path = os.path("./")
    with open(os.path.join(path, name), 'w') as json_file:
        json.dump(dictionary_object, json_file)


def create_keyboard_layout_feature(keyboard_layout: np.ndarray, empty_letter: str = "X") -> Tuple[dict, dict]:
    """
    Creates features based on the keyboard layout.

   Parameters
    ----------
    keyboard_layout: np.ndarray
        Keyboard layout as array. Row should be equal, if there is empty space
        is should be filled with empty_letter.
    empty_letter: str
        Value which fill up empty spaces in keyboard_layout. It can't be one
        of the letters in keyboard_layout

    Returns
    -------
    out: Tuple[dict, dict]
        Return Tuple of created features. First is feature based on manhattan distance.
        Second is feature with 8 lists of adjacent letters.
    """
    key_layout_dist_dict = create_distance_key_layout_dict(keyboard_layout,empty_letter)
    key_layout_neighbor_lists = create_neighbors_key_layout_dict(keyboard_layout, empty_letter)

    return key_layout_dist_dict, key_layout_neighbor_lists

def create_keyboard_layout_position_dict(keyboard_layout: np.ndarray,
                                         empty_letter: str = "X",
                                         layout: str = "QWERTY") -> dict:
    """
    Create dictionary with keys as signs and values as indices of those keys in
    the keyboard_layout.
    In case you use different layout then QWERTY probably you should adjust
    indices for space " ".

    Parameters
    ----------
    keyboard_layout: np.ndarray
        Keyboard layout as numpy array. If it is uneven is should be filled
        with empty_letters to achive the same length of every row.
    empty_letter: str
        Filling of keyboard_layout in case of uneven rows.
    layout: str
        Type of keyboard layout

    Returns
    -------
    out: dict
        Dictionary with indices for signs form keyboard

    """
    position_dict = {}
    for idx, x in np.ndenumerate(keyboard_layout):
        if x == empty_letter:
            continue
        if x == " " and layout == "QWERTY":
            shape = keyboard_layout.shape
            idx[1] = shape[1] // 2  # change second idx on middle of the row for QWERTY
            try:
                position_dict[x] = idx
            except KeyError:
                continue
        if len(x) > 1:
            position_dict[x[0]] = idx
            position_dict[x[1]] = idx
        else:
            position_dict[x] = idx
    return position_dict


def cast_password_to_vector(password: str, position_dict: str) -> np.ndarray:
    """
    Creates vector from password based on the dict with keys as
    letters and values as their index on keyboard

    Parameters
    ----------
    password: str
        Well password is a password
    position_dict:dict

    Returns
    -------
    out: np.ndarray
        Vector of password
    """
    vector = np.asarray([position_dict[letter] for letter in password])
    vector = np.sum(vector, axis=0)
    return vector


