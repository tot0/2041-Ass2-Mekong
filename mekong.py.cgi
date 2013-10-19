#!/usr/bin/env python
#Lucas Pickup, z3424653, lpickup

import cgi
import cgitb
cgitb.enable()  # for troubleshooting

print "Content-type: text/html;charset=utf-8"
print

print """
    <html>

        <head><title>Sample CGI Script</title></head>

        <body>

            <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

print """

            <p>Previous message: %s</p>

            <p>form

            <form method="post">
                <p>message: <input type="text" name="message"/></p>
            </form>

        </body>

</html>
""" % cgi.escape(message)