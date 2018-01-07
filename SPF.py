# SPF.PY checks the following:
# 1. if SPF record is present
# 2. if SPF action is configured for Hard/Soft fail

# Modules
import dns.resolver

# Init
spfRecord = None
totalScore = 0
maxScore = 2

# user inpurt: domain name
domain = input("Enter domain for SPF check:")

try:
    # Querying for the domain's TXT records
    answers = dns.resolver.query(domain, 'TXT')

    # Enumarates through all of the TXT records and pulls the SPF record
    for rdata in answers:
        if "v=spf" in rdata.to_text():
            spfRecord = rdata.to_text()
            print('SPF in place', spfRecord)

    # If no SPF record is available
    if spfRecord is None:
        print('SPF is not in place for domain:', domain)
        print(domain, 'is exposed to spoofing attacks')

    # If SPF is present and configured with HardFail -
    elif "-all" in spfRecord:
        totalScore+=2
        print("HardFail inplace")

    # Is SPF is present and configured with SoftFail ~
    else:
        totalScore+=1
        print("SoftFail in place")

    # Prints the total score of the SPF test
    print('Total SPF score for domain',domain,'is',totalScore,'/',maxScore)

# If there is not such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain',domain)

# If there are no TXT records available for that domain
except (dns.resolver.NoAnswer):
    print('SPF is not in place for domain:',domain)
    print(domain, 'is exposed to spoofing attacks')
    print('Total SPF score for domain', domain, 'is', totalScore, '/', maxScore)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')