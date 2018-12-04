#!/usr/bin/env python
import requests
import json

def getbyurl():
    proxies = []
    proxy_url = 'https://github.com/fate0/proxylist/raw/master/proxy.list'
    try:
        response = requests.get(proxy_url)
        response = response.text.split('\n') if response.status_code == requests.codes.ok else None
        response.remove('')
        proxies = [json.loads(proxy.strip(' \r\n')) for proxy in response ]
    except Exception as e:
        print(e)
    finally:
        return proxies

def getproxy():
    proxies = getbyurl()
    print('Got {} proxy'.format(len(proxies)))
    return proxies

def get_http():
    http_proxy = []
    proxies = getproxy()
    for proxy in proxies:
        if proxy['type'] == 'http':
            http_proxy.append(proxy)

    print('Got {} http proxy'.format(len(http_proxy)))
    return http_proxy

def get_https():
    https_proxy = []
    proxies = getproxy()
    for proxy in proxies:
        if proxy['type'] == 'https':
            https_proxy.append(proxy)

    print('Got {} https proxy'.format(len(https_proxy)))
    return https_proxy

def check():
    https_proxy = get_https()

    total = len(https_proxy)
    count = 1
    for proxy in https_proxy:
        if proxy['type'] == 'http':
            continue
        try:
            response = requests.get('https://api-ipv4.ip.sb/ip', proxies = {proxy['type']: '{}://{}:{}'.format(proxy['type'],proxy['host'], proxy['port'])}, timeout=3)
            print('[{}/{}] Get ip {} by proxy {}://{}:{}'.format(count, total, response.text.strip(' \r\n'), proxy['type'], proxy['host'], proxy['port']))
        except requests.exceptions.ProxyError:
            print('[{}/{}] proxy error'.format(count, total))
        except requests.exceptions.ConnectTimeout:
            print('[{}/{}] connect timeout'.format(count, total))
        except requests.exceptions.ReadTimeout:
            print('[{}/{}] read timeout'.format(count, total))
        finally:
            count += 1

if __name__ == '__main__':
    check()

