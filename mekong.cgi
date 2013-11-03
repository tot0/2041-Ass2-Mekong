#!/usr/bin/python2.7
#Lucas Pickup, z3424653, lpickup

# Standard python modules.
import cgi, Cookie
import cgitb
cgitb.enable(display=0, logdir="./logs")  # for troubleshooting
import re, os

# My own custom modules.
import config
from html import *
from database import *
from validation import *
from email1 import *

# If the mekong database doesn't exist create it.
if (not os.path.exists(config.db_dir)):
	create_db()

# Global variable of path to script.
config.base_path = re.sub(r'mekong\.cgi$', '', os.environ['SCRIPT_URI'])

##################################################################
# Cookie Handling
##################################################################

# Check for user_id cookie and load the appropriate user.
if ("HTTP_COOKIE" in os.environ):
	cookies = os.environ['HTTP_COOKIE']
	cookies = cookies.split(';')
	for cookie in cookies:
		cookie = cookie.split('=')
		name = cookie[0].strip()
		value = cookie[1].strip()
		if (name == "user_id"):
			config.cur_user_id = int(value)
			config.cur_user = read_user(config.cur_user_id, None)
			if (config.cur_user == None):
				config.cur_user_id = None
			break
		else:
			config.cur_user_id = None
			config.cur_user = None

else:
	config.cur_user_id = None
	config.cur_user = None

# This will either set a cookie, or delete a cookie depending on arguments it's passed.
def set_cookie(cookie, user_id):
	if (cookie == 1):
		user_cookie = Cookie.SimpleCookie()
		user_cookie['user_id'] = user_id
		print user_cookie
	elif (cookie == 2):
		user_cookie = Cookie.SimpleCookie()
		user_cookie['user_id'] = user_id
		user_cookie['user_id']['expires'] = 0
		print user_cookie

##################################################################
# Misc Functions
##################################################################

# This could've been more fancy and would be for real webdev, 
# but this sort of secruity really wasn't a priority for this assignment.
def gen_verify_code(user_id):
	code = user_id
	return code

##################################################################
# Search Functions
##################################################################

# Based of andrewt's search from perl version. Heavily modified though.
def search_books_terms(search_terms, category="default_search"):
	books = read_books()

	matches = []

	for book in books:
		n_matches = 0
		for search_term in search_terms:
			next_book = 0
			match = 0
			term = search_term
			field = str(book[category])
			term = re.sub(r'[!()*:$\^?]', '', term)
			m = re.search(term.lower(), field.lower())
			if (m):
				match = 1
			if match:
				n_matches += 1
				next_book = 1
				break

		if (n_matches > 0):
			matches.append(book)
		if (next_book):
			next_book = 0
			continue

	# Makes a dict key'd by the isbn's with the sales rank as the value.
	matches_sorted = {}
	for book in matches:
		if ("sales_rank" not in book):
			sales_rank = 10000000
		else:
			sales_rank = book['sales_rank']
		matches_sorted[book['isbn']] = int(sales_rank)

	# Returns a list of tuples in the form [key, value] sorted by the value of matches_sorted dict.
	matches = [(k) for k in sorted(matches_sorted, key=matches_sorted.get)]

	return matches


def search_results(search_terms, category, page_num):
	search_terms = search_terms.strip()
	matches = search_books_terms(search_terms.split(), category)

	matches_list = [matches[k][0] for k in xrange(len(matches))]
	
	# rediculous piece of code to facilitate pagination.
	if ((len(matches) / 50)%50 == 0 and (len(matches) / 50) > 1):
		num_pages = int((len(matches) / 50))
	else:
		num_pages = int(len(matches) / 50) + 1
	pag = True
	if (num_pages == 1):
		start = 0
		stop = len(matches)
		pag = False
	elif (int(page_num) >= num_pages):
		start = (int(num_pages) * 50) - 49
		stop = len(matches)
	else:
		start = (int(page_num) * 50) - 50
		stop = int(page_num) * 50

	start_table(str(start + 1) + "-" + str(stop), len(matches))

	for i in xrange(start, stop):
		display_search_result(matches[i],)

	end_table(pag, num_pages)


##################################################################
# Control Functions
##################################################################

# If I thought about this a bit more it could probably be restructured so page_header() 
# doesn't have to before everything. But because of the couple of tiems i need to cookies, it is. 
def load_page(page, isbn=None, form=None):

	if (page == "book"):
		if (isbn == None):
			page_header()
			four_oh_four()
		else:
			page_header()
			book_page(isbn)
	elif (page == "register"):
		if ("page_next" in form and form.getvalue("page_next") == "register_validate"):
			if (register_validate(form)):
				page_header()
				verify_email(form.getvalue('email_reg'), gen_verify_code(read_user(None, form.getvalue('username_reg'))['id']))
				email_validate_page()
			else:
				page_header()
				auth_error(config.last_error)
				register_form()
		else:
			page_header()
			register_form()
	elif (page == "verification"):
		validate_code = form.getvalue('code')
		if (validate_user(validate_code)):
			page_header()
			validation_success()
		else:
			page_header()
			auth_error(config.last_error)
	elif (page == "login"):
		page_header()
		login_form()
	elif (page == "logout"):
		set_cookie(2, config.cur_user_id)
		config.cur_user_id = None
		config.cur_user = None
		page_header(1)
		home_page()
		login_form()
	elif (page == "cart"):
		if (config.cur_user_id != None):
			if ('book_add' in form):
				add_to_cart(form.getvalue('book_add'), form.getvalue('num_books'))
			page_header()
			cart_page()
		else:
			page_header()
			login_4_cart()
	elif (page == "update_cart"):
		update_cart(form)
		page_header()
		cart_page()
	elif (page == "checkout"):
		page_header()
		checkout_page()
	elif (page =="checkout_complete"):
		if (validate_checkout(form)):
			write_order(config.cur_user_id, form.getvalue('cc_checkout'), form.getvalue('cc_expire_checkout'))
			clear_user_cart(config.cur_user_id)
			page_header()
			orders_page()
		else:
			page_header()
			auth_error(config.last_error)
			checkout_page()
	elif (page == "orders"):
		page_header()
		orders_page()
	elif (page == "account"):
		page_header()
		account_page()
	elif (page == "updated_details"):
		if (register_validate(form)):
			config.cur_user = read_user(config.cur_user_id, None)
			page_header()
			account_page()
		else:
			page_header()
			auth_error(config.last_error)
			account_page()			
	elif (page == "recover_pass"):
		page_header()
		recover_pass_page()
	elif (page == "recover_sent"):
		user = check_user_email(form.getvalue('recovery_email'))
		if (user != None):
			recovery_email(user['email'], reset_user_pass(user['id']))
			page_header()
			recover_email_sent()
		else:
			page_header()
			auth_error("That email doesn't appear to be in our database!")
			recover_pass_page()
	elif (page == "secret"):
		page_header()
		secret_page()
	else:
		page_header()
		four_oh_four()


def main():

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
			page_header()
			search_results(search_terms, form.getvalue('filter'), form.getvalue('page_num'))
		elif ("username" in form and "password" in form):
			if (auth_login(username, password)):
				config.cur_user = read_user(config.cur_user_id, None)
				set_cookie(1, config.cur_user_id)
				page_header()
				home_page()
			else:
				page_header()
				auth_error(config.last_error)
				login_form()
		else:
			if (config.cur_user_id == None):
				page_header(1)
				home_page()
				login_form()
			else:
				page_header()
				home_page()


	page_trailer()



main()
