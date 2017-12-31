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
domain = input("Enter domain for VRFY check:")
validUser = input("Enter a valid email address:")

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

                    # HELO request
                    conn.helo()

                    # Running the SMTP VRFY command again the server SMTP server.
                    vrfyResponse = conn.verify(validUser)

                    # Checks if the VRFY returned a valid result.
                    if "250" in vrfyResponse:
                        maxScore += 1
                        print('Server',adata,"returns a valid response for VRFY command")
                        print("VRFY provides attackers a way to query for user / email address validity")

                    # If server blocks VRFY command
                    else:
                        totalScore += 1
                        maxScore += 1
                        print("Server",adata, "does not provide VRFY command")

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