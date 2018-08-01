# coding=utf-8
import urllib
import urllib.request as request
import mongodbfactory as mgf
from lxml import etree
import datetime



url = 'http://www.amazon.com/Block-Software-Deluxe-State-Refund/dp/B075QDY2VM/ref=br_msw_pdt-4/147-5957349-5213813'  
domainName="http://www.amazon.com"

class ProductInfo(object):
	def __init__(self,pid,title,reviews,read,run,createdDate,lastUpdateDate):
		self.productId=pid
		self.title=title
		self.reviews=reviews
		self.read=read
		self.run=run
		self.createdDate=datetime.datetime.now()
		self.lastUpdateDate=lastUpdateDate

class CustomerReviewsStar(object):
	def __init__(self,pid,url,starType,read,run,createdDate,lastUpdateDate):
		self.productId=pid
		self.url=url
		self.starType=starType
		self.read=read
		self.run=run
		self.createdDate=createdDate
		self.lastUpdateDate=lastUpdateDate

class Review(object):
	def __init__(self,pid,customerReviewsStarId,title,author,reviewDate,reviewBody,read,createdDate,lastUpdateDate):
		self.productId=pid
		self.customerReviewsStarId=customerReviewsStarId
		self.reviewTitle=title
		self.reviewAuthor=author
		self.reviewDate=reviewDate
		self.reviewBody=reviewBody
		self.read=read
		self.createdDate=createdDate
		self.lastUpdateDate=lastUpdateDate

def getHtml(url):
	headers = { 'Host':'www.amazon.com',
	            'Connection':'keep-alive',
	            'Cache-Control':'max-age=0',
	            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	            'Cookie': 'skin=noskin; session-id=147-5957349-5213813; session-id-time=2082787201l; x-wl-uid=1CrNnx+pQtJlAhNd0aveyp9YNFxMx09qg8HT+tiTu5t7c+jrB74HVgfrI9AGPLmrXQehjkLkIYYE=; ubid-main=133-3814776-2992129; session-token=hFE5Z9hqKSqmiq8zmmKIY8hJP7yUeqOElf0f1FAS+IJtP6jpaxON/rkxuUF9yjB8s8aPGZyTgrKQsB+L16f8z8iqlNmNwS4uBEaRI7kOYBz5Tspjav+hsl4D68W4sLwaPdRWFkcKYB6SApdBI2V5MZqf2r80PKRH3aqIygCsRG1cYI9ZwNBie4ITpm9ALQkZTLr1BX7J0seLah32eP2fCnCuqhVycALi0FBgLZ1UjICcWpfgohgtbJ8cnt/m4EUm; csm-hit=tb:JBSWXTB1M09CDMZE26Q3+s-SFWAG0HHWM54CY1KTF60|1522936468522&adb:adblk_no',
	            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	            # 'Accept-Encoding': 'gzip, deflate, sdch', #不要这行，这请求后压缩的，在IE下回解压，在这里没有解压，所以不要
	            'Upgrade-Insecure-Requests':'1',
	            'Accept-Language': 'zh-CN,zh;q=0.9'
	}
	data = None
	req = request.Request(url, data, headers)
	response = request.urlopen(req)
	html = response.read()
	# print(dir(req))
	# print(req.header_items())
	html=html.decode('utf-8')
	html=html.replace("\n",'')
	return html

def parseProductInfo(url):
	# print(html)
	html=getHtml(url)
	tree=etree.HTML(html)
	ASIN=tree.xpath("//*[@id='ASIN']")
	asin_value=listGetKey(ASIN,"value")
	reviews=tree.xpath("//*[@id='acrCustomerReviewText']/text()")
	title=tree.xpath('//*[@id="productTitle"]/text()')
	# threeStarUrl=tree.xpath('//*[@id="histogramTable"]/tbody/tr[3]/td[1]/a/text()')
	threeStarUrl=tree.xpath('//*[@title="3 star"]/@href') 
	twoStarUrl=tree.xpath('//*[@title="2 star"]/@href')
	oneStarUrl=tree.xpath('//*[@title="1 star"]/@href')

	productVO=ProductInfo(asin_value,list2str(title),list2str(reviews),0,0,datetime.datetime.now(),None)
	mgf.db_amazon.PRODUCT_INFO.insert(productVO.__dict__)
	# print(productVO.__dict__)

	crslist=list()
	customerReviewStarVO=CustomerReviewsStar(productVO.productId,list2str(threeStarUrl),"3 star",0,0,datetime.datetime.now(),None)
	crslist.append(customerReviewStarVO.__dict__)
	# mgf.db_amazon.commentpage.insert(commentPage.__dict__)
	customerReviewStarVO=CustomerReviewsStar(productVO.productId,list2str(twoStarUrl),"2 star",0,0,datetime.datetime.now(),None)
	crslist.append(customerReviewStarVO.__dict__)
	# mgf.db_amazon.commentpage.insert(commentPage.__dict__)
	customerReviewStarVO=CustomerReviewsStar(productVO.productId,list2str(oneStarUrl),"1 star",0,0,datetime.datetime.now(),None)
	crslist.append(customerReviewStarVO.__dict__)
	# mgf.db_amazon.commentpage.insert(commentPage.__dict__)
	mgf.db_amazon.CUSTOMER_REVIEWS_STAR.insert(crslist)
	# run = 1,已执行
	mgf.db_amazon.PRODUCT_INFO.update({"productId":productVO.productId},{"$set":{"run":1}},{multi:true})
	# print(crslist)

def runReviewPage(productId,crsId,url):
	_commentUrl=domainName+url
	html=getHtml(_commentUrl)
	tree=etree.HTML(html)
	reviews=tree.xpath("//*[@id='cm_cr-review_list']/div[@data-hook='review']")
	nextReviewsPageUrl=list2str(tree.xpath("//*[@id='cm_cr-pagination_bar']//li[@class='a-selected page-button']/following-sibling::li[1]/a/@href"))
	# nextReviewsPageNum=tree.xpath("//*[@id='cm_cr-pagination_bar']//li[@class='a-selected page-button']/following-sibling::li[1]/a/text()")
	reviewslist=list()
	for review in reviews:
		reviewTitle=review.xpath(".//a[@data-hook='review-title']/text()")
		reviewAuthor=review.xpath(".//a[@data-hook='review-author']/text()")
		reviewDate=review.xpath(".//span[@data-hook='review-date']/text()")
		reviewBody=review.xpath(".//span[@data-hook='review-body']/text()")
		_review=Review(productId,crsId,reviewTitle,reviewAuthor,reviewDate,reviewBody,0,datetime.datetime.now(),None)
		reviewslist.append(_review.__dict__)
		# print(comment.__dict__)
	mgf.db_amazon.REVIEWS.insert(reviewslist)
	print("----------------nextReviewsPageUrl "+nextReviewsPageUrl)
	# print(crsId+"----------------runReviewPage "+str(list2str(nextReviewsPageNum))+" over--------------")
	if(nextReviewsPageUrl!=''):
		runReviewPage(productId,crsId,nextReviewsPageUrl)

def parseReview(productId):
	customerReviewsStars=mgf.db_amazon.CUSTOMER_REVIEWS_STAR.find({"productId":productId})
	for customerReviewsStar in customerReviewsStars:
		# print(commentPage)
		runReviewPage(productId,customerReviewsStar.get("_id"),customerReviewsStar.get("url"))
		break
	print(productId+"----------------parseReview over--------------")

def list2str(iter):
	# print(type(iter))
	if len(iter) > 0:
		return iter[0].strip()
	else:
		return ""

def listGetKey(iter,key):
	# print(type(iter))
	if len(iter) > 0:
		return iter[0].get(key)
	else:
		return ""

def nowtime2Mongo():
	return datetime.datetime.now()-datetime.timedelta(hours=8);

if __name__=='__main__':
	# urlList=mgf.db_amazon.productList.find()
	# for product in urlList:
	# 	# print(product.get("_id"),product.get("url"))
	# 	print(product.get("url"))
	# 	html=getHtml(product.get("url"))
	# 	parsePageInfo(product.get("_id"),html)
	print(url)
	# parseProductInfo(url)
	parseReview("B075QDY2VM")
	# testComment()

