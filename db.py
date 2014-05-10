from pymongo import MongoClient
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
		m = md5.new()
		m.update(data['password'])
		account_data['password'] = m.hexdigest()

		users.insert(account_data)

	return errors

# attempt to login the identified user, return success status
def login(data):
	users = db.users

	user = {'username': data['username']}
	m = md5.new()
	m.update(data['password'])
	user['password'] = m.hexdigest()

	if users.find_one(user):
		return True
	return False

# return the hashed email linked with the given username
def hashedEmail(username):
	user = db.users.find_one({'username': username})
	if user:
		m = md5.new()
		m.update(user['email'])
		return m.hexdigest()
	return None
