# VRFY.PY checks if the SMTP server behind the MX records are exposed to VRFY command.
# Attackers can use VRFY command to validate users and email addresses.

# TODO: I SEND YOU IP AND DOMAIN!!!!! YOU BUILD THE VALID USER STRING WITH "administrator@"+DOMAIN

# Modules
import socket
import TestGen
import smtplib
from smtplib import SMTP

class VRFY(TestGen.Test):
    name = 'VRFY'
    #TODO: send spf_object the class and the logging will take the class object
    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def VRFYcheck(self, ip_string):
        # Init
        mxRecords = None
        aRecords = None
        maxScore = 0
        totalScore = 0
        hostname = socket.gethostname()

        # user input: Domain name
        domain = input("Enter domain for VRFY check:")

        # TODO: What to do with the valid email address - Ron need to answer
        validUser = input("Enter a valid email address:")
        try:
            # TODO: host=adata.to_text() CHANGE TO host=ip.to_text()
            conn = SMTP(host=ip_string,local_hostname=hostname)
            print("conn passed successfully")

            # HELO request
            conn.ehlo_or_helo_if_needed()

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

