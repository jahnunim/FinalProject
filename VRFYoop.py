# VRFY.PY checks if the SMTP server behind the MX records are exposed to VRFY command.
# Attackers can use VRFY command to validate users and email addresses.


# Modules
import socket
import TestGen
import smtplib
from smtplib import SMTP

class VRFY(TestGen.Test):
    name = 'VRFY'
    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def VRFYcheck(self, ip_string, domain):
        # Init
        mxRecords = None
        aRecords = None
        vrfy_object = VRFY(ip_string)
        maxScore = 0
        totalScore = 0
        info_send = ""
        hostname = socket.gethostname()
        # Build user address
        validUser = "info@" + domain

        try:
            conn = SMTP(host=ip_string,local_hostname=hostname,timeout=10)

            vrfy_object.Log(ip_string, 'VRFY', 'conn passed successfully')

            # HELO request
            conn.ehlo_or_helo_if_needed()

            # Running the SMTP VRFY command again the server SMTP server.
            vrfyResponse = conn.verify(validUser)

            # Checks if the VRFY returned a valid result.
            if "250" in vrfyResponse:
                maxScore += 1
                info_send += "Server returns a valid response for VRFY command. VRFY provides attackers a way to query for user / email address validity"
                vrfy_object.Log(ip_string, 'VRFY', 'Server returns a valid response for VRFY command. VRFY provides attackers a way to query for user / email address validity')
            # If server blocks VRFY command
            else:
                totalScore += 1
                maxScore += 1
                info_send += "Server does not provide VRFY command"
                vrfy_object.Log(ip_string, 'VRFY', 'Server does not provide VRFY command')

            # Terminates the SMTP connection
            conn.quit()

        # If no connection to the SMTP server
        except(smtplib.socket.gaierror):
            info = "Unable to establish SMTP connection to server: " + ip_string
            info_send += "Unable to establish SMTP connection to server: " + ip_string + "%-1"
            vrfy_object.Log(ip_string, 'VRFY', info)
            return (info_send)

            # If the server refused our HELO message.
        except(smtplib.SMTPHeloError):
            info = "The server " + ip_string + "refused our HELO message"
            info_send += "The server " + ip_string + "refused our HELO message" + "%-1"
            SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)
            return (info_send)

        # If the server did not respond within the socket timeout window.
        except(socket.timeout):
            info = "Initial connection failed with timeout to IP " + ip_string
            info_send += "Initial connection failed with timeout to ip" + ip_string + "%-1"
            vrfy_object.Log(ip_string, 'VRFY', info)
            return (info_send)

# Prints the test's total score
# Logs and return the total score of the VRFYTLS test
        score_result = vrfy_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        vrfy_object.Log(ip_string, 'SCORE VRFY', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)

