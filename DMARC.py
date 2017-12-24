# DMARC.PY checks the following:
# 1. If DMARC record is present
# 2. DMARC actions (none/reject/quarantine)
# 3. Admin reports


# Modules
import dns.resolver

# Reset: DMARC record, totalScore, maxScore
dmarcRecord = None
maxScore = 3
totalScore = 0

# user input: Domain name
domain = input("Enter domain for DMARC check:")

# Builds the DMARC domain
dmarcdomain = '_dmarc.' + domain

# Query for the domain TXT
try:
    answer = dns.resolver.query(domain, 'A')

    # DMARC record logic
    try:
        answer = dns.resolver.query(dmarcdomain, 'TXT')

        # Get the DMARC record
        for rdata in answer:
            if "v=DMARC1" in rdata.to_text():
                dmarcRecord = rdata.to_text()
                totalScore += 1
                print('DMARC in place', dmarcRecord)

        # Check: how the receiving mail server should threat a failed DMARC test for this domain
        if ("p=reject" or "p=quarantine") in dmarcRecord:
            totalScore += 1
            print('DMARC action reject/quarantine is configured')
        elif "p=none" in dmarcRecord:
            print('DMARC action configures as None')

        # Check: administrator email address for report / fail DMARC
        if ("rua=mailto:" or "ruf=mailto:") in dmarcRecord:
            totalScore += 1
            print('DMARC has administrator reports')
        else:
            print("DMARC is missing reports admin")

    #############################################################################################
    ## Temporary dropping off this test, as the sub-domain by default goes by the P value.
    #   # Check: does the domain should handles sub-domains as well
    #    if ("sp=reject" or "sp=quarantine") in dmarcRecord:
    #        score += 1
    #        print("DMARC action reject/quarantine configured for sub-domains")
    #    else:
    #        print("DMARC action is None for sub-domains")
    ###########################################################################################

    # Check: if there is no DMARC record for that domain
    except (dns.resolver.NXDOMAIN):
        print('DMARC record is not in place for domain:',domain)
        print(domain,'is exposed to spoofing attacks')

    print('Total DMARC score for domain',domain,'is',totalScore,'/',maxScore)

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain:',domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')




