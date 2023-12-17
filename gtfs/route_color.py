_old_frequent = set(['6', '7', '10', '11', '12', '14', '25', '40',
                 '44', '51', '53', '80', '85', '87', '88', '90', '111'])
_old_rapid = set(['39', '45', '57', '61', '62', '63', '74', '75', '97', '98', '99'])
_old_connexion = set(['221', '222', '228', '231', '232',
                  '234', '236', '237', '252', '256', '257', '258', '261', '262', '263', '264', '265', '267', '268', '270', '271', '272', '273', '277', '278', '282', '283', '284', '290', '291', '294', '299'])

# TODO: Check if the 10 is still considered frequent
_new_frequent = set(['5', '6', '7', '11', '12', '14', '25', '40', '41', '44', '45',
                 '61', '62', '63', '68', '74', '75', '80', '85', '88', '90', '98', '111'])
_new_connexion = set(['221', '222', '228', '234', '237', '256', '261',
                  '262', '263', '265', '266', '275', '276', '277', '283', '294', '299'])

_colors = {
    "regular": "#212121",
    "frequent": "#F68E1D",
    "rapid": "#0074BF",
    "connexion": "#9B5BA4",
}


def route_color(route_number, mode="old"):
    if mode == "old":
        if route_number in _old_frequent:
            return _colors["frequent"]
        elif route_number in _old_rapid:
            return _colors["rapid"]
        elif route_number in _old_connexion:
            return _colors['connexion']
        else:
            return _colors['regular']
    elif mode == "new":
        if route_number in _new_frequent:
            return _colors["frequent"]
        elif route_number in _new_connexion:
            return _colors['connexion']
        else:
            return _colors['regular']
    else:
        raise ValueError("'mode' must be 'new' or 'old")
