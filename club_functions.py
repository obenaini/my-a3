""" CSC108 Assignment 3: Club Recommendations 
Author: Ossama Benaini
Student number: 1006092933
"""

from typing import List, Tuple, Dict, TextIO

##### Sample Data (Used by Doctring examples) #####

P2F = {'Jesse Katsopolis': ['Danny R Tanner', 'Joey Gladstone',
                            'Rebecca Donaldson-Katsopolis'],
       'Rebecca Donaldson-Katsopolis': ['Kimmy Gibbler'],
       'Stephanie J Tanner': ['Michelle Tanner', 'Kimmy Gibbler'],
       'Danny R Tanner': ['Jesse Katsopolis', 'DJ Tanner-Fuller',
                          'Joey Gladstone']}

P2C = {'Michelle Tanner': ['Comet Club'],
       'Danny R Tanner': ['Parent Council'],
       'Kimmy Gibbler': ['Rock N Rollers', 'Stamp Club'],
       'Jesse Katsopolis': ['Parent Council', 'Rock N Rollers'],
       'Joey Gladstone': ['Comics R Us', 'Parent Council']}


##### Helper functions #####
def recommend_club_pts_friend(person_to_friends: Dict[str, List[str]],
                              person_to_clubs: Dict[str, List[str]],
                              person: str,) -> List[str]:
    """Returns list of club recommendations and their associated amount of
       points depending on the the clubs in which their friends belong to

       >>> recommend_club_pts_friend(P2F, P2C, "Rebecca Donaldson-Katsopolis")
       [('Rock N Rollers', 1), ('Stamp Club', 1)]
       >>> recommend_club_pts_friend(P2F, P2C, "Danny R Tanner")
       [('Comics R Us', 1), ('Rock N Rollers', 1)]
    """
    lst = []
    c = get_clubs_of_friends(person_to_friends, person_to_clubs, person)
    for i in range(len(c)):
        c[i] = (c[i], 1)
    lst = c
    return lst

def recommend_clubs_pts_clubs(person_to_clubs: Dict[str, List[str]],
                              person: str,) -> List[str]:
    """Returns list of club recommendations and their associated amount of
       points depending on members of potential clubs.

       >>> recommend_clubs_pts_clubs(P2C, 'Jesse Katsopolis')
       [('Parent Council', 1), ('Rock N Rollers', 1)]
       """
    lst = []
    people = []
    pot_clubs = []
    inverted = invert_and_sort(person_to_clubs)
    if person in person_to_clubs.keys():
        clubs = person_to_clubs[person]
    else:
        return []
    
    for club in clubs:
        if person in inverted[club]:
            people = inverted[club]
        for pot_person in people:
            if pot_person in person_to_clubs.keys():
                pot_clubs = person_to_clubs[pot_person]
            for clubsss in pot_clubs:
                if clubsss not in person_to_clubs[person]:
                    lst.append((club, 1))
    return lst
                    
 

##### Required functions #####

def load_profiles(profiles_file: TextIO) -> Tuple[Dict[str, List[str]],
                                                  Dict[str, List[str]]]:
    """Return a two-item tuple containing a "person to friends" dictionary
    and a "person_to_clubs" dictionary with the data from profiles_file.

    NOTE: Functions (including helper functions) that have a parameter of type
          TextIO do not need docstring examples.
    """
    person, clubs = {}, {}
    prev_line = "\n"
    key = ""
    for line in profiles_file:
        new_line = line.strip()
        if "," in new_line and prev_line == "\n":
            index = new_line.index(",")
            key = new_line[index + 2:] + " " + new_line[:index]
        elif prev_line != "\n" and "," in new_line:
            new_index = new_line.index(",")
            new_name = new_line[new_index + 2:] + " " + new_line[:new_index]
            person.setdefault(key, []).append(new_name)
        elif prev_line != "\n" and "," not in new_line and new_line != "":
            clubs.setdefault(key, []).append(new_line)
        prev_line = line
    for key, values in person.items():
        person[key] = sorted(values)
    for key, values in clubs.items():
        clubs[key] = sorted(values)
    return (person, clubs)
    

def get_average_club_count(person_to_clubs: Dict[str, List[str]]) -> float:
    """Return the average number of clubs that a person in person_to_clubs
    belongs to.

    >>> get_average_club_count(P2C)
    1.6
    """
    total_clubs = 0
    total_values = 0
    for sublist in person_to_clubs.values():
        total_clubs += len(sublist)
        total_values += 1
    if total_values == 0:
        return 0.0
    else:
        return total_clubs / total_values

def get_last_to_first(
        person_to_friends: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Return a "last name to first name(s)" dictionary with the people from the
    "person to friends" dictionary person_to_friends.

    >>> get_last_to_first(P2F) == {
    ...    'Katsopolis': ['Jesse'],
    ...    'Tanner': ['Danny R', 'Michelle', 'Stephanie J'],
    ...    'Gladstone': ['Joey'],
    ...    'Donaldson-Katsopolis': ['Rebecca'],
    ...    'Gibbler': ['Kimmy'],
    ...    'Tanner-Fuller': ['DJ']}
    True
    """
    d = {}
    for key in person_to_friends.keys():
        index = key.index(" ")
        if " " in key[index + 1:]:
            index = key.index(" ", index + 1)
        k_last, k_first = key[index + 1:], key[:index]
        if k_last not in d.keys():
            d.setdefault(k_last, [k_first])
        elif k_last in d.keys() and k_first not in d[k_last]:
            d.setdefault(k_last, d[k_last]).append(k_first)
    for value in person_to_friends.values():
        for person in value:
            index = person.index(" ")
            if " " in person[index + 1:]:
                index = person.index(" ", index + 1)
            v_last, v_first = person[index + 1:], person[:index]
            if v_last not in d.keys():
                d.setdefault(v_last, [v_first])
            elif v_last in d.keys() and v_first not in d[v_last]:
                d.setdefault(v_last, d[v_last]).append(v_first)
    for keys, values in d.items():
        d[keys] = sorted(values)
    return d

def invert_and_sort(key_to_value: Dict[object, object]) -> Dict[object, list]:
    """Return key_to_value inverted so that each key is a value (for
    non-list values) or an item from an iterable value, and each value
    is a list of the corresponding keys from key_to_value.  The value
    lists in the returned dict are sorted.

    >>> invert_and_sort(P2C) == {
    ...  'Comet Club': ['Michelle Tanner'],
    ...  'Parent Council': ['Danny R Tanner', 'Jesse Katsopolis',
    ...                     'Joey Gladstone'],
    ...  'Rock N Rollers': ['Jesse Katsopolis', 'Kimmy Gibbler'],
    ...  'Comics R Us': ['Joey Gladstone'],
    ...  'Stamp Club': ['Kimmy Gibbler']}
    True
    """
    d = dict()
    if key_to_value == {}:
        return {}
    for key, value in key_to_value.items():
        if type(value) == list:
            for element in value:
                d.setdefault(element, list()).append(key)
        else:
            d.setdefault(value, list()).append(key)
    if len(d.values()) > 1:
        for new_key, new_value in d.items():
            d[new_key] = sorted(new_value)
    return d


def get_clubs_of_friends(person_to_friends: Dict[str, List[str]],
                         person_to_clubs: Dict[str, List[str]],
                         person: str) -> List[str]:
    """Return a list, sorted in alphabetical order, of the clubs in
    person_to_clubs that person's friends from person_to_friends
    belong to, excluding the clubs that person belongs to.  Each club
    appears in the returned list once per each of the person's friends
    who belong to it.

    >>> get_clubs_of_friends(P2F, P2C, 'Danny R Tanner')
    ['Comics R Us', 'Rock N Rollers']
    """
    lst = []
    if person in person_to_friends.keys():
        friends = person_to_friends[person]
    else:
        return []
    for friend in friends:
        if friend in person_to_clubs.keys():
            for club in person_to_clubs[friend]:
                if person not in person_to_clubs.keys():
                    lst.append(club)    
                elif club not in person_to_clubs[person]:
                    lst.append(club)
    lst.sort()
    return lst


def recommend_clubs(
        person_to_friends: Dict[str, List[str]],
        person_to_clubs: Dict[str, List[str]],
        person: str,) -> List[Tuple[str, int]]:
    """Return a list of club recommendations for person based on the
    "person to friends" dictionary person_to_friends and the "person
    to clubs" dictionary person_to_clubs using the specified
    recommendation system.

    >>> recommend_clubs(P2F, P2C, 'Stephanie J Tanner',)
    [('Comet Club', 1), ('Rock N Rollers', 1), ('Stamp Club', 1)]
    """
    rec1 = recommend_club_pts_friend(person_to_friends, person_to_clubs, person)
    rec2 = recommend_clubs_pts_clubs(person_to_clubs, person)
    new_list = []
    if rec2 == []:
        return rec1
    for elements in rec1:
        for sublist in rec2:
            if elements[0] == sublist[0]:
                new_value = elements[1] + sublist[1]
                new_list.append((elements[0], new_value))
            elif elements[0] != sublist[0]:
                new_list.append(elements)
                new_list.append(sublist)
    
    return new_list



if __name__ == '__main__':
    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    import doctest
    doctest.testmod()

    # Required test files
    doctest.testfile("test_get_average_club_count.txt")
    doctest.testfile("test_get_last_to_first.txt")
