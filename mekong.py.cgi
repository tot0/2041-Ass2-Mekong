#!/usr/bin/python2.7
#Lucas Pickup, z3424653, lpickup

import cgi
import cgitb
import re, os
import json, sqlite3
from Book_class import Book
#import Book_class
cgitb.enable(display=0, logdir="./logs")  # for troubleshooting

book_file = "books.json"
orders_dir = "orders/"
baskets_dir = "baskets/"
users_db = "users/users.db"
last_error = ""
user_details = {}

def page_header():
	print "Content-type: text/html;charset=utf-8"
	print ""
	print """
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>mekong.com.au</title>

		<!-- Favicon -->
		<link rel="shortcut icon" href="./favicon.ico" type="image/x-icon">
		<link rel="icon" href="./favicon.ico" type="image/x-icon">

		<!-- Bootstrap/swatch -->
		<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css" rel="stylesheet">
		<link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
		<link href="./stylish-portfolio.css" rel="stylesheet">
		<link href="./bootstrap.css" rel="stylesheet">

	</head>

	<body>
	"""

def home_page():
	print """
		<!-- Full Page Image Header Area -->
		<div id="top" class="header">
			<div class="vert-text">
				<h1 class="diff_shadow">Mekong</h1>
				<h3 class="diff_shadow">The <em>Authors</em> Channel To <em>You</em></h3>
				<form class="">
					<style>
						.input-group-lg-home {
							max-width: 500px;
							padding: 15px;
							margin: 0 auto;
						}
					</style>
					<div class="input-group input-group-lg-home">
						<input type="text" class="form-control" placeholder="Search for books..." name="search_terms" autofocus>
						<span class="input-group-btn">
						<button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
						</span>
					</div>

					<h3 class="diff_shadow">Or...</h3>
				</form>
				<a class="btn btn-primary" href="#login">Log in</a>
			</div>
		</div>
		<!-- /Full Page Image Header Area -->
	"""

def login_form():
	print """
		<div id="login" class="row col-sm-12">
			<div class="col-sm-6" style="padding:20px 0px 50px 0px;">
				<form method="post" class="form-signin">
	        		<h2 class="form-signin-heading">Please sign in</h2>
	        		<input type="text" class="form-control" placeholder="Username" name="username">
	        		<input type="password" class="form-control" placeholder="Password" name="password">
	        		<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
	      		</form>
	      	</div>

	      	<div class="col-sm-6"  style="padding:20px 0px 50px 0px;">
	      			<form class="form-signin">
		      			<h2 class="form-signin-heading">Don't have an account?</h2>
		      			<a class="btn btn-lg btn-primary btn-block" type="button" href="?page=register">Register</a>
	      			</form>
	      	</div>
      	</div>
	"""

def login_home():
	print """
		<div class="container">
			<h1>Mekong</h1>
			<h3>isn't she just beaut...</h3>
			<img src="./mekong_bg.jpg"/>
		</div>

	"""

# This tutorial helped ALOT http://www.9lessons.info/2012/04/bootstrap-registration-form-tutorial.html
def register_form():
	print """
		<div class="container">
			<form id="registration" role="form" method="post">
				<fieldset>
					<h3>Personal Details</h3>
					<div class="form-group">
						<label class="sr-only">Name</label>
						<input id="name" class="form-control" type="text" name="name_reg" placeholder="Full Name">
					</div>
					<div class="form-group">
						<label class="sr-only" for="username">Username</label>
						<input id="username" class="form-control" type="text" name="username_reg" placeholder="Username" rel="popover" data-content="Please enter your desired username." data-original-title="Username">
					</div>
					<div class="form-group">
						<label class="sr-only">Password</label>
						<input id="password" class="form-control" type="password" name="password_reg" placeholder="Password">
					</div>
					<div class="form-group">
						<label class="sr-only">Confirm Password</label>
						<input id="password" class="form-control" type="password" name="password_con_reg" placeholder="Confirm Password">
					</div>
					<div class="form-group">
						<label class="sr-only">Email</label>
						<input id="email" class="form-control" type="text" name="email_reg" placeholder="Email">
					</div>
					<hr style="border-top:1px solid #5a5a5a;">
					<h3>Address Details</h3>
					<div class="form-group">
						<label class="sr-only">Street Address</label>
						<input id="street" class="form-control" type="text" name="street_reg" placeholder="Street Address e.g. 16 Vantage Pl">
					</div>
					<div class="form-group">
						<label class="sr-only">City</label>
						<input id="city" class="form-control" type="text" name="city_reg" placeholder="City">
					</div>
					<div class="form-group">
						<label class="sr-only">State</label>
						<select id="state" class="form-control" name="state_reg">
							<option>NSW</option>
							<option>QLD</option>
							<option>VIC</option>
							<option>WA</option>
							<option>SA</option>
							<option>ACT</option>
							<option>NT</option>
							<option>TAS</option>
						</select>
					</div>
					<div class="form-group">
						<label class="sr-only">Postcode</label>
							<input id="postcode" class="form-control" type="text" name="postcode_reg" placeholder="Postcode">
					</div>
					<div class="form-group">
						<button class="btn btn-primary btn-lg" type="submit">Submit</button>
						<input type="hidden" name="page_next" value="register_validate">
					</div>
				</fieldset>
			</form>
		</div>
	"""

def search_form():
	print """
			<style>
				body { padding-top: 70px; }
			</style>

			<form class="navbar-fixed-top">
				<style>
					.input-group-lg-home {
						max-width: 500px;
						padding: 15px;
						margin: 0 auto;
					}
				</style>
				<div class="input-group input-group-lg-home">
					<input type="text" class="form-control" placeholder="Search for books..." name="search_terms" autofocus>
					<span class="input-group-btn">
					<button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
					</span>
				</div>

			</form>
	"""

def start_table():
	print """
		<div class="row col-sm-12">
			<div class="col-lg-2"></div>
			<div class="col-lg-8">
				<table class="table table-hover col-lg-8">
	"""


def display_search_result(isbn):
	book = read_book(isbn)

	print """
					<tr>
						<td>
							<a href="#">
						    	<img src=%s height=75 width=65>
						  	</a>
						 </td>
						 <td>
						    	<a href="?page=book&isbn=%s"><h4>%s</h4></a>
						    	%s	
						</td>
					</tr>
	""" % (book.smallimageurl, book.isbn, book.title, book.all_authors)

def end_table():
	print """
				</table>
			</div>
			<div class="col-lg-2"></div>
		</div>
			<center><em>Displaying first 20 results...</em></center>
	"""

def book_page(isbn):
	book = read_book(isbn)
#style="max-width: %spx;"
	print """
			<div class="row col-sm-12">
				<div class="col-sm-1"></div>
				<div class="col-sm-4">
					<img class="img-responsive pull-right" style="border: 3px solid #000; margin-top:22px;" src="%s"/>
				</div>
				<div class="col-sm-6">
					<h2><strong>%s</strong></h2>
					by	%s </br>
					<hr style="border-top:1px solid #5a5a5a;">
					<p>%s</p>
					<hr style="border-top:1px solid #5a5a5a;">
					Date Published: <b>%s</b> by <em>%s</em></br>

					</br>

					<div class="well" style="padding:5px 5px 5px 5px; ">
						<div style="margin-top:4px; float:left;">
							Price: <em><strong>%s</strong></em>
						</div>
						<a class="btn btn-default btn-sm pull-right" href="?page=cart&book_add=%s">Add to Cart</a>
						<div class="clearfix"></div>
					</div>
				</div>
				<div class="col-sm-1"></div>
			</div>

	""" % (book.largeimageurl, book.title, book.all_authors, book.productdescription, book.publication_date, book.publisher, book.price, book.isbn)


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

def four_oh_four():
	print """
			<div id="top" class="header" style="background: url(mekong_ohno.jpg) no-repeat center center fixed;">
				<div class="vert-text" style="color: black; vertical-align:text-top; padding:100px 0px 0px 0px;">
					<h1 class="" style="text-shadow: 1px 1px 0px rgba(255, 255, 255, 1);">Oops!</h1>
					<h3 class="" style="text-shadow: 2px 2px 3px rgba(255, 255, 255, 1);">It appears while enjoying <strong>Mekong</strong> you've veered into a sand bank!</h3>

					<a class="btn btn-primary" href="?">Drift Home</a>
				</div>
			</div>
	"""

def page_trailer():
	print """
		<script src="http://codeorigin.jquery.com/jquery-2.0.3.min.js"></script>
		<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>

		<script type="text/javascript">
			$(function() {
				$('a[href*=#]:not([href=#])').click(function() {
					if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
						var target = $(this.hash);
						target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
						if (target.length) {
							$('html,body').animate({
								scrollTop: target.offset().top
							}, 1000);
							return false;
						}
					}
				});
			});
		</script>

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


def auth_password(password, password_con):
	global last_error

	if (re.search(' ', password)):
		last_error = "Sorry passwords can't contain white space :("
		return False

	if (len(password) < 5):
		last_error = "Sorry we require passwords to be at least 5 characters long."
		return False

	if (password != password_con):
		last_error = "Oops! It appears your passwords don't match. :("
		return False

	return True

def authenticate(username, password):
	return True

def register_validate(form):

	if (auth_username(form.getvalue('username_reg'))):
		username = form.getvalue('username_reg')
	else:
		auth_error(last_error)
		register_form()
		return False

	if (auth_password(form.getvalue('password_reg'), form.getvalue('password_con_reg'))):
		password = form.getvalue('password_reg')
	else:
		auth_error(last_error)
		register_form()
		return False

	return True


def read_books():

	f = open(book_file,'r')
	books_details = json.load(f)

	books = []
	for book_details in (books_details.values()):
		books.append(Book(book_details))

	f.close()

	return books

def read_book(isbn):

	f = open(book_file, 'r')
	books_details = json.load(f) 

	book_details = books_details[isbn]
	book = Book(book_details)

	f.close

	return book

# This took just as long as read_books, but now it's working,
# and I defintely understand how it works indepth now after 
# having to heavily modify it.
def search_books_terms(search_terms):
	books = read_books()

	matches = []

#	unknown_fields = []
#	for search_term in search_terms:
#		m = re.match(r'([^:]+):', search_term)
#		if (m and m.group(1) not in ):
#			unknown_fields.append(m.group(1))

	for i in xrange(len(books)):
		n_matches = 0
		for search_term in search_terms:
			next_book = 0
			match = 0
			term = search_term
			m = re.match(r'([^:]+):(.*)', search_term)
			if m:
				search_type = m.group(1)
				term = m.group(2)

			field = books[i].default_search
			field = re.sub(r'[!().:]', '', field)
			#regex = re.compile('\s+%s\s+' % term.lower())
			m = re.search(term.lower(), field.lower())#regex.search(field.lower())
			if (m):
				match = 1
			#regex = re.compile('^%s\s+' % term.lower())
			#m = regex.search(field.lower())
			#if (m):
			#	match = 1
			if match:
				n_matches += 1
				next_book = 1
				break

		if (n_matches > 0):
			matches.append(i)
		if (next_book):
			next_book = 0
			continue

	# Makes a dict key'd by the isbn's with the sales rank as the value.
	matches_sorted = {}
	for i in matches:
		sales_rank = books[i].salesrank
		matches_sorted[books[i].isbn] = int(sales_rank)

	# Returns a list of tuples in the form [key, value] sorted by the value of matches_sorted dict.
	matches = [(k) for k in sorted(matches_sorted, key=matches_sorted.get)]

	return matches


def search_books(search_string):
	search_string = re.sub('\s*$', '', search_string)
	search_string = re.sub('^\s*', '', search_string)
	return search_books_terms(search_string.split())

def search_results(search_terms):
	matches = search_books(search_terms)
	matches_list = [matches[k][0] for k in xrange(len(matches))]
	search_form()
	start_table()
	if (len(matches) < 20):
		num_results = len(matches)
	else:
		num_results = 20
	for i in xrange(num_results):
		display_search_result(matches[i])
	end_table()

def read_user():
	con = sqlite3.connect(users_db)

	with con:
		cur = con.cursor()
		cur.execute("SELECT SQLITE_VERSION()")

		data = cur.fetchone()

		print "SQLite version: %s" % data



def load_page(page, isbn, form):

	if (page == "book"):
		if (isbn == None):
			four_oh_four()
		else:	
			book_page(isbn)
	elif (page == "register"):
		if ("page_next" in form and form.getvalue("page_next") == "register_validate"):
			if (register_validate(form)):
				login_home()
		else:
			register_form()
	elif (page == "login_home"):
		login_home()
	elif (page == "user"):
		read_user()


def main():
	page_header()

	form = cgi.FieldStorage()
	page = form.getvalue("page")
	isbn = form.getvalue("isbn")
	username = form.getvalue("username")
	password = form.getvalue("password")
	search_terms = form.getvalue("search_terms")

	if ("page" in form):
		load_page(page, isbn, form)
	else:
		if ("search_terms" in form):
			search_results(search_terms)
		elif ("username" in form and "password" in form):
			if (auth_username(username)):
				if (auth_password(password)):
					load_page("login_home")
				else:
					auth_error(last_error)
					login_form()
			else:
				auth_error(last_error)
				login_form()
		else:
			home_page()
			login_form()


	page_trailer()



main()