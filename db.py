from pymongo import MongoClient
import sha as hasher
import md5

db = MongoClient().frozen_data

# return a list of errors, or if there are none, create the account
def create_account(data):
	users = db.users
	errors = []

	u = users.find({'username': data['username']})
	if u.count() > 0:
		errors.append('username-used')

	u = users.find({'email': data['email']})
	if u.count() > 0:
		errors.append('email-used')

	if data['password'] != data['password-conf']:
		errors.append('password-mismatch')

	if not errors: # create the account
		account_data = {s: data[s] for s in ['username', 'email']}

		# use hash of password
		account_data['password'] = hasher.new(data['password']).hexdigest()

		users.insert(account_data)

	return errors

# attempt to login the identified user, return success status
def login(data):
	users = db.users

	user = {'username': data['username']}
	m = hasher.new()
	m.update(data['password'])
	user['password'] = m.hexdigest()

	if users.find_one(user):
		return True
	return False

# return user object with given username
def getInfo(username):
	user = db.users.find_one({'username': username})
	if user:
		user['hashed_email'] = md5.new(user['email'].lower()).hexdigest()
		return user
	return None

# return all users starting with given string
def matchUsername(username):
	result = db.users.find({
		'username': {
			'$regex': username,
			'$options': 'i'
		}
	})
	return [{k: u[k] for k in u
	              if k != '_id'}
		    for u in result]

# create and store new game with given data
def newGame(data):
	game = {"players" : [data[s] for s in ['user', 'opponent']],
	        "finished" : False,
	        "turn" : 1,
	        "game_id" : db.games.count(),
	        "srces" : [[],[]],
	        "jsons" : [[],[]],
	        "states" : [] }
	db.games.insert(game)

def getActiveGames():
	games = db.games.find({"finished": False})
	return [game for game in games]

def getGame(game_id):
	game = db.games.find_one({'game_id': game_id})
	if game:
		return game
	return None

def updateGame(game_id, game_data):
	if not db.games.find_one({'game_id': game_id}):
		return False
	
	if '_id' in game_data.keys():
		del game_data['_id']
	db.games.update({'game_id': game_id}, {'$set': game_data})
	return True
