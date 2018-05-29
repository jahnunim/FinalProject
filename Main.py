print("Main")

# Imports
import SPFoop, DMARCoop, MXoop, SMTPTLSoop, VRFYoop, OpenRealyoop, ReverseDNSoop, BlackListSpamhausoop
import dns.resolver
import json



# Consts#
# Test names:
SPF = 'SPF'
DMARC = 'DMARC'
MX = 'MX'
OPENRELAY = 'OpenRelay'
SMTPTLS = 'SMTPTLS'
REVERSEDNS = 'REVERSEDNS'
VRFY = 'VRFY'
BLSPAMHAUS = 'BlackListSpamhaus'


# initialize log file. where?
# coding style - phyton

# get domain by init or by method SPFcheck
#TODO: one dicetonery MX and IP and save result. save 2nd run for the same MX

# Output to test
output='just some info for tests%55'

#############################################################################################################################
# Update the primary dictionary with the results from the IPs dictionary.
# The rational is to save tests on IPs that were already tested.
# Input: dict_to_update - primary dictionary to update
# ip_results_dict - the IPs dictionary with the results.
# domain - which needs to be updated, ip - the smtp server's ip, test_name - the name of the test which called the update.
##############################################################################################################################
def update_from_IP_dict(dict_to_update,ip_results_dict,domain,ip,test_name):
    # Gets the score and information of the tests, from the IP results dictionary
    score = (ip_results_dict[ip][test_name]).get("score", "")
    info = (ip_results_dict[ip][test_name]).get("info", "")

    # Updates the primary dictionary with the results
    dict_to_update[domain][ip] = {}
    dict_to_update[domain][ip]['tests'] = {}
    dict_to_update[domain][ip]['tests'][test_name] = {'score': score,
                                                    'info': info,
                                                    'info_json': info}
    # returns dictionary to update
    return (dict_to_update)

#####################################################
# Get MX records for domain
# INPUT: domain to pull the MX records for.
####################################################
def get_mx(domain):
    try:
        # Queries the DNS for the MX records
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

############################################
# Get server IPs behind the MX records
# INPUT: list of mx_records
#Output: dictonary mapping KEY=IP, VALUE=MX
############################################
def get_ip_from_mx(mx_records):
    # init dic
    mx_to_ip_dict = {}

    # Enumerates through all the domain's MX records
    for single_mx in mx_records:
        split_mx = (single_mx.to_text().split(" "))[1]
        split_mx= split_mx[:-1]

        # Query for A records
        aRecords = dns.resolver.query(split_mx,'A')

        # Enumerates through all A records behind the MX record.
        for ip in aRecords:
            # Add the IP to dictionary as a key.
            mx_to_ip_dict[ip.address] = split_mx

    return(mx_to_ip_dict)

#########################
#update_ip_dict_results
# Updates the IP dictionary with results
#######################
def update_ip_dict_results(ip_dict,ip,test_name,result):
    ip_dict[ip][test_name] = {'score': (result.split('%'))[1],
                                          'info': (result.split('%'))[0],
                                          'info_json': (result.split('%'))[0]}
    return(ip_dict)

##################################################################################
# This is the logic of building the primary Dictionary.
# This Logic calls for each test and returns the final Output of the module.
# Input: list of domains.
# Output: Dictionary to be dump as a json file.
################################################################################
def DicBuild(domains_list):
    # Init dictionaries
    ip_results_dict = {}
    domains_dict = {}

    # Top enumeration through all domains
    for domain in domains_list:
        domains_dict[domain] = {}

        # Func: returns the MX records behind the domain
        mxResults = get_mx(domain)

        # Checks if the MX passed sucessfully.
        if (mxResults == dns.resolver.NoNameservers):
            domains_dict[domain] = {'Error':'No DNS server found'}
            # TODO: LOGGING and increase general attribute
            break
        elif (mxResults == dns.resolver.NXDOMAIN):
            domains_dict[domain] = {'Error': 'No such domain found'}
            break
        elif (mxResults == dns.resolver.NoAnswer):
            domains_dict[domain] = {'Error': 'There are no MX records for that domain'}
            break

        # Get all IPs behind the MX record of the domain
        ips_dict = get_ip_from_mx(mxResults)

        ########################################
        # Tests in DOMAIN level: SPF, DMARC, MX#
        ########################################

        # Init
        domains_dict[domain]['tests'] = {}

        #############
        # SPF logic #
        #############
        spfObj = SPFoop.SPF(domain)
        output = spfObj.SPFcheck(domain)
        #Updates primary dictionary.
        domains_dict[domain]['tests'][SPF] = {'grade': (output.split('%'))[1], 'info': (output.split('%'))[0],
                                      'info_json': (output.split('%'))[0]}

        #output = 'just some info for tests%55'

        ################
        # DMARC logic #
        ################
        #TODO: Call DMARC # output = DMARC()
        dmarcObj = DMARCoop.DMARC(domain)
        output = dmarcObj.DMARCcheck(domain)
        domains_dict[domain]['DMARC'] = {'grade':(output.split('%'))[1],'info':(output.split('%'))[0],'info_json':(output.split('%'))[0]}

        #############
        # MX logic #
        #############
        #TODO: Call MX # output = MX()
        mxObj = MXoop.MX(domain)
        output = mxObj.MXcheck(domain)
        domains_dict[domain]['MX'] = {'grade':(output.split('%'))[1],'info':(output.split('%'))[0],'info_json':(output.split('%'))[0]}

        # Tests in IP level: OpenRelay, SMTPTLS, VRFY
        for ip_key in ips_dict:
            if ip_key not in ip_results_dict:
                ip_results_dict[ip_key] = {}
                domains_dict[domain][ip_key] = {'mx': ips_dict[ip_key], 'tests': {}}

                ##################
                # IP based tests #
                ##################

                #################
                # SMTPTLS logic #
                #################
                # TODO: SMTPTLS call
                # output=smtptls(adata)
                # updates primary dictionary
                smtptlsObj = SMTPTLSoop.SMTPTLS(ip_key)
                output = smtptlsObj.SMTPTLScheck(ip_key)
                #output = 'just some info for tests%55'
                domains_dict[domain][ip_key]['tests'][SMTPTLS] = {'grade': (output.split('%'))[1],
                                                                   'info': (output.split('%'))[0],
                                                                   'info_json': (output.split('%'))[0]}

                # In case using update_ip_dict func will be used
                #ip_results_dict = update_ip_dict_results(ip_results_dict,ip,'SMTPTLS',output)

                # Updates the IP_RESULTS dictionary
                output = 'just some info for tests%55'
                ip_results_dict[ip_key][SMTPTLS] = {'score': (output.split('%'))[1],
                                                     'info': (output.split('%'))[0],
                                                     'info_json': (output.split('%'))[0]}


                #################
                # VRFY logic #
                #################
                #
                # output=smtptls(adata)
                # updates primary dictionary
                vrfyObj = VRFYoop.VRFY(ip_key)
                output = vrfyObj.VRFYcheck(ip_key,domain)
                # output = 'just some info for tests%55'
                domains_dict[domain][ip_key]['tests'][VRFY] = {'grade': (output.split('%'))[1],
                                                                  'info': (output.split('%'))[0],
                                                                  'info_json': (output.split('%'))[0]}

                # In case using update_ip_dict func will be used
                # ip_results_dict = update_ip_dict_results(ip_results_dict,ip,'SMTPTLS',output)

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][VRFY] = {'score': (output.split('%'))[1],
                                                    'info': (output.split('%'))[0],
                                                    'info_json': (output.split('%'))[0]}


                ###################
                # OpenRelay logic #
                ###################
                openrelayObj = OpenRealyoop.OpenRelay(ip_key)
                output = openrelayObj.OpenRelaycheck(ip_key)
                # output = 'just some info for tests%55'
                domains_dict[domain][ip_key]['tests'][OPENRELAY] = {'grade': (output.split('%'))[1],
                                                                  'info': (output.split('%'))[0],
                                                                  'info_json': (output.split('%'))[0]}

                # In case using update_ip_dict func will be used
                # ip_results_dict = update_ip_dict_results(ip_results_dict,ip,'SMTPTLS',output)

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][OPENRELAY] = {'score': (output.split('%'))[1],
                                                    'info': (output.split('%'))[0],
                                                    'info_json': (output.split('%'))[0]}

                ###############
                # Reverse DNS #
                ###############
                reversednsObj = ReverseDNSoop.ReverseDNS(ip_key)
                output = reversednsObj.ReverseDNScheck(ip_key)
                # output = 'just some info for tests%55'
                domains_dict[domain][ip_key]['tests'][REVERSEDNS] = {'grade': (output.split('%'))[1],
                                                                    'info': (output.split('%'))[0],
                                                                    'info_json': (output.split('%'))[0]}

                # In case using update_ip_dict func will be used
                # ip_results_dict = update_ip_dict_results(ip_results_dict,ip,'SMTPTLS',output)

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][REVERSEDNS] = {'score': (output.split('%'))[1],
                                                      'info': (output.split('%'))[0],
                                                      'info_json': (output.split('%'))[0]}

                ######################
                # Blacklist Spamhaus #
                ######################
                blacklistObj = BlackListSpamhausoop.BlackList(ip_key)
                output = blacklistObj.BlackListcheck(ip_key)
                # output = 'just some info for tests%55'
                domains_dict[domain][ip_key]['tests'][BLSPAMHAUS] = {'grade': (output.split('%'))[1],
                                                                     'info': (output.split('%'))[0],
                                                                     'info_json': (output.split('%'))[0]}

                # In case using update_ip_dict func will be used
                # ip_results_dict = update_ip_dict_results(ip_results_dict,ip,'SMTPTLS',output)

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][BLSPAMHAUS] = {'score': (output.split('%'))[1],
                                                       'info': (output.split('%'))[0],
                                                       'info_json': (output.split('%'))[0]}



            else:
                # Updates the primary dictionary from the IP results dictionary
                domains_dict = update_from_IP_dict(domains_dict, ip_results_dict, domain, ip_key, SMTPTLS)
                domains_dict = update_from_IP_dict(domains_dict, ip_results_dict, domain, ip_key, VRFY)
                domains_dict = update_from_IP_dict(domains_dict, ip_results_dict, domain, ip_key, OPENRELAY)
                domains_dict = update_from_IP_dict(domains_dict, ip_results_dict, domain, ip_key, BLSPAMHAUS)

    return(domains_dict)


#domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
domains_list = ['valensiweb.com','chukustar.com','tomersegal.com','segale5.onmicrosoft.com','ronandsharontestdomain.com']
final_dict = DicBuild(domains_list)

print(json.dumps(final_dict,indent=4))




#TODO: closing file and delete

#choose = input("Enter the number of the option you wants: \n 1. Black list spam haus \n 2. DMARC \n 3. MX \n 4. Open Realy \n 5. Reverse DNS \n 6. SMTP TLS \n 7. SPF \n 8. VRFY \n 9. all")
#domain = input("Enter domain for SPF check:")
#if choose is 1:
#   p = SPFoop(domain)
#   p.SPFCheck(domain)

#p1 = SPFoop.SPF('valensiweb.com')
#p1.SPFcheck('valensiweb.com')
#p4 = SPFoop.SPF('RonandSharonnosuchdomain.com')
#p4.SPFcheck('RonandSharonnosuchdomain.com')
#p2 = SPFoop.SPF('nice.com')
#p2.SPFcheck('nice.com')
#p3 = SPFoop.SPF('chukustar.com')
#p3.SPFcheck('chukustar.com')

# score = (ip_results_dict[adata]['SMTPTLS']).get("score", "")
# info = (ip_results_dict[adata]['SMTPTLS']).get("info", "")

# if adata not in domains_dictt[domain]:
#  domains_dict[domain][adata] = {}
#  domains_dict[domain][adata]['tests'] = {}

# domains_dict[domain][adata]['tests']['SMTPTLS'] = {'score': score,
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

# dmp = json.dump(domains_dict,fp="c:/temp/dump.txt")
# for x in domains_dict:
#    for y in domains_dict[x]:
#        print(y, ':', domains_dict[x][y])

# print(json.dumps(domains_dict, indent=4))

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


# ADVANCE HERE
# Querying for the domain's MX records
# mx_records = dns.resolver.query(domain, 'MX')

# Calling the SPF test for domain
# Adds SPF test output to the dictionary.