import random
import requests
import re
import json


URL = '192.168.1.1'


# 登陆
def login(username, password):
    payload = {'username': username, 'psd': password}
    s = requests.Session()
    r = s.post('http://' + URL + '/cgi-bin/luci', params=payload)
    r = re.compile(r"token: '([a-z0-9]{32})'").findall(r.text)
    return {'session': s, 'token': r[0]}


# 查看信息
def view(session):
    payload = {'get': 'part', '_': random.random()}
    r = session.post('http://' + URL + '/cgi-bin/luci/admin/settings/gwinfo', params=payload)
    return json.loads(r.text)


# 登出
def logout(session, token):
    payload = { 'token': token, '_': random.random()}
    session.post('http://' + URL + '/cgi-bin/luci/admin/logout', params=payload)


# 重启
def reboot(session, token):
    payload = { 'token': token, '_': random.random()}
    r = session.post('http://' + URL + '/cgi-bin/luci/admin/reboot', params=payload)
    print(r.url)
    print(r.text)


# example
s = login('useradmin', '*******')
r = view(s['session'])
print(r)
print(r['WANIP'])
# reboot(s['session'], s['token'])
