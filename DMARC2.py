# DMARC.PY checks the following:
# 1. If DMARC record is present
# 2. DMARC actions (none/reject/quarantine)
# 3. Admin reports

# Domain based

# Modules
import dns.resolver

# Init
dmarcRecord = None
maxScore = 0
totalScore = 0

# user input: Domain name
domain = input("Enter domain for DMARC check:")

# Builds the DMARC domain
dmarcdomain = '_dmarc.' + domain

# Query for the existence of domain
try:
    answer = dns.resolver.query(domain, 'A')

    # DMARC record logic
    try:
        answer = dns.resolver.query(dmarcdomain, 'TXT')

        # Get the DMARC record
        for rdata in answer:
            if "v=DMARC1" in rdata.to_text():
                dmarcRecord = rdata.to_text()
                maxScore += 1
                totalScore += 1
                print('DMARC in place', dmarcRecord)

                # Check: how the receiving mail server should threat a failed DMARC test for this domain
                if (" p=reject" or " p=quarantine") in dmarcRecord:
                    maxScore += 1
                    totalScore += 1
                    print('DMARC action reject/quarantine is configured')

                elif "p=none" in dmarcRecord:
                    maxScore += 1
                    print('DMARC action configures as None')

                # Check: administrator email address for report / fail DMARC
                if ("rua=mailto:" or "ruf=mailto:") in dmarcRecord:
                    maxScore += 1
                    totalScore += 1
                    print('DMARC has administrator reports')
                else:
                    maxScore += 1
                    print('DMARC has no administrator reports address configured')

                break

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




