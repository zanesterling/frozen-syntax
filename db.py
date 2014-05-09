from pymongo import MongoClient

db = MongoClient().frozen_data

def createAccount(data):
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

	if not errors:
		account_data = {s: data[s] for s in ['username', 'email', 'password']}
		users.insert(account_data)

	return errors
