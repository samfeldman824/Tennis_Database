# pylint: disable-all
import pandas as pd

shot_dictionary = {
    "j": ["Shot Type", "forehand"],
    "k": ["Shot Type", "backhand"],
    "u": ["Shot Type", "fh slice"],
    "i": ["Shot Type", "bh slice"],
    "o": ["Shot Type", "fh volley"],
    "p": ["Shot Type", "bh volley"],
    "l": ["Shot Type", "overhead"],
    "n": ["Shot Type", "fh dropshot"],
    "m": ["Shot Type", "bh dropshot"],
    "g": ["Shot Type", "fh lob"],
    "h": ["Shot Type", "bh lob"],
    "*": ["Rally Ending", "Winner"],
    "@": ["Rally Ending", "Unforced Error"],
    "#": ["Rally Ending", "Forced Error"],
    "!": ["Rally Ending", "Fault"],
    "1": ["Shot Direction", "line"],
    "2": ["Shot Direction", "middle"],
    "3": ["Shot Direction", "cross"],
    "4": ["Shot Direction", "inside-out"],
    "5": ["Shot Direction", "inside-in"],
    "6": ["Shot Direction", "t"],
    "7": ["Shot Direction", "body"],
    "8": ["Shot Direction", "wide"],
    "w": ["Location", "wide"],
    "d": ["Location", "deep"],
    "n": ["Location", "net"]
}


string1 = "6b3b1f3b2f2f1f3b3b3s3b3b3b3s3b1f2b3s2f1n@"
string2 = "7b3b2f4s2s3v3o5z2f4d@"
shots_list = ["j", "k", "u", "i", "o", "p", "l", "n", "m", "g", "h"]
players = ['Sam Feldman', 'Corey Craig']

def parse_point(point: str, shots_list: list) -> list:
    substrings = []
    current_substring = ""
    # substrings.append(point[0])

    only_serve = True
    char_index = 0
    for char in point:
        if char in shots_list:
            only_serve = False
            break
        char_index += 1
    
    if not only_serve:
        substrings.append(point[0:char_index])
        i = char_index
        while i < len(point):
            char = point[i]
            if char in shots_list:
                # Add the current character and the characters after it until the next "f" or "b"
                j = i + 1
                while j < len(point) and point[j] not in shots_list:
                    j += 1
                current_substring = point[i:j]
                # Add the current substring to the list
                if current_substring != "":
                    # print(current_substring)
                    substrings.append(current_substring)
                i = j
        # substrings.pop(0)
        return substrings
    else:
        return [point]

# print(parse_point(my_string, shots_list))  # Output: ['f3d@', 'b3n']

def parse_shots(shots: list, shot_options: dict, first_or_second: str, players: list, server: str, score: str):
    headers = ['Shot Type', 'Shot Direction', 'Rally Ending', 'Location', 'Return', 'Player', 'Score']
    df = pd.DataFrame(columns=headers)

    table_i = 0

    if players[0] != server:
        players[1] = players[0]
        players[0] = server
        

    for index, shot in enumerate(shots):
        if index % 2 == 0:
            df.at[table_i, 'Player'] = players[0]
        else:
            df.at[table_i, 'Player'] = players[1]

        

        # print(shot)
        if index == 0:
            serve = shot[0]
            mapped_serve = shot_options[serve]
            df.at[table_i, 'Shot Direction'] = mapped_serve[1]
            df.at[table_i, 'Shot Type'] = first_or_second + ' serve'
            if first_or_second == 'first':
                df.at[table_i, 'Score'] = score
            else:
                df.at[table_i, 'Score'] = ''
        else:
            df.at[table_i, 'Score'] = ''
        

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
    df['Rally Ending'].fillna('in', inplace=True)

    return df
    # print(df)

def parse_match(filepath: str):
    match_df = pd.DataFrame()
    df = pd.read_csv(filepath)
    players_column = df['Players'].to_list()
    players = [players_column[0], players_column[1]]

    for index, row in df[["Server", "Score", "1st", "2nd", ]].iterrows():
        point_df = pd.DataFrame()
        point_df2 = pd.DataFrame()
        server = str(row.values.tolist()[0])
        game_score = str(row.values.tolist()[1])
        first_serve = str(row.values.tolist()[2])
        second_serve = str(row.values.tolist()[3])
        shots = parse_point(first_serve, shots_list)
        point_df = parse_shots(shots, shot_dictionary, 'first', players, server, game_score)

        if second_serve != 'nan':
            shots = parse_point(second_serve, shots_list)
            point_df2 = parse_shots(shots, shot_dictionary, 'second', players, server, game_score)
        
        point_df = pd.concat([point_df, point_df2], axis=0)
        point_df = point_df.reset_index(drop=True)
        match_df = pd.concat([match_df, point_df], axis=0)
    return match_df

# match_df = parse_match('/Users/samfeldman/Desktop/Tennis_Database/points_sheet.csv')
# print(match_df)


# shots_list1 = parse_point(string1, shots_list)
# shots_list2 = parse_point(string2, shots_list)
# # shots_list = ['8', 'f3', 'f4', 'b1', 's3', 'z3', 'o1*']
# df1 = parse_shots(shots_list1, shot_dictionary, ['Sam Feldman', 'Roger Chou'])
# df2 = parse_shots(shots_list2, shot_dictionary, ['Sam Feldman', 'Roger Chou'])

# combined_df = pd.concat([df1, df2], axis=0)
# combined_df = combined_df.reset_index(drop=True)
# print(combined_df)


# print(parse_point("7w*f4b2s4", shots_list))
# print(parse_point("7n", shots_list))
match_df = parse_match('./csvs/corey.csv')
print(match_df)
# print(parse_point("7b3f3b2s3f3*", shots_list))