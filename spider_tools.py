import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36',
    'Content-Type': 'text/html; charset=utf-8',
}

# headers={

# 'Referer': 'https://developer.android.com/',
# 'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
# 'sec-ch-ua-mobile': '?1',
# 'sec-ch-ua-platform': "Android",
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36 Edg/107.0.0.0'

# }

proxies={}
# proxies = {'http': 'http://192.168.1.34:1080', 'https': 'http://192.168.1.34:1080'}
#请求外部链接数据
def get_extranet_requests_data(hostUrl):
    return requests.get(hostUrl,headers=headers,proxies=proxies)


