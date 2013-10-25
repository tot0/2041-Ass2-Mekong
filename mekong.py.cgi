#!/usr/bin/python2.7
#Lucas Pickup, z3424653, lpickup

import cgi, Cookie
import cgitb
import re, os
import json, sqlite3
from Book_class import Book
#import Book_class
cgitb.enable(display=0, logdir="./logs")  # for troubleshooting

book_file = "books.json"
db_dir = "mekong.db"
last_error = ""

def read_user(user_id):
	con = sqlite3.connect(db_dir)

	with con:
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute('select * from users')
		
		rows = cur.fetchall()

		for row in rows:
			if (row['id'] == user_id):
				break
	return row

if ("HTTP_COOKIE" in os.environ):
	cookies = os.environ['HTTP_COOKIE']
	cookies = cookies.split('; ')
	for cookie in cookies:
		cookie = cookie.split('=')
		name = cookie[0]
		value = cookie[1]
		if (name == "user_id"):
			cur_user_id = value
			cur_user = read_user(cur_user_id)

else:
	cur_user_id = None
	cur_user = None

def page_header(cookie=0, user_id=0):
	global cur_user_id

	if (cookie == 1):
		user_cookie = Cookie.SimpleCookie()
		user_cookie['user_id'] = user_id
		print user_cookie
	elif (cookie == 2):
		user_cookie = Cookie.SimpleCookie()
		user_cookie['user_id'] = user_id
		user_cookie['user_id']['expires'] = 0
		print user_cookie


	if (cur_user_id != None):
		first_name = cur_user['first_name']
		disabled = ""
	else:
		first_name = "No User"
		disabled = "disabled" 

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
		<link href="//netdna.bootstrapcdn.com/bootswatch/3.0.0/slate/bootstrap.min.css" rel="stylesheet">
		<link href="stylish-portfolio.css" rel="stylesheet">
		<link href="flat-ui.css" rel="stylesheet">
		<link href="mekong.css" rel="stylesheet">

	</head>

	<body style="padding-top: 50px;">

		<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
			<!-- Brand and toggle get grouped for better mobile display -->
			<div class="navbar-header">
				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="?" style="padding:5px 15px;"><img src="mekong_sm.png" height="40" width="40" /></a>
			</div>

			<!-- Collect the nav links, forms, and other content for toggling -->
			<div class="collapse navbar-collapse navbar-ex1-collapse">
				<ul class="nav navbar-nav">
					<!-- <li><a href="#">Link</a></li> -->
				</ul>
				<form class="navbar-form navbar-left">
					<style>
						.input-group-lg-nav {
							max-width: 500px;
							padding: 0px;
							margin: 0 auto;
						}
					</style>
					<div class="input-group input-group-lg-nav">
						<input type="text" class="form-control" placeholder="Search for books..." name="search_terms">
						<span class="input-group-btn">
						<button class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
						</span>
					</div>

				</form>
				<ul class="nav navbar-nav navbar-right">
					<li class="dropdown %s">
						<a href="#" class="dropdown-toggle %s" data-toggle="dropdown">%s <b class="caret"></b></a>
						<ul class="dropdown-menu">
							<li><a href="?page=account">Account</a></li>
							<li><a href="?page=basket">Basket</a></li>
							<li><a href="?page=orders">Orders</a></li>
							<li><a href="?page=logout">Log Out</a></li>
						</ul>
					</li>
				</ul>
			</div><!-- /.navbar-collapse -->
		</nav>

	""" % (disabled, disabled, first_name)

def home_page():
	print """
		<!-- Full Page Image Header Area -->
		<div id="top" class="header">
			<div class="vert-text">
				<h1 class="logo">Mekong</h1>
				<h3 class="logo">The <em>Authors</em