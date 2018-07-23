print("Main")

# Imports
import SPFoop, DMARCoop, MXoop, SMTPTLSoop, VRFYoop, OpenRealyoop, ReverseDNSoop, BlackListSpamhausoop, TestGen
import dns.resolver
import json

# Consts
# Test names:
SPF = 'SPF'
DMARC = 'DMARC'
MX = 'MX'
OPENRELAY = 'OpenRelay'
SMTPTLS = 'SMTPTLS'
REVERSEDNS = 'REVERSEDNS'
VRFY = 'VRFY'
BLSPAMHAUS = 'BlackListSpamhaus'

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
# OUTPUT: dictonary mapping KEY=IP, VALUE=MX
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
# Updates the IP dictionary with results
#########################

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
##################################################################################

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
            TestGen.testID += 1
            break
        elif (mxResults == dns.resolver.NXDOMAIN):
            domains_dict[domain] = {'Error': 'No such domain found'}
            TestGen.testID += 1
            break
        elif (mxResults == dns.resolver.NoAnswer):
            domains_dict[domain] = {'Error': 'There are no MX records for that domain'}
            TestGen.testID += 1
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

        ################
        # DMARC logic #
        ################

        dmarcObj = DMARCoop.DMARC(domain)
        output = dmarcObj.DMARCcheck(domain)
        domains_dict[domain]['DMARC'] = {'grade':(output.split('%'))[1],'info':(output.split('%'))[0],'info_json':(output.split('%'))[0]}

        #############
        # MX logic #
        #############

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

                # updates primary dictionary
                smtptlsObj = SMTPTLSoop.SMTPTLS(ip_key)
                output = smtptlsObj.SMTPTLScheck(ip_key)
                domains_dict[domain][ip_key]['tests'][SMTPTLS] = {'grade': (output.split('%'))[1],
                                                                   'info': (output.split('%'))[0],
                                                                   'info_json': (output.split('%'))[0]}

                # Updates the IP_RESULTS dictionary
                output = 'just some info for tests%55'
                ip_results_dict[ip_key][SMTPTLS] = {'score': (output.split('%'))[1],
                                                     'info': (output.split('%'))[0],
                                                     'info_json': (output.split('%'))[0]}

                #################
                # VRFY logic #
                #################

                vrfyObj = VRFYoop.VRFY(ip_key)
                output = vrfyObj.VRFYcheck(ip_key,domain)
                domains_dict[domain][ip_key]['tests'][VRFY] = {'grade': (output.split('%'))[1],
                                                                  'info': (output.split('%'))[0],
                                                                  'info_json': (output.split('%'))[0]}

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][VRFY] = {'score': (output.split('%'))[1],
                                                    'info': (output.split('%'))[0],
                                                    'info_json': (output.split('%'))[0]}

                ###################
                # OpenRelay logic #
                ###################

                openrelayObj = OpenRealyoop.OpenRelay(ip_key)
                output = openrelayObj.OpenRelaycheck(ip_key)
                domains_dict[domain][ip_key]['tests'][OPENRELAY] = {'grade': (output.split('%'))[1],
                                                                  'info': (output.split('%'))[0],
                                                                  'info_json': (output.split('%'))[0]}

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][OPENRELAY] = {'score': (output.split('%'))[1],
                                                    'info': (output.split('%'))[0],
                                                    'info_json': (output.split('%'))[0]}

                ###############
                # Reverse DNS #
                ###############

                reversednsObj = ReverseDNSoop.ReverseDNS(ip_key)
                output = reversednsObj.ReverseDNScheck(ip_key)
                domains_dict[domain][ip_key]['tests'][REVERSEDNS] = {'grade': (output.split('%'))[1],
                                                                    'info': (output.split('%'))[0],
                                                                    'info_json': (output.split('%'))[0]}

                # Updates the IP_RESULTS dictionary
                ip_results_dict[ip_key][REVERSEDNS] = {'score': (output.split('%'))[1],
                                                      'info': (output.split('%'))[0],
                                                      'info_json': (output.split('%'))[0]}

                ######################
                # Blacklist Spamhaus #
                ######################

                blacklistObj = BlackListSpamhausoop.BlackList(ip_key)
                output = blacklistObj.BlackListcheck(ip_key)
                domains_dict[domain][ip_key]['tests'][BLSPAMHAUS] = {'grade': (output.split('%'))[1],
                                                                     'info': (output.split('%'))[0],
                                                                     'info_json': (output.split('%'))[0]}

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

