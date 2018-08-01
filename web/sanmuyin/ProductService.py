from . import mongodbfactory as mgf

def queryProductList():
	productList=mgf.db_amazon.PRODUCT_INFO.find({"productId":"B075QDY2VM"})
	return productList