from requests import get,post,Session
from requests.exceptions import RequestException
from contextlib import closing

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