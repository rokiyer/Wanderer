import re
import datetime
import time
from bs4 import BeautifulSoup
from urlparse import urljoin

def filter_tags(s):  
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #CDATA  
    re_script=re.compile('<\s*script[^>]*>(.|\n)*?<\s*/\s*script\s*>',re.I)#Script  
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style  
    re_br=re.compile('<br\s*?/?>')
    re_h=re.compile('</?\w+[^>]*>')
    re_doc=re.compile('<!.*?>')
    re_comment=re.compile('<!.*-->')
    re_blank_entity=re.compile('(&nbsp|(\s)+)')
    s=re_cdata.sub('',s)#
    s=re_script.sub('',s) 
    s=re_style.sub('',s)
    s=re_br.sub('\n',s)
    s=re_h.sub('',s)
    s=re_doc.sub('',s)
    s=re_blank_entity.sub(' ',s)
    s=re_comment.sub('',s)
    return s  

# def findUrls(s):
#     url_reg = '(((http|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?)'
#     pattern = re.compile(url_reg)
#     urls_result = pattern.findall(s)
#     outlinks = ''
#     for match in urls_result:
#         outlinks += ',' + match[0]
#     return outlinks
def findUrls(content , url):
    soup = BeautifulSoup(content)
    anchor_arr = soup.find_all('a')
    outlinks = ''
    
    for anchor in anchor_arr:
        link = anchor.get('href')
        if link == None:
            continue
        if link.find('://') == -1:
            link = urljoin(url,link)
        outlinks += ',' + link
    return outlinks


def completeLinks(link_arr , prefix):
    for i in range(0,len(link_arr)):
        if link_arr[i].find('://') == -1:
            link_arr[i] = prefix + link_arr[i]
    return link_arr


def findTitle(content):
    title_reg = '<title>(.*)</title>'
    pattern = re.compile(title_reg , re.I)
    result = pattern.findall(content)
    if(result == []):
        return ""
    else:
        return result[0]

def findLastModifyTime(content):
    title_reg = 'Last-Modified:.*,(.*[:|\d]+)'
    pattern = re.compile(title_reg , re.I)
    result = pattern.findall(content)
    if(result == []):
        return 0
    else:
        datetime_str = result[0]
        if datetime_str.find('-') == -1:
            s = datetime.datetime.strptime(datetime_str,' %d %b %Y %H:%M:%S')
            return time.mktime(s.timetuple())
        else:
            s = datetime.datetime.strptime(datetime_str,' %d-%b-%Y %H:%M:%S')
            return time.mktime(s.timetuple())


def allowUrl(url):
    pattern = re.compile('cc.sjtu.edu.cn')
    result = pattern.search(url)
    return (result == None)

def allowUrlFilter():
    reg_arr = ['^http://news.sjtu.edu.cn(/)?']
    pattern_arr = []
    for reg in reg_arr:
        pattern = re.compile(reg,re.I)
        pattern_arr.append(pattern)
    return pattern_arr

def denyUrlFilter():
    reg_arr = ['.*\.(jpg|jpeg|png|gif|iso|rar|zip|exe|pdf|rm|avi|tmp|xls|txt|doc)$','.*#$']
    pattern_arr = []
    for reg in reg_arr:
        pattern = re.compile(reg,re.I)
        pattern_arr.append(pattern)
    return pattern_arr

