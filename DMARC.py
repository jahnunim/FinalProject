# DMARC RECORD EXMAPLE

# RESOURCE:
# https://sendgrid.com/blog/what-is-dmarc/

#The TXT record name should be "_dmarc.your_domain.com."

# What I want to handle?
# 1. NO DMARC
# 2. No SubDomain configured
# 3. Rua? RUF?
# rua=mailto:dmarc@sendgrid.com

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