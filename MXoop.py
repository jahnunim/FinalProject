# MX.PY checks if the domain has multiple MX records
# Advise to make sure additional MX endpoints are secured as the primary endpoint.


# Modules
import TestGen

class MX(TestGen.Test):
    name = 'MX'
    def __init__(self, domain):
        self.domain = domain
        TestGen.Test.InitialLog(self)

    def MXcheck(self, domain):
        # Init
        mx_object = MX(domain)
        mxRecords = None
        maxScore = 1
        totalScore = 1
        info_send = ""

        mxRecords = mx_object.get_dns_records(domain, 'MX', 'MX')

        #  1 MX record in place.
        if len(mxRecords) == 1:
            info_send += "Only 1 MX record available for domain. "
            info_send += "MX record:" + mxRecords[0].to_text()
            info_send += " Please make sure that your MX points to a secured relay"
            mx_object.Log(domain, 'MX', 'Only 1 MX record available for domain. Please make sure that your MX points to a secured relay')

        # For multiple MX records
        if len(mxRecords) > 1:
            info_send += "There are multiple MX records for domain. "
            for rdata in mxRecords:
                info_send+= "MX record:" + rdata.to_text()
            info_send += "Please make sure that your additional MX endpoints are secured as your primary MX."
            mx_object.Log(domain, 'MX', 'There are multiple MX records for domain. Please make sure that your additional MX endpoints are secure as your primary MX.')

        # Logs and return the total score of the MX test
        score_result = mx_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        mx_object.Log(domain, 'SCORE MX.', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)