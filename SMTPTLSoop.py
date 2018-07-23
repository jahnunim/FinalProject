### NEED SOME MORE TESTING!
## Maybe try using SMTP.ehlo_or_helo_if_needed()
## And react to exception:
#SMTPHeloError
#The server didn’t reply properly to the HELO greeting.

# SMTPTLS.PY check if the servers behind the MX records are supporting TLS.

# Modules
import socket
import dns.resolver
import smtplib
import TestGen
from smtplib import SMTP

class SMTPTLS(TestGen.Test):
    name = 'SMTPTLS'

    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def SMTPTLScheck(self, ip_string):
        # Init
        mxRecords = None
        aRecords = None
        maxScore = 0
        totalScore = 0
        hostname = socket.gethostname()
        info_send = ""
        SMTPTLS_object = SMTPTLS(ip_string)

        try:
            conn = SMTP(host=ip_string,local_hostname=hostname,timeout=10)

            # EHLO request
            conn.ehlo()

            # Checks if the EHLO response has STARTTLS
            if conn.has_extn('STARTTLS'):
                maxScore += 1
                totalScore += 1
                info = "Server " + ip_string + " support TLS"
                info_send += "Server " + ip_string + " support TLS"
                SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)

            # If server does not support STARTTLS
            else:
                maxScore += 1
                info = "Server " + ip_string + " does not support TLS"
                info_send += "Server " + ip_string + " does not support TLS"
                SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)

            # Terminates the SMTP connection
            conn.quit()

        # If no connection to the SMTP server
        except(smtplib.socket.gaierror):
            info = "Unable to establish SMTP connection to server: " + ip_string
            info_send += "Unable to establish SMTP connection to server: " + ip_string + "%-1"
            SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)
            return (info_send)

        # If the server refused our HELO message.
        except(smtplib.SMTPHeloError):
            info = "The server " + ip_string + "refused our HELO message"
            info_send += "The server " + ip_string + "refused our HELO message" + "%-1"
            SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)
            return (info_send)

        except(socket.timeout):
            info = "Initial connection failed with timeout to IP " + ip_string
            info_send += "Initial connection failed with timeout to ip" + ip_string + "%-1"
            SMTPTLS_object.Log(ip_string, 'SMTPTLS', info)
            return (info_send)

        # Logs and return the total score of the VRFYTLS test
        score_result = SMTPTLS_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        SMTPTLS_object.Log(ip_string, 'SCORE SMTPTLS', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)