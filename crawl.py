# encoding: utf8
import fetch
import parse
import generate
import time  

print 'Crawl - Start... '
print '='*50
fetch.fetchAll('all')
parse.parseAll('all')
generate.generateAll()
print '='*50
