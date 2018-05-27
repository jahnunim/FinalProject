import SPFoop
import dns.resolver
import json

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

# Gets IP from MX record list
def get_ip_from_mx(mx_records):
    mx_to_ip_dict = {}

    # Enumerates through all the domain's MX records
    print (mx_records)
    for single_mx in mx_records:
        split_mx = (single_mx.to_text().split(" "))[1]
        split_mx = split_mx[:-1]

        # Query for A records
        aRecords = dns.resolver.query(split_mx,'A')

        # Enumerates through all A records behind the MX record.
        for ip in aRecords:
            mx_to_ip_dict[ip] = single_mx

    return(mx_to_ip_dict)

# Update the IPs dict with results
def update_from_IP_dict(dict_to_update,ip_results_dict,domain,ip,test_name):
    score = (ip_results_dict[ip][testname]).get("score", "")
    info = (ip_results_dict[ip][test_name]).get("info", "")
    if ip not in dict_to_upate[domain]:
        dict_to_update[domain][ip] = {}
        dict_to_update[domain][ip]['tests'] = {}
        dict_to_update[domain][ip]['tests'][test_name] = {'score': score,
                                                       'info': info,
                                                       'info_json': info}
        return (dict_to_update)


# MAIN + LOGIC
#domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
#aRecords = ['1.1.1.1','2.2.2.2','1.1.1.1','3.3.3.3']
#split_mx = 'MX Record Example'
output='just some info for tests%55'


domain_list=['valensiweb.com','chukustar.com']
ip_results_dict = {}
domains_dict = {}

for single_domain in domain_list:

    mx_results = get_mx(single_domain)
    ips_dict = get_ip_from_mx(mx_results)

    for ip_key in ips_dict:
        if ip_key not in ip_results_dict:
            ip_results_dict[ip_key] = {}
            domains_dict[domain][ip_key] = {'mx': ip_key, 'tests': {}}

                # TESTS #
                # SMTPTLS #

                # output=smtptls(adata)
            domains_dict[domain][adata]['tests']['SMTPTLS'] = {'grade': (output.split('%'))[1],
                                                                'info': (output.split('%'))[0],
                                                                'info_json': (output.split('%'))[0]}

            ip_results_dict[adata]['SMTPTLS'] = {'score': (output.split('%'))[1],
                                                     'info': (output.split('%'))[0],
                                                     'info_json': (output.split('%'))[0]}
        else:
            update_from_IP_dict(domains_dict,ip_results_dict,domain,ip_key, 'SMTPTLS')

print(json.dumps(domains_dict,indent=4))