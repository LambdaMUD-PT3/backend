from area_room import roomGraph
# from django.contrib.auth.models import User
from adventure.models import Room
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adv_project.settings')


# class Room:
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = int(x)
#         self.y = int(y)

#     def __repr__(self):
#         # if self.e_to is not None:
#         #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"([{self.id}] {self.x}, {self.y}: {self.name}:\n{self.description})"

#     def connectRooms(self, direction, connecting_room):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)

#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.rooms = {}

    def loadGraph(self, roomGraph):
        #{"0": 
        #  {"room_id": 0, 
        #   "title": "A brightly lit room", 
        #   "description": "You are standing in the center of a brightly lit room.", 
        #   "coordinates": "(60,60)", 
        #   "players": ["player204"],
        #   "terrain": "NORMAL",
        #   "items": [],
        #   "exits": ["n", "s", "e", "w"],
        #   "cooldown": 1.0,
        #   "errors": [],
        #   "messages": [],
        #   "visited": {"n": "?", "s": "?", "e": "?", "w": "?"},
        #   "x": 60,
        #   "y": 60},
        numRooms = len(roomGraph)
        rooms = [None] * numRooms
        gridSize = 1

        newGraph = {}
        for key in roomGraph.keys():
            # Convert non-int keys to int
            newId = int(key)
            newGraph[newId] = {}
            newGraph[newId].update(roomGraph[key])
            
        roomGraph = newGraph
        # print(f"DEBUG::roomGraph::{roomGraph}")

        for i in roomGraph.keys():
            try:
                x = int(roomGraph[i]['x'])
                y = int(roomGraph[i]['y'])
            except:
                print(f"ERROR::loadGraph::{roomGraph[i]}")
            gridSize = max(gridSize, x, y)


            # self.rooms[i] = Room(roomGraph[i])
            # id, name, description, x, y
            # print(f"DEBUG::{i}, {roomGraph[i].get('title')}, {roomGraph[i].get('description')}, {roomGraph[i].get('x')}, {roomGraph[i].get('y')}")
            self.rooms[i] = Room(i, roomGraph[i].get('title'), roomGraph[i].get('description'), roomGraph[i].get('x'), roomGraph[i].get('y'))
            self.rooms[i].save()
            # print(f"DEBUG::room::{self.rooms[i]}")
            # self.rooms[i].printRoomDescription()

        self.grid = []
        gridSize += 1
        self.gridSize = gridSize

        for i in range(0, gridSize):
            self.grid.append([None] * gridSize)
        
        # print(f"DEBUG::rooms::{self.rooms}")
        for roomID in roomGraph.keys():
            room = self.rooms[roomID]
            self.grid[room.x][room.y] = room
            if 'n' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('n'))
                self.rooms[roomID].connectRooms('n', self.rooms[ex])
            if 's' in roomGraph[roomID]['exits'] :
                # print(f"Connecting {self.rooms[roomID]}")
                # print(f"to... {self.rooms[ex]}")
                ex = int(roomGraph[roomID]['exits'].get('s'))
                self.rooms[roomID].connectRooms('s', self.rooms[ex])
            if 'e' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('e'))
                self.rooms[roomID].connectRooms('e', self.rooms[ex])
            if 'w' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('w'))
                self.rooms[roomID].connectRooms('w', self.rooms[ex])
        
        self.startingRoom = self.rooms[roomID]



    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # Reverse the array to draw from top to bottom
        reverse_grid = []
        for i in range(len(self.grid) - 1, -1, - 1):
            reverse_grid.append(self.grid[i])
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)

# w = World()
# w.loadGraph(roomGraph)
# w.print_rooms()