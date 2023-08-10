from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint, choice
from models.review import Review, Grade
from models.product import Product, Price
from database import Database
import datetime
import json
from time import sleep


driver = webdriver.Chrome()
db = Database('old_database.db')
products_to_scrap = [
    {'category': 1, 'url': 'https://br.shein.com/SHEIN-Belle-Square-Neck-Slant-Pocket-Wedding-Dress-p-19154675-cat-3089.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/SHEIN-Priv-Colorblock-Button-Front-Crop-Blouse-Split-Thigh-Skirt-p-17904473-cat-1780.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/SHEIN-Frenchy-Twist-Front-Batwing-Sleeve-Button-Through-Dress-p-20228245-cat-1727.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/LOVE-LEMONADE-Floral-Sequin-Mesh-Overlay-Cami-Party-Dress-p-18284594-cat-5361.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/SHEIN-EZwear-Solid-Crop-Cami-Top-Wide-Leg-Pants-p-14016272-cat-1780.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/Trendy-EOS-Women-Dresses-p-10969354-cat-1727.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=2'},
    {'category': 2, 'url': 'https://br.shein.com/Manfinity-Homme-Men-Solid-Button-Front-Shirt-p-14096386-cat-6309.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 2, 'url': 'https://br.shein.com/Manfinity-RSRT-Men-Seagull-Coconut-Tree-Graphic-Contrast-Trim-Polo-Shirt-p-18053504-cat-1981.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 2, 'url': 'https://br.shein.com/Men-Solid-V-Neck-Tee-p-19781418-cat-1980.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 2, 'url': 'https://br.shein.com/Men-Shirts-p-12893369-cat-1979.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=2'},
    {'category': 2, 'url': 'https://br.shein.com/Manfinity-Homme-Men-Plus-Solid-Zip-Up-Jacket-p-18973835-cat-6300.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 3, 'url': 'https://br.shein.com/Manfinity-Homme-Men-Plus-Solid-Zip-Up-Jacket-p-18973835-cat-6300.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_3%60ps%3D4_3%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 3, 'url': 'https://br.shein.com/SHEIN-Kids-CHARMNG-Toddler-Girls-Floral-Print-Ruffle-Trim-Blouse-Pants-Set-p-16321717-cat-2117.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_4%60ps%3D4_4%60jc%3Dreal_2031&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 3, 'url': 'https://br.shein.com/Boys-Pants-p-17523184-cat-1995.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_4%60ps%3D4_4%60jc%3Dreal_2031&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=2'},
    {'category': 4, 'url': 'https://br.shein.com/SHEIN-Contrast-Trim-Halter-Bikini-Swimsuit-p-14956628-cat-1866.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_1%60ps%3D4_1%60jc%3DitemPicking_003147526&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 4, 'url': 'https://br.shein.com/SHEIN-VCAY-Tassel-Tie-Neck-Contrast-Lace-Batwing-Sleeve-Cover-Up-Dress-p-16629760-cat-2176.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_1%60ps%3D4_1%60jc%3DitemPicking_003147526&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 4, 'url': 'https://br.shein.com/Color-Block-Zip-Front-One-Piece-Swimsuit-p-15143715-cat-2193.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_1%60ps%3D4_1%60jc%3DitemPicking_003147526&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 5, 'url': 'https://br.shein.com/Glamorous-Hot-Pink-Loafer-Pumps-For-Women-Bow-Decor-Point-Toe-Satin-Pyramid-Heeled-Pumps-p-13199218-cat-1750.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_8%60ps%3D4_7%60jc%3DitemPicking_100123134&src_module=Women&src_tab_page_id=page_home1691039833989&mallCode=1'},
    {'category': 5, 'url': 'https://br.shein.com/Sporty-Sneakers-For-Women-Colorblock-Letter-Graphic-Lace-Up-Sneakers-p-12452250-cat-1913.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_8%60ps%3D4_7%60jc%3DitemPicking_100123134&src_module=Women&src_tab_page_id=page_home1691039833989&mallCode=1'},
    {'category': 5, 'url': 'https://br.shein.com/Women-Casual-Shoes-p-19885601-cat-1913.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_8%60ps%3D4_7%60jc%3DitemPicking_100123134&src_module=Women&src_tab_page_id=page_home1691039833989&mallCode=2'},
    {'category': 6, 'url': 'https://br.shein.com/1pc-Classic-Oval-Shaped-Gold-Frame-Tea-Legs-Decor-Fashion-Eyeglasses-p-18241608-cat-1770.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_11%60ps%3D4_10%60jc%3Dreal_1765&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 6, 'url': 'https://br.shein.com/Scarves-p-14444594-cat-1872.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_11%60ps%3D4_10%60jc%3Dreal_1765&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=2'},
    {'category': 6, 'url': 'https://br.shein.com/1pc-Small-Square-Frame-Retro-Fashion-Sunglasses-With-Metal-Legs-For-Sun-Protection-p-19367823-cat-3927.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_11%60ps%3D4_10%60jc%3Dreal_1765&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 6, 'url': 'https://br.shein.com/Litchi-Embossed-Belt-p-11963261-cat-1875.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_11%60ps%3D4_10%60jc%3Dreal_1765&src_module=Women&src_tab_page_id=page_home1691027241335&mallCode=1'},
    {'category': 1, 'url': 'https://br.shein.com/Women-Skirts-p-20329467-cat-1732.html?src_identifier=fc%3DWomen%60sc%3DNOVIDADES%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar01%60jc%3Durl_https%253A%252F%252Fbr.shein.com%252Fnew%252FWHATS-NEW-sc-00255950.html&src_module=topcat&src_tab_page_id=page_goods_detail1691097821808&mallCode=2'},
    {'category': 1, 'url': 'https://br.shein.com/SHEIN-Frenchy-Button-Front-Ruffle-Hem-Denim-Dress-p-19819068-cat-1931.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dshopbycate%60hz%3DhotZone_13%60ps%3D4_12%60jc%3DitemPicking_001121425&src_module=Women&src_tab_page_id=page_home1691098086132&mallCode=1'}
]
example_names = ['Micael', 'João', 'Maria', 'José', 'Ana', 'Pedro']

for index, product in enumerate(products_to_scrap):
    driver.get(product['url'])
    sleep(2)
    price = float(driver.find_element(By.CLASS_NAME, 'product-intro__head-mainprice').find_element(By.TAG_NAME, 'span').text.replace('R$', '').strip().replace(',', '.'))
    images_divs = driver.find_elements(By.CLASS_NAME, 'product-intro-zoom__item')
    images = []
    for i in range(3):
        images.append(images_divs[i].find_element(By.TAG_NAME, 'img').get_property('src'))
    details = driver.find_elements(By.CLASS_NAME, 'product-intro__description-table-item')
    try:
        product_review = driver.find_element(By.CLASS_NAME, 'rate-des').get_property('innerText').strip()
    except:
        product_review = None
    if product_review:
        Review.commit_review(
            db,
            Review(
                id=None,
                author_id=randint(1, 6),
                product_id=index+1,
                content=product_review,
                grade=randint(3, 5),
                date=datetime.datetime.now().strftime('%d-%m-%Y'),
                author_name=choice(example_names)
            )
        )
    Product.commit_product(
        db,
        Product(
            id=None,
            name=driver.find_element(By.CLASS_NAME, 'product-intro__head-name').text.replace('\n', ' ').replace('SHEIN', '').strip(),
            price=price,
            price_old=randint(int(price+1), int(price*2)),
            category=product['category'],
            promotion=True if randint(0, 1) == 1 else False,
            image_url=images[0],
            description=driver.find_element(By.CLASS_NAME, 'product-intro__description').text.replace('\n', ' ').strip(),
            color=None,
            additional_info=json.dumps({key : value for key, value in zip([detail.find_element(By.CLASS_NAME, 'key').get_property('innerText').strip().replace(':', '') for detail in details], [detail.find_element(By.CLASS_NAME, 'val').get_property('innerText').strip() for detail in details])}, ensure_ascii=False),
            extra_images=json.dumps({f'img{i+1}': img for i, img in enumerate(images[1:])}, ensure_ascii=False),
        )
    )
