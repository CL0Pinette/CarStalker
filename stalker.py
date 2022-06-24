#!/usr/bin/env python3

import requests
import json
import argparse
import re
import urllib3

from rich.console import Console
from rich.table import Table
from itertools import cycle
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

url_plate = "https://www.vroomly.com/api/v1/vehicleselecter/vehicle/from_plate/?setInSession=true&plate="

url_vin = "http://fr.vindecoder.pl/"

url_proxy = "https://free-proxy-list.net/"

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plate", help="Licence Plate")
parser.add_argument('-v','--vin',help="VIN of the car")

args = parser.parse_args()

# Set the vars
plate      = (args.plate)
vin        = (args.vin)

# setup proxies

r = requests.get(url_proxy)
soup = BeautifulSoup(r.text,"html.parser")

proxies_list = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", soup.find("textarea", {"class": "form-control"}).contents[0])

proxy_pool = cycle(proxies_list)

if plate is not None:
    if not re.fullmatch("[a-zA-Z]{2}-[0-9]{3}-[a-zA-Z]{2}", plate):
        temp = plate.split("-")
        if len(temp) == 1 and len(temp[0]) == 7:
            plate = f"{temp[0][0:2]}-{temp[0][2:5]}-{temp[0][5:7]}"
        elif len(temp) == 2 and len(temp[0]) + len(temp[1]) == 7:
            if len(temp[0]) == 5:
                plate = f"{temp[0][0:2]}-{temp[0][2:5]}-{temp[1]}"
            elif len(temp[1]) == 5:
                plate = f"{temp[0]}-{temp[1][0:3]}-{temp[1][3:5]}"
            else:
                console.print("[red][-][/red] BAD PLATE !")
        else:
            console.print("[red][-][/red] BAD PLATE !")

    r = requests.get(f"{url_plate}{plate}")
    j = json.loads(r.text)
    if type(j["plate"]) == str:
        console.print(f"[green][+][/green] Found info for {plate}")
        for key, value in j.items():
            console.print("[green]\t[+] [/green]", end="")
            print(key, end=": ")
            print(value)
        console.print()
        flag = True
        while flag or "daily limit" in r.text or r.status_code != 200:
            proxy = next(proxy_pool)
            try:
                r = requests.get(f"{url_vin}{j['vin']}", proxies={"http": proxy, "https": proxy}, timeout=7, verify=False)
                flag = False
            except KeyboardInterrupt:
                exit()
            except :
                flag = True
        soup = BeautifulSoup(r.text, "html.parser")
        tables_list = soup.find_all("table")

        console.print()
        table = Table(show_header=True, title="Fabricant", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[0].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Analyse du numéro de VIN", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[1].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Informations de base", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[2].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Spécification du véhicule", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[3].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Équipement standard", header_style="bold magenta")
        table.add_column("Option")
        for r in tables_list[4].find_all("tr"):
            if len(r.find_all("span")) == 0:
                value = r.td.contents[0]
                table.add_row(value, end_section=True)
            else:
                value = r.td.span.contents[0]
                table.add_row(value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Équipement optionnel", header_style="bold magenta")
        table.add_column("Optiom")
        for r in tables_list[5].find_all("tr"):
            if len(r.find_all("span")) == 0:
                value = r.td.contents[0]
                table.add_row(value, end_section=True)
            else:
                value = r.td.span.contents[0]
                table.add_row(value, end_section=True)
        console.print(table)

    else :
        if "🤔" in j["plate"][0]:
            console.print("[red][-][/red] We cannot find any informations for this plate")
        else:
            console.print(f"""[red][-][/red] {j['plate'][0].replace("nous ne pouvons pas encore calculer d'estimation pour votre", 'We cannot find more information about this')}""")

if vin is not None:
    if len(vin) != 17:
        console.print("[red][-][/red] BAD VIN !")
    else:
        flag = True
        while flag or "daily limit" in r.text or r.status_code != 200:
            proxy = next(proxy_pool)
            try:
                r = requests.get(f"{url_vin}{vin}", proxies={"http": proxy, "https": proxy}, timeout=7, verify=False)
                flag = False
            except KeyboardInterrupt:
                exit()
            except :
                flag = True
        soup = BeautifulSoup(r.text, "html.parser")
        tables_list = soup.find_all("table")

        console.print()
        table = Table(show_header=True, title="Fabricant", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[0].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Analyse du numéro de VIN", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[1].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Informations de base", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[2].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Spécification du véhicule", header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for r in tables_list[3].find_all("tr"):
            key = r.th.contents[0]
            value = r.td.contents[0]
            table.add_row(key, value)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Équipement standard", header_style="bold magenta")
        table.add_column("Option")
        for r in tables_list[4].find_all("tr"):
            if len(r.find_all("span")) == 0:
                value = r.td.contents[0]
                table.add_row(value, end_section=True)
            else:
                value = r.td.span.contents[0]
                table.add_row(value, end_section=True)
        console.print(table)

        console.print()
        table = Table(show_header=True, title="Équipement optionnel", header_style="bold magenta")
        table.add_column("Optiom")
        for r in tables_list[5].find_all("tr"):
            if len(r.find_all("span")) == 0:
                value = r.td.contents[0]
                table.add_row(value, end_section=True)
            else:
                value = r.td.span.contents[0]
                table.add_row(value, end_section=True)
        console.print(table)
