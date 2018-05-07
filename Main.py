print("Main")
import SPFoop

# get domain list from file
# export to file -  resulter
# OOP:
    # scoring
    # Ctor
    # Dtor
# logger (another py?) (time, test name, input, output)
# coding style - phyton
# Rest API

p1 = SPFoop.SPF('valensiweb.com')
p1.SPFcheck('valensiweb.com')
p4 = SPFoop.SPF('kakipipikakipipikakipipi.com')
p4.SPFcheck('kakipipikakipipikakipipi.com')
p2 = SPFoop.SPF('nice.com')
p2.SPFcheck('nice.com')
p3 = SPFoop.SPF('chukustar.com')
p3.SPFcheck('chukustar.com')


#TODO: closing file and delete

#choose = input("Enter the number of the option you wants: \n 1. Black list spam haus \n 2. DMARC \n 3. MX \n 4. Open Realy \n 5. Reverse DNS \n 6. SMTP TLS \n 7. SPF \n 8. VRFY \n 9. all")
#domain = input("Enter domain for SPF check:")
#if choose is 1:
#   p = SPFoop(domain)
#   p.SPFCheck(domain)



