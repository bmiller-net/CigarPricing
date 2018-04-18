import xlwt
import page_parser
import time
import re
import configparser
import os

def run():
    book = xlwt.Workbook()
    
    get_prices(book, page_parser.get_ihav_prices, "iHavanas")
    #get_prices(book, page_parser.get_coh_prices, "Cigars of Habanos")
    #get_prices(book, page_parser.get_cubanlous_prices, "Cuban Lous")
    #get_prices(book, page_parser.get_finestcc_prices, "Finest Cuban Cigars")
    
    filename = "App_Data/" + time.strftime("%Y%m%d") + "_ihav_prices.xls"
    book.save(filename)
    
def get_prices(workbook, retrieve_function, source_name):
    prices = retrieve_function()
    sheet = workbook.add_sheet(source_name)
    
    for idx, price in enumerate(prices):
        sheet.write(idx, 0, price["brand"])
        sheet.write(idx, 1, price["name"])
        sheet.write(idx, 2, price["quantity"])
        sheet.write(idx, 3, price["price"])

def get_unique():
    ihav = page_parser.get_ihav_prices()
    coh = page_parser.get_coh_prices()
    cl = page_parser.get_cubanlous_prices()
    fcc = page_parser.get_finestcc_prices()
    
    inventory = []
    # inventory = return_unique_inventory(ihav, inventory)
        
    # inventory = return_unique_inventory(coh, inventory)
        
    # inventory = return_unique_inventory(cl, inventory)
        
    # inventory = return_unique_inventory(fcc, inventory)
    
    joined_items = {}
    
    for item in ihav:
        display_tuple = get_display_tuple(item["brand"], item["name"], item["quantity"])
        key = ()
        uniform_item = get_uniform_item_tuple(display_tuple[0], display_tuple[1], display_tuple[2])
        for inv in inventory:
            if (get_uniform_item_tuple(inv[0], inv[1], inv[2]) == uniform_item):
                key = inv
                break
        if (key == () or uniform_item not in joined_items):
            inventory.append(uniform_item)
            joined_items[uniform_item] = { "brand": display_tuple[0], "name": display_tuple[1], "quantity": display_tuple[2] }
        joined_items[uniform_item]["ihav"] = item["price"]
        
    for item in coh:
        display_tuple = get_display_tuple(item["brand"], item["name"], item["quantity"])
        key = ()
        uniform_item = get_uniform_item_tuple(display_tuple[0], display_tuple[1], display_tuple[2])
        for inv in inventory:
            if (get_uniform_item_tuple(inv[0], inv[1], inv[2]) == uniform_item):
                key = inv
                break
        if (key == () or uniform_item not in joined_items):
            inventory.append(uniform_item)
            joined_items[uniform_item] = { "brand": display_tuple[0], "name": display_tuple[1], "quantity": display_tuple[2] }
        joined_items[uniform_item]["coh"] = item["price"]
        
    for item in cl:
        display_tuple = get_display_tuple(item["brand"], item["name"], item["quantity"])
        key = ()
        uniform_item = get_uniform_item_tuple(display_tuple[0], display_tuple[1], display_tuple[2])
        for inv in inventory:
            if (get_uniform_item_tuple(inv[0], inv[1], inv[2]) == uniform_item):
                key = inv
                break
        if (key == () or uniform_item not in joined_items):
            inventory.append(uniform_item)
            joined_items[uniform_item] = { "brand": display_tuple[0], "name": display_tuple[1], "quantity": display_tuple[2] }
        joined_items[uniform_item]["cl"] = item["price"]
        
    for item in fcc:
        display_tuple = get_display_tuple(item["brand"], item["name"], item["quantity"])
        key = ()
        uniform_item = get_uniform_item_tuple(display_tuple[0], display_tuple[1], display_tuple[2])
        for inv in inventory:
            if (get_uniform_item_tuple(inv[0], inv[1], inv[2]) == uniform_item):
                key = inv
                break
        if (key == () or uniform_item not in joined_items):
            inventory.append(uniform_item)
            joined_items[uniform_item] = { "brand": display_tuple[0], "name": display_tuple[1], "quantity": display_tuple[2] }
        joined_items[uniform_item]["fcc"] = item["price"]
    
    book = xlwt.Workbook()
    uitems = book.add_sheet("Inventory")
    uitems.write(0, 0, "Brand")
    uitems.write(0, 1, "Name")
    uitems.write(0, 2, "Quantity")
    uitems.write(0, 3, "iHav")
    uitems.write(0, 4, "CoH")
    uitems.write(0, 5, "CubanLous")
    uitems.write(0, 6, "FinestCC")
    idx = 1
    
    brands_to_include = get_brands_to_include()
    
    for key,uitem in joined_items.items():
        
        brand = uitem["brand"]
        name = uitem["name"]
        quantity = key[2]
        
        if brand not in brands_to_include:
            continue
        
        uitems.write(idx, 0, brand)
        uitems.write(idx, 1, name)
        uitems.write(idx, 2, quantity)
        
        if ("ihav" in uitem):
            uitems.write(idx, 3, uitem["ihav"].strip())
        
        if ("coh" in uitem):
            uitems.write(idx, 4, uitem["coh"].strip())
        
        if ("cl" in uitem):
            uitems.write(idx, 5, uitem["cl"].strip())
        
        if ("fcc" in uitem):
            uitems.write(idx, 6, uitem["fcc"].strip())
        
        idx+=1
    filename = "App_Data/" + time.strftime("%Y%m%d-%H%M") + "_prices.xls"
    book.save(filename)
    
def return_unique_inventory(items, inventory = []):
    for item in items:
        uniform_item = get_uniform_item_tuple(item["brand"], item["name"], item["quantity"])
        
        item_found = False
        for inv in inventory:
            uniform_inv = get_uniform_item_tuple(inv[0], inv[1], inv[2])
            if (uniform_item == uniform_inv):
                item_found = True
                break
        
        if (item_found):
            break
            
        inventory.append((item["brand"], item["name"], item["quantity"]))
    
    return inventory

def fix_brand(input_string):
    return input_string.replace("H.Upmann", "H. Upmann").replace("Hupmann", "H. Upmann").replace("Hoyo De Monterrey", "Hoyo de Monterrey").replace("Jose L. Piedra", "Jose Piedra").replace("Quai Orsay", "Quai DOrsay").replace("Romeo Y Julieta", "Romeo y Julieta").replace("San Cristobal De La Habana", "San Cristobal")

def get_display_tuple(brand, name, quantity):
    brand = fix_brand(brand)
    
    if brand.lower() == 'cohiba':
        name = name.replace("Robustos ", "Robusto ")
    
    if name.lower().endswith(" - lcdh"):
        name = name[:len(name)-7]
    
    if name.lower().endswith("lcdh"):
        name = name[:len(name)-4]
    
    if brand.lower() == 'hoyo de monterrey':
        if name.lower().startswith('hoyo '):
            name = name[5:]
        if name.lower().endswith("robusto"):
            name = name.replace("Petit Robusto", "Petit Robustos")
    
    if brand.lower() == 'h. upmann':
        name = name.replace("Connossieur", "Connoisseur")
        name = name.replace("Half Coronas", "Half Corona")
        name = name.replace("Royal Robustos", "Royal Robusto")
    
    if brand.lower() == 'montecristo':
        name = name.replace("Churchill Anejados", "Churchills Anejados")
        name = name.replace("Edmundos", "Edmundo")
    
    if brand.lower() == 'partagas':
        if name.endswith("Short"):
            name = name.replace("Short", "Shorts")
        
    if brand.lower() == 'romeo y julieta':
        name = name.replace("Sport Largos", "Sports Largos")

    if brand.lower() == 'la gloria cubana':
        name = name.replace("Medaille D Or No.4", "Medaille D`or No.4")
    
    name = re.sub('No(?P<number>[0-9]+)', 'No.\g<number>', name)
    
    name = format_for_display(name)
    
    
    return (brand, name, quantity)
    
def get_uniform_item_tuple(brand, name, quantity):
    brand_stripped = strip_special(fix_brand(brand)).lower()
    name_stripped = strip_special(name.replace("A/T", "Tubos")).lower()
    quantity_stripped = strip_special(quantity).replace("Box", "").replace("(Cabinet)", "").strip().lower()
    
    return (brand_stripped, name_stripped, quantity_stripped)
    
def strip_special(input_string):
    return re.sub('[-/\\\. ]', '', input_string).strip()
    
def format_for_display(input_string):
    return input_string.replace(". ", ".").replace("A/T", "Tubos")
    
def get_brands_to_include():
    settings_file = 'settings.ini'
    root_node = 'DEFAULT'
    brands_key = 'BrandsToInclude'
    
    if not os.path.exists(settings_file):
        return
    config = configparser.ConfigParser()
    config.read(settings_file)
    if root_node not in config:
        return
    if brands_key not in config[root_node]:
        return
    brands_to_include = config[root_node][brands_key]
    return list(map(lambda brand: brand.strip(), brands_to_include.split(',')))