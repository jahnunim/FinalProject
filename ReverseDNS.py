# REVERSEDNS.PY checks if the MX records behind the domain has PTR.
# If PTR is missing, the domain's SMTP connection might be rejected due to Reverse DNS test.

# IP TEST

# Modules
import dns.resolver

# Init
mxRecord = None
aRecord = None
ptrRecord = None
maxScore = 0
totalScore = 0

# user input: Domain name
domain = input("Enter domain for Reverse DNS check:")

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

                # Builds the PTR record string
                ptrString = adata.to_text()
                ptrString = '.'.join(reversed(ptrString.split("."))) + ".in-addr.arpa"
                print (ptrString)

                # Pulls the PTR record
                try:
                    ptrRecord = dns.resolver.query(ptrString,'PTR')
                    print(ptrRecord)
                    maxScore+=1
                    totalScore+=1

                # If no PTR record
                except (dns.resolver.NXDOMAIN):
                    print('No PTR records for the SMTP server', adata)
                    maxScore += 1

        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are no A records for domain', mxRecord)

    print('Total ReverseDNS score for domain', domain, 'is', totalScore, '/', maxScore)

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain', domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print('There are no MX records for domain', domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')