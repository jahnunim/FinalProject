#### Not sure that this test gives something.
# I will put it on hold for the meentime.

# 1. Query MX
# 2. Query A behind MX
# 3. Query PTR for IPs behind the A

# Modules
import dns.resolver

# Reset: mxRecord ,aRecord, ptrRecord, maxScore
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
        print(splitMX)

        try:
            aRecord = dns.resolver.query(splitMX,'A')

            for adata in aRecord:
                print(adata)
                ptrString = adata.to_text()
                ptrString = '.'.join(reversed(ptrString.split("."))) + ".in-addr.arpa"
                print (ptrString)
                try:
                    ptrRecord = dns.resolver.query(ptrString,'PTR')
                    print(ptrRecord)
                    maxScore+=1
                    totalScore+=1

                except (dns.resolver.NoAnswer):
                    print('No PTR records for the SMTP server', adata)
                    maxScore += 1

        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are not A records for domain', mxRecord)

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