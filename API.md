### Registration
* `curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password1":"testpassword", "password2":"testpassword"}' localhost:8000/api/registration/`
* Response:
  * `{"key":"6b7b9d0f33bd76e75b0a52433f268d3037e42e66"}`

### Login
* Request:
  * `curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}' localhost:8000/api/login/`
* Response:
  * `{"key":"6b7b9d0f33bd76e75b0a52433f268d3037e42e66"}`

### Initialize
* Request:  (Replace token string with logged in user's auth token)
  * `curl -X GET -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' localhost:8000/api/adv/init/`
* Response:
  * `{"uuid": "c3ee7f04-5137-427e-8591-7fcf0557dd7b", "name": "testuser", "title": "Outside Cave Entrance", "description": "North of you, the cave mount beckons", "players": []}`

### Move
* Request:  (Replace token string with logged in user's auth token)
  * `curl -X POST -H 'Authorization: Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66' -H "Content-Type: application/json" -d '{"direction":"n"}' localhost:8000/api/adv/move/`
* Response:
  * `{"name": "testuser", "title": "Foyer", "description": "Dim light filters in from the south. Dusty\npassages run north and east.", "players": [], "error_msg": ""}`
