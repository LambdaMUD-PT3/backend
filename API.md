### Registration
* `curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password1":"testpassword", "password2":"testpassword"}' https://lambda-mud-11.herokuapp.com/api/registration/`
* Response:
  * `{"key":"6b7b9d0f33bd76e75b0a52433f268d3037e42e66"}`

### Login
* Request:
  * `curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}' https://lambda-mud-11.herokuapp.com/api/login/`
* Response:
  * `{"key":"6b7b9d0f33bd76e75b0a52433f268d3037e42e66"}`

### Initialize
* Request:  (Replace token string with logged in user's auth token)
  * `curl -X GET -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' https://lambda-mud-11.herokuapp.com/api/adv/init/`
* Response:
  * `{"uuid": "c3ee7f04-5137-427e-8591-7fcf0557dd7b", "name": "testuser", "title": "Outside Cave Entrance", "description": "North of you, the cave mount beckons", "players": []}`

### Move
* Request:  (Replace token string with logged in user's auth token)
  * `curl -X POST -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' -H "Content-Type: application/json" -d '{"direction":"n"}' https://lambda-mud-11.herokuapp.com/api/adv/move/`
* Response:
  * `{"name": "testuser", "title": "Foyer", "description": "Dim light filters in from the south. Dusty\npassages run north and east.", "players": [], "error_msg": ""}`

### Rooms
* Request:  (Replace token string with logged in user's auth token)
  * `curl -X GET -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' https://lambda-mud-11.herokuapp.com/api/adv/rooms/`
* Response:
  * `{"3700": {"title": "Entrance to Mud School", "description": "This is the entrance to the Merc Mud School.  Go north to go through mud\nschool.  If you have been here before and want to go directly to the arena,\ngo south.\n\nA sign warns 'You may not pass these doors once you have passed level 5.'\n", "x": 3, "y": 0, "exits": {"n": 3757, "e": 3706}}, (and all the others)}`

### Say
* Request: (Replace token string with logged in user's auth token)
  * `curl -X POST -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' -H "Content-Type: application/json" -d '{"message":"Hello World!"}' https://lambda-mud-11.herokuapp.com/api/adv/rooms/`
* Response:
  * `{"message": "You said, \"Hello World!\""}`