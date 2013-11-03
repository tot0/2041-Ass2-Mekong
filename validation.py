# validation..py contains functions that validate input fields and such.
import re
import config
import database
import html
import email1

def auth_login(username, password):

	if (not auth_username(username)):
		return False
	if (not auth_password(password, password)):
		return False

	user = database.read_user(0, username)
	if (user == None):
		return False

	if (user["password_hash"] == password):
		if (user['verified'] == "Yes"):
			config.cur_user_id = user["id"]
			return True
		else:
			config.last_error = """
								Sorry it appears your account hasn't been verified.
								Please check your email for the verification link we sent when you created your account.
								We'll resend the email now, just in case.
								"""
			email1.verify_email(user['email'], user['id'])
			return False
	else:
		config.last_error = "Sorry the password you've entered appears to be incorrect."
		return False

def auth_username(username):

	if (not re.match('^[a-zA-Z][a-zA-Z0-9]*$', username)):
		config.last_error = "Sorry our logins only support letters and numbers, and they need to start with a letter."
		return False

	if (len(username) < 3 or len(username) > 8):
		config.last_error = "Sorry your username needs to be between 3 and 8 characters long."
		return False

	return True


def auth_password(password, password_con):

	if (re.search(' ', password)):
		config.last_error = "Sorry passwords can't contain white space :("
		return False

	if (len(password) < 5):
		config.last_error = "Sorry we require passwords to be at least 5 characters long."
		return False

	if (password != password_con):
		config.last_error = "Oops! It appears your passwords don't match. :("
		return False

	return True

def legal_address(form):
	return True

def validate_user(validate_code):
	if (database.read_user(validate_code, None) != None):
		user = ("Yes", validate_code)
		fields = "verified=?"
		database.update_user(fields, user)
		return True
	else:
		config.last_error = "This validation code is invalid!"
		return False

def register_validate(form):

	if (auth_username(form.getvalue('username_reg'))):
		username = form.getvalue('username_reg')
	else:
		html.page_header()
		html.auth_error(config.last_error)
		html.register_form()
		return False

	if (auth_password(form.getvalue('password_reg'), form.getvalue('password_con_reg'))):
		password = form.getvalue('password_reg')
	else:
		html.page_header()
		html.auth_error(config.last_error)
		html.register_form()
		return False

	if (form.getvalue('page') == "updated_details"):
		user = (form.getvalue('username_reg'), 
			form.getvalue('first_name_reg'), 
			form.getvalue('last_name_reg'), 
			form.getvalue('email_reg'), 
			form.getvalue('password_reg'),
			form.getvalue('street_reg'), 
			form.getvalue('city_reg'), 
			form.getvalue('state_reg'), 
			form.getvalue('postcode_reg'),
			config.cur_user_id)
		fields = "username=?,first_name=?,last_name=?,email=?,password_hash=?,street=?,city=?,state=?,postcode=?"
		database.update_user(fields, user)
	else:
		user = (form.getvalue('username_reg'), 
			form.getvalue('first_name_reg'), 
			form.getvalue('last_name_reg'), 
			form.getvalue('email_reg'), 
			form.getvalue('password_reg'), 
			form.getvalue('street_reg'), 
			form.getvalue('city_reg'), 
			form.getvalue('state_reg'), 
			form.getvalue('postcode_reg'), 
			'No')
		database.write_user(user)

	return True

def legal_cc(number, expiry):
	m = re.match(r'^\d{16}$', number)
	if not m:
		config.last_error = "Sorry Credit Card numbers must be 16 digits."
		return False

	m = re.match(r'^\d\d\/\d\d$', expiry)
	if not m:
		config.last_error = "Sorry Credit Card expiry dates must be in the form mm/yy. e.g. '06/17'"
		return False

	return True

def validate_checkout(form):
	cc_number = form.getvalue('cc_checkout')
	cc_expire = form.getvalue('cc_expire_checkout')

	if not legal_cc(cc_number, cc_expire):
		return False

	if not legal_address(form):
		return False

	return True
