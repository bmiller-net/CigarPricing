import xlwt
import page_parser
import time
import re
import configparser
import os
import unidecode
import data_layer

def get_unique():
    site_prices = page_parser.get_prices()

    inventory = []
    
    joined_items = {}
        
    book = xlwt.Workbook()
    uitems = book.add_sheet("Inventory")
    uitems.write(0, 0, "Brand")
    uitems.write(0, 1, "Name")
    uitems.write(0, 2, "Quantity")
    
    col = 3
    
    brands_to_include = list(map(lambda x: x.lower(), get_brands_to_include()))
    for source,prices in site_prices.items():
        items = process_site_items(prices, source)
        for key,value in items.items():
            if key[0] not in brands_to_include:
                continue
            if key not in joined_items:
                joined_items[key] = { "brand": value[0], "name": value[1], "quantity": value[2] }
            joined_items[key][source] = value[3]
        uitems.write(0, col, source)
        col += 1
        
    idx = 1
    
    
    for key,uitem in joined_items.items():
        brand = uitem["brand"]
        name = uitem["name"]
        quantity = key[2]
        
        uitems.write(idx, 0, brand)
        uitems.write(idx, 1, name)
        uitems.write(idx, 2, quantity)
        
        col = 3
        for source in list(site_prices.keys()):
            if source in uitem.keys():
                uitems.write(idx, col, uitem[source].strip())
            col += 1
        
        idx+=1
    filename = "App_Data/" + time.strftime("%Y%m%d-%H%M") + "_prices.xls"
    book.save(filename)

def load_database():
    site_prices = page_parser.get_prices()

    inventory = []
    
    joined_items = {}
        
    brands_to_include = list(map(lambda x: x.lower(), get_brands_to_include()))
    for source,prices in site_prices.items():
        items = process_site_items(prices, source)
        for key,value in items.items():
            if key[0] not in brands_to_include:
                continue
            if key not in joined_items:
                joined_items[key] = { "brand": value[0], "name": value[1], "quantity": value[2] }
            joined_items[key][source] = { "price": value[3], "is_in_stock": value[4] }
    
    records_to_load = []
    for key,uitem in joined_items.items():
        brand = uitem["brand"]
        name = uitem["name"]
        quantity = key[2]
        
        for source in list(site_prices.keys()):
            if source in uitem.keys():
                records_to_load.append([ brand, name, quantity, source, uitem[source]["price"], uitem[source]["is_in_stock"] ] )
    
    print("items: "+str(len(joined_items)))
    
    number_of_records = data_layer.insert_prices(records_to_load)
    print(str(number_of_records) + " records loaded")
                
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
    
def get_display_tuple(brand, name, quantity, price, is_in_stock):
    brand = fix_brand(brand)
    name = fix_name(name)
    quantity = fix_quantity(quantity)
    price = fix_price(price)
    
    if brand.lower() == 'cohiba':
        name = name.replace("Robustos ", "Robusto ")
        name = name.replace("Priamides ", "Piramides ")
        name = name.replace("Pirmides ", "Piramides ")
        name = name.replace("Coronas Especiales", "Corona Especiales")
        name = re.sub('siglo', 'Siglo', name, flags=re.IGNORECASE)
        name = re.sub('[ ]bhk[ ]', ' ', name, flags=re.IGNORECASE)
        if name.startswith("Genios"):
            name = "Maduro 5 Genios"
        if name.startswith("Magicos"):
            name = "Maduro 5 Magicos"
        if name.startswith("Secretos"):
            name = "Maduro 5 Secretos"
        if name.endswith("Robusto"):
            name = name + "s"
        name = name.replace("Gran Reserva", "Grand Reserva")
        name = re.sub("Siglo (?P<numeral>([IVX]){1,3})", lambda match: r'Siglo {}'.format(match.group(1).upper()), name, flags=re.IGNORECASE)
    
    if brand.lower() == 'cuaba':
        name = name.replace("Diademas", "Diadema")
        name = name.replace("Salomones", "Salomon")
    
    if name.lower().endswith(" - lcdh"):
        name = name[:len(name)-7]
    
    if name.lower().endswith("lcdh"):
        name = name[:len(name)-4]
    
    if brand.lower() == "el rey del mundo":
        name = name.replace("Demi Tasse", "Demi-Tasse")
        if name.startswith("Rey Del Mundo"):
            name = name[14:]
    
    if brand.lower() == "fonseca":
        name = name.replace("CADETES", "Cadetes")
    
    if brand.lower() == 'hoyo de monterrey':
        if name.lower().startswith('hoyo '):
            name = name[5:]
        if name.lower().endswith("robusto"):
            name = name.replace("Petit Robusto", "Petit Robustos")
        if name.startswith("du"):
            name = name.replace("du ", "Du ")
        if name.startswith("des"):
            name = name.replace("des", "Des")
        name = name.replace("Epicure Especiales", "Epicure Especial")
    
    if brand.lower() == 'h. upmann':
        name = name.replace("Connossieur", "Connoisseur")
        name = name.replace("Half Coronas", "Half Corona")
        name = name.replace("Royal Robustos", "Royal Robusto")
        if name.startswith("Upmann "):
            name = name[7:]
        if name.endswith("Epicure"):
            name = name + "s"
        name = name.replace("Majestics", "Majestic")
    
    if brand.lower() == 'la gloria cubana':
        name = re.sub(' [d][ \'\`]or ', ' d\'or ', name, flags=re.IGNORECASE)
        name = re.sub('th aniversdario', 'Aniversario', name, flags=re.IGNORECASE)
    
    if brand.lower() == 'montecristo':
        name = name.replace("Churchill Anejados", "Churchills Anejados")
        name = name.replace("Edmundos", "Edmundo")
        name = name.replace("Especiales No", "Especial No")
        name = re.sub("anniversario", "Aniversario", name, flags=re.IGNORECASE)
    
    if brand.lower() == 'partagas':
        if name.endswith("Short"):
            name = name.replace("Short", "Shorts")
        name = name.replace("Millefleurs", "Mille Fleurs")

    if brand.lower() == 'punch':
        name = re.sub('(Punch)?[ ]?[-]?[ ]?(Punch)', 'Punch', name)
        name = name.replace('Sabrosos Asia ', 'Sabrosos Asian ')
        name = name.replace('DOro', 'D\'Oro')
        name = name.replace('selection', 'Selection')
        
    if brand.lower() == 'romeo y julieta':
        name = name.replace("Churchills", "Churchill")
        name = name.replace("Sport Largos", "Sports Largos")
        name = re.sub('(?P<romeo>romeo[A-Za-z0-9\. ]*)Tubos', '\g<romeo>', name, flags=re.IGNORECASE)
        name = name.replace("Millefleurs", "Mille Fleurs")
        name = name.replace("Regalias D Londres", "Regalias de Londres")
        name = name.replace("Exhibition", "Exhibicion")
        name = name.replace("Coronitas en Cedros", "Coronitas en Cedro")
        if name.endswith("Petit Julieta"):
            name = name + "s"

    if brand.lower() == 'la gloria cubana':
        name = name.replace("Medaille D Or No.4", "Medaille D`or No.4")
            
    if brand.lower() == 'saint luis rey':
        name = name.replace("Inca ", "Incas")

    return (brand, name, quantity, price, is_in_stock)

def fix_brand(input_string):
    brands_from_settings = get_brands_to_include()
    fixed_brand = unidecode.unidecode(input_string.strip())
    fixed_brand = re.sub('h([\.]?[ ]?)upmann', 'H. Upmann', fixed_brand, flags=re.IGNORECASE)
    fixed_brand = re.sub("Quai [D]?[']?Orsay", "Quai D'Orsay", fixed_brand, flags=re.IGNORECASE)
    fixed_brand = re.sub("Jose Piedra", "Jose L. Piedra", fixed_brand, flags=re.IGNORECASE)
    fixed_brand = re.sub("San Cristobal", "San Cristobal De La Habana", fixed_brand, flags=re.IGNORECASE)
    for brand in brands_from_settings:
        if fixed_brand.lower() == brand.lower():        
            return brand
    return fixed_brand

def fix_name(input_string):
    output_string = re.sub('[ ][A][\/]?[T]', ' Tubos', unidecode.unidecode(input_string), flags=re.IGNORECASE)
    output_string = re.sub('N[o]?([ ]?)(?P<number>[0-9]+)', 'No.\g<number>', output_string)
    output_string = re.sub('[.][ ]', '.', output_string)
    output_string = re.sub('([\(][d][ ]?[\d]{4}[\)])?([ ](lcdh)?(hse)?(el)?[ ][\d]{4})?([*])?', '', output_string, flags=re.IGNORECASE)
    output_string = re.sub('((slb)?)((cab(inet)?)?)(jar[ ])?([(]hand rolled[)])?(([ ]box[ ])?(of[ ])?)([ ][\d]{2,4})?', '', output_string, flags=re.IGNORECASE)
    output_string = re.sub(' de ', ' de ', output_string, flags=re.IGNORECASE)
    output_string = re.sub(' du ', ' du ', output_string, flags=re.IGNORECASE)
    output_string = re.sub(' en ', ' en ', output_string, flags=re.IGNORECASE)
    output_string = output_string.replace("Edicion Limitada", "Limited Edition")
    if output_string.lower().endswith('tubo'):
        output_string = output_string + "s"
    output_string = re.sub('tubos', 'Tubos', output_string, flags=re.IGNORECASE)
    return output_string.strip()
    
def fix_quantity(input_string):
    output_string = re.sub('((slb)?)((Box)?)((Set)?)((Humidor)?)([\(]?Cab(inet)?[\)]?)?((Pack)?)((Cube)?)((Jar)?)([ ]of[ ])?', '', input_string, flags=re.IGNORECASE).strip()
    output_string = re.sub('(?P<quantity>[\d])x(?P<boxes>[\d])', '\g<quantity> x \g<boxes>', output_string, flags=re.IGNORECASE)
    return output_string

def fix_price(input_string):
    return re.sub('([$,`\']?)', '', input_string).strip()
    
def strip_special(input_string):
    return re.sub('[-/\\\. ]', '', input_string).strip()
    
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
    
def process_site_items(items, source):
    uniform_items = {}
    for item in items:
        display_tuple = get_display_tuple(item["brand"], item["name"], item["quantity"], item["price"], item["is_in_stock"])
        if any(map(lambda x: x is None, list(display_tuple))):
            continue
        uniform_item = (display_tuple[0].lower(), display_tuple[1].lower(), display_tuple[2].lower())
        uniform_items[uniform_item] = display_tuple

    return uniform_items
    
#get_unique()