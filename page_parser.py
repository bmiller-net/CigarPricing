from bs4 import BeautifulSoup
import services
import json

def get_coh_prices():
    coh_price_page = services.get_coh()
    coh_parsed = BeautifulSoup(coh_price_page, "html.parser")
    brand = ""
    items = []
    for row in coh_parsed.select("tr[id^='grid_DX']"):
        if (row.get("id") == None or row.text == None):
            continue
        print(row.get("id"))
        if (row.get("id").startswith("grid_DXGroup")):
            if (row.select("td")[1].text.startswith("Brand:")):
                brand = row.select("td")[1].text[7:]
                print(brand)
        if (row.get("id").startswith("grid_DXData")):
            item = {}
            cells = row.select("td")
            item["brand"] = brand
            item["name"] = cells[1].text.strip()
            item["quantity"] = cells[2].text.strip()
            item["price"] = cells[4].text.strip()[2:]
            items.append(item)
    
    return items
        
def get_ihav_prices():
    ihav_price_page = services.get_ihav()
    ihav_parsed = BeautifulSoup(ihav_price_page, "html.parser")
    brand = ""
    items = []
    for row in ihav_parsed.select("td.body_boder > table > tr"):
        inner_row = row.select("td > table > tr")[0]
        cells = inner_row.select("td")
        first_cell = cells[0]
        cell_parts = first_cell.text.split(" - ")
        
        brand = cell_parts[0].strip()
        name = cell_parts[1].strip()
        quantity = cell_parts[2].strip()
        
        price_text = cells[2].text.strip()
        price = price_text[3:]
        
        item = {}
        item["brand"] = brand
        item["name"] = name
        item["quantity"] = quantity
        item["price"] = price
        items.append(item)
    
    return items

def get_cubanlous_prices():
    cl_price_page = services.get_cubanlous()
    cl_json = json.loads(cl_price_page)
    cl_parsed = BeautifulSoup(cl_json["productList"], "html.parser")
    brand = ""
    items = []
    for row in cl_parsed.select(".product-container"):
        product_name = row.select(".product-name")[0]
        product_text = product_name.text
        link = product_name.get("href")
        
        brand_begin = "https://www.cubanlous.com/"
        brand_begin_idx = len(brand_begin)
        
        quantity_begin = "("
        quantity_begin_idx = product_text.index(quantity_begin) + 1
        quantity_end = ")"
        quantity_end_idx = product_text.index(quantity_end)
        quantity = product_text[quantity_begin_idx:quantity_end_idx]
        
        brand_end = "-cigars/"
        name = ""
        try:
            brand_end_idx = link.index(brand_end)
            brand = link[brand_begin_idx:brand_end_idx].replace("-", " ")
            name = link[brand_end_idx+len(brand_end):].replace("-"+quantity, "").replace("-", " ")
            name = name.replace(brand, "")
        except:
            continue
        
        price = row.select(".product-price")[0].text.strip()[1:]
        
        item = {}
        item["brand"] = brand.strip().title()
        item["name"] = name.strip().title()
        item["quantity"] = quantity
        item["price"] = price
        items.append(item)
    
    return items
    
def get_finestcc_prices():
    finestcc_price_page = services.get_finestcc()
    finestcc_parsed = BeautifulSoup(finestcc_price_page, "html.parser")
    brand = ""
    items = []
    for brand_section in finestcc_parsed.select("div.category_products_container"):
        try:
            brand = brand_section.select(".subcategory_title")[0].text.strip()
        except:
            continue
        
        for product in brand_section.select(".product_container"):
            name = product.select(".product_title")[0].text
            
            for option in product.select(".product_price > div"):
                item = {}
                item["brand"] = brand
                item["name"] = name.replace(brand, "").strip()
                item["price"] = option.select(".original,.special")[0].text.strip()[3:]
                item["quantity"] = option.select(".sticks")[0].text.strip()
                items.append(item)
    
    return items