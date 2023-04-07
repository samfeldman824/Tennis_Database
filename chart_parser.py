# pylint: disable-all
import pandas as pd

shot_dictionary = {
    "f": ["Shot Type", "forehand"],
    "b": ["Shot Type", "backhand"],
    "r": ["Shot Type", "fh slice"],
    "s": ["Shot Type", "bh slice"],
    "v": ["Shot Type", "fh volley"],
    "z": ["Shot Type", "bh volley"],
    "o": ["Shot Type", "overhead"],
    "*": ["Rally Ending", "Winner"],
    "@": ["Rally Ending", "Unforced Error"],
    "#": ["Rally Ending", "Forced Error"],
    "1": ["Shot Direction", "cross"],
    "2": ["Shot Direction", "middle"],
    "3": ["Shot Direction", "line"],
    "4": ["Shot Direction", "inside-out"],
    "5": ["Shot Direction", "inside-in"],
    "6": ["Shot Direction", "wide"],
    "7": ["Shot Direction", "body"],
    "8": ["Shot Direction", "t"],
    "w": ["Location", "wide"],
    "d": ["Location", "deep"],
    "n": ["Location", "net"]
}


my_string = "6b3b1f3b2f2f1f3b3b3s3b3b3b3s3b1f2b3s2f1n@"
shots_list = ["f", "b", "r", "s", "v", "z", "o"]

def parse_point(point: str, shots_list: list) -> list:
    substrings = []
    current_substring = ""
    substrings.append(point[0])

    i = 1
    while i < len(point):
        char = point[i]
        if char in shots_list:
            # Add the current character and the characters after it until the next "f" or "b"
            j = i + 1
            while j < len(point) and point[j] not in shots_list:
                j += 1
            current_substring = point[i:j]
            # Add the current substring to the list
            substrings.append(current_substring)
            i = j
    return substrings

# print(parse_point(my_string, shots_list))  # Output: ['f3d@', 'b3n']

def parse_shots(shots: list, shot_options: dict, players: list):
    headers = ['Shot Type', 'Shot Direction', 'Location', 'Type of Miss', 'Return', 'Player']
    df = pd.DataFrame(columns=headers)

    table_i = 0
    for index, shot in enumerate(shots):
        if index % 2 == 0:
            df.at[table_i, 'Player'] = players[0]
        else:
            df.at[table_i, 'Player'] = players[1]

        if index == 0:
            serve = shot[0]
            mapped_serve = shot_options[serve]
            df.at[table_i, 'Shot Direction'] = mapped_serve[1]
            df.at[table_i, 'Shot Type'] = "serve"
        

        if index == 1:
            df.at[table_i, 'Return'] = True
        else:
            df.at[table_i, 'Return'] = False
        i = 0
        while i < len(shot):
            char = shot[i]
            mapped_char = shot_options[char]
            column = mapped_char[0]
            stat = mapped_char[1]
            df.at[table_i, column] = stat
            i += 1
        table_i += 1

    df['Location'].fillna('in', inplace=True)
    df['Type of Miss'].fillna('in', inplace=True)
    df['Rally Ending'].fillna('in', inplace=True)

    print(df)
    
shots_list = parse_point(my_string, shots_list)
# shots_list = ['8', 'f3', 'f4', 'b1', 's3', 'z3', 'o1*']
parse_shots(shots_list, shot_dictionary, ['Sam Feldman', 'Roger Chou'])

