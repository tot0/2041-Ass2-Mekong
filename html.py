# html.py contains all the functions for mekong.cgi which output html.
import config
import database
import re, os


def navbar(): 
	# make sure search terms are retained.
	m = re.match(r'^filter=[^&]*&search_terms=([^&]+)', os.environ['QUERY_STRING'])
	if m:
		search_terms = re.sub(r'%3A', ':', re.sub(r'[+]', ' ', m.group(1)))
	else:
		search_terms = ""
	print """ 
	<body style="padding-top: 50px;">

		<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
			<!-- Brand and toggle get grouped for better mobile display -->
			<div class="navbar-header">
				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="?" style="padding:5px 5px; border:0px 0px 0px 0px;"><img src="assets/mekong_sm.png" height="40" width="40" /></a>
			</div>

			<!-- Collect the nav links, forms, and other content for toggling -->
			<div class="collapse navbar-collapse navbar-ex1-collapse">
				<form class="navbar-form navbar-left" style="border:0; height:35px;" method="get">
					<div class="input-group" style="width:500px;">
						<span class="input-group-btn" style="height:35px;">
							<select id="filter" name="filter" class="dropdown-toggle">
								<option value="default_search">Filter</option>
								<option value="default_search">Default</option>
            					<option value="title">Title</option>
					            <option value="authors">Authors</option>
					            <option value="productdescription">Description</option>
					            <option value="year">Year</option>
					            <option value="publisher">Publisher</option>
          					</select>
						</span>
						<input type="text" class="form-control input-sm" placeholder="Search for books..." name="search_terms" style="top:-10px;" value="%s">
						<input type="hidden" name="page_num" value="1">
						<span class="input-group-btn">
							<button class="btn btn-default" type="submit" style="height:35px; top:-5px;"><span class="glyphicon glyphicon-search" style="top:-2px;"></span></button>
						</span>
					</div>
				</form>
	""" % (search_terms)
	if (config.cur_user_id != None):
		first_name = config.cur_user['first_name']
		print """
				<ul class="nav navbar-nav navbar-right">
					<li class="dropdown" style="top:8px; right:-65px;">
						<a href="#" class="dropdown-toggle" data-toggle="dropdown" style="border:0 !important;">%s <b class="caret"></b></a>
						<ul class="dropdown-menu">
							<li><a href="?page=account">Account</a></li>
							<li>
								<a href="?page=cart">
									Cart
									<span class="label label-default" style="background-color:#16a085;">%s</span>
								</a>
							</li>
							<li><a href="?page=orders">Orders</a></li>
							<li><a href="?page=logout">Log Out</a></li>
						</ul>
					</li>
				</ul>
			</div><!-- /.navbar-collapse -->
		</nav>

		""" % (first_name, database.get_user_cart_num_items(config.cur_user_id))
	else:
		print """
				<div class="nav navbar-nav navbar-right">
					<a href="?page=login" class="btn" style="border:0 !important; margin-top:3px;">Log in</a>
				</div>
			</div><!-- /.navbar-collapse -->
		</nav>
		"""


def page_header(homepage=0):
	print "Content-type: text/html;charset=utf-8"
	print ""
	print """
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>mekong.com.au</title>

			<!-- Favicon -->
			<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
			<link rel="icon" href="favicon.ico" type="image/x-icon">

			<!-- ALL THE CSS -->
			<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css" rel="stylesheet">
			<link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
			<link href="assets/mekong.css" rel="stylesheet">
			<link href="assets/flatui/bootstrap.css" rel="stylesheet">
			<link href="assets/flatui/flat-ui.css" rel="stylesheet">

		</head>
	"""
	if not homepage:
		navbar()


def home_page():
	print """
		<!-- Full Page Image Header Area -->
		<div id="top" class="header">
			<div class="vert-text">
				<h1 class="logo" style="text-shadow: 3px 3px 2px rgba(150, 150, 150, 1);">Mekong</h1>
				<h3 class="logo" style="text-shadow: 3px 3px 2px rgba(150, 150, 150, 1);">The <em>Authors</em> Channel To <em>Yo<a href="?page=secret" style="color:white;">u</a></em></h3>
				<form class="">
					<style>
						.input-group-lg-home {
							max-width: 500px;
							padding: 15px;
							margin: 0 auto;
						}
					</style>
					<div class="input-group input-group-lg-home">
						<input type="hidden" name="filter" value="default_search">
						<input type="text" class="form-control" placeholder="Search for books..." name="search_terms" autofocus>
						<input type="hidden" name="page_num" value="1">
						<span class="input-group-btn">
							<button class="btn btn-primary" type="submit" style="padding-bottom:11px;"><span class="glyphicon glyphicon-search"></span></button>
						</span>
					</div>
	"""
	if (config.cur_user_id == None):
		print """
						<h3 style="text-shadow: 3px 3px 2px rgba(150, 150, 150, 1);">Or...</h3>
					</form>
					<a class="btn btn-primary" href="#login">Log in</a>
		"""
	print """
			</div>
		</div>
		<!-- /Full Page Image Header Area -->
	"""

def login_form():
	print """
		<div id="login" class="row col-sm-12">
			<div class="col-sm-6" style="padding:20px 0px 50px 0px;">
				<form method="post" class="form-signin" action="?">
	        		<h2 class="form-signin-heading">Please sign in</h2>
	        		<input type="text" class="form-control" placeholder="Username" name="username">
	        		<input type="password" class="form-control" placeholder="Password" name="password">
	        		<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
	      			<a href="?page=recover_pass" style="font-size: 15px;">Can't remeber your password? Click Here.</a>
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

# This tutorial helped ALOT http://www.9lessons.info/2012/04/bootstrap-registration-form-tutorial.html
def register_form():
	print """
		<div class="container">
			<form id="registration" role="form" method="post">
				<fieldset>
					<h3>Personal Details</h3>
					<div class="form-group">
						<label class="sr-only">First Name</label>
						<input id="first_name" class="form-control input-lg" type="text" name="first_name_reg" placeholder="First Name" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Last Name</label>
						<input id="last_name" class="form-control input-lg" type="text" name="last_name_reg" placeholder="Last Name" required>
					</div>
					<div class="form-group">
						<label class="sr-only" for="username">Username</label>
						<input id="username" class="form-control input-lg" type="text" name="username_reg" placeholder="Username" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Password</label>
						<input id="password" class="form-control input-lg" type="password" name="password_reg" placeholder="Password" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Confirm Password</label>
						<input id="confirm_password" class="form-control input-lg" type="password" name="password_con_reg" placeholder="Confirm Password" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Email</label>
						<input id="email" class="form-control input-lg" type="email" name="email_reg" placeholder="Email" required>
					</div>
					<hr style="border-top:1px solid #5a5a5a;">
					<h3>Address Details</h3>
					<div class="form-group">
						<label class="sr-only">Street Address</label>
						<input id="street" class="form-control input-lg" type="text" name="street_reg" placeholder="Street Address e.g. 16 Vantage Pl" required>
					</div>
					<div class="form-group">
						<label class="sr-only">City</label>
						<input id="city" class="form-control input-lg" type="text" name="city_reg" placeholder="City" required>
					</div>
					<div class="form-group">
						<label class="sr-only">State</label>
						<select id="state" name="state_reg" value="NSW" required>
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
						<input id="postcode" class="form-control input-lg" type="number" min="1" name="postcode_reg" placeholder="Postcode" required>
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
					<input type="hidden" name="page_num" value="1">
					<span class="input-group-btn">
					<button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
					</span>
				</div>

			</form>
	"""

def pagination(num_pages):
	pos1_active = ""
	pos2_active = ""
	pos3_active = ""
	pos4_active = ""
	pos5_active = ""
	pos6_active = ""
	pos7_active = ""
	pos8_active = ""
	pos9_active = ""
	m = re.match(r'^filter=([^&]*)&search_terms=([^&]*)&page_num=([^&]*)', os.environ['QUERY_STRING'])
	if m:
		filter_str = "?filter=" + m.group(1) + "&"
		page_num = int(m.group(3))
		terms = m.group(2)

	if (page_num == 1):
		pos1_active = "class=\"active\""
		pos0 = filter_str + "search_terms=" + terms + "&page_num=1"
		pos1 = filter_str + "search_terms=" + terms + "&page_num=1"
		pos1_label = "1"
		pos2 = filter_str + "search_terms=" + terms + "&page_num=2"
		pos2_label = "2"
		pos3 = filter_str + "search_terms=" + terms + "&page_num=3"
		pos3_label = "3"
		pos4 = filter_str + "search_terms=" + terms + "&page_num=4"
		pos4_label = "4"
		pos5 = filter_str + "search_terms=" + terms + "&page_num=5"
		pos5_label = "5"
		pos6 = filter_str + "search_terms=" + terms + "&page_num=6"
		pos6_label = "6"
		pos7 = filter_str + "search_terms=" + terms + "&page_num=7"
		pos7_label = "7"
		pos8 = filter_str + "search_terms=" + terms + "&page_num=8"
		pos8_label = "8"
		pos9 = filter_str + "search_terms=" + terms + "&page_num=9"
		pos9_label = "9"
		pos10 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 1)
	elif (page_num < 5):
		if (page_num == 2):
			pos2_active = "class=\"active\""
		elif (page_num == 3):
			pos3_active = "class=\"active\""
		elif (page_num == 4):
			pos4_active = "class=\"active\""
		pos0 = filter_str + "search_terms=" + terms + "&page_num="  + str(page_num - 1)
		pos1 = filter_str + "search_terms=" + terms + "&page_num=1"
		pos1_label = "1"
		pos2 = filter_str + "search_terms=" + terms + "&page_num=2"
		pos2_label = "2"
		pos3 = filter_str + "search_terms=" + terms + "&page_num=3"
		pos3_label = "3"
		pos4 = filter_str + "search_terms=" + terms + "&page_num=4"
		pos4_label = "4"
		pos5 = filter_str + "search_terms=" + terms + "&page_num=5"
		pos5_label = "5"
		pos6 = filter_str + "search_terms=" + terms + "&page_num=6"
		pos6_label = "6"
		pos7 = filter_str + "search_terms=" + terms + "&page_num=7"
		pos7_label = "7"
		pos8 = filter_str + "search_terms=" + terms + "&page_num=8"
		pos8_label = "8"
		pos9 = filter_str + "search_terms=" + terms + "&page_num=9"
		pos9_label = "9"
		pos10 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 1)
	elif (page_num == num_pages):
		pos9_active = "class=\"active\""
		pos0 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos1 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 4)
		pos1_label = str(page_num - 4)
		pos2 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 3)
		pos2_label = str(page_num - 3)
		pos3 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 2)
		pos3_label = str(page_num - 2)
		pos4 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos4_label = str(page_num - 1)
		pos5 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 4)
		pos5_label = str(page_num)
		pos6 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 3)
		pos6_label = str(page_num + 1)
		pos7 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 2)
		pos7_label = str(page_num + 2)
		pos8 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 1)
		pos8_label = str(page_num + 3)
		pos9 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages)
		pos9_label = str(page_num + 4)
		pos10 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages)
	elif (page_num > (num_pages - 4)):
		if (page_num == num_pages - 3):
			pos6_active = "class=\"active\""
		elif (page_num == num_pages - 2):
			pos7_active = "class=\"active\""
		elif (page_num == num_pages - 1):
			pos8_active = "class=\"active\""
		pos0 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos1 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 4)
		pos1_label = str(page_num - 4)
		pos2 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 3)
		pos2_label = str(page_num - 3)
		pos3 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 2)
		pos3_label = str(page_num - 2)
		pos4 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos4_label = str(page_num - 1)
		pos5 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 4)
		pos5_label = str(page_num)
		pos6 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 3)
		pos6_label = str(page_num + 1)
		pos7 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 2)
		pos7_label = str(page_num + 2)
		pos8 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages - 1)
		pos8_label = str(page_num + 3)
		pos9 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages)
		pos9_label = str(page_num + 4)
		pos10 = filter_str + "search_terms=" + terms + "&page_num=" + str(num_pages)
	else:
		pos5_active = "class=\"active\""
		pos0 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos1 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 4)
		pos1_label = str(page_num - 4)
		pos2 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 3)
		pos2_label = str(page_num - 3)
		pos3 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 2)
		pos3_label = str(page_num - 2)
		pos4 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num - 1)
		pos4_label = str(page_num - 1)
		pos5 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num)
		pos5_label = str(page_num)
		pos6 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 1)
		pos6_label = str(page_num + 1)
		pos7 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 2)
		pos7_label = str(page_num + 2)
		pos8 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 3)
		pos8_label = str(page_num + 3)
		pos9 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 4)
		pos9_label = str(page_num + 4)
		pos10 = filter_str + "search_terms=" + terms + "&page_num=" + str(page_num + 1)

	print """
			<div class="pagination">
				<ul>
					<li class="previous"><a href="%s" class="fui-arrow-left"></a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li %s><a href="%s">%s</a></li>
					<li class="next"><a href="%s" class="fui-arrow-right"></a></li>
				</ul>
          	</div>
	""" % (pos0, pos1_active, pos1, pos1_label, pos2_active, pos2, pos2_label, pos3_active, pos3, pos3_label, pos4_active, pos4, pos4_label, pos5_active, pos5, pos5_label, pos6_active, pos6, pos6_label, pos7_active, pos7, pos7_label, pos8_active, pos8, pos8_label, pos9_active, pos9, pos9_label, pos10)

def start_table(display_range, num_books):
	print """
		<div class="row col-sm-12">
			<div class="col-lg-2"></div>
			<div class="col-lg-8">
				<center>
					<h6>Displaying %s of %s results...</h6>
				</center>
				<table class="table table-hover col-lg-8">
	""" % (display_range, num_books)


def display_search_result(isbn):
	book = database.read_book(isbn)

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
						<td class="pull-right" style="height:100%%;">
							<a class="btn btn-primary" href="?page=cart&num_books=1&book_add=%s" style="background-color:#9b59b6;"><span class="glyphicon glyphicon-shopping-cart"></span></a>
							<strong style="color:#8e44ad;">%s</strong>
						</td>
					</tr>
	""" % (book['smallimageurl'], book['isbn'], book['title'], book['authors'], book['isbn'], book['price'])

def end_table(pag, num_pages):
	print """
				</table>
			</div>
			<div class="col-lg-2"></div>
		</div>
		<center>
	"""
	if pag:
		pagination(num_pages)
	print """
		</center>
	"""


def book_page(isbn):
	book = database.read_book(isbn)
#style="max-width: %spx;"
	print """
			<div class="row">
				<div class="col-sm-1 col-md-1 col-lg-2"></div>
				<div class="col-sm-4 col-md-4 col-lg-3">
					<center><img class="img-responsive" style="border: 3px solid #000; margin-top:22px;" src="%s"/></center>
					<br>
					<table class="table" style="margin-right:100px;">
						<tr>
							<td>
								Catalog:
							</td>
							<td>
								%s
							</td>
						</tr>
						<tr>
							<td>
								Binding:
							</td>
							<td>
								%s
							</td>
						</tr>
						<tr>
							<td>
								No. Pages:
							</td>
							<td>
								%s
							</td>
						</tr>
						<tr>
							<td>
								Sales Rank:
							</td>
							<td>
								%s
							</td>
						</tr>
						<tr>
							<td>
								Edition:
							</td>
							<td>
								%s
							</td>
						</tr>
					</table>
				</div>

				<div class="col-sm-6 col-md-6 col-lg-5">
					<h2><strong>%s</strong></h2>
					by	%s </br>
					<hr style="border-top:1px solid #5a5a5a;">
					<p>%s</p>
					<hr style="border-top:1px solid #5a5a5a;">
					Date Published: <b>%s</b> by <em>%s</em></br>

					</br>

					<div class="well" style="padding:5px 5px 5px 5px; ">
						<div class="pull-left" style="margin-top:5px;">
							Price: <em><strong>%s</strong></em>
						</div>
						<form method="get" class="pull-right" style="max-width:200px;">
							<input type="hidden" name="page" value="cart">
							<input type="hidden" name="book_add" value="%s">
							<div class="input-group">
      							<input class="form-control pull-right" type="number" name="num_books" max="1000000000000" min="1" value="1" style="max-width:70px;">
      							<span class="input-group-btn">
        							<button class="btn btn-primary" type="submit" style="height:42px;">Add to Cart</button>
  								</span>
    						</div>				
						</form>
						<div class="clearfix"></div>
					</div>
				</div>
				<div class="col-sm-1 col-md-1 col-lg-2"></div>
			</div>
	""" % ( book['largeimageurl'], book['catalog'], book['binding'], book['numpages'], book['salesrank'], book['edition'], book['title'], book['authors'], book['productdescription'], book['publication_date'], book['publisher'], book['price'], book['isbn'])
	m = re.match(r'^([^,]*)' ,book['authors'])
	author_books(m.group(1), book['isbn'])


def author_books(author, current_isbn):
	books = database.read_books_by_author(author)

	print """
		<div class="row">
			<div class="col-sm-1 col-md-1 col-lg-2"></div>
			<div class="col-sm-10 col-md-10 col-lg-8">
				<h4 style="text-align:center;">More by this author...</h4>		
				<table class="table table-hover col-lg-8">
	"""
	i = 0
	for book in books:
		i += 1
		if (book['isbn'] != current_isbn):
			display_search_result(book['isbn'])
		if (i == 10):
			break

	print """
				</table>
			</div>
			<div class="col-sm-1 col-md-1 col-lg-2"></div>
		</div>
	"""

def cart_page():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px; padding-bottom:20px;">
				<h3 style="text-align:center;">You have %s items in your cart.</h3>
			</div>
		</div>
		<form method="post" action="?page=update_cart">
		<div class="row col-sm-12">
			<div class="col-lg-2"></div>
			<div class="col-lg-8">
				<table class="table table-hover col-lg-8" style="margin:20px;">
					<thead>
						<tr>
							<th></th>
							<th>Book</th>
							<th>Price</th>
							<th>Quantity</th>
							<th>Total</th>
						</tr>
					</thead>
	""" % (database.get_user_cart_num_items(config.cur_user_id))
	total_price = 0
	cart = database.get_user_cart(config.cur_user_id)
	for item in cart:
		book = database.read_book(item['isbn'])
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
						<td>
							<strong>%s</strong>
						</td>
						<td>
							<input class="input-sm" type="number" name="num_books_%s" min="1" max="1000000000000" value="%s" style="max-width:100px;"></br>
							<label>
								<input type="checkbox" name="remove_%s" value="remove">
								Remove
							</label>
							</div>
						</td>
						<td>
							<strong>$%s</strong>
						</td>
					</tr>
		""" % (book['smallimageurl'], book['isbn'], book['title'], book['authors'], book['price'], book['isbn'], item['num'], book['isbn'], (float(item['num']) * float(re.sub(r'\$', '', book['price']))))
		total_price += (float(item['num']) * float(re.sub(r'\$', '', book['price'])))
	print """
					<thead>
						<tr>
							<th></th>
							<th></th>
							<th></th>
							<th>Sum Total:</th>
							<th>$%s</th>
						</tr>
					</thead>
				</table>
			</div>
			<div class="col-lg-2"></div>
		</div>
	"""	% total_price
	print """
			<center>
				<button class="btn btn-primary" type="submit" style="background-color:#3498db;">Update Cart</button>
				<a class="btn btn-primary" type="button" href="?page=checkout" style="background-color:#2ecc71">Checkout</a>
			</center>
		</form>
	"""

def checkout_page():
	print """
		<div class="row col-sm-12">
			<div class="col-sm-2 col-md-4 col-lg-4"></div>
			<div class="col-sm-8 col-md-4 col-lg-4">
				<form method="post" action="?page=checkout_complete">
					<h3 style="text-align:center;">Shipping Details</h3>
					<input class="form-control" type="text" name="name_checkout" value="%s">
					<input class="form-control" type="text" name="street_address_checkout" value="%s">
					<input class="form-control" type="text" name="city_checkout" value="%s">
					<div class="row">
						<div class="col-sm-6">
							<select id="state" class="" name="state_checkout" value="%s" style="width">
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
						<div class="col-sm-6 pull-right">
							<label class="sr-only">Postcode</label>
							<input id="postcode" class="form-control input-lg pull-right" type="text" name="postcode_checkout" placeholder="Postcode" value="%s">
						</div>
					</div>
					<h3 style="text-align:center;">Payment Details</h3>
					<input class="form-control" type="number" min="1" name="cc_checkout" placeholder="Credit Card Number" required>
					<input class="form-control" type="text" name="cc_expire_checkout" placeholder="Card Expiry Date (mm/yy)" required>
					<center><button class="btn btn-primary" type="submit" style="margin:10px;">Complete Order</button></center>
				</form>
			</div>
			<div class="col-sm-2 col-md-4 col-lg-4"></div>
		</div>		
	""" % ((config.cur_user['first_name'] + " " + config.cur_user['last_name']), config.cur_user['street'], config.cur_user['city'], config.cur_user['state'], config.cur_user['postcode'])

	print """
		<div class="row col-sm-12">
			<div class="col-lg-2"></div>
			<div class="col-lg-8">
				<table class="table table-hover col-lg-8" style="margin:20px;">
					<thead>
						<tr>
							<th></th>
							<th>Book</th>
							<th>Price</th>
							<th>Quantity</th>
							<th>Total</th>
						</tr>
					</thead>
	"""
	total_price = 0
	for item in database.get_user_cart(config.cur_user_id):
		book = database.read_book(item['isbn'])
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
						<td>
							<strong>%s</strong>
						</td>
						<td>
							<input class="input-sm" type="number" name="num_books_%s" min="1" value="%s" style="max-width:100px;" disabled></br>
						</td>
						<td>
							<strong>$%s</strong>
						</td>
					</tr>
		""" % (book['smallimageurl'], book['isbn'], book['title'], book['authors'], book['price'], book['isbn'], item['num'], (float(item['num']) * float(re.sub(r'\$', '', book['price']))))
		total_price += (float(item['num']) * float(re.sub(r'\$', '', book['price'])))
	print """
					<thead>
						<tr>
							<th></th>
							<th></th>
							<th></th>
							<th>Sum Total:</th>
							<th>$%s</th>
						</tr>
					</thead>
				</table>
			</div>
			<div class="col-lg-2"></div>
		</div>
	"""	% total_price
	print """
		<center>
			<a class="btn btn-default" href="?page=cart" style="background-color:#3498db;">Edit Cart</a>
		</center>

	"""

def orders_page():
	orders = database.get_user_orders(config.cur_user_id)
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px; padding-bottom:20px;">
				<h3 style="text-align:center;">You have made %s orders.</h3>
			</div>
		</div>
	""" % (len(orders))
	for order in orders:
		total_price = 0	
		print """
		<br>
		<div class="row col-sm-12">
			<div class="col-lg-2"></div>
			<div class="col-lg-8">
				<div class="row">
					<div class="col-sm-1"></div>
					<div class="col-sm-5 pull-left">
						<div class="h3">Order ID: %s </br></div>
						<div class="h7">Timestamp: <b>%s</b></div>
					</div>
					<div class="col-sm-5" style="bottom:-16px;">
						<div class="h6">Credit Card No.: %s </br></div>
						<div class="h7">Credit Card Expiry: <b>%s</b></div>
					</div>
				</div>
				<div class="col-sm-1"></div>
				<table class="table table-hover col-lg-8" style="margin:20px;">
					<thead>
						<tr>
							<th></th>
							<th>Book</th>
							<th>Price</th>
							<th>Quantity</th>
							<th>Total</th>
						</tr>
					</thead>
		""" % (order['id'], order['time_stamp'], re.sub(r'^\d{12}', r'************', str(order['cc_num'])), order['cc_exp'])
		total_price = 0
		for item in order['items']:
			book = database.read_book(item['isbn'])
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
						<td>
							<strong>%s</strong>
						</td>
						<td>
							<input class="input-sm" type="number" name="num_books_%s" min="1" value="%s" style="max-width:100px;" disabled></br>
						</td>
						<td>
							<strong>$%s</strong>
						</td>
					</tr>
			""" % (book['smallimageurl'], book['isbn'], book['title'], book['authors'], book['price'], book['isbn'], item['num'], (float(item['num']) * float(re.sub(r'\$', '', book['price']))))
			total_price += (float(item['num']) * float(re.sub(r'\$', '', book['price'])))
		print """
				<thead>
					<tr>
						<th></th>
						<th></th>
						<th></th>
						<th>Sum Total:</th>
						<th>$%s</th>
					</tr>
				</thead>
			</table>
		</div>
		<div class="col-lg-2"></div>
	</div>
		"""	% total_price

def email_validate_page():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px;">
				<h1 style="text-align:center;">An email has been dispatched via boat!</h1>
				<h4>You will need to open the link in the email to verify your account, only verified accounts are able to login.</h4>
				<center><a class="btn btn-primary" href="?">Drift Home</a></center>
			</div>
		</div>
	"""

def validation_success():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px;">
				<h1 style="text-align:center;">Validation Successful</h1>
				<a class="btn btn-primary" href="?">Drift Home</a>
				<a class="btn btn-primary" href="?page=login">Login</a>
			</div>
		</div>
	"""
def recover_pass_page():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px;">
				<form method="post" action="?page=recover_sent">
					<h1 style="text-align:center;">No Worries!</h1>
					<h4>Just give us the email you used when creating your account and we'll reset your password, then send it to you.</h4>
					<input class="form-control input-lg" type="email" name="recovery_email" placeholder="Enter email associated with your account..." required></input>
					<center><button class="btn btn-primary" type="submit">Send Email</button></center>
				</form>
			</div>
		</div>
	"""

def recover_email_sent():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px; text-align:center;">
				<h1>Cool Beans!</h1>
				<h3>It's off to your inbox!</h3>
				<a class="btn btn-primary" href="?">Drift Home</a>
				<a class="btn btn-primary" href="?page=login">Login</a>
			</div>
		</div>
	"""	

def login_4_cart():
	print """
		<div class="container">
			<div class="jumbotron" style="margin-top:20px; padding-top:10px; text-align:center;">
				<h1>Oops!</h1>
				<h3>Sorry only registered users can use the cart feature of Mekong!</h3>
				<h5>If you would like to purchase some books please login, or register.</h5>
				<a class="btn btn-primary" href="?page=register">Register</a>
				<a class="btn btn-primary" href="?">Drift Home</a>
				<a class="btn btn-primary" href="?page=login">Login</a>
			</div>
		</div>
	"""

def account_page():
	print """
		<div class="container">
			<form id="registration" role="form" method="post" action="?page=updated_details">
				<fieldset>
					<h3>Personal Details</h3>
					<div class="form-group">
						<label class="sr-only">First Name</label>
						<input id="name" class="form-control input-lg" type="text" name="first_name_reg" placeholder="First Name" value="%s" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Last Name</label>
						<input id="name" class="form-control input-lg" type="text" name="last_name_reg" placeholder="Last Name" value="%s" required>
					</div>
					<div class="form-group">
						<label class="sr-only" for="username">Username</label>
						<input id="username" class="form-control input-lg" type="text" name="username_reg" placeholder="Username" value="%s" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Password</label>
						<input id="password" class="form-control input-lg" type="password" name="password_reg" placeholder="Password" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Confirm Password</label>
						<input id="password" class="form-control input-lg" type="password" name="password_con_reg" placeholder="Confirm Password" required>
					</div>
					<div class="form-group">
						<label class="sr-only">Email</label>
						<input id="email" class="form-control input-lg" type="email" name="email_reg" placeholder="Email" value="%s" required>
					</div>
					<hr style="border-top:1px solid #5a5a5a;">
					<h3>Address Details</h3>
					<div class="form-group">
						<label class="sr-only">Street Address</label>
						<input id="street" class="form-control input-lg" type="text" name="street_reg" placeholder="Street Address e.g. 16 Vantage Pl" value="%s" required>
					</div>
					<div class="form-group">
						<label class="sr-only">City</label>
						<input id="city" class="form-control input-lg" type="text" name="city_reg" placeholder="City" value="%s" required>
					</div>
					<div class="row">
						<div class="col-sm-6">
							<div class="form-group">
								<label class="sr-only">State</label>
								<select id="state" name="state_reg" style="width" required>
									<option value="0">NSW</option>
									<option value="1">QLD</option>
									<option value="2">VIC</option>
									<option value="3">WA</option>
									<option value="4">SA</option>
									<option value="5">ACT</option>
									<option value="6">NT</option>
									<option value="7">TAS</option>
								</select>
								<script>$(document).ready($('#state').val('%s'));</script>
							</div>
							</div>
							<div class="col-sm-6 pull-right">
							<div class="form-group">
								<label class="sr-only">Postcode</label>
								<input id="postcode" class="form-control input-lg pull-right" type="number" min="1" name="postcode_reg" placeholder="Postcode" value="%s" required>
							</div>
						</div>
					</div>
					<div class="form-group">
						<center><button class="btn btn-primary btn-lg" type="submit">Update</button></center>
					</div>
				</fieldset>
			</form>
		</div>
	""" % (config.cur_user['first_name'], config.cur_user['last_name'], config.cur_user['username'], config.cur_user['email'], config.cur_user['street'], config.cur_user['city'], config.cur_user['state'], config.cur_user['postcode'])

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
			<div id="top" class="header" style="background: url(assets/mekong_ohno.jpg) no-repeat center center fixed;">
				<div class="vert-text" style="color: black; vertical-align:text-top; padding:100px 0px 0px 0px;">
					<h1 class="" style="text-shadow: 1px 1px 0px rgba(255, 255, 255, 1);">Oops!</h1>
					<h3 class="" style="text-shadow: 2px 2px 3px rgba(255, 255, 255, 1);">It appears while enjoying <strong>Mekong</strong></br> you've veered into a sand bank!</h3>

					<a class="btn btn-primary" href="?">Drift Home</a>
				</div>
			</div>
	"""

def secret_page():
	print """
			<div id="top" class="header" style="background: url(assets/mekong_secret.jpg) no-repeat center center fixed;">
				<div class="vert-text" style="color: black; vertical-align:text-top; padding:100px 0px 0px 0px;">
					<h1 class="" style="text-shadow: 1px 1px 0px rgba(255, 255, 255, 1);">Oops!</h1>
					<h3 class="" style="text-shadow: 2px 2px 3px rgba(255, 255, 255, 1);">Well this is a bit <strong>Awkward</strong></br> no ones supposed to see this...</h3>

					<a class="btn btn-primary" href="?">Drift Home</a>
				</div>
			</div>
	"""


def page_trailer():
	print """
		<script src="assets/js/jquery-1.8.3.min.js"></script>
	    <script src="assets/js/jquery-ui-1.10.3.custom.min.js"></script>
	    <script src="assets/js/jquery.ui.touch-punch.min.js"></script>
	    <script src="assets/js/bootstrap.min.js"></script>
	    <script src="assets/js/bootstrap-select.js"></script>
	    <script src="assets/js/bootstrap-switch.js"></script>
	    <script src="assets/js/flatui-checkbox.js"></script>
	    <script src="assets/js/flatui-radio.js"></script>
	    <script src="assets/js/jquery.tagsinput.js"></script>
	    <script src="assets/js/jquery.placeholder.js"></script>
	    <script src="assets/js/jquery.validate.min.js"></script>


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

		<script>
			$("select").selectpicker({style: 'btn-hg btn-primary', menuStyle: 'dropdown-inverse'});
		</script>
		<script>
			$('.dropdown-toggle').width(150).height(35);
			$('.dropdown-toggle').css('padding', '0');
		</script>
	</body>
</html>
	"""