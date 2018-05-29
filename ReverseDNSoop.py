# REVERSEDNS.PY checks if the MX records behind the domain has PTR.
# If PTR is missing, the domain's SMTP connection might be rejected due to Reverse DNS test.

# IP TEST

# Modules
import dns.resolver
import TestGen

class ReverseDNS(TestGen.Test):
    name = 'ReverseDNS'
    #TODO: send spf_object the class and the logging will take the class object
    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def ReverseDNScheck(self, ip_string):
        # Init
        mxRecord = None
        aRecord = None
        ptrRecord = None
        maxScore = 0
        totalScore = 0
        info_send = ""
        reverse_object = ReverseDNS(ip_string)

        # Builds the PTR record string
        ptrString = ip_string
        ptrString = '.'.join(reversed(ptrString.split("."))) + ".in-addr.arpa"

        # Pulls the PTR record
        try:
            ptrRecord = dns.resolver.query(ptrString,'PTR')
            maxScore+=1
            totalScore+=1
            info_send += "There is a valid PTR record"
            reverse_object.Log(ip_string, 'ReverseDNS', 'There is a valid PTR record')

        # If no PTR record
        except (dns.resolver.NXDOMAIN):
            info_send += "No PTR records for the SMTP server"
            reverse_object.Log(ip_string, 'ReverseDNS', 'No PTR records for the SMTP server')
            maxScore += 1

        # Prints the test's total score
        # Logs and return the total score of the VRFYTLS test
        score_result = reverse_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        reverse_object.Log(ip_string, 'SCORE VRFY', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)