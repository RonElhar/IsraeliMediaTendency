from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        # print(results)
        # if len(results) == 1:
        # print(url)
        if len(results) > 3:
            # print(results[1])
            return results[1]
        else:
            # print(results[0])
            return results[0]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
