# BlackListSpamhaus.PY checks if your mail servers are listed in Spamhaus black list.
# This to ensure that email from your organization won't be rejected.
# If your email servers are listed on a BlackList it may indicate for any potential abuse of your servers.

# IP based domain

# Modules
import dns.resolver

# Init
bl = "zen.spamhaus.org"
#myIP = "14.114.37.4"
mxRecord = None
aRecord = None
ptrRecord = None
maxScore = 0
totalScore = 0

# user input: Domain name
domain = input("Enter domain for black list check:")

# Query for the domain MX
try:
    # Querying for the domain's MX records
    mxRecord = dns.resolver.query(domain, 'MX')

    # Enumaretes through all the domain's MX records
    for rdata in mxRecord:
        splitMX = (rdata.to_text().split(" "))[1]
        splitMX = splitMX[:-1]

        # Pulls the A records behind the MX records
        try:
            aRecord = dns.resolver.query(splitMX,'A')

            # for each A record, check if a PTR record is present.\
            for adata in aRecord:
                # Query for Spamhaus zone, if no result returns - IP not listed in black list
                try:
                    # New DNS resolver
                    my_resolver = dns.resolver.Resolver()

                    # Builds the query
                    query = '.'.join(reversed(str(adata).split("."))) + "." + bl

                    # Queries Spamhaus DNS.
                    answers = my_resolver.query(query,"A")

                    # If no exception was triggered, IP is listed in bl.
                    # Gets the TXT record to build te link for details.
                    maxScore +=1
                    answer_txt = my_resolver.query(query,"TXT")
                    print('IP: %s IS listed in %s (%s: %s)' % (adata, bl, answers[0], answer_txt[0]))

                # Exception raised, IP not listed in BL.
                except(dns.resolver.NXDOMAIN):
                    maxScore += 1
                    totalScore +=1
                    print('IP: %s is NOT listed in %s' % (adata, bl))

        except (dns.resolver.NoAnswer):
        print('There are not A records for domain', domain)

    print('Total ReverseDNS score for domain', domain, 'is', totalScore, '/', maxScore)

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain', domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print('There are not MX records for domain', domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')