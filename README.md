# Pilot: Rapportering til SSB basert på SAF-T

_Dette er en pilot for å forenkle rapporteringen til SSB. Den dekker i første omgang rapportering til [varehandelsindeksen](https://www.ssb.no/varehandel-og-tjenesteyting/varehandel/statistikk/varehandelsindeksen). Istedenfor å finne de relevante omsetningstallene manuelt, inneholder denne siden kode som kan hente de relevante tallene fra en oppdatert SAF-T-fil._

## Bakgrunn
Det nordiske samarbeidsprosjektet [Nordic Smart Government and Business](https://nordicsmartgovernment.org/) ser på en rekke ulike måter å forenkle hverdagen til bedrifter i Norge. Et av områdene er [Open Accounting and Simplified Reporting](https://nordicsmartgovernment.org/open-accounting). Denne piloten er en del av dette arbeidet.

## SAF-T og potensialet for forenkling
Bokføringsloven stiller krav om å kunne levere bokføringsdata på et standardisert, elektronisk format. Som resultat av det kravet kan alle digitale bokføringssytem generere en SAF-T-fil med detaljerte data fra bokføringssystemet. Statistisk sentralbyrå (SSB) har analysert SAF-T og konkludert med at svært mye av den rapporteringen bedrifter må gjøre til SSB, er spørsmål etter informasjon som enten finnes i eller kan utledes av dataene i en SAF-T-fil. Forutsetningen er at bokføringen er korrekt og oppdatert for den aktuelle tidsperioden.

### Hvorfor ikke bare overføre hele SAF-T-filen til SSB
For SSB kan det være aktuelt å kreve at bedrifter som er pålagt rapportering, sender dem SAF-T-filen, slik at SSB dermed kan trekke ut de relevante tallene selv. Dette kan trolig forenkle prosessen med å rapportere til SSB. Men det er også ulemper med en slik løsning. De to viktigste er kanskje at bedriftene vil måtte begynne å gi fra seg mye mer detaljert informasjon om hvem som kjøper og selger hva og til hvilke priser enn de gjør idag, og at en slik tilnærming bare vil fungere for SSB, som har lovhjemmel til å be om informasjon fra bedrifter.

Hvor mye detaljer bedrifter skal gi fra seg om kjøp og salg er et vanskelig spørsmål. Høsten 2021 var det et tema for en høring fra Skatteetaten - [Forslag om opplysningsplikt for salgs- og kjøpstransaksjoner](https://www.skatteetaten.no/rettskilder/type/horinger/opplysningsplikt-salgs-og-kjopstransaksjoner/). Noen av motforestillingene er utfordringene knyttet til personvern, bedriftshemmeligheter og også nasjonal sikkerhet.

Når det gjelder det andre punktet, at overføringen av hele SAF-T-filen er løsning som bare vil fungere for SSB og eventuelt andre etater som har eller kan skaffe lovhjemmel, så kan man spørre seg om det egentlig er et problem. Det offentlige har tradisjonelt laget rapporteringsløsninger spesielt for rapportering til offentlig sektor -- med stor suksess. Et veldig godt eksempel er Altinn.

Men det som har blitt tydeligere de siste årene er at bedrifter opplever en stor -- og viktigere -- stadig økende rapporteringsbyrde til _andre_ enn offentlige etater. Så selv om vi forenkler rapporteringen til det offentlige, blir verdien "spist opp" av stadig økende krav til å rapportere til kunder, banker, investorer og andre aktører. Hvis vi da lager løsninger for rapportering til det offentlige som _bare_ kan benyttes for rapportering til det offentlige, får løsningene begrenset verdi for bedriftene.

### Det grønne skiftet forsterker næringslivets etterspørsel etter rapportering
Trenden med økt etterspørsel etter rapportering fra andre aktører i næringslivet, blir tydelig forsterket av det grønne skiftet, og oppmerksomhet rundt flere forhold enn bare de finansielle, f.eks. "Environment - Social - Governance", "People - Planet - Profit" eller "trippel bunnlinje". Men også for det finansielle er det en svakhet at årsregnskap gir et såpass forsinket bilde av situasjonen, så det er ofte behov for mer oppdatert informasjon.

For et konkurransedyktig næringslivet er det derfor viktig at vi klarer å finne løsninger for å forenkle rapportering som kan brukes i så mange situasjoner som mulig, uavhengig av om det er SSB, Skatteetaten, Brønnøysundregistrene, banken, investoren, den potensielle kunden, forsikringsselskapet, huseieren eller andre som trenger tilgang til oppdaterte data.

### Siste måneds omsetning - for SSB og huseiere
For å gjøre det helt konkret; vi vet at mange bedrifter må levere omsetningstall for siste måned til SSB, som del av varehandelsindeksen. Samtidig vet vi at mange bedrifter i de samme bransjene, leier lokaler der husleien delvis styres av omsetningen. Da ønsker huseier det samme tallet. Det finnes sikkert også andre aktører som ber om det samme, som f.eks. bransjeorganisasjoner som utarbeider statistikk for bransjen.

Den administrative byrden ved å finne frem og rapportere er like stor i begge tilfellene, så om vi lager en løsning som automatiserer rapporteringen til SSB, men ikke løser behovet for rapportering til huseieren, har vi bare halvert den administrative byrden. Men hvis løsningen kan gjenbrukes for begge rapporteringene, kan vi fjerne tilnærmet 100 %. Og selv om næringslivet kanskje har tilstrekkelig tillit til SSB at de ville godtatt å levere komplette SAF-T-filer, så vil de neppe alle være like komfortable med å brette ut detaljene om seg selv på den måten til huseieren.

## Hvordan virker piloten?
Piloten er laget som en nettside, som for tiden er gjort tilgjengelig fra Github, slik det fremgår av domenenavnet i nettadressen: https://nordicsmartgovernment.github.io/statistikkpilot_ssb/

Når brukeren åpner nettsiden lastes det ned en komplett Python-applikasjon, som kjører i nettleservinduet. Når brukeren velger en fil, leser Python-applikasjonen filen og konverterer den til et format som gjør det mulig å bruke det kjente Python-verktøyet for dataanalyse, Pandas, for å filtrere de relevante transaksjonene, og summere disse.

### Fullt innsyn i logikken
Siden all Python-koden som er spesifikk for applikasjonen er lastet ned i nettleseren, er den også tilgjengelig for å inspiseres av brukeren. På den måten kan man kontrollere logikken og det er helt transparent hva som skjer, dersom man har et minimum av kunnskap om Python. Noe av koden finnes i kildekoden til selve nettsiden (index.html), mens noe av koden finnes i egen python-filer, som main.py og saft2dataframe.py.

### Ingen sending/overføring av detaljene i SAF-T-filen
Også de som ikke kjenner Python kan få bekreftet at dette er en nettside som ikke sender SAF-T-filen til et eksternt nettsted: Etter å ha åpnet nettsiden, kan brukeren skru på flymodus/trekke ut nettverkskabelen, og sånn sett forsikre seg om det ikke er noen muligheter for å kommunisere over internett. Likevel vil det fortsatt være mulig å åpne en SAF-T-fil som er lagret lokalt, og analysere den (steg 1 til 3 på nettsiden).

### Begrensninger
De to største begrensningene i løsningen slik den er nå, er for det første stegene _før_ piloten, det vil si tilgjengeliggjøring av en SAF-T-fil fra bokføringssystemet.

Tilgang til SAF-T-filen er ikke standardisert og innebærer antagelig flere manuelle steg i bokføringssystemet. I en ideell løsning vil det være mulig å aksessere denne direkte fra rapporteringsnettsiden. Det kunne antagelig latt seg gjøre dersom nettsiden ble levert fra bokføringssystemet.

Det andre er overføring av omsetningstallene til mottakeren. Per nå er det bare en illustrasjon på at tallene kan overføres til et eksternt API, men det finnes ikke idag noe API som er satt opp til å ta imot disse tallene, og her må det også finnes en måte å få bekreftet avsenderen av tallene. Dette kan kanskje løses ved at tallene rapporteres til et nettsted, som så ber brukeren om å autentisere seg og bekrefte dem før innsending.

## Teknologi
Selv om Python og Pandas er blant de mest kjente og brukte verktøyene for analyse av data, så er det tradisjonelt utfordrende å få et python-miljø opp å kjøre på en PC eller mobiltelefon. Men våren 2022 ble PyScript annonsert, og selv om dette er i en tidlig fase, fungerer det allerede som mekanisme for å kjøre Python i en nettleser, og samtidig kunne interagere med nettleseren for funksjoner som å åpne fil, og kjøre kode når f.eks. brukeren klikker på en knapp.

Siden det har lav terskel for å testes ut, er dette verktøyene som er valgt for piloten. Det utelukker ikke at andre teknologivalg kan være aktuelle for fremtidige løsninger. Det viktige er at 1) koden må kjøres _hos brukeren_, og ikke være avhengig av at brukeren sender fra seg de detaljerte dataene, og 2) det må være teknologi som er utbredt, gratis/uten bindinger, som gjør at den kan tas i bruk av og inspiseres av mange.

