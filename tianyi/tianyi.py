import random
import requests
import re
import json


URL = '192.168.1.1'
UNAME = 'useradmin'
UPWD  = 'xxx'

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

    
#  查看状态
def gwstatus(session):
    payload = {'get': 'part', '_': random.random()}
    r = session.post('http://' + URL + '/cgi-bin/luci/admin/settings/gwstatus', params=payload)
    return json.loads(r.text)
    
	
# 查看端口映射
def portmap_list(session):
    payload = {'get': 'part', '_': random.random()}
    r = session.post('http://' + URL + '/cgi-bin/luci/admin/settings/pmDisplay', params=payload)
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
s = login(UNAME, UPWD)
r = view(s['session'])
status = gwstatus(s['session'])
pmlist = portmap_list(s['session'])

print(r)
print(r['WANIP'])
print(status)
print(pmlist)
logout(s['session'], s['token'])
# reboot(s['session'], s['token'])