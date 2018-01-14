# SPF.PY checks the following:
# 1. if SPF record is present
# 2. if SPF action is configured for Hard/Soft fail

# Modules
import dns.resolver

# Init
spfRecord = None
totalScore = 0
maxScore = 0

# user inpurt: domain name
domain = input("Enter domain for SPF check:")

try:
    # Querying for the domain's TXT records
    answers = dns.resolver.query(domain, 'TXT')

    # Enumarates through all of the TXT records and pulls the SPF record
    for rdata in answers:
        if "v=spf" in rdata.to_text():
            maxScore += 1
            totalScore += 1
            spfRecord = rdata.to_text()
            print('SPF in place', spfRecord)

            # If SPF is present and configured with HardFail -
            if "-all" in spfRecord:
                maxScore += 1
                totalScore += 1

                print("HardFail inplace")
            # If HardFail not inplace
            else:
                maxScore +=1
                print("HardFail is not in place")
            break

    # Checks if SPF test passed:
    if spfRecord is None:
        print('SPF is not in place for domain:', domain)
        print(domain, 'is exposed to spoofing attacks')

    # Prints the total score of the SPF test
    print('Total SPF score for domain', domain, 'is', totalScore, '/', maxScore)

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