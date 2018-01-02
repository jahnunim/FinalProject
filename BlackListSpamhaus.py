# BlackListSpamhaus.PY checks if your mail servers are listed in Spamhaus black list.
# This to ensure that email from your organization won't be rejected.
# If your email servers are listed on a BlackList it may indicate for any potential abuse of your servers.

# Modules
import dns.resolver

# Init
bl = "zen.spamhaus.org"
myIP = "14.114.37.4"

try:
    my_resolver = dns.resolver.Resolver() #create a new resolver
    query = '.'.join(reversed(str(myIP).split("."))) + "." + bl #convert 144.76.252.9 to 9.252.76.144.zen.spamhaus.org
    answers = my_resolver.query(query, "A") #perform a record lookup. A failure will trigger the NXDOMAIN exception
    answer_txt = my_resolver.query(query, "TXT") #No exception was triggered, IP is listed in bl. Now get TXT record
    print ('IP: %s IS listed in %s (%s: %s)' %(myIP, bl, answers[0], answer_txt[0]))
except dns.resolver.NXDOMAIN:
    print('IP: %s is NOT listed in %s' %(myIP, bl))