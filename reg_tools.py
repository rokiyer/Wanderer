import re

def filter_tags(s):  
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #CDATA  
    re_script=re.compile('<\s*script[^>]*>(.|\n)*?<\s*/\s*script\s*>',re.I)#Script  
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style  
    re_br=re.compile('<br\s*?/?>')
    re_h=re.compile('</?\w+[^>]*>')
    re_doc=re.compile('<!.*?>')
    re_comment=re.compile('<!--.*-->')
    re_blank=re.compile('(\s)+')
    s=re_cdata.sub('',s)#
    s=re_script.sub('',s) 
    s=re_style.sub('',s)
    s=re_br.sub('\n',s)
    s=re_h.sub('',s)
    s=re_doc.sub('',s)
    s=re_comment.sub('',s)
    s=re_blank.sub(' ',s)
    return s  

def findUrls(s):
    url_reg = '(((http|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?)'
    pattern = re.compile(url_reg)
    urls_result = pattern.findall(s)
    outlinks = ''
    for match in urls_result:
        outlinks += ',' + match[0]
    return outlinks

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
        return ""
    else:
        import datetime
        import time
        s = datetime.datetime.strptime(result[0],' %d %b %Y %H:%M:%S')
        return time.mktime(s.timetuple())
    


def validUrl(url):
	content = f.read()
	f.close()
	pattern = re.compile('(((http|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?)')
	result = pattern.findall(content)
	for match in result:
		print match[0]
