import dns.resolver
import datetime
import os.path


Logpath = "c:/temp/testfile.txt"
testID = 1

class Test:
    def __init__(self, domain):
        self.domain = domain
        self.InitialLog()

    def get_dns_records(self, domain, record_type, method_name):
        try:
            answers = dns.resolver.query(domain, record_type)
            return answers
        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            if method_name is 'DMARC':
                error = 'DMARC record is not in place for domain. domain is exposed to spoofing attacks'
            else:
                error = 'There is no such Domain'
            self.Log(domain, method_name, error)
            answers = -2
            return answers
        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            if (record_type == 'MX'):
                error = 'There are no ', record_type, ' records for domain'
                self.Log(domain, method_name, error.__str__())
            else:
                error = 'There are no ', record_type, ' records for domain'
                self.Log(domain, method_name, error)
        # If no nameServers available
        except (dns.resolver.NoNameservers):
            error = 'No name servers found'
            self.Log(domain, method_name, error)
            answers = -1
            return answers

    def InitialLog(self):
        if os.path.isfile(Logpath):
            test_file = open(Logpath, 'a')
        else:
            test_file = open(Logpath, 'a')
            test_file.writelines('testID,date,time,domain/IP address,testname,info' + '\n')
            test_file.close()

    def Log(self, domain, testname, info):
        self.testname = testname
        self.info = info
        test_file = open(Logpath, 'a')
        time = datetime.datetime.now()
        datestr = time.strftime('%m/%d/%Y')
        timestr = time.strftime('%H:%M:%S')

        test_file.writelines(testID.__str__() + ",")
        test_file.writelines(datestr + ",")
        test_file.writelines(timestr + ",")
        test_file.writelines(domain + ",")
        test_file.writelines(testname + ",")
        test_file.writelines(info)
        test_file.writelines("\n")
        test_file.close()

    def Score(self, current, max):
        self.score = 0
        if max is not 0:
            result = current / max * 100
        else:
            result = 0
        return (result)

    def say_hi(self):
        print('Hello, my name is', self.name)

#p = Test('valensiweb.com')
#p.InitialLog()
#p.get_dns_records('Chuku2', 'MX')
#p.get_dns_records('Chuku3', 'TXT')