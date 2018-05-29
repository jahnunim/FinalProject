# BlackListSpamhaus.PY checks if your mail servers are listed in Spamhaus black list.
# This to ensure that email from your organization won't be rejected.
# If your email servers are listed on a BlackList it may indicate for any potential abuse of your servers.


# Modules
import dns.resolver
import TestGen

class BlackList(TestGen.Test):
    name = 'BlackList'
    def __init__(self, ip_string):
        self.ip_string = ip_string
        TestGen.Test.InitialLog(self)

    def BlackListcheck(self, ip_string):
        # Init
        bl = "zen.spamhaus.org"
        #myIP = "14.114.37.4"
        mxRecord = None
        aRecord = None
        ptrRecord = None
        maxScore = 0
        totalScore = 0
        info_send = ""
        bl_object = BlackList(ip_string)

        # Query for Spamhaus zone, if no result returns - IP not listed in black list
        try:
            # New DNS resolver
            my_resolver = dns.resolver.Resolver()

            # Builds the query
            query = '.'.join(reversed(str(ip_string).split("."))) + "." + bl

            # Queries Spamhaus DNS.
            answers = my_resolver.query(query,"A")

            # If no exception was triggered, IP is listed in bl.
            # Gets the TXT record to build te link for details.
            maxScore +=1
            answer_txt = my_resolver.query(query,"TXT")
            info_send += 'IP: %s IS listed in %s (%s: %s)' % (ip_string, bl, answers[0], answer_txt[0])
            info = 'IP: %s IS listed in %s (%s: %s)' % (ip_string, bl, answers[0], answer_txt[0])
            bl_object.Log(ip_string, 'BlackListSpamhaus', info)
        # Exception raised, IP not listed in BL.
        except(dns.resolver.NXDOMAIN):
            maxScore += 1
            totalScore +=1
            info_send += 'IP: %s is NOT listed in %s' % (ip_string, bl)
            info = 'IP: %s is NOT listed in %s' % (ip_string, bl)
            bl_object.Log(ip_string, 'BlackListSpamhaus', info)

        score_result = bl_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        bl_object.Log(ip_string, 'SCORE VRFY', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)