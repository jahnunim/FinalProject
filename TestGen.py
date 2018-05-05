import dns.resolver
import datetime

Logpath = "c:/temp/testfile.txt"

class Test:
    def __init__(self, domain):
        self.domain = domain
        self.InitialLog()

    def get_dns_records(self, domain, record_type):
        try:
            answers = dns.resolver.query(domain, record_type)
            return answers
        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            error = 'There is no Domain'
            self.Log(domain, 'get_dns_record', error)
        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            if (record_type == 'MX'):
                error = 'There is no', record_type, ' records for domain'
                self.Log(domain, 'get_dns_record', error.__str__())
            else:
                error = 'The domain ', domain, 'is exposed to spoffing attacks'
                self.Log(domain, 'get_dns_record', error)
        # If no nameServers available
        except (dns.resolver.NoNameservers):
            error = 'No name servers found'
            self.Log(domain, 'get_dns_record', error)

    def InitialLog(self):
        test_file = open(Logpath, 'w+')
        test_file.writelines('date,time,domain,testname,info' + '\n')
        test_file.close()

    def Log(self, domain, testname, info):
        self.testname = testname
        self.info = info
        test_file = open(Logpath, 'a')
        time = datetime.datetime.now()
        datestr = time.strftime('%m/%d/%Y')
        timestr = time.strftime('%H:%M:%S')

        test_file.writelines(datestr + ",")
        test_file.writelines(timestr + ",")
        test_file.writelines(domain + ",")
        test_file.writelines(testname + ",")
        test_file.writelines(info)
        test_file.close()

    def Score(self, current, max):
        self.score = 0
        result = current / max * 100
        return (result)

    def say_hi(self):
        print('Hello, my name is', self.name)

p = Test('valensiweb.com')
p.InitialLog()
#p.get_dns_records('Chuku2', 'MX')
#p.get_dns_records('Chuku3', 'TXT')

# The previous 2 lines can also be written as
# Person().say_hi()