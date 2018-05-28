# SPF.PY checks the following:
# 1. if SPF record is present
# 2. if SPF action is configured for Hard/Soft fail

# Modules
import TestGen

class SPF(TestGen.Test):
    name = 'SPF'
    #TODO: send spf_object the class and the logging will take the class object
    def __init__(self, domain):
        self.domain = domain
        TestGen.Test.InitialLog(self)

    def SPFcheck(self, domain):
        # Init
        spf_object = SPF(domain)
        spfRecord = None
        totalScore = 0
        maxScore = 0
        info_send = ""

        # Querying for the domain's TXT records
        answers = spf_object.get_dns_records(domain, 'TXT', 'SPF')
        if answers is None:
            info_send += "The domain is exposed to spoffing attacks. "
            spf_object.Log(domain, 'SPF', 'is exposed to spoofing attacks')
        elif answers is -1:
            score_result = "%-1"
            TestGen.testID += 1
            info_send += "No name server founds. "
            info_send += score_result
            return (info_send)
        elif answers is -2:
            score_result = "%-2"
            TestGen.testID += 1
            info_send += "There is no such domain. "
            info_send += score_result
            return (info_send)
        else:
            # Enumarates through all of the TXT records and pulls the SPF record
            for rdata in answers:
                if "v=spf" in rdata.to_text():
                    maxScore += 1
                    totalScore += 1
                    spfRecord = rdata.to_text()
                    info = "SPF in place ", spfRecord
                    info_send += "SPF in place. "
                    spf_object.Log(domain, 'SPF', info)

                    # If SPF is present and configured with HardFail -
                    if "-all" in spfRecord:
                        maxScore += 1
                        totalScore += 1

                        info = "HardFail inplace. "
                        info_send += info
                        spf_object.Log(domain, 'SPF', info)
                    # If HardFail not inplace
                    else:
                        maxScore +=1
                        info = "HardFail is not in place. "
                        info_send += info
                        spf_object.Log(domain, 'SPF', info)
                    break
        # Checks if SPF test passed:


        # Logs and return the total score of the SPF test
        score_result = spf_object.Score(totalScore,maxScore)
        score_result = "%" + score_result.__str__()
        spf_object.Log(domain, 'SCORE SPF', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)