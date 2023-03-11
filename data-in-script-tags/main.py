import requests
from selectolax.parser import HTMLParser
import chompjs
import json


url = "https://www.fjallraven.com/uk/en-gb/bags-gear/backpacks-bags/trekking-backpacks/lappland-hike-15?_t_q=&_t_hit.id=Luminos_Storefront_Web_Features_Catalog_Product_Domain_CommonProduct/CatalogContent_40ad3b28-3b95-4cf9-96ca-716269fcee25_en-GB&_t_hit.pos=3&_t_tags=andquerymatch%2clanguage%3aen%2csiteid%3a162d49d9-f0ac-4d2d-a110-e8143f6ca828&v=F27230%3a%3a7323450464615"

resp = requests.get(url)
html = HTMLParser(resp.text)

data = html.css("script[type='text/javascript']")

for script in data:
    try:
        new = chompjs.parse_js_object(script.text())
        if 'variants' in new:
            with open("export.json", "w") as f:
                json.dump(new, f)
    except:
        pass
