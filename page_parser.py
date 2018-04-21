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
        if (row.get("id").startswith("grid_DXGroup")):
            if (row.select("td")[1].text.startswith("Brand:")):
                brand = row.select("td")[1].text[7:]
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
        price = price_text[2:]
        
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
            name = link[brand_end_idx+len(brand_end):]
            if (name.endswith("-cigars")):
                name = name[:len(name)-7]
            name = name.replace("-"+quantity, "").replace("-", " ").strip()
            if name.startswith(brand):
                name = name[len(brand):]
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
            name = product.select(".product_title")[0].text.strip()
            
            for option in product.select(".product_price > div"):
                item = {}
                item["brand"] = brand
                if name.startswith(brand):
                    name = name[len(brand):]
                item["name"] = name.strip()
                item["price"] = option.select(".original,.special")[0].text.strip()[3:]
                item["quantity"] = option.select(".sticks")[0].text.strip()
                items.append(item)
                
    return items
    
def get_cigarone_prices():
    cigarone_price_page = services.get_cigarone()
    cigarone_parsed = BeautifulSoup(cigarone_price_page, "html.parser")
    brand = ""
    items = []
    for brand_section in cigarone_parsed.select("section.section"):
        try:
            brand = brand_section.select("h1.banner-caption")[0].text.strip()
        except:
            continue
        
        for product in brand_section.select(".product-table"):
            columns = product.select(".column")
            
            name = columns[0].text.strip()
            
            quantity = columns[1].text.strip()
            
            price_column = columns[2]
            price = ""
            special_price = price_column.select(".price-discounted")
            if (len(special_price) > 0):
                price = special_price[0].text.strip()
            else:
                price = price_column.text.strip()
            
            item = {}
            item["brand"] = brand
            item["name"] = name
            item["price"] = price[2:]
            item["quantity"] = quantity
            
            # print(item["brand"]+"|"+item["name"]+"|"+item["price"]+"|"+item["quantity"])
            
            items.append(item)
                
    
    return items
    
def get_topcubans_prices():
    topcubans_price_page = services.get_topcubans()
    topcubans_parsed = BeautifulSoup(topcubans_price_page, "html.parser")
    brand = ""
    items = []
    for product in topcubans_parsed.select("section.product-grid div.column"):
        brand = product.select("div.brand-name")[0].text.strip()
        name = product.select("div.product-name")[0].text.strip()
        quantity = product.select("div.product-unit-name")[0].text.strip()
        price = product.select("span.price-discounted,span.price")[0].text.strip()
                
        item = {}
        item["brand"] = brand
        item["name"] = name
        item["price"] = price[2:]
        item["quantity"] = quantity
            
        items.append(item)
    
    return items
    
def get_yulcigars_prices():
    price_page = services.get_yulcigars()
    parsed = BeautifulSoup(price_page, "html.parser")
    brand = ""
    items = []
    for row in parsed.select("table tr")[1:]:
        if not row.text.strip():
            continue
            
        columns = row.select("td")
        style = ""
        if "style" in row.attrs:
            style = row["style"]
        elif "style" in columns[0].attrs:
            style = columns[0]["style"]
        else:
            continue
            
        if "height: 15.75pt;" in style:
            brand = row.text.strip()
            continue
        
        if "height: 15pt;" not in style:
            continue
        
        name = columns[0].text.strip()
        quantity = columns[5].text.strip()
        
        box_price = columns[4].text.replace(",", ".").strip()
        single_price = columns[1].text.replace(",", ".").strip()
        price1 = columns[2].text.replace(",", ".").strip()
        price2 = columns[3].text.replace(",", ".").strip()
        
        # add single price
        single = {}
        single["brand"] = brand
        single["name"] = name
        single["price"] = single_price
        single["quantity"] = "single"
        items.append(single)
        
        quantities = quantity.split("/")
        
        current_quantity = 0
        
        if price2 != "0.00":
            if price1 != "0.00":
                size1 = {}
                size1["brand"] = brand
                size1["name"] = name
                size1["price"] = price1
                size1["quantity"] = "3" if current_quantity not in quantities else quantities[current_quantity].strip()
                current_quantity += 1
                items.append(size1)
        
            size2 = {}
            size2["brand"] = brand
            size2["name"] = name
            size2["price"] = price2
            size2["quantity"] = "10" if current_quantity not in quantities else quantities[current_quantity].strip()
            items.append(size2)

        item = {}
        item["brand"] = brand
        item["name"] = name
        item["price"] = box_price
        item["quantity"] = quantities[len(quantities)-1].strip()

        items.append(item)
    print("Cuba items: "+ str(len(items)))
    return items
    
def get_prices():
    ihav = get_ihav_prices()
    coh = get_coh_prices()
    cl = get_cubanlous_prices()
    fcc = get_finestcc_prices()
    c1 = get_cigarone_prices()
    tc = get_topcubans_prices()
    cuba = get_yulcigars_prices()
    return { "iHav": ihav, "CoH": coh, "CubanLous": cl, "FinestCC": fcc, "CigarOne": c1, "TopCubans": tc, "Cuba": cuba }