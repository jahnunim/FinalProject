print("Main")
import SPFoop
import DMARCoop
import dns.resolver
import json

# get domain list from file?? RestAPI??
# initilize log file. where?
# coding style - phyton
# Rest API
# get domain by init or by method SPFcheck
#TODO: one dicetonery MX and IP and save result. save 2nd run for the same MX

p1 = SPFoop.SPF('valensiweb.com')
info1 = p1.SPFcheck('valensiweb.com')
p4 = SPFoop.SPF('RonandSharonnosuchdomain.com')
info4 = p4.SPFcheck('RonandSharonnosuchdomain.com')
p2 = SPFoop.SPF('nice.com')
info2 = p2.SPFcheck('nice.com')
p3 = SPFoop.SPF('chukustar.com')
info3 = p3.SPFcheck('chukustar.com')

print(info1)
print(info2)
print(info3)
print(info4)

p1 = DMARCoop.DMARC('valensiweb.com')
info1 = p1.DMARCcheck('valensiweb.com')
p4 = DMARCoop.DMARC('RonandSharonnosuchdomain.com')
info4 = p4.DMARCcheck('RonandSharonnosuchdomain.com')
p2 = DMARCoop.DMARC('nice.com')
info2 = p2.DMARCcheck('nice.com')
p3 = DMARCoop.DMARC('chukustar.com')
info3 = p3.DMARCcheck('chukustar.com')

print(info1)
print(info2)
print(info3)
print(info4)

#TODO: closing file and delete

#choose = input("Enter the number of the option you wants: \n 1. Black list spam haus \n 2. DMARC \n 3. MX \n 4. Open Realy \n 5. Reverse DNS \n 6. SMTP TLS \n 7. SPF \n 8. VRFY \n 9. all")
#domain = input("Enter domain for SPF check:")
#if choose is 1:
#   p = SPFoop(domain)
#   p.SPFCheck(domain)









