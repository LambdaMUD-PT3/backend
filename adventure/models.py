from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from area_room import roomGraph

class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)


    def connectRooms(self, direction, destinationRoom):
        destinationRoomID = destinationRoom
        try:
            destinationRoom = Room.objects.get(room_id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()


    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

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
        # gridSize = 1

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
            # gridSize = max(gridSize, x, y)


            # self.rooms[i] = Room(roomGraph[i])
            # id, name, description, x, y
            # print(f"DEBUG::{i}, {roomGraph[i].get('title')}, {roomGraph[i].get('description')}, {roomGraph[i].get('x')}, {roomGraph[i].get('y')}")
            self.rooms[i] = Room(i, roomGraph[i].get('title'), roomGraph[i].get('description'), roomGraph[i].get('x'), roomGraph[i].get('y'))
            self.rooms[i].save()
            # print(f"DEBUG::room::{self.rooms[i]}")
            # self.rooms[i].printRoomDescription()

        # self.grid = []
        # gridSize += 1
        # self.gridSize = gridSize

        # for i in range(0, gridSize):
        #     self.grid.append([None] * gridSize)
        
        # print(f"DEBUG::rooms::{self.rooms}")
        for roomID in roomGraph.keys():
            room = self.rooms[roomID]
            # self.grid[room.x][room.y] = room
            if 'n' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('n'))
                self.rooms[roomID].connectRooms('n', ex)
            if 's' in roomGraph[roomID]['exits'] :
                # print(f"Connecting {self.rooms[roomID]}")
                # print(f"to... {self.rooms[ex]}")
                ex = int(roomGraph[roomID]['exits'].get('s'))
                self.rooms[roomID].connectRooms('s', ex)
            if 'e' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('e'))
                self.rooms[roomID].connectRooms('e', ex)
            if 'w' in roomGraph[roomID]['exits'] :
                ex = int(roomGraph[roomID]['exits'].get('w'))
                self.rooms[roomID].connectRooms('w', ex)
        
        # self.startingRoom = self.rooms[roomID]

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





