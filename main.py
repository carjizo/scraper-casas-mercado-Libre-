from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

url_to_scrap = "https://listado.mercadolibre.com.pe/inmuebles/venta/#applied_filter_id%3DOPERATION%26applied_filter_name%3DOperaci%C3%B3n%26applied_filter_order%3D4%26applied_value_id%3D242075%26applied_value_name%3DVenta%26applied_value_order%3D3%26applied_value_results%3D1035%26is_custom%3Dfalse"
#Funcion para parseo de la direccion de la casa

def get_address(data):
    part = data.split(",")
    partAmount = len(part)
    if(partAmount == 3):
        return {'address' : part[0], 'city' : part[1], 'region' : part[2]}
    elif(partAmount > 3):
        return {'address' : " ".join(part[:len(part)-3]), 'city' : part[partAmount-2], 'region' : part[partAmount-1]}
    elif(partAmount < 3):
        for i in range(0,100):
            print("error:")
            print(data)
        return {'address' : 'FAIL', 'city' : 'FAIL', 'region' : data}

def house_li_html_to_obj(house_li_html):
    #Obtiene el url de la imagen
    img = house_li_html.find("img")
    try: 
        img_url = img['data-src']
    except:
        img_url = img['src']

    #Obtiene el precio
    price = house_li_html.find(class_="price-tag-fraction").text.replace(".", "")

    # Obtiene el Titulo de la publicacion
    title = house_li_html.find(class_="ui-search-item__title").text

    #Obtiene la direccion de la casa
    address = house_li_html.find(class_="ui-search-item__location").text
    address = get_address(address)

    #Obtiene tamaño y/o cantidad de habitaciones
    all_attribute = house_li_html.find_all(class_="ui-search-card-attributes__attribute")
    size = ""
    rooms = ""
    if(len(all_attribute) > 0):
        if("cubiertos" in all_attribute[0].text):
            size = all_attribute[0].text   
        else:
            rooms = all_attribute[0].text  

    if(len(all_attribute) > 1):
        rooms = all_attribute[1].text  

    #Obtiene la url de la publicacion
    url = house_li_html.find("a")["href"]
    #Devuelve objeto con esta data
    return {"img_url" : img_url, "price" : price,
    "title" : title, 'address' : address['address'], 
    'city' : address['city'], 'region' : address['region'], 
    "size" : size, "rooms" : rooms, "url" : url}

ruta = ChromeDriverManager(path="./chromedriver").install()
s = Service(ruta)
driver = webdriver.Chrome(service=s)
driver.get(url_to_scrap)
html_code = driver.page_source

soup = BeautifulSoup(html_code, 'lxml')

#encontrar todos los li wue tienen clase ui-search-layout__item
all_house_li =  soup.find_all("li", class_="ui-search-layout__item")


for house_li_html in all_house_li:
    house_obj = house_li_html_to_obj(house_li_html)
    print(house_obj)

# house_li_html_to_obj(all_house_li)
