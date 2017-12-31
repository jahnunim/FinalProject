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
maxScore = 3
totalScore = 0

# user input: Domain name
mxRecord = input("Enter domain for Reverse DNS check:")

# Query for the domain MX
try:
    # Querying for the domain's MX records
    mxRecord = dns.resolver.query(mxRecord, 'MX')


    # Enumaretes through all the domain's MX records
    for rdata in mxRecord:
        splitMX = (rdata.to_text().split(" "))[1]
        splitMX = splitMX[:-1]
        print(splitMX)

        try:
            aRecord = dns.resolver.query(splitMX,'A')

            for adata in aRecord:
                print (adata.to_text())
        ################################## --> Still not sure what the PTR checks - MX or SMTP server name

        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are not A records for domain', mxRecord)


# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain', mxRecord)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print('There are not MX records for domain', mxRecord)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')