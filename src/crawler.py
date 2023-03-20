import requests
import re
from db.mongo import getDb, connect2db, createIndexes
import json
from config.envparams import Params
from config.statuslogger import LOGGER
from datetime import datetime
import time
import http.client

path = './'
PARAM_FILE_PATH = "./params.json"
prms = Params(param_file_path=PARAM_FILE_PATH)
logger = LOGGER(status=prms.DEBUG, param_handler=prms)
'''
headers = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')}
'''
headers = {
        'Cookie': 'bm_sz=8BAFD46034DB80A2A1024A30C9BA36A4~YAAQZMETAs7e8aZ1AQAAGVygxwngqRySkk1jU/AZffaF5IDK0/MAgCBFi03x5PfN+PfeaT8oYDDy96BOHL6/AgQyQQA/cd3p1sVuArfk+LOzfNA0zs/XqQNyPq9nLJCV8DHU/aUU3Mn2BBIoJShZmwcwTQKMw9p/N9ipasIC0FaGSVDLDxX4jt5Xp/v7JJMK73Q/oIs=; _abck=1E82F1EF50E796EEFCDC8FFCED2C4519~-1~YAAQZMETAs/e8aZ1AQAAGVygxwT67LmcNzafu84DL8buhhMmeaSC8FFbdT2VIoCGhDywtkBgMRR/9A7rRrbIPuBBmqW9HzXPq66Cww+VE9Bt4NrKM8qlw0l4328cFNztrVIxbryfMNDbdUf3IP2N9Tq68mAvRU9Q+DaBKdg/R/8oUqNW3Kq+pNFt/BT76f7AtTzQuZMqlgbKx5kVExsHtgiQJbM/Se84KVfExe64Pi5i29LHiIT7i2pDsFMTKg3nuFlncghvryV5H/+yIljIXwDDVy2pZ7qfg5IWVA0mG9kmEbz+EFiGJxKTohRBjkc=~-1~-1~-1; ak_bmsc=AD8855452E34922A2F0A2186E5E9DE4E0213C11DFA0600000D09B05FA584603B~plwlnAyb3xdQqO7AORZzDZLVcJR7xAxzGg7PBAinHuUNRwI65HQR++ngzMxztqUh0TxVwIOKC8sc7Ec1my8094HtgbfChSOQt0VMyb1QMuFDOQD1+cMEBRRKlwYKPaikXvie51nN9ro+zDvn5xMEX6MLosX0l7Nwe2YbwO89aGxuIiE9PiYpHWH+ku8F6WD/6+EtGLeOxkFbBeFzymsDcQLJpdC6Ts+dyhiyQM9v6Ojao='
    }
hepsiburada_link = "www.hepsiburada.com"
mongoclient = connect2db(prms.DB_HOST_IP, prms.DB_HOST_PORT, prms.MAXSEVSELDELAY, logging=logger.log)
createIndexes(mongoclient, prms, logging=logger.log)

def get_sitemap_links(link):
    links = []
    conn = http.client.HTTPSConnection(link)
    payload = ''
    conn.request("GET", "/sitemaps/sitemap.xml", payload, headers)
    res = conn.getresponse()
    data = res.read()
    splitted = data.decode("utf-8").split("<sitemap>")[1:]
    for text in splitted:
        pattern = "<loc>https://www.hepsiburada.com/sitemaps/(.*?)</loc>"
        substring = re.search(pattern, text).group(1)
        links.append(substring)
    return links


def get_comment_sitemap_links(link):
    links = []
    conn = http.client.HTTPSConnection(link)
    payload = ''
    conn.request("GET", "/sitemaps/yorumlar/sitemap.xml", payload, headers)
    res = conn.getresponse()
    data = res.read()
    splitted = data.decode("utf-8").split("<sitemap>")[1:]
    for text in splitted:
        pattern = "<loc>https://www.hepsiburada.com/sitemaps/(.*?)</loc>"
        substring = re.search(pattern, text).group(1)
        links.append(substring)
    return links


def get_products(link):
    prod_links = []
    conn = http.client.HTTPSConnection(hepsiburada_link)
    payload = ''
    sub_link = "/sitemaps/"+link
    try:
        conn.request("GET", sub_link, payload, headers)
        res = conn.getresponse()
        data = res.read()
        splitted = data.decode("utf-8").split("<url>")[1:]
        for text in splitted:
            pattern = "<loc>https://www.hepsiburada.com/(.*?)</loc>"
            substring = re.search(pattern, text).group(1)
            prod_links.append(substring)
    except requests.exceptions.ChunkedEncodingError:
        time.sleep(5)
        get_products(link)
    return prod_links


def get_comments(link):
    prod_links = []
    conn = http.client.HTTPSConnection(hepsiburada_link)
    payload = ''
    sub_link = "/sitemaps/" + link
    try:
        conn.request("GET", sub_link, payload, headers)
        res = conn.getresponse()
        data = res.read()
        splitted = data.decode("utf-8").split("<url>")[1:]
        for text in splitted:
            pattern = "<loc>https://www.hepsiburada.com/(.*?)</loc>"
            substring = re.search(pattern, text).group(1)
            prod_links.append(substring)
    except requests.exceptions.ChunkedEncodingError:
        time.sleep(5)
        get_comments(link)
    return prod_links


def get_prod_details(page, non_id):
    prod_detail_dict = dict()
    non_detail_id = "non"+str(non_id)
    non_detail_dict = dict()
    conn = http.client.HTTPSConnection(hepsiburada_link)
    payload = ''
    conn.request("GET", "/"+page, payload, headers)
    res = conn.getresponse()
    data = res.read()
    utag_data = data.decode("utf-8").split(";")
    for data in utag_data:
        if "utag_data" in data:
            prod_detail = data
            pattern = "{(.*?)}"
            try:
                prod_detail_text = "{"+re.search(pattern, prod_detail).group(1)+"}"
                prod_detail_dict = json.loads(prod_detail_text)
            except (AttributeError, json.decoder.JSONDecodeError):
                non_detail_dict["id"] = non_detail_id
                non_detail_dict["non_taken_page"] = page
                _db = getDb(mongoclient, prms.DB, logging=logger.log)
                collection = _db[prms.DB_HEPSIBURADA_COLLECTION]
                try:
                    collection.insert_one(non_detail_dict)
                except Exception as e:
                    logger.log.info(str(e))

    return prod_detail_dict


def get_comment_details(page):
    conn = http.client.HTTPSConnection(hepsiburada_link)
    payload = ''
    conn.request("GET", "/" + page, payload, headers)
    res = conn.getresponse()
    data = res.read()
    comment_data = data.decode("utf-8")
    splitted = comment_data.split(";")
    for data in splitted:
        if 'window.HERMES.YORUMLAR' in data:
            prod_data = data
            # pattern = '"data":(.*)</script>'
            # prod_detail_text = re.search(pattern, prod_data).group(1)
            # prod_detail_dict = json.loads(prod_detail_text)
            try:
                prod_detail_text = prod_data[prod_data.index('"data":')+len('"data":'):prod_data.index('"location"')].strip()[:-1]
                prod_detail_dict = json.loads(prod_detail_text)
                return prod_detail_dict
            except ValueError:
                continue


def run_prod_details_hepsiburada():
    start = datetime.now()
    sitemap_links = get_sitemap_links(hepsiburada_link)
    default_blank_value = ""
    id_counter = 0
    for link in sitemap_links:
        try:
            prods = get_products(link)
        except (TimeoutError, OSError):
            logger.log.info("Error occured. Try 30 minutes later")
            time.sleep(1800)
            continue
        for prod_link in prods:
            id_counter += 1
            try:
                raw_prod_dict = get_prod_details(prod_link, id_counter)
            except (TimeoutError, OSError):
                logger.log.info("Error occured. Try 30 minutes later")
                time.sleep(1800)
                continue
            if not raw_prod_dict:
                continue
            prod_dict = dict()
            try:
                prod_dict['site_name'] = raw_prod_dict['page_site_name']
            except KeyError:
                prod_dict['site_name'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['category_path'] = raw_prod_dict['category_path']
            except KeyError:
                prod_dict['category_path'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['seller_name'] = raw_prod_dict['order_store']
            except KeyError:
                prod_dict['seller_name'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['page_url'] = raw_prod_dict['page_url']
            except KeyError:
                prod_dict['page_url'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['price'] = raw_prod_dict['product_prices'][0]
            except KeyError:
                prod_dict['price'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['unit_price'] = raw_prod_dict['product_unit_prices'][0]
            except KeyError:
                prod_dict['unit_price'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['brand'] = raw_prod_dict['product_brand']
            except KeyError:
                prod_dict['brand'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['id'] = raw_prod_dict['product_ids'][0]
            except KeyError:
                prod_dict['id'] = id_counter
                prod_dict['raw_data'] = raw_prod_dict
                logger.log.info("id not found. Assigned id is: " + str(id_counter))
            try:
                prod_dict['category'] = raw_prod_dict['product_categories'][0]
            except KeyError:
                prod_dict['category'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['barcode'] = raw_prod_dict['product_barcode']
            except KeyError:
                prod_dict['barcode'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['name'] = raw_prod_dict['product_name_array']
            except KeyError:
                prod_dict['name'] = default_blank_value
                prod_dict['raw_data'] = raw_prod_dict
            try:
                ids_split = raw_prod_dict['category_id_hierarchy'].split('>')
                names_split = raw_prod_dict['category_name_hierarchy'].split('>')
                category_dict = dict()
                for index, key in enumerate(names_split):
                    key = key.lstrip().rstrip()
                    ids_split[index] = ids_split[index].lstrip().strip()
                    category_dict[key] = ids_split[index]
                prod_dict['category_dict'] = category_dict
            except KeyError:
                prod_dict['category_dict'] = dict()
                prod_dict['raw_data'] = raw_prod_dict
            try:
                prod_dict['product_status'] = raw_prod_dict['product_status']
            except KeyError:
                prod_dict['product_status'] = ""
                prod_dict['raw_data'] = raw_prod_dict

            _db = getDb(mongoclient, prms.DB, logging=logger.log)
            collection = _db[prms.DB_HEPSIBURADA_COLLECTION]
            try:
                collection.insert_one(prod_dict)
                logger.log.info(prod_dict['id'] + " is inserted")
            except Exception as e:
                logger.log.info(str(e))
    end = datetime.now()
    logger.log.info("Process finished in " + str(end - start))


def run_comments_hepsiburada():
    # start = datetime.now()
    sitemap_links = get_comment_sitemap_links(hepsiburada_link)
    default_blank_value = ""
    for link in sitemap_links:
        try:
            prods = get_comments(link)
        except (TimeoutError, OSError):
            logger.log.info("Error occured. Try 30 minutes later")
            time.sleep(1800)
            continue
        for prod_link in prods:
            try:
                raw_comment_dict = get_comment_details(prod_link)
            except (TimeoutError, OSError):
                logger.log.info("Error occured. Try 30 minutes later")
                time.sleep(1800)
                continue
            if not raw_comment_dict:
                continue
            comment_dict = dict()
            try:
                comment_dict['page_url'] = raw_comment_dict['selectedVariant']['url']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['page_url'] = default_blank_value
            comment_dict['site_name'] = 'Hepsiburada'
            try:
                comment_dict['product_id'] = raw_comment_dict['sku'].lower()
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['product_id'] = default_blank_value
            try:
                comment_dict['product_barcode'] = raw_comment_dict['selectedVariant']['barcode'][0]
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['product_barcode'] = default_blank_value
            try:
                comment_dict['product_name'] = raw_comment_dict['selectedVariant']['name']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['product_name'] = default_blank_value
            try:
                comment_dict['product_brand'] = raw_comment_dict['product']['brand']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['product_brand'] = default_blank_value
            try:
                comment_dict['best_comment'] = raw_comment_dict['userReviews']['data']['bestUserContent']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['best_comment'] = default_blank_value
            try:
                comment_dict['approved_comment_list'] = raw_comment_dict['userReviews']['data']['approvedUserContent']['approvedUserContentList']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['approved_comment_list'] = default_blank_value
            try:
                comment_dict['merchants_from_comments'] = raw_comment_dict['userReviews']['data']['filterData']['merchants']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['merchants_from_comments'] = default_blank_value
            try:
                comment_dict['product_variants'] = raw_comment_dict['selectedVariant']['variantListing']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['product_variants'] = default_blank_value
            try:
                comment_dict['average_star'] = raw_comment_dict['userReviews']['data']['summary']['average']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['average_star'] = default_blank_value
            try:
                comment_dict['star_details'] = raw_comment_dict['userReviews']['data']['summary']['details']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['star_details'] = default_blank_value
            try:
                comment_dict['comment_count'] = raw_comment_dict['userReviews']['data']['summary']['userContentCount']
            except:
                comment_dict['raw_data'] = raw_comment_dict
                comment_dict['comment_count'] = default_blank_value
            db = getDb(mongoclient, prms.DB, logging=logger.log)
            collection = db[prms.DB_HEPSIBURADA_COMMENTS_COLLECTION]
            try:
                collection.insert_one(comment_dict)
                logger.log.info(raw_comment_dict['sku'].lower() + " comments inserted.")
            except Exception as e:
                logger.log.info(str(e))

