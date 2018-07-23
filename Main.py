import Logic, json

domains_list = ['valensiweb.com','chukustar.com','tomersegal.com','segale5.onmicrosoft.com','ronandsharontestdomain.com']
final_dict = Logic.DicBuild(domains_list)
print(json.dumps(final_dict,indent=4))