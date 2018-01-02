# OpenRelay.PY check if the SMTP servers behind the MX records are Open Relays.
# If a server is an open relay, it can easily be put into Black Lists
# or be used by attackers as a "proxy" smtp for attacks.

# NEED TO CHECK WITH AN OPEN RELAY SERVER THAT THE TEST PASSES.#


# Modules
import socket
import dns.resolver
import smtplib
from smtplib import SMTP
fromAddress = "test@openrelay.com"
toAddress = "test@chukustars.com"
msg = "Open Relay test"

# Init
mxRecords = None
aRecords = None
maxScore = 0
totalScore = 0
hostname = socket.gethostname()

# user input: Domain name
domain = input("Enter domain for Open Relay check:")

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
                    conn = SMTP(host=adata.to_text(),local_hostname=hostname)
                    print("conn passed successfully")

                    # HELO request
                    conn.ehlo_or_helo_if_needed()

                    # Tries to relay an email to a non-accepted domain
                    try:
                        conn.sendmail(fromAddress,toAddress,msg)

                        # If we did not hit the exception, we were able to relay to a non-accepted domain
                        maxScore += 1
                        print('Server', adata, "returns a valid response for relaying an email through the SMTP server")
                        print("Open Relay provides attackers a way to relay emails through your SMTP server")

                    # Exception will raise if we are not able to relay.
                    except(smtplib.SMTPRecipientsRefused):
                        totalScore += 1
                        maxScore += 1
                        print("Server", adata, "is not an open relay")

                    # Terminates the SMTP connection
                    conn.quit()

                # If no connection to the SMTP server
                except(smtplib.socket.gaierror):
                    print("Unable to establish SMTP connection to server:", adata)

            # Prints the test's total score
            print('Total Open Relay score for domain', domain, 'is', totalScore, '/', maxScore)

        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            print('There is no domain', splitMX)
        # If there are no A records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are no A records for MX', splitMX)

# If there is no such domain
except (dns.resolver.NXDOMAIN):
    print('There is no domain', domain)

# If there are no MX records available for that domain
except (dns.resolver.NoAnswer):
    print('There are no MX records for domain', domain)

# If no nameServers available
except (dns.resolver.NoNameservers):
    print('No name servers found')