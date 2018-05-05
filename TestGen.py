import dns.resolver

class Test:
    def __init__(self, domain):
        self.domain = domain
        try:
            self.answers = dns.resolver.query(domain, 'TXT')
        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            print('There is no domain', domain)
        # If no nameServers available
        except (dns.resolver.NoNameservers):
            print('No name servers found')
    def say_hi(self):
        print('Hello, my name is', self.name)

    def Log(self, testname, info):
        try:
            open('c:\temp\log.txt')

        self.testname = testname
        self.info = info

    def Score(self):
        self.score = 0

p = Test('Swaroop')
p.say_hi()

# The previous 2 lines can also be written as
# Person().say_hi()