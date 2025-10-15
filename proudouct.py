from bs4 import BeautifulSoup
import requests
import json
from time import sleep
import datetime
from colorama import Fore
now = datetime.datetime.now()
data = {}

def get_product(category_name, products):
    try:
        data[category_name] = {}
        counter = 1
        for product in products:
            url = f"https://smartwise.ir{product}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)

            if res.status_code != 200:
                print(Fore.RED+f"Error fetching {url}")
                continue

            soup = BeautifulSoup(res.text, "lxml")

            title_tag = soup.select_one("h1.product_title")
            price_tag = soup.select_one("p.price span.woocommerce-Price-amount")

            if title_tag and price_tag:
                data[category_name][f"product{counter}"] = {
                    "name": title_tag.text.strip(),
                    "Price": price_tag.text.strip(),
                    "Image Addres": f"{title_tag.text.strip()}.png",
                    "Url": f"{url}",
                    "Time": f"{now}",
                }
                print(f"✅ Saved: {title_tag.text.strip()}")
                counter += 1
            else:
                print(Fore.RED+f"❌ Could not parse product at {url}")
                data[category_name][f"product{counter}"] = {
                    "name": title_tag.text.strip(),
                    "Price": "ناموجود",
                    "Image Addres": f"{title_tag.text.strip()}.png",
                    "Url": f"{url}",
                    "Time": f"{now}",
                }
                print(f"✅ Saved: {title_tag.text.strip()}")
                counter += 1
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")

def save_json():
    try:
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("📁 products.json has been created and saved!")
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")


def product_category_smart_keys():
    try:
        links = ["/product/eco-series-single-pole-smart-switch/"
        ,"/product/eco-two-pole-series-smart-switch/"
        ,"/product/eco-series-smart-switch-three-pole/"
        ,"/product/eco-series-4-pole-smart-switch/"
        ,"/product/eco-series-smart-switch-curtain/"
        ,"/product/echo-handview-series-smart-key-contactless/"
        ,"/product/elite-pro-series-smart-key/",
        "/product/elite-series-smart-key/"]
        get_product("smart_keys",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    

def product_category_smart_touch_panel():
    try:
        links = ["/product/touch-panel-model-elitepad-10/",
                 "/product/33/",
                 "/product/touch-panel-elite-pad-7-inch/"]
        get_product("smart_touch_panel",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_central_controller_gateway():
    try:
        links = ["/product/wireless-gateway-plus-series/",
                 "/product/touch-panel-model-elitepad-4/",
                 "/product/wired-zigbee-gateway/",
                 "/product/zigbee-wireless-gateway/",
                 "/product/zigbee-gateway-elite-pad-model/"]
        
        get_product("central_controller_gateway",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_sensors_smart():
    try:
        links = ["/product/portable-smart-gas-sensor/",
                 "/product/irrf-sensor/",
                 "/product/temperature-and-humidity-sensor-2/",
                 "/product/smoke-detection-sensor/",
                 "/product/smart-alarm/",
                 "/product/light-detection-sensor/",
                 "/product/light-detection-sensor/",
                 "/product/18/",
                 "/product/human-detection-sensor/",
                 "/product/water-leakage-sensor/",
                 "/product/infrared-sensor-ir/",
                 "/product/temperature-and-humidity-sensor/",
                 "/product/gas-leak-detection-sensor/",
                 "/product/smoke-detection-sensor-smoke-detector/",
                 "/product/smart-light-sensor/",
                 "/product/human-presence-detection-sensor/",
                 "/product/smart-siren/"]
        
        get_product("sensors_smart",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_handles_smart():
    try:
        links = ["/product/specifications-of-the-smart-door-handle-model-swg03/",
                 "/product/specifications-of-the-smart-door-handle-model-swg05/",
                 "/product/specifications-of-the-smart-handle-model-swd26-face/",
                 "/product/specifications-of-the-smart-handle-model-swdf04-basic/",
                 "/product/specifications-of-smart-handle-model-swn19-face/",
                 "/product/specifications-of-smart-handle-model-swx7-face/",
                 "/product/specifications-of-smart-handle-model-swx10-face/",
                 "/product/room-door-handle-g03/",
                 "/product/anti-theft-door-handle-swd26-face/",
                 "/product/room-door-handle/",
                 "/product/anti-theft-door-handle-swdf04-basic/",
                 "/product/anti-theft-door-handle-swn19-face/",
                 "/product/anti-theft-door-handle-swx7-face/",
                 "/product/anti-theft-door-handle-swx10-face/"]
        get_product("handles_smart",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
    
def product_category_systems_audio():
    try:
        links = ["/product/8-inch-all-in-one-music-player/",
                 "/product/music-player-volume/",
                 "/product/4-inch-full-touch-music-player/",
                 "/product/touch-panel-model-elitepad-4/",]
        get_product("systems_audio",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_speakers():
    try:
        links = ["/product/rx6180-speaker/",
                 "/product/rx9180-speaker/",
                 "/product/speaker-rx-9160-380w/",
                 "/product/speaker-rx-5580-25w/",]
        get_product("speakers",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")


def product_category_security_and_surveillance_equipment():
    try:
        links = ["/product/smart-alarm-2/",
                 "/product/smart-camera/",]
        get_product("security_and_surveillance_equipment",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_smart_iphone():
    try:
        links = ["/product/internal-panel-m72t/",
                 "/product/internal-panel-m92t/",
                 "/product/outdoor-panel-single-bell-villa-kit-p901/",
                 "/product/outdoor-panel-single-bell-villa-kit-p902/",
                 "/product/outdoor-panel-single-bell-villa-kit-p904/",
                 "/product/m75t-internal-panel/",
                 "/product/external-panel-coding-d17/",
                 "/product/%d9%be%d9%86%d9%84-%d8%af%d8%a7%d8%ae%d9%84%db%8c-m75t/",
                 "/product/internal-panel-m72t-2/",
                 "/product/internal-panel-m72t-2/",
                 "/product/internal-panel-m92t-2/",
                 "/product/external-panel-coding-d30a/",
                 "/product/external-panel-coding-d22a/",
                 "/product/external-panel-coding-d22/",
                 "/product/external-panel-coding-d21a/"]
        get_product("smart_iphone",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
    
def product_category_miscellaneous_equipment():
    try:
        links = ["/product/remote-control/",
                 "/product/curtain-motor/",
                 "/product/smart-mcb-electrical-fuse/",
                 "/product/electrical-outlet/",
                 "/product/antenna-tv/",
                 "/product/telephone-socket/",
                 "/product/lan-network-socket/"]
        get_product("miscellaneous_equipment",links)
        save_json()
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")


def get_all_product():
    try:
        while True:
            print(Fore.GREEN+f"Start At |{now}|")
            sleep(5)
            print(Fore.GREEN+f"Start Get controller gateway products")
            product_category_central_controller_gateway()
            print(Fore.GREEN+f"Start Get handles smart products")
            sleep(5)
            product_category_handles_smart()
            print(Fore.GREEN+f"Start Get miscellaneous equipment products")
            sleep(5)
            product_category_miscellaneous_equipment()
            print(Fore.GREEN+f"Start Get surveillance_equipment products")
            sleep(5)
            product_category_security_and_surveillance_equipment()
            print(Fore.GREEN+f"Start Get sensors_smart products")
            sleep(5)
            product_category_sensors_smart()
            print(Fore.GREEN+f"Start Get smart iphone products")
            sleep(5)
            product_category_smart_iphone()
            print(Fore.GREEN+f"Start Get smart keys products")
            sleep(5)
            product_category_smart_keys()
            print(Fore.GREEN+f"Start Get smart touch panel products")
            sleep(5)
            product_category_smart_touch_panel()
            print(Fore.GREEN+f"Start Get speakers products")
            sleep(5)
            product_category_speakers()
            print(Fore.GREEN+f"Start Get systems audio products")
            sleep(5)
            product_category_systems_audio()
            sleep(5)
            print(Fore.GREEN+f"Down! Time : {now}")
            print(Fore.RED+"get product in 24h")

            sleep(86400)
    except Exception as ex:
        print(Fore.RED+f"Error Info: {ex}")
get_all_product()