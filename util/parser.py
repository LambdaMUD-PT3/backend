import sys
from adventure.models import Player, Room

def parse_area(filename):
    '''
    Read from a ROM area file, and convert to our use.
    '''
    if len(filename) < 2:
        print("Error:: Missing filename for generate_rooms.")
        exit(0)

    area = {}
    roomsFound = False
    roomNum = None
    prevLine = None
    roomDesc = ""
    dirFound = None
    reverseDirs = {"n": "s", "s": "n", "e": "w", "w": "e", "u": "d", "d": "u"}
    count = 0

    with open(filename) as file:

        for line in file:

            line = line.strip()
            
            # Only read in the rooms
            if line == "#ROOMS":
                # print(f"DEBUG::roomsFound")
                roomsFound = True
                continue

            if roomsFound == True:
                # print(f"DEBUG::line::{line}")
                # A '#' signifies a new room.
                if "#" in line:
                    # count += 1
                    # if count > 5:
                    #     exit()
                    # print(f"DEBUG::# in line:{line}")
                    # a '#0' signifies end of section
                    if line == "#0":
                        print("End of rooms found.")
                        break

                    roomNum = line[1:]
                    # print(f"DEBUG::roomNum::{roomNum}")
                    if roomNum not in area.keys():
                        area[roomNum] = {}

                    area[roomNum].update( { "room_id": roomNum } )
                    prevLine = "roomNum"
                    continue

                # Line after roomNum is the room title
                if prevLine == "roomNum":
                    # print(f"DEBUG::roomName::{line[:-1]}")
                    area[roomNum].update( {"title" : line[:-1]} )
                    prevLine = "roomName"
                    continue

                # Lines after roomName are the description
                if prevLine ==  "roomName" and line != "~":
                    if len(line) < 1:
                        roomDesc += "\n"
                    else:
                        roomDesc += line + "\n"
                    continue
                elif prevLine == "roomName" and line == "~":
                    # print(f"DEBUG::desc::{roomDesc}")
                    area[roomNum].update( {"description" : roomDesc } )
                    prevLine = "roomDesc"
                    continue

                # After the description should be exits
                if prevLine == "roomDesc" or prevLine == "dirDone":
                    # D[0-5] signify direction
                    if line == "D0":
                        dirFound = "n"
                    elif line == "D1":
                        dirFound = "e"
                    elif line == "D2":
                        dirFound = "s"
                    elif line == "D3":
                        dirFound = "w"
                    elif line == "D4":
                        dirFound = "u"
                    elif line == "D5":
                        dirFound = "d"

                    if dirFound is not None:
                        # print(f"DEBUG::dirFound::{dirFound}")
                        prevLine = "dirFound"
                        if "exits" not in area[roomNum].keys():
                            area[roomNum]["exits"] = {}
                        continue

                if prevLine == "dirFound":                    
                    if dirFound is not None and len(line) > 0:
                        
                        if line[0] == "0" or line[0] == "1":
                            dirLine = line.split()
                            # print(f"DEBUG::dirLine::{dirLine[2]}")
                            # area[roomNum]["exits"].update( {f"{dirFound}" : dirLine[2]} )
                            area[roomNum]['exits'][dirFound] = dirLine[2]
                            print(f"DEBUG::dir::{area[roomNum]['exits']}")
                            prevLine = "dirDone"
                            dirFound = None
                            continue

                if line.strip() == "S":
                    # Room is done, reset variables.
                    area[roomNum].update({'x': 0, 'y': 0})
                    roomNum = None
                    prevLine = None
                    roomDesc = ""
                    dirFound = None
                    continue

                


    print(area)


if len(sys.argv) < 2:
    print("Error: Missing argument. Syntax: `python3 parser.py <*.are file>`")
    exit(0)

parse_area(sys.argv[1])