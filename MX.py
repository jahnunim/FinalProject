# Modules
import dns.resolver

# Reset: mxRecords, score?
mxRecord = None
maxScore = 3
totalScore = 0


# user input: Domain name
domain = input("Enter domain for MX records check:")

try:
    # Querying for the domain's MX records
    answers = dns.resolver.query(domain, 'MX')

    # Enumarates through all of the TXT records and pulls the SPF record
    if len(answers) == 1:
        print('Only 1 MX record available for domain',domain)
        print ('MX record:',answers[0].to_text())
        print('Please make sure that your MX points to a secured relay')
    if len(answers) > 1:
        print('There are multiple MX records for domain', domain)
        for rdata in answers:
            print('MX record:',rdata.to_text())

        print('Please make sure that your additional MX endpoints are secured as your primary MX.')

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain',domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print ('There are not MX records for domain',domain)