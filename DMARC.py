# DMARC RECORD EXMAPLE

# RESOURCE:
# https://sendgrid.com/blog/what-is-dmarc/

#The TXT record name should be "_dmarc.your_domain.com."

# What I want to handle?
# 1. NO DMARC
# 2. No SubDomain configured
# 3. Rua? RUF?
# rua=mailto:dmarc@sendgrid.com

import dns.resolver

# Reset DMARC record & score
score = 0
DMARCRecord = None

# Requests from the user the domain to check
domain = input("What's the domain you wish to check his DMARC record?")

# Builds the DMARC domain
domain = '_dmarc.' + domain




try:
    # Querying for the domain's _DMARC TXT records
    answer = dns.resolver.query(domain, 'TXT')

    ############# HERE IS WHERE I STOPPED - QUERY THE DMARC RECORD########

    for rdata in answer:
        if "v=spf" in rdata.to_text():
            spfRecord = rdata.to_text()
            print('SPF in place', spfRecord)
    # If no SPF record is available
    if spfRecord is None:
        print("SPF record not in place!")
    # If SPF is present and configured with HardFail -
    elif "-all" in spfRecord:
        score+=2
        print("HardFail inplace")
    # Is SPF is present and configured with SoftFail ~
    else:
        score+1
        print("SoftFail inplace")
    # Prints the total score of the SPF test
    print('Your SPF score is: ', score)

# If there is not such domain
except (dns.resolver.NXDOMAIN):
    print('There is no such domain')
# If there are not TXT records available for that domain
except (dns.resolver.NoAnswer):
    print ('There are no TXT records for this domain')