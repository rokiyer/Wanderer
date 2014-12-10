import database
import crawl

# url = "http://www.sjtu.edu.cn"

# result = crawl.crawlSinglePage(url)
# # code head content error
# #insertToMysql( url , code  , head , content , error ):

# print result[0]

# database.insertToMysql( url , result[1] , result[1] , result[2] , result[3] )

crawl.crawl()

