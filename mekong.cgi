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

# Set global user variables by reading the user's cookies.

config.base_path = re.sub(r'mekong\.py\.cgi$', '', os.environ['SCRIPT_URI'])

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
			break
		else:
			config.cur_user_id = None
			config.cur_user = None

else:
	config.cur_user_id = None
	config.cur_user = None

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

def gen_verify_code(user_id):
	code = user_id

	return code

##################################################################
# Search Functions
##################################################################

# This took just as long as read_books, but now it's working,
# and I defintely understand how it works indepth now after 
# having to heavily modify it.
def search_books_terms(search_terms, catergory="default_search"):
	books = read_books()

	matches = []

#	unknown_fields = []
#	for search_term in search_terms:
#		m = re.match(r'([^:]+):', search_term)
#		if (m and m.group(1) not in ):
#			unknown_fields.append(m.group(1))

	for book in books:
		n_matches = 0
		for search_term in search_terms:
			next_book = 0
			match = 0
			term = search_term
			field = str(book[catergory])
			field = re.sub(r'[!().:]', '', field)
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


def search_books(search_string, catergory):
	search_string = re.sub('\s*$', '', search_string)
	search_string = re.sub('^\s*', '', search_string)
	return search_books_terms(search_string.split(), catergory)

def search_results(search_terms, catergory, page_num):
	matches = search_books(search_terms, catergory)
	matches_list = [matches[k][0] for k in xrange(len(matches))]
	
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
			auth_error(last_error)
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
			auth_error(config.last_error)
			recover_pass_page()
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
