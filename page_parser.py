from bs4 import BeautifulSoup
import services

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
    
    for item in items:
        print(item["brand"] + "|" + item["name"] + "|" + item["quantity"] + "|" + item["price"])