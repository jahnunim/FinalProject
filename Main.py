print("Main")
import SPFoop
import dns.resolver
import json

# get domain list from file?? RestAPI??
# initilize log file. where?
# coding style - phyton
# Rest API
# get domain by init or by method SPFcheck
#TODO: one dicetonery MX and IP and save result. save 2nd run for the same MX

def DicBuild(domain_list):
    # Create Dictionary from domain list
    for domain in domain_list:
        domains_dic[domain] = {}
        output = SPFoop(domain)
        domains_dic[domain]['SPF'] = {'grade':output.score,'info':output.info,'info_json':output.info}
        domains_dic[domain]['DMARC'] = {'grade':output.score,'info':output.info,'info_json':output.info}

        try:
            # Querying for the domain's MX records
            mx_records = dns.resolver.query(domain_name, 'MX')

            # Enumerates through all the domain's MX records
            for rdata in mx_records:
                split_mx = (rdata.to_text().split(" "))[1]
                split_mx = split_mx[:-1]

                # Tries to pull all A records behind the MX record
                try:
                    # Query for A records
                    aRecords = dns.resolver.query(split_mx,'A')

                    # Enumerates through all A records behind the MX record.
                    for adata in aRecords:
                        if adata not in domains_dic:
                            domains_dic[domain][adata] = {'mx':split_mx,'tests':{}}
                # If there is no such domain
                except (dns.resolver.NXDOMAIN):
                    print('There is no domain', split_mx)
                # If there are no A records available for that domain
                except (dns.resolver.NoAnswer):
                    print('There are no A records for MX', split_mx)

        # If there is no such domain
        except (dns.resolver.NXDOMAIN):
            print('There is no domain', domain)

        # If there are no MX records available for that domain
        except (dns.resolver.NoAnswer):
            print('There are no MX records for domain', domain)

        # If no nameServers available
        except (dns.resolver.NoNameservers):
            print('No name servers found')

        with open('domains.json', 'w') as data_file:
            json.dump(domains_dic, data_file)
            data_file.close
    #dmp = json.dump(domains_dic,fp="c:/temp/dump.txt")
    #for x in domains_dic:
    #    for y in domains_dic[x]:
    #        print(y, ':', domains_dic[x][y])

    print (json.dump(domains_dic, indent=4, sort_keys=True))

domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
domains_dic = {}



for domain in domains_list:
    DicBuild(domain)

#p1 = SPFoop.SPF('valensiweb.com')
#p1.SPFcheck('valensiweb.com')
#p4 = SPFoop.SPF('RonandSharonnosuchdomain.com')
#p4.SPFcheck('RonandSharonnosuchdomain.com')
#p2 = SPFoop.SPF('nice.com')
#p2.SPFcheck('nice.com')
#p3 = SPFoop.SPF('chukustar.com')
#p3.SPFcheck('chukustar.com')


#TODO: closing file and delete

#choose = input("Enter the number of the option you wants: \n 1. Black list spam haus \n 2. DMARC \n 3. MX \n 4. Open Realy \n 5. Reverse DNS \n 6. SMTP TLS \n 7. SPF \n 8. VRFY \n 9. all")
#domain = input("Enter domain for SPF check:")
#if choose is 1:
#   p = SPFoop(domain)
#   p.SPFCheck(domain)









