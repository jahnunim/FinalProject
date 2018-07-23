# OpenRelay.PY check if the SMTP servers behind the MX records are Open Relays.
# If a server is an open relay, it can easily be put into Black Lists
# or be used by attackers as a "proxy" smtp for attacks.


# Modules
import socket
import TestGen
import dns.resolver
import smtplib
from smtplib import SMTP
fromAddress = "test@openrelay.com"
toAddress = "test@chukustar.com"
msg = "Open Relay test"

class OpenRelay(TestGen.Test):
    name = 'OpenRelay'

    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def OpenRelaycheck(self, ip_string):
        # Init
        mxRecords = None
        aRecords = None
        maxScore = 0
        totalScore = 0
        hostname = socket.gethostname()
        info_send = ""
        relay_object = OpenRelay(ip_string)

        try:
            conn = SMTP(host=ip_string,local_hostname=hostname,timeout=10)

            relay_object.Log(ip_string, 'OpenRelay', 'conn passed successfully')

            # HELO request
            conn.ehlo_or_helo_if_needed()

            # Tries to relay an email to a non-accepted domain
            try:
                conn.sendmail(fromAddress,toAddress,msg)

                # If we did not hit the exception, we were able to relay to a non-accepted domain
                maxScore += 1
                info_send += "Server returns a valid response for relaying an email through the SMTP server. Open Relay provides attackers a way to relay emails through your SMTP server"
                relay_object.Log(ip_string, 'OpenRelay', 'Server returns a valid response for relaying an email through the SMTP server. Open Relay provides attackers a way to relay emails through your SMTP server')

            # Exception will raise if we are not able to relay.
            except(smtplib.SMTPRecipientsRefused):
                totalScore += 1
                maxScore += 1
                info_send += "Server is not an Open Relay"
                relay_object.Log(ip_string, 'OpenRelay', 'Server is not an Open Relay')

            # Terminates the SMTP connection
            conn.quit()

        # If no connection to the SMTP server
        except(smtplib.socket.gaierror):
            info = "Unable to establish SMTP connection to server: " + ip_string
            info_send += "Unable to establish SMTP connection to server: " + ip_string + "%-1"
            relay_object.Log(ip_string, 'OpenRelay', info)
            return (info_send)

        except(socket.timeout):
            info = "Initial connection failed with timeout to IP " + ip_string
            info_send += "Initial connection failed with timeout to ip" + ip_string + "%-1"
            relay_object.Log(ip_string, 'OpenRelay', info)
            return (info_send)

        # Prints the test's total score
        # Logs and return the total score of the VRFYTLS test
        score_result = relay_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        relay_object.Log(ip_string, 'SCORE VRFY', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)
