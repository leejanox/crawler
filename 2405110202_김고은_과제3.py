from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = 'https://search.shopping.naver.com/ns' # 네이버 쇼핑 홈

driver.get(url)
time.sleep(2)

# 검색어 입력
query = '아티산키캡'
driver.find_element(By.ID, 'input_text').click()
time.sleep(1)
driver.find_element(By.ID, 'input_text').send_keys(query)
time.sleep(2)
#driver.find_element(By.ID, 'input_text').send_keys(Keys.ENTER)
driver.find_element(By.CLASS_NAME, '_searchInput_button_search_pA3ap').click()
time.sleep(2)

# 페이지 다운
for i in range(2):
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    
# 상품명 출력
product_name = []
product_price = []
product_link = []
product_delivery = []
product_rank = []
product_review =[]

products = driver.find_elements(By.CLASS_NAME, 'basicProductCardInformation_title__Bc_Ng')
prices = driver.find_elements(By.CLASS_NAME, 'priceTag_inner_price__TctbK')
links = driver.find_elements(By.CLASS_NAME, 'basicProductCard_basic_product_card__TdrHT')
deliveries = driver.find_elements(By.CLASS_NAME, 'productCardPrice_number__IjAYb')
ranks = driver.find_elements(By.CLASS_NAME, 'productCardReview_text__A9N9N productCardReview_star__7iHNO')
reviews = driver.find_elements(By.CLASS_NAME, 'productCardReview_text__A9N9N')

for i in range(len(products)):
    product = products[i]
    price = prices[i]
    link = links[i].find_element(By.TAG_NAME, 'a')
    delivery = deliveries[i]
    rank = ranks[i]
    review = reviews[i]
    
    product_name = (product.text) # 상품명
    product_price=(price.text.replace('\n', '')) # 상품가격
    product_link=(link.get_attribute('href')) # 상품링크
    product_delivery=(delivery.text.replace('\n','')) # 배송비
    product_rank=(rank.text) # 순위
    product_review=(review.text.replace('리뷰','')) # 리뷰
    print(f'no.{i+1}'+'\n'+f'상품명: {product_name}'+'\n'+ f'가격: {product_price}'+'\n'+ f'링크: {product_link}'+'\n'+f'배송비: {product_delivery}'+'\n'+f'별점: {product_rank}'+'\n'+f'리뷰: {product_review} 개'+'\n')