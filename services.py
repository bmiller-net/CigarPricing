from requests import get,post,Session
from requests.exceptions import RequestException
from contextlib import closing
import time

def get_coh():
    s = Session()
    s.get("https://www.cigarsofhabanos.com/")
    url = "https://www.cigarsofhabanos.com/search_product.aspx?pST=A&qsType=0&qsBrand=0&qsProduct=&qsPriceCat=0&qsPrice1=0&qsPrice2=0&qsLenCat=0&qsLen1=0&qsLen2=0&qsGuageCat=0&qsGuage1=0&qsGuage2=0"
    try:
        with closing(s.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def get_ihav():
    s = Session()
    s.get("https://www.ihavanas.com/")
    url = "https://www.ihavanas.com/advancesearch.php"
    headers = { "Content-Type": "multipart/form-data; boundary=---------------------------7845160828623" }
    body = '-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtSearch"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtregemail"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtregpswd"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtrm"\r\n\r\nN\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="cmbtype"\r\n\r\n0\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="cmbbrand"\r\n\r\n0\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtproduct"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtPF"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtPT"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtLF"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtLT"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtRGF"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtRGT"\r\n\r\n\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="btnSubmit"\r\n\r\nSubmit\r\n-----------------------------7845160828623\r\nContent-Disposition: form-data; name="txtNL"\r\n\r\nN\r\n-----------------------------7845160828623--\r\n'
    try:
        with closing(s.post(url, data=body, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content.replace(b'54%"<', b'54%"><')
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def get_cubanlous():
    s = Session()
    s.get("https://www.cubanlous.com/")
    timestamp = round(time.time() * 1000)
    url = "https://www.cubanlous.com/modules/blocklayered_mod/blocklayered_mod-ajax.php?id_category_layered=81&layered_price_slider=49_950&orderby=name&orderway=asc&n=500forceSlide&_=" + str(timestamp)
    headers = { "Accept": "application/json, text/javascript, */*; q=0.01" }
    try:
        with closing(s.get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def get_finestcc():
    s = Session()
    s.get("https://www.finestcubancigars.com/")
    timestamp = round(time.time() * 1000)
    url = "https://www.finestcubancigars.com/brands/all-cigar-brands.html"
    headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" }
    try:
        with closing(s.get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)