#!/usr/bin/env python2.7
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
		<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css" rel="stylesheet">
		<link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
		<link href="./bootstrap.css" rel="stylesheet">
	</head>

	<body>
		<div class="container">
	"""

def login_form():
	print """
			<form method="post" class="form-signin">
        		<h2 class="form-signin-heading">Please sign in</h2>
        		<input type="test" class="form-control" placeholder="Username" name="username" autofocus>
        		<input type="password" class="form-control" placeholder="Password" name="password">
        		<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      		</form>
	"""

def search_form():
	print """
			<form class="">
				<div class="input-group input-group-lg">
					<input type="text" class="form-control" placeholder="Search for books..." name="search_terms">
					<span class="input-group-btn">
						<button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
					</span>
				</div>
			</form>
	"""
def display_search_results(isbn):
	print """
			<div class="media">
				<a class="pull-left" href="#">
			    	<img class="media-object" src=%s height=75 width=65>
			  	</a>
			  	<div class="media-body">
			    	<h4 class="media-heading">%s</h4>
			    		%s
			  	</div>
			</div>

	"""% (book_details[isbn]["smallimageurl"], book_details[isbn]["title"], book_details[isbn]["productdescription"])


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

		<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
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
			#print isbn, " - ", field, ": ", value, "</br>"
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
			#print isbn, " - ", field, ": ", value, "</br>"

	f.close()


# This took just as long as read_books, but now it's working,
# and I defintely understand how it works indepth now after 
# having to heavily modify it.
def search_books_terms(search_terms):

	unknown_fields = []
	for search_term in search_terms:
		m = re.match(r'([^:]+):', search_term)
		if (m and m.group(1) not in attribute_names):
			unknown_fields.append(m.group(1))

	matches = []
	for isbn in (sorted(book_details)):
		n_matches = 0
		if ("=default_search=" not in book_details[isbn]):
			book_details[isbn]["=default_search="] = book_details[isbn]["title"]+"\n"+book_details[isbn]["authors"]

		for search_term in search_terms:
			next_isbn = 0
			match = 0
			search_type = "=default_search="
			term = search_term
			m = re.match(r'([^:]+):(.*)', search_term)
			if m:
				search_type = m.group(1)
				term = m.group(2)
			if (search_type not in book_details[isbn]):
				next_isbn = 1
				break
			field = book_details[isbn][search_type]
			field = re.sub(r'[!().:]', '', field)
			regex = re.compile('\s+%s\s+' % term.lower())
			m = regex.search(field.lower())
			if (m):
				match = 1
			regex = re.compile('^%s\s+' % term.lower())
			m = regex.search(field.lower())
			if (m):
				match = 1
			if match:
				n_matches += 1
				next_isbn = 1
				break

		if (n_matches > 0):
			matches.append(isbn)
		if (next_isbn):
			next_isbn = 0
			continue

	# Makes a dict key'd by the isbn's with the sales rank as the value.
	matches_sorted = {}
	for match in matches:
		max_sales_rank = 100000000
		if ("salesrank" not in book_details[match]):
			book_details[match]["salesrank"] = max_sales_rank
		sales_rank = book_details[match]["salesrank"]
		matches_sorted[match] = int(sales_rank)

	# Returns a list of tuples in the form [key, value] sorted by the value of matches_sorted dict.
	matches = [(k, matches_sorted[k]) for k in sorted(matches_sorted, key=matches_sorted.get)]

	return matches



def search_books(search_string):
	search_string = re.sub('\s*$', '', search_string)
	search_string = re.sub('^\s*', '', search_string)
	return search_books_terms(search_string.split())

def search_results(search_terms):
	matches = search_books(search_terms)
	matches_list = [matches[k][0] for k in xrange(len(matches))]
	for isbn in matches_list:
		display_search_results(isbn)


def main():
	page_header()

	read_books()
	"""
	matches = []
	matches = search_books("cool")
	print matches
	"""
	form = cgi.FieldStorage()
	username = form.getvalue("username")
	password = form.getvalue("password")
	search_terms = form.getvalue("search_terms")

	if ("search_terms" in form):
		search_results(search_terms)
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



main()