from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)

    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'exits':room.getExits(), 'room_id': room.room_id}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(room_id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'exits':nextRoom.getExits(), 'error_msg':"", 'room_id': nextRoom.room_id}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'exits':room.getExits(), 'error_msg':"You cannot move that way.", 'room_id': room.room_id}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    msg = data['message']
    room = player.room().room_id
    pusher.trigger(f'room-{room}', u'talk', {'message':f'{player.user.username} says, "{msg}"'})
    # # IMPLEMENT
    # return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
    return JsonResponse({'message': f'You said, "{msg}"'})


@csrf_exempt
@api_view(["POST"])
def look(request):
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    item = data['look_at']
    room = player.room()
    views = json.loads(room.views)

    if item in views:
        msg = views.get(item)
    
    return JsonResponse({'looked_at': msg})


@csrf_exempt
@api_view(["GET"])
def rooms(request):
    user = request.user
    roomData = {}
    queryset = Room.objects.all()

    for room in queryset:
        roomData[room.room_id] = {}
        roomData[room.room_id].update({
            "x": room.x,
            "y": room.y,
            "exits": {}
        })

        if room.n_to > 0:
            roomData[room.room_id]["exits"].update({"n": room.n_to})
        if room.s_to > 0:
            roomData[room.room_id]["exits"].update({"s": room.s_to})
        if room.e_to > 0:
            roomData[room.room_id]["exits"].update({"e": room.e_to})
        if room.w_to > 0:
            roomData[room.room_id]["exits"].update({"w": room.w_to})

    return JsonResponse(roomData, safe=True)