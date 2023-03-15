import asyncio
import io
import json

import pandas as pd
from js import FileReader, document
from pyodide.ffi import create_proxy
from pyodide.http import open_url
from request import request  # request-funksjonen fra pyscript, siden 'requests' mangler
from pyscript import Element

# egne moduler
from saft2dataframe import gle2df
        
  
# Koden for å lese fil er hentet fra her:
# https://github.com/amrrs/pyscript-file-uploader/blob/main/index.html

saft_innhold = ""  # global variabel, teksten fra saft-fila
saft = pd.DataFrame()  # global variabel
omsetning = pd.DataFrame() # global variabel
orgnr: str = ""  #
år: int = 0
måned: int = 0
min_måned: int = 0
maks_måned: int = 0

MÅNEDER = {'Januar': 1,
 'Februar': 2,
 'Mars': 3,
 'April': 4,
 'Mai': 5,
 'Juni': 6,
 'Juli': 7,
 'August': 8,
 'September': 9,
 'Oktober': 10,
 'November': 11,
 'Desember': 12}


def hent_saft_innhold() -> io.StringIO:
    if saft_innhold == "":
        print('Du må først velge en lokal fil')
        return None
    else:
#        print(f'Her er saft_innhold: {saft_innhold[:100]}')
        return io.StringIO(saft_innhold)

def lag_månedsalternativer(min_måned: int, maks_måned: int) -> str:
    '''returnerer en liste med de aktuelle månedene som brukeren kan velge
    TODO: Bytte fra tall til månedsnavn'''
    global MÅNEDER
    åpning = '<datalist id="måneder">\n'
    avslutning = '</datalist>'

    måneder_liste = ''
    for i in range(maks_måned)[min_måned-1:]:
         måneder_liste += f'<option value="{list(MÅNEDER.keys())[i]}"/>\n'
    
    return åpning + måneder_liste + avslutning

def oppdater_månedsvelger(år: int, min_måned: int, maks_måned: int) -> None:
    '''Endrer månedsvelgeren basert på hvilke data som finnes i SAF-T-filen.'''
    el = Element('a2')
    el.element.innerHTML = f'''
    <h1>Steg 2: Velg rapporteringsperiode</h1>
    <p>År: {år}</p>
    <p>Velg måneden det skal rapporteres for:</p>
    <label for="maaned_velger">Velg måned:</label>
    <input type="text" id="maaned_velger" name="maaned_velger" required="true"
       list="måneder">
    
    {lag_månedsalternativer(min_måned, maks_måned)}
'''
    


def read_complete(event) -> pd.DataFrame:
# event is ProgressEvent

    # del 1 er å lese fila og transformere til pandas df
    content = document.getElementById("content")
    global saft_innhold, saft, orgnr, år, min_måned, maks_måned
    saft_innhold = event.target.result

    saft, orgnr = gle2df(hent_saft_innhold())

    # del 2 er å forberede velger for rapporteringsperiode
    if len(år_liste := saft['PeriodYear'].unique()) != 1:
        raise()
    år = år_liste[0]
    min_måned = saft['Period'].min()
    maks_måned = saft['Period'].max()
    oppdater_månedsvelger(år, min_måned, maks_måned)
    #gjentar oppsettet for å oppdage endringer i måned:
    oppsett_for_å_oppdage_valgt_måned()

    # del 3 er å informere brukeren og åpne neste steg
    el = Element('resultat_a1')
    el.write('Filen er lest, gå til neste steg')

    el = Element('a2')
    el.add_class('visible')
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


def prosesser_måned(x):
    global måned, MÅNEDER
    måned = MÅNEDER[document.getElementById('maaned_velger').value]
    Element('a3').add_class('visible')
    Element('a3').remove_class('hidden')
    

def oppsett_for_å_oppdage_valgt_måned():
    valgt_måned = create_proxy(prosesser_måned)
    e_måned = document.getElementById("maaned_velger")
    e_måned.addEventListener("change", valgt_måned, False)


oppsett_for_lesing_av_lokal_fil()
oppsett_for_å_oppdage_valgt_måned()