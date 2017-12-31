

# Modules
import dns.resolver
import  smtplib
from smtplib import SMTP

# Reset: mxRecords, score?
mxRecords = None
maxScore = 3
totalScore = 0

# user input: Domain name
#domain = input("Enter domain for SMTP TLS check:")

splitMX = "40.68.241.53"
try:
    conn = SMTP('12324353143413412414')
    #conn.ehlo()


    #if conn.has_extn('STARTTLS'):
     #   print('Domain support STARTTLS')

except(smtplib.SMTPConnectError):
    print("Unable to establish SMTP connection")
