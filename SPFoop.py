# SPF.PY checks the following:
# 1. if SPF record is present
# 2. if SPF action is configured for Hard/Soft fail

# Modules
import TestGen

class SPF(TestGen.Test):
    def __init__(self, domain):
        self.domain = domain

    def SPFcheck(self, domain):
        # Init
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
                TestGen.Test.Log(self, domain, 'SPF', info)

                # If SPF is present and configured with HardFail -
                if "-all" in spfRecord:
                    maxScore += 1
                    totalScore += 1

                    info = "HardFail inplace"
                    TestGen.Test.Log(self, domain, 'SPF', info)
                # If HardFail not inplace
                else:
                    maxScore +=1
                    info = "HardFail is not in place"
                    TestGen.Test.Log(self, domain, 'SPF', info)
                break

        # Checks if SPF test passed:
        if spfRecord is None:
            TestGen.Test.Log(self, domain, 'SPF','is exposed to spoofing attacks')

        # Prints the total score of the SPF test
        score_result = TestGen.Test.Score(self, totalScore,maxScore)
        TestGen.Test.Log(self, domain, 'SCORE', score_result.__str__())