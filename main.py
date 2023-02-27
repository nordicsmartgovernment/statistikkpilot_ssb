import asyncio
import io
import json

import pandas as pd
from js import FileReader, document
from pyodide import create_proxy
from pyodide.http import open_url
from request import request  # request-funksjonen fra pyscript, siden 'requests' mangler
from pyscript import Element

# egne moduler
from saft2dataframe import saft2dataframe
        
  
# Koden for å lese fil er hentet fra her:
# https://github.com/amrrs/pyscript-file-uploader/blob/main/index.html

saft_innhold = ""  # global variabel, teksten fra saft-fila
saft = pd.DataFrame()  # global variabel
omsetning = pd.DataFrame() # global variabel
orgnr: str = ""  #
år: int = 0
måned: int = 0

def hent_saft_innhold() -> io.StringIO:
    if saft_innhold == "":
        print('Du må først velge en lokal fil')
        return None
    else:
#        print(f'Her er saft_innhold: {saft_innhold[:100]}')
        return io.StringIO(saft_innhold)


def read_complete(event) -> pd.DataFrame:
# event is ProgressEvent

    content = document.getElementById("content")
    global saft_innhold, saft, orgnr
    saft_innhold = event.target.result
#    print(f'Har oppdatert saft_innhold: {saft_innhold[:100]}')


    saft, orgnr = saft2dataframe(hent_saft_innhold())
#    print(f'''har oppdatert saft dataframe, med innholdet i saft-fila som begynner med {saft_innhold[:100]}
#
#          Variabelen saft har følgende kolonner: {saft.columns}''')

    #document.getElementById('a2').style.display = 'block'  >> erstattet med pyscript-funksjonaliteten under, med element
    el = Element('resultat_a1')
    el.write('Filen er lest, gå til neste steg')

    el = Element('a2')
    el.remove_class('hidden')


async def process_file(x):
    fileList = document.getElementById('saftfil').files

    for f in fileList:
        # reader is a pyodide.JsProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)

        #console.log("done")

        reader.onload = onload_event

        reader.readAsText(f)

        return  # lurer litt på hvorfor det er return inne i for-løkken ... kanskje en typo av meg?


def oppsett_for_lesing_av_lokal_fil():
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("saftfil")
    e.addEventListener("change", file_event, False)


def prosesser_år(x):
    global år
    år = document.getElementById('aar_velger').valueAsNumber


def prosesser_måned(x):
    global måned
    måned = document.getElementById('maaned_velger').valueAsNumber
    

def oppsett_for_å_oppdage_valgt_måned_og_år():
    valgt_år = create_proxy(prosesser_år)
    valgt_måned = create_proxy(prosesser_måned)

    e_år = document.getElementById("aar_velger")
    e_måned = document.getElementById("maaned_velger")

    e_år.addEventListener("change", valgt_år, False)
    e_måned.addEventListener("change", valgt_måned, False)
    



oppsett_for_lesing_av_lokal_fil()
oppsett_for_å_oppdage_valgt_måned_og_år()