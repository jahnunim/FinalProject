# DMARC.PY checks the following:
# 1. If DMARC record is present
# 2. DMARC actions (none/reject/quarantine)
# 3. Admin reports


# Modules
import TestGen

class DMARC(TestGen.Test):
    name = 'DMARC'
    def __init__(self, domain):
        self.domain = domain
        TestGen.Test.InitialLog(self)


    def DMARCcheck(self, domain):
        # Init
        dmarcRecord = None
        dmarc_object = DMARC(domain)
        totalScore = 0
        maxScore = 0
        info_send = ""

        # Builds the DMARC domain
        dmarcdomain = '_dmarc.' + domain

        # Query for the existence of domain

        answers = dmarc_object.get_dns_records(domain, 'A', 'DMARC')

        if answers is -1:
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
                answers = dmarc_object.get_dns_records(dmarcdomain, 'TXT', 'DMARC')
                if answers is -2:
                    # Check: if there is no DMARC record for that domain
                    score_result = "%0"
                    TestGen.testID += 1
                    info_send += "DMARC record is not in place for domain. domain is exposed to spoofing attacks"
                    info_send += score_result
                    return (info_send)
                    # Get the DMARC record
                else:
                    for rdata in answers:
                        if "v=DMARC1" in rdata.to_text():
                            maxScore += 1
                            totalScore += 1
                            dmarcRecord = rdata.to_text()
                            info = "DMARC in place ", dmarcRecord
                            info_send += "DMARC in place. "
                            dmarc_object.Log(domain, 'DMARC', info)

                            # Check: how the receiving mail server should threat a failed DMARC test for this domain
                            if (" p=reject" or " p=quarantine") in dmarcRecord:
                                maxScore += 1
                                totalScore += 1
                                info = "DMARC action reject/quarantine is configured "
                                info_send += "DMARC action reject/quarantine is configured. "
                                dmarc_object.Log(domain, 'DMARC', info)
                            elif "p=none" in dmarcRecord:
                                maxScore += 1
                                info = "DMARC action configures as None "
                                info_send += "DMARC action configures as None. "
                                dmarc_object.Log(domain, 'DMARC', info)

                            # Check: administrator email address for report / fail DMARC
                            if ("rua=mailto:" or "ruf=mailto:") in dmarcRecord:
                                maxScore += 1
                                totalScore += 1
                                info = "DMARC has administrator reports "
                                info_send += "DMARC has administrator reports. "
                                dmarc_object.Log(domain, 'DMARC', info)
                            else:
                                maxScore += 1
                                info = "DMARC has no administrator reports address configured "
                                info_send += "DMARC has no administrator reports address configured. "
                                dmarc_object.Log(domain, 'DMARC', info)
                            break
        # Logs and return the total score of the DMARC test
        score_result = dmarc_object.Score(totalScore, maxScore)
        score_result = "%" + score_result.__str__()
        dmarc_object.Log(domain, 'SCORE DMARC', score_result)
        info_send += score_result
        TestGen.testID += 1

        return (info_send)




