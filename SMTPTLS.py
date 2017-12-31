### NEED SOME MORE TESTING!
### TEST EDUCATION.GOV.IL - 81.218.97.38 - TELNET 25 responds with black screen.

# Modules
import dns.resolver
import smtplib
from smtplib import SMTP

# Reset: mxRecords, aRecords, maxScore, totalScore?
mxRecords = None
aRecords = None
maxScore = 0
totalScore = 0

# user input: Domain name
domain = input("Enter domain for TLS supportability check:")

# Query for the domain MX
try:
    # Querying for the domain's MX records
    mxRecords = dns.resolver.query(domain, 'MX')

    # Enumerates through all the domain's MX records
    for rdata in mxRecords:
        splitMX = (rdata.to_text().split(" "))[1]
        splitMX = splitMX[:-1]

        # Tries to pull all A records behind the MX record
        try:
            # Query for A records
            aRecords = dns.resolver.query(splitMX,'A')

            # Enumerates through all A records behind the MX record.
            for adata in aRecords:
                # Tries to make connection to the SMTP server (in 25).
                print(adata)
                try:
                    conn = SMTP(adata.to_text())

                    # EHLO request
                    conn.ehlo()

                    # Checks if the EHLO response has STARTTLS
                    if conn.has_extn('STARTTLS'):
                        maxScore += 1
                        totalScore += 1
                        print('Server',adata,"support TLS")
                    # If server does not support STARTTLS
                    else:
                        maxScore += 1
                        print("Server",adata, "does not support tls")

                    # Terminates the SMTP connection
                    conn.quit()

                # If no connection to the SMTP server
                except(smtplib.socket.gaierror):
                    print("Unable to establish SMTP connection to server:", adata)

            # Prints the test's total score
            print('Total TLS score for domain', domain, 'is', totalScore, '/', maxScore)

        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            print('There is no domain', splitMX)
        # If there are no A records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are not A records for MX', splitMX)


# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain', domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print('There are not MX records for domain', domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')