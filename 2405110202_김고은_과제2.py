from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = 'https://shopping.naver.com/home' # 네이버 쇼핑 홈

driver.get(url)
time.sleep(3)

driver.find_element(By.CLASS_NAME, '_shoppingHomeSearch_shopping_home_search_iNKvf').click()
time.sleep(3)

# 검색어 입력
query = '바람막이'
driver.find_element(By.ID, 'input_text').send_keys(query)
time.sleep(3)
driver.find_element(By.ID, 'input_text').send_keys(Keys.ENTER)
time.sleep(3)

# 페이지 다운
for i in range(10):
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    
# 상품명 출력
product_name = []
product_price = []
product_link = []

products = driver.find_elements(By.CLASS_NAME, 'basicProductCardInformation_title__Bc_Ng')
prices = driver.find_elements(By.CLASS_NAME, 'priceTag_inner_price__TctbK')
links = driver.find_elements(By.CLASS_NAME, 'basicProductCard_basic_product_card__TdrHT')

for i in range(len(products)):
    product = products[i]
    price = prices[i]
    link = links[i].find_element(By.TAG_NAME, 'a')
    
    product_name = product.text # 상품명
    product_price = price.text.replace('\n', '') # 상품가격
    product_link = link.get_attribute('href') # 상품링크
    print(f'no.{i+1}'+'\n'+f'상품명: {product_name}'+'\n'+ f'가격: {product_price}'+'\n'+ f'링크: {product_link}'+'\n')
    
#product_price.replace('\n', '')
