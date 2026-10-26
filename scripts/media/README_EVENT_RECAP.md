# Kehä-Ketut – automaattinen kilpailupäivän yhteiskooste (pilotti)

**Tavoite:** 2–12 luotettua MP4-ottelutallennetta → samaan kilpailuun kohdistettu yksi 9:16 MP4, kansikuva, kolme alustakohtaista tekstiä ja koneellisesti arvioitu julkaisukelpoisuus **ilman yksittäistä manuaalista hyväksyntävaihetta silloin, kun kaikki ennalta sovitut ehdot täyttyvät**.

**Tämä pilotti ei vielä julkaise eikä lataa mediaa Metricooliin.** Aiempi `build_reel.py` toimii yksittäisen ottelun kuvaamisen ja aikaleimojen kontrolloidussa versiossa; tämä uusi `event_recap.py` on itsenäinen monen videon kokoaja ja käyttää nykyistä `suggest_clips.py`-analyysimoduulia. Itse julkaisu vaatii erillisen, **yksityisessä ympäristössä** ajettavan mediatallennuksen ja julkaisun orkestroijan. Älä aja yksityistä MP4-materiaalia julkisessa GitHub Actions -työnkulussa tai GitHub Pagesissa.

## Syöttö

- Yhden kilpailupäivän MP4-tiedostot **yksityisessä** kansiossa. Tiedoston nimi ei yksin todista ottelijaa, tulosta eikä käyttöoikeutta.
- `event_manifest.json` määrittää kilpailun `event_id`-tunnisteen ja jokaiselle tiedostolle `bout_id`-tunnisteen sekä punaisen/sinisen kulman nimet, sarjan, ikäluokan ja nimettävän seuranyrkkeilijän. Esimerkki: `scripts/media/example_hameenlinna_event_20261024.json` (tiedostonimet ovat esimerkkejä eivätkä automaattisesti olemassa).
- **Erillisestä luotetusta lähteestä** rakennettu virallinen tuloslista: vaadi täsmälleen sama tapahtuma-ID, bout-ID ja ottelijapari. Älä yhdistä BoxerBasen rinnakkaisia seuraprofiileja nimen perusteella.
- Yksityisen järjestelmän oikeusrekisteri, jossa on kilpailunjärjestäjän videolupa ja kullekin bout-ID:lle ja alkuperäisen MP4-tiedoston SHA-256:lle sidottu julkaisuoikeus. Juniorilta edellytetään lisäksi tallennettua huoltajan/edustajan julkaisulupaa ja oikeaa suostumuspolkua. **Älä julkaise itse oikeustodisteita.**
- Pysyvä, tapahtuma-ID:llä avainnettu julkaisuloki / deduplikointilukko.

## Aja ilman uutta käsin valittua leikevalintaa

```bash
python3 scripts/media/event_recap.py \
  --manifest /private/event_manifest.json \
  --media-dir /private/raw \
  --logo /private/Keha-Ketut-logo-header-HD.png \
  --output-dir /private/ready \
  --official-results /private/official_results.json \
  --rights-records /private/rights_records.json \
  --ledger /private/publication_ledger.json
```

Riippuvuudet: Python 3.10+, Pillow, `ffmpeg` ja `ffprobe`, `scripts/media/suggest_clips.py` samassa hakemistossa.

Tämä työkalu **ei käsittele uskotulla tavalla syötteen `approved:true`-kenttää**, vaan lukee oikeustiedot erillisestä etukäteen varmennetusta yksityisestä rekisteristä. `--preflight-only` valmistaa tekstit ja julkaisun tarkistusraportin **ilman MP4-videon renderöintiä**. Jos tapahtuman jossakin ottelussa automaattisesti havaittu aktiivinen osuus on liian vähäinen, se jättää koko materiaalin poikkeustilaan eikä poista ottelijaa hiljaa pois videolta.

Tulosteet:

- `RKK_event_recap_draft.mp4`: yhteinen 9:16, H.264/AAC-yhteiskooste. Kehävideo näytetään leveänä tummalla taustalla **ilman rajauskatkoja**; alaosa jätetään somekäyttöliittymille. Alku- ja lopputunnus sekä jokaisen ottelijan nimikortti tulevat automaattisesti.
- `kansikuva.png`: sama seuran brändi.
- `social_captions.json`: kolme eri tekstiversiota, ilman tulosten keksimistä.
- `publication_handoff.json`: linkitettävät paikalliset media-artefaktit, yhtenäinen `event_id`, kanavat, **`auto_publish_ready`** ja estojen syyt. Julkaisun kuluttavan palvelun pitää tehdä riippumaton varmistus ennen lähettämistä; tiedostoa ei saa pitää allekirjoitettuna julkaisulupana.

## Vihreä automaattinen julkaisupolku

1. Vain seuran luotetun vastaanoton tiedostot; ei raakaa internetistä tullutta automaattista julkaisuvaltuutusta.
2. Tapahtuma- ja ottelutunnisteet vastaavat luotettavan lähteen julkisia tulostietoja.
3. Jokaiselle MP4:lle tiedostosisältöön sidottu julkaisuoikeus. Juniorit eivät siirry julkiseen jakeluun ilman erillistä luparekisteritietoa.
4. Jokaisesta ottelusta löytyy riittävät, selkeästi rajatut aidot toimintajaksot. Automaattinen liikepistemäärä **ei** väitä mittaavansa osumia tai paremmuutta.
5. Videon ja tekstin tekninen tarkistus + täsmällisesti määritelty julkaisutunniste, ei tuplajulkaisuja.
6. Vasta tämän jälkeen **yksityinen media- ja julkaisupalvelu** saa toimittaa saman hyväksytyn MP4:n Meta/Instagram/YouTube-kanaviin Metricoolin välityksellä. Ei tarvitse joka videolle uutta ihmisklikkausta silloin kun pysyvät ehdot toteutuvat.
7. Jos jokin ehto ei toteudu, **HOLD / poikkeus**, ei automaattista julkaisua.

### Liiketoiminta- ja integraatioraja

- Metricool MCP toimii myös Free-tilauksessa, mutta yhteys näkyy tällä hetkellä **ChatGPT-istunnossa**, ei automaattisesti paikallisessa Python-skriptissä. Palvelinajoon tarvitaan erikseen konfiguroitu valtuutettu MCP-asiakas, esimerkiksi jatkuvasti toimiva oma yksityinen palvelin ja OAuth, sekä videoiden vakaa/tilapäinen julkaisukanavien hyväksymä tallennus ennen lähettämistä. Tämä vaatii todellisen integraatio- ja julkaisukokeen.
- Metricoolin suora HTTP REST API on Advanced/Custom-tilauksen ominaisuus; sitä ei pidä luvata Free-tilauksessa.
- Metricool Free: yhteensä **20 toteutunutta julkaisutapahtumaa kuukaudessa**, ja yksi samasta videosta Facebookiin, Instagramiin ja YouTubeen tehty julkaisu käyttää **kolme** tätä kiintiötä. Mittaa kiintiö ja mahdollinen kanavakohtainen virhe jokaisessa ajossa.
- Facebook/Instagram/YouTube-julkaisukanavat kuuluvat oikeaan Kehä-Ketut-brändiin `7632678`, mutta uusia postauksia ei tehdä, jos sama tapahtuma on jo julkaistu samaan kanavaan.

## Tämänhetkisen Hämeenlinnan esimerkin faktat

Virallinen lähde: https://www.boxerbase.com/e/d6jfSSe5nRpe/matches . Tapahtuman ottelut 16 Simo Pöyry – Lauri Mäenpää, 19 Gleb Simanov – Sampo Paananen ja 33 Kosmo Grönroos – Khaled Samkanai näkyvät rinnakkaiseen seuraprofiiliin merkittyinä. `bout_id`-tunnisteet ovat **kilpailun ottelunumerot**, eivät takeita sisäisestä BoxerBase-ID:stä. Kosmo on tapahtumassa B-juniorien sarjassa, joten alaikäiselle oletetaan tiukempi käyttöoikeuspolku. Älä tee tosiasiallista kolmikon koostetta ennen kuin kaikki tähän tarkoitukseen tarkoitetut videot ovat käsittelyssä.

## Suoritetut testit

`python -m unittest discover -s tests -p 'test_event_recap.py' -v` – 8 yksikkötestiä, yksi erillinen aito ffmpeg-smoke test (aktivoidaan `RKK_RUN_VIDEO_SMOKE=1`). Kokeessa kaksi geneeristä synteettistä MP4-tiedostoa yhdistettiin yhdeksi videoksi ja todettiin tulos oikean kokoiseksi. Lisäksi käyttäjän aiemman yhden 6 min ottelutallenteen kanssa valmistui noin 9 s **automaattisesti leikkauskohdat valitseva esikatselu**, jota ei julkaistu. Tämän vaiheen tavoite on teknisen käsittelyn toistettavuus, ei täysin valmis toimituksellinen urheiluvideo.
