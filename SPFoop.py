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

        # Querying for the domain's TXT records
        answers = spf_object.get_dns_records(domain, 'TXT', 'SPF')
        if answers is None:
            spf_object.Log(domain, 'SPF', 'is exposed to spoofing attacks')
        elif answers is -1:
            score_result = -1
            TestGen.testID += 1
            return (score_result)
        else:
            # Enumarates through all of the TXT records and pulls the SPF record
            for rdata in answers:
                if "v=spf" in rdata.to_text():
                    maxScore += 1
                    totalScore += 1
                    spfRecord = rdata.to_text()
                    info = 'SPF in place', spfRecord
                    spf_object.Log(domain, 'SPF', info)

                    # If SPF is present and configured with HardFail -
                    if "-all" in spfRecord:
                        maxScore += 1
                        totalScore += 1

                        info = "HardFail inplace"
                        spf_object.Log(domain, 'SPF', info)
                    # If HardFail not inplace
                    else:
                        maxScore +=1
                        info = "HardFail is not in place"
                        spf_object.Log(domain, 'SPF', info)
                    break
        # Checks if SPF test passed:


        # Prints the total score of the SPF test
        score_result = spf_object.Score(totalScore,maxScore)
        score_result = score_result.__str__() + "%"
        spf_object.Log(domain, 'SCORE SPF', score_result)

        TestGen.testID += 1

        return (score_result)