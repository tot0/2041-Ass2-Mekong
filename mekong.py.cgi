#!/usr/bin/env python
#Lucas Pickup, z3424653, lpickup

import cgi
import cgitb
import re
cgitb.enable(display=0, logdir="./logs")  # for troubleshooting

base_dir = "."
book_file = base_dir + "/books.json"
orders_dir = base_dir + "/orders"
baskets_dir = base_dir + "/baskets"
user_dir = base_dir + "/users"
last_error = ""
attribute_names = {}
user_details = {}
book_details = {}


def page_header():
	print "Content-type: text/html;charset=utf-8"
	print ""
	print """
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>mekong.com.au</title>

		<!-- Bootstrap/swatch -->
		<link href="./bootstrap.css" rel="stylesheet">
		<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
	</head>

	<body>
		<div class="container">
	"""

def login_form():
	print """
			<form method="post" class="form-signin">
        		<h2 class="form-signin-heading">Please sign in</h2>
        		<input type="test" class="form-control" placeholder="Email" name="username" autofocus>
        		<input type="password" class="form-control" placeholder="Password" name="password">
        		<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      		</form>
	"""

def search_form():
	print """
			<form method="post" id="custom-search-form" class="form-search form-horizontal pull-right">
			    <div class="input-append span12">
			        <input type="search" class="search-query" placeholder="Search" name="search_terms">
			        <button type="submit" class="btn"><i class="icon-search"></i></button>
			    </div>
			</form>
	"""

def auth_error(item):
	print """
		<p>
		</p>
		<style>
			.alert {
				text-align: center;
			}
		</style>
		<div class="alert alert-danger">
        	<strong>Oops!</strong> %s
      	</div>
	""" % item
	login_form()

def page_trailer():
	print """
		</div> <!-- /container -->
	</body>
</html>
	"""



def auth_username(username):
	global last_error

	if (not re.match('^[a-zA-Z][a-zA-Z0-9]*$', username)):
		last_error = "Sorry our logins only support letters and numbers, and they need to start with a letter."
		return False

	if (len(username) < 3 or len(username) > 8):
		last_error = "Sorry your username needs to be between 3 and 8 characters long."
		return False

	return True


def auth_password(password):
	global last_error

	if (re.search(' ', password)):
		last_error = "Sorry passwords can't contain white space :("
		return False

	if (len(password) < 5):
		last_error = "Sorry we require passwords to be at least 5 characters long."
		return False

	return True

def authenticate(username, password):
	return True


# Adapted from perl version, TOOK A LOT OF DEBUGGING TO GET THIS TO WORK.
def read_books():
	global book_details

	f = open(book_file,'r')

	for line in f:
		m = re.match('^\s*"(\d+X?)"\s*:\s*{\s*$', line)
		if (m):
			isbn = m.group(1)
			continue
		l = re.match('\s*"([^"]+)"\s*:\s*"(.*)",?\s*', line)
		n = re.match('\s*"([^"]+)"\s*:\s*\[\s*', line)
		if l:
			field = l.group(1)
			value = l.group(2)
			if field in attribute_names:
				attribute_names[field] += 1
			else:
				attribute_names[field] = 1
			value = re.sub(r'([^\\]|^)\\"', r'\g<1>', value)

			if isbn in book_details:
				book_details[isbn][field] = {}
				book_details[isbn][field] = value
			else:
				book_details[isbn] = {}
				book_details[isbn][field] = {}
				book_details[isbn][field] = value
		elif n:
			field = n.group(1)
			if field in attribute_names:
				attribute_names[field] += 1
			else:
				attribute_names[field] = 1
			a = []
			for line2 in f:
				m = re.match('^\s*\]\s*,?\s*$',line2)
				if m:
					break
				m = re.match('^\s*"(.*)"\s*,?\s*$',line2)
				if m:		
					a.append(m.group(1))
			value = "\n".join(a)
			value = re.sub(r'([^\\]|^)\\"', r'\g<1>"', value)

			if isbn in book_details:
				book_details[isbn][field] = {}
				book_details[isbn][field] = value
			else:
				book_details[isbn] = {}
				book_details[isbn][field] = {}
				book_details[isbn][field] = value

	f.close()




def main():
	page_header()

	read_books()

	page_trailer()
"""	
	form = cgi.FieldStorage()
	username = form.getvalue("username")
	password = form.getvalue("password")
	search_terms = form.getvalue("search_terms")

	if ("search_terms" in form):
		print "<h1>Items:</h1>"
		print search_terms
	elif ("username" in form and "password" in form):

		if (auth_username(username)):
			if (auth_password(password)):
				search_form()
			else:
				auth_error(last_error)
		else:
			auth_error(last_error)
	else:
		login_form()

	page_trailer()
"""


main()