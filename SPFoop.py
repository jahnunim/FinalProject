# SPF.PY checks the following:
# 1. if SPF record is present
# 2. if SPF action is configured for Hard/Soft fail

# Modules
import TestGen

class SPF(TestGen.Test):
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
        answers = TestGen.Test.get_dns_records(self, domain, 'TXT')

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
        if spfRecord is None:
            spf_object.Log(domain, 'SPF','is exposed to spoofing attacks')

        # Prints the total score of the SPF test
        score_result = spf_object.Score(totalScore,maxScore)
        spf_object.Log(domain, 'SCORE SPF', score_result.__str__())
        return (score_result)