import requests
import random

proxy_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=1818"
response = requests.get(proxy_url)
data = response.text.split("\r\n")[::-1]
webhook_urls = ["https://discord.com/api/webhooks/1250437027237855283/kMbHluQdsS4kZDKBAFRLP2SxrRjvaM9IpP59KtfI_219AaaGIIRE9Tw7oLwXIXqAtIU1","https://discord.com/api/webhooks/1250437026885664818/s6GzOsrqhjz5QyXjL5TfP_eOzM3Mt9nsZTnAGEjQ5PCjZxtxtpbKZyWvQx53j3lH9wKR","https://discord.com/api/webhooks/1250437027237855283/kMbHluQdsS4kZDKBAFRLP2SxrRjvaM9IpP59KtfI_219AaaGIIRE9Tw7oLwXIXqAtIU1"]
values = {"username":"test","content": "test"}
while True:
    proxy = {"http":random.choice(data)}
    wh_url = random.choice(webhook_urls)
    response = requests.post(wh_url,json=values,proxies=proxy)
    print(f"proxy: {proxy}\nstatus code: {response.status_code}")
