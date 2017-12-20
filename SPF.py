# the SPF.PY tests if the domain has SPF record registered & if it configures as HardFail.

import dns.resolver

print(dir(dns.resolver))

import sys
print(sys.path)

# SPF score
score = 0

try:
    answers = dns.resolver.query('valensiweb.com', 'TXT')

    for rdata in answers:
        if "v=spf" in rdata.to_text():
            spfRecord = rdata.to_text()
            score+= 1
            print('SPF in place',spfRecord)
            if "-all" in rdata.to_text():
                print("HardFail inplace")
                score+=1
            else:
                print("SoftFail inplace")
                ## I NEED TO FIX THIS! ##
        else:
            print("SPF record not in place!")

    print('your score is: ',score)


except (dns.resolver.NXDOMAIN):
    print('There is no such domain')
except (dns.resolver.NoAnswer):
    print ('There are no TXT records for this domain')



#spfRecord = [s for s in rdata if "v=spf" in s]
        #$spfRecord = [txt_string for txt_string in rdata.strings if "v=spf" in txt_string]
    # print('TXT:', rdata.to_text())
    # print(' query qname:', answers.qname, ' num ans.', len(answers))