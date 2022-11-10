import requests, threading

# all top-level domains 
# also known as the two to three letters words after a dot
# example: "https://www.google.com/"
#                              ^^^

TLD_DOMAINS = []

# get the domains from file 
TLD_f = open("misc/tlds.txt", "r+")
TLD_DOMAINS = TLD_f.read().split("\n") 
TLD_f.close()


# check for all top-level domains for intelligent url input 
def __TLD_CLOUD_CHECK__():
    # send request and download the content
    _domains = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt").content.decode("ascii") 

    domains = ""

    # remove all comments and leave domains only
    for tld in _domains.split("\n"):
        if not tld.startswith("#"):
            domains += f"{tld}\n"


    # save it to file 
    if not domains == "":
        f = open("misc/tlds.txt", "w+") 
        f.write(domains) 
        f.close() 

def check_for_tlds(): 
    # tld check thread to eventually prevent from the whole app's crashing 
    # and simulatenuously check the domains and run the app
    threading.Thread(None, __TLD_CLOUD_CHECK__).start()