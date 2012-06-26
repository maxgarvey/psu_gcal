I have essentially got to the point where I am runing into this error:

          www.mail-archive.com/google-apps-mgmt-apis@googlegroups.com/msg01752.html

However, in our case, it's working with the gam command line tool, just not
sending a direct Atom XML request with the change. It looks like a pretty
current issue. I have written some code to implement when they do allow the
API to modify groupsettings, but it won't work when calling it from the app
right now, I keep getting Error 503: Service Unavailable.

Confusing thing is, when I go from the python shell, and use the exact same
library, same env, it totally does work.  
