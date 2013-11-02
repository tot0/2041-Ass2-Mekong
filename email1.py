# email1.py contains functions related to sending emails in python.

import smtplib
import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def verify_email(email, verification_code):
	me = "verify@mekong.com.au"
	you = email
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Mekong Account Verification"
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	text = """
		This email is to verify you own this email address and aren't some silly internet robot.
		All you need to do is go to this url:
			%s
		and we'll have you verified as soon as one of the trained monekey's on our dev team wakes up.

		Mekong - The Authors Channel To You.
		"""
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hey!<br>
	       This email is to verify you own this email address and aren't some silly internet robot.<br>
		   All you need to do is click this link: <a href="%s">OH MY GOD PLEASE CLICK ME!</a><br>
	       We'll have you verified as soon as one of the trained monekey's on our dev team wakes up.<br>
	       <br>
	       <img src="%s"></img>
	       <b>Mekong</b>, The <i>Authors</i> Channel To <i>You</i>.
	    </p>
	  </body>
	</html>
	""" % (config.base_path + "mekong.py.cgi?page=verification&code=" + str(verification_code), config.base_path + "mekong_sm.png")

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('smtp.cse.unsw.edu.au')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()


def recovery_email(email, password):
	me = "password_recovery@mekong.com.au"
	you = email
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Mekong Password Recovery"
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	text = """
		This email is to inform you we have reset your password, hopefully you told us to do this!
		Your new password is:
			%s

		Follow this link to login: %s
		Mekong - The Authors Channel To You.
		""" % (password, config.base_path + "mekong.py.cgi?page=login")
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hey!<br>
	       This email is to inform you we have reset your password, hopefully you told us to do this!<br>
		   Your new password is: <b>%s</b><br>
	       <br>
	       <a href="%s">Follow this link to login.</a><br>
	       <br>
	       <img src="%s"></img>
	       <b>Mekong</b>, The <i>Authors</i> Channel To <i>You</i>.
	    </p>
	  </body>
	</html>
	""" % (password, config.base_path + "mekong.py.cgi?page=login", config.base_path + "mekong_sm.png")

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('smtp.cse.unsw.edu.au')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()	