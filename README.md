# Pilot: Rapportering til SSB basert på SAF-T

_Dette er en pilot for å forenkle rapporteringen til SSB. Den dekker i første omgang rapportering til [varehandelsindeksen](https://www.ssb.no/varehandel-og-tjenesteyting/varehandel/statistikk/varehandelsindeksen). Istedenfor å finne de relevante omsetningstallene manuelt, inneholder denne siden kode som kan hente de relevante tallene fra en oppdatert SAF-T-fil._

## Bakgrunn
Det nordiske samarbeidsprosjektet [Nordic Smart Government and Business](https://nordicsmartgovernment.org/) ser på en rekke ulike måter å forenkle hverdagen til bedrifter i Norge. Et av områdene er [Open Accounting and Simplified Reporting](https://nordicsmartgovernment.org/open-accounting). Denne piloten er en del av dette arbeidet.

## SAF-T og potensialet for forenkling
Bokføringsloven stiller krav om å kunne levere bokføringsdata på et standardisert, elektronisk format. Som resultat av det kravet kan alle digitale bokføringssytem generere en SAF-T-fil med detaljerte data fra bokføringssystemet. Statistisk sentralbyrå (SSB) har analysert SAF-T og konkludert med at svært mye av den rapporteringen bedrifter må gjøre til SSB, er spørsmål etter informasjon som enten finnes i eller kan utledes av dataene i en SAF-T-fil. Forutsetningen er at bokføringen er korrekt og oppdatert for den aktuelle tidsperioden.

For SSB kan det være aktuelt å kreve at bedrifter som er pålagt rapportering, sender dem SAF-T-filen, slik at SSB dermed kan trekke ut de relevante tallene selv. Dette kan trolig forenkle prosessen med å rapportere til SSB. Men det er også ulemper med en slik løsning. De to viktigste er kanskje at bedriftene vil måtte begynne å gi fra seg mye mer detaljert informasjon om hvem som kjøper og selger hva og til hvilke priser enn de gjør idag, og at en slik tilnærming bare vil fungere for SSB, som har lovhjemmel til å be om informasjon fra bedrifter. Det siste er viktig fordi vi vet det er mange aktører som i forskjellige situasjoner har bruk for lignende informasjon som for eksempel omsetning eller overskudd, og det vil være verdifullt for bedriftene å kunne dele det, på en enkel, og maskinlesbar måte, men uten å måtte dele alle detaljene.
