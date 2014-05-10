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
