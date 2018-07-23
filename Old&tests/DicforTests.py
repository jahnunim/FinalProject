import json
import copy

#b = copy.deepcopy(a)

domains_list = ['valensiweb.com','chukustar.com','ronandsharontestdomain.com']
aRecords = ['1.1.1.1','2.2.2.2','1.1.1.1','3.3.3.3']
split_mx = 'MX Record Exmaple'
output='just some info for tests%55'
domains_dict = {}
ip_results_dict = {}
#domains_list = ['valensiweb.com']
for domain in domains_list:
    domains_dict[domain] = {}
    # Calling the SPF test for domain
    #output = SPFoop(domain)
    # Adds SPF test output to the dictionary.
    domains_dict[domain]['tests'] = {}
    domains_dict[domain]['tests']['SPF'] = {'score': (output.split('%'))[1], 'info': (output.split('%'))[0],
                                           'info_json': (output.split('%'))[0]}

    for adata in aRecords:
        if adata not in ip_results_dict:
            print(adata + ' IP NOT FOUND!')
            # Init ip_results_dict[ip]
            ip_results_dict[adata] = {}

            domains_dict[domain][adata] = {'mx': split_mx, 'tests': {}}
            # SMTPTLS
            # Updating Domains dictonary
            domains_dict[domain][adata]['tests']['SMTPTLS'] = {'score': (output.split('%'))[1],
                                                              'info': (output.split('%'))[0],
                                                              'info_json': (output.split('%'))[0]}
            # Updating IP results dictonary
            #ip_results_dict[adata]['SMTPTLS'] = {}
            ip_results_dict[adata]['SMTPTLS'] = {'score': (output.split('%'))[1],
                                                              'info': (output.split('%'))[0],
                                                              'info_json': (output.split('%'))[0]}

            #OpenRelay
            domains_dict[domain][adata]['tests']['OpenRelay'] = {'score': (output.split('%'))[1],
                                                              'info': (output.split('%'))[0],
                                                              'info_json': (output.split('%'))[0]}

            #ip_results_dict[adata]['OpenRelay'] = {}
            ip_results_dict[adata]['OpenRelay'] = {'score': (output.split('%'))[1],
                                                 'info': (output.split('%'))[0],
                                                 'info_json': (output.split('%'))[0]}

            #print (domains_dict[domain][adata]['tests']['SMTPTLS'])
            print (ip_results_dict[adata]['OpenRelay'])

        else:
            print (adata + ' - IP FOUND')
            print (ip_results_dict[adata]['OpenRelay'])
            score = (ip_results_dict[adata]['SMTPTLS']).get("score", "")
            print ('SCORE IS' + score)
            #print ('this is the copy!!!!  ' + ip_results_copy)
            #print ('This is the SCORE of SMTPLS' + score)
            info =  (ip_results_dict[adata]['SMTPTLS']).get("info", "")
            if adata not in domains_dict[domain]:
                domains_dict[domain][adata] = {}
                domains_dict[domain][adata]['tests'] = {}

            domains_dict[domain][adata]['tests']['SMTPTLS'] ={'score': score,
                                                              'info': info,
                                                              'info_json': info}

            score = ip_results_dict[adata]['OpenRelay'].get("score", "")
            info =  ip_results_dict[adata]['OpenRelay'].get("info", "")
            domains_dict[domain][adata]['tests']['OpenRelay'] = {'score': score,
                                                              'info': info,
                                                              'info_json': info}

print(json.dumps(domains_dict,indent=4))