# MX.PY checks if the domain has multiple MX records
# Advise to make sure additional MX endpoints are secured as the primary endpoint.

# Domain based test

# Modules
import dns.resolver

# Init
mxRecords = None
maxScore = 3
totalScore = 0


# user input: Domain name
domain = input("Enter domain for MX records check:")

try:
    # Querying for the domain's MX records
    mxRecords = dns.resolver.query(domain, 'MX')

    # Enumerates through all of the MX records
    if len(mxRecords) == 1:
        print('Only 1 MX record available for domain',domain)
        print ('MX record:',mxRecords[0].to_text())
        print('Please make sure that your MX points to a secured relay')
    if len(mxRecords) > 1:
        print('There are multiple MX records for domain', domain)
        for rdata in mxRecords:
            print('MX record:',rdata.to_text())

        print('Please make sure that your additional MX endpoints are secured as your primary MX.')

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain',domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print ('There are no MX records for domain',domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')