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

domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
#aRecords = ['1.1.1.1','2.2.2.2','1.1.1.1','3.3.3.3']
#split_mx = 'MX Record Example'
output='just some info for tests%55'

# Update the primary dictionary from IPs dictionary
def update_from_IP_dict(dict_to_update,ip_results_dict,domain,ip,test_name):
    score = (ip_results_dict[ip][test_name]).get("score", "")
    info = (ip_results_dict[ip][test_name]).get("info", "")
    #if ip not in dict_to_upate[domain]:
    dict_to_update[domain][ip] = {}
    dict_to_update[domain][ip]['tests'] = {}
    dict_to_update[domain][ip]['tests'][test_name] = {'score': score,
                                                    'info': info,
                                                    'info_json': info}
    return (dict_to_update)

# GET MX for domain
def get_mx(domain):
    try:
        mx_records = dns.resolver.query(domain, 'MX')
        return(mx_records)
    # If there is no such domain
    except (dns.resolver.NXDOMAIN):
        return(dns.resolver.NXDOMAIN)

    # If there are no MX records available for that domain
    except (dns.resolver.NoAnswer):
        print('There are no MX records for domain', domain)
        return (dns.resolver.NoAnswer)

    # If no nameServers available
    except (dns.resolver.NoNameservers):
        return (dns.resolver.NoNameservers)

def get_ip_from_mx(mx_records):
    mx_to_ip_dict = {}

    # Enumerates through all the domain's MX records
    for single_mx in mx_records:
        split_mx = (single_mx.to_text().split(" "))[1]
        split_mx= split_mx[:-1]

        # Query for A records
        aRecords = dns.resolver.query(split_mx,'A')



        # Enumerates through all A records behind the MX record.
        for ip in aRecords:
            print(ip.to_text())
            mx_to_ip_dict[ip.address] = split_mx

    return(mx_to_ip_dict)


def DicBuild(domains_list):
    ip_results_dict = {}
    domains_dict = {}
    # Top enumeration through all domains
    for domain in domains_list:
        domains_dict[domain] = {}

        # Func: query the MX records behind the domain
        mxResults = get_mx(domain)

        if (mxResults == dns.resolver.NoNameservers):
            domains_dict[domain] = {'Error':'No DNS server found'}
            break
        elif (mxResults == dns.resolver.NXDOMAIN):
            domains_dict[domain] = {'Error': 'No such domain found'}
            break
        elif (mxResults == dns.resolver.NoAnswer):
            domains_dict[domain] = {'Error': 'There are no MX records for that domain'}
            break

        # Get all IPs behind the MX record of the domain
        ips_dict = get_ip_from_mx(mxResults)
        print (ips_dict)

        # Tests in DOMAIN level: SPF, DMARC, MX

        # Init
        domains_dict[domain]['tests'] = {}

        # SPF logic
        #output = SPFoop(domain)
        domains_dict[domain]['tests']['SPF'] = {'grade': (output.split('%'))[1], 'info': (output.split('%'))[0],
                                      'info_json': (output.split('%'))[0]}

        #domains_dict[domain]['DMARC'] = {'grade':(output.split('%'))[1],'info':(output.split('%'))[0],'info_json':(output.split('%'))[0]}
        #domains_dict[domain]['MX'] = {'grade':(output.split('%'))[1],'info':(output.split('%'))[0],'info_json':(output.split('%'))[0]}

        # Tests in IP level: OpenRelay, SMTPTLS, VRFY
        for ip_key in ips_dict:
            if ip_key not in ip_results_dict:
                ip_results_dict[ip_key] = {}
                domains_dict[domain][ip_key] = {'mx': ips_dict[ip_key], 'tests': {}}

                # TESTS #
                # SMTPTLS #

                # output=smtptls(adata)
                domains_dict[domain][ip_key]['tests']['SMTPTLS'] = {'grade': (output.split('%'))[1],
                                                                   'info': (output.split('%'))[0],
                                                                   'info_json': (output.split('%'))[0]}

                ip_results_dict[ip_key]['SMTPTLS'] = {'score': (output.split('%'))[1],
                                                     'info': (output.split('%'))[0],
                                                     'info_json': (output.split('%'))[0]}
            else:
                update_from_IP_dict(domains_dict, ip_results_dict, domain, ip_key, 'SMTPTLS')


         # ADVANCE HERE
        # Querying for the domain's MX records
        #mx_records = dns.resolver.query(domain, 'MX')

        # Calling the SPF test for domain
        # Adds SPF test output to the dictionary.



                    # # Enumerates through all A records behind the MX record.
                    # for adata in aRecords:
                    #     if adata not in ip_results_dict:
                    #         ip_results_dict[adata] = {}
                    #
                    #         domains_dict[domain][adata] = {'mx':split_mx,'tests':{}}
                    #         # SMTPTLS
                    #         #output=smtptls(adata)
                    #         domains_dict[domain][adata]['tests']['SMTPTLS'] = {'grade': (output.split('%'))[1], 'info': (output.split('%'))[0],
                    #                   'info_json': (output.split('%'))[0]}
                    #
                    #         ip_results_dict[adata]['SMTPTLS'] = {'score': (output.split('%'))[1],
                    #                                              'info': (output.split('%'))[0],
                    #                                              'info_json': (output.split('%'))[0]}
                    #     else:
                    #         update_from_IP_dict(domains_dict,ip_results_dict,domain,adata,'SMTPTLS')


    return(domains_dict)
                            #score = (ip_results_dict[adata]['SMTPTLS']).get("score", "")
                            #info = (ip_results_dict[adata]['SMTPTLS']).get("info", "")

                            #if adata not in domains_dictt[domain]:
                             #  domains_dict[domain][adata] = {}
                              #  domains_dict[domain][adata]['tests'] = {}

                            #domains_dict[domain][adata]['tests']['SMTPTLS'] = {'score': score,
                             #                                                  'info': info,
                              #                                                 'info_json': info}

        #         # If there is no such domain
        #         except (dns.resolver.NXDOMAIN):
        #             print('There is no domain', split_mx)
        #         # If there are no A records available for that domain
        #         except (dns.resolver.NoAnswer):
        #             print('There are no A records for MX', split_mx)
        #
        # # If there is no such domain
        # except (dns.resolver.NXDOMAIN):
        #     print('There is no domain', domain)
        #
        # # If there are no MX records available for that domain
        # except (dns.resolver.NoAnswer):
        #     print('There are no MX records for domain', domain)
        #
        # # If no nameServers available
        # except (dns.resolver.NoNameservers):
        #     print('No name servers found')

    #dmp = json.dump(domains_dict,fp="c:/temp/dump.txt")
    #for x in domains_dict:
    #    for y in domains_dict[x]:
    #        print(y, ':', domains_dict[x][y])

        #print(json.dumps(domains_dict, indent=4))

#domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
domains_list = ['valensiweb.com','chukustar.com','tomersegal.com','segale5.onmicrosoft.com']
final_dict = DicBuild(domains_list)

print(json.dumps(final_dict,indent=4))

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









