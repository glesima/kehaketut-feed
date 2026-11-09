## 9.11.2026 – julkaisun ja analytiikan eriaikaisuus

Kehä-Kettujen Facebook- ja Instagram-postaukset Ilon Suomen mestaruudesta julkaistiin Metricoolin mukaan `PUBLISHED`-tilassa 9.11.2026 klo 17.00 Europe/Helsinki, mutta Metricoolin someanalytiikan julkaisuhaut palauttivat samana iltana edelleen vanhoja rivejä tai tyhjän listan. `docs/facebook.json` ja `docs/instagram.json` korjattiin varmennetusta julkaisutiedosta (brändi 7632678, Facebook-sivu 160875127258478, Instagram kehaketut ja suorat julkiset linkit), **ei uudesta postauksesta**. Syötteeseen otetaan vain jo `PUBLISHED`-tilaiset, julkisen osoitteen sisältävät julkaisut; luonnoksia, ajastettuja tai epäonnistuneita ei hyväksytä.

Instagramin PUBLISHED-vastauksen kuvan julkinen media-URL voi olla `https://static.metricool.com/planner/YYYYMM/<brand>-file-<id>.jpeg`, ei vain Metan CDN. Kuvavälimuisti sallii nyt tarkasti rajatun HTTPS Metricool-mediaosoitteen ja tarkistaa kuvan JPEG-sisällön ennen atomista talletusta. Jos kuva ei ole saatavilla, aiemmat kuvat ja uusimman julkaisun linkki säilyvät; sivulla näytetään neutraali `KUVA`-ruutu.

Jatkossa automaatiot tarkistavat julkisen Metricool `PUBLISHED`-tilan tarvittaessa erillisenä varmistettuna lähteenä, jos Analytics ei heti sisällä julkaisuja, eivätkä saa poistaa vahvistettua postausta yhden viiveellisen analytiikkahaun takia. Uudet nettisivun kortit ovat enintään kolme uusinta per kanava. Uutta Facebook- tai Instagram-julkaisua ei luoda tässä tietosynkronoinnissa.

# Tiiviit Instagram- ja Facebook-nostot ilman Juiceria

## Toteutus

`social-embed.js` v4 näyttää molempien kanavien kortit samassa DOM:ssa. Sama Yhdistysavaimen `rkk-social-unified`-elementti ja script-osoite säilyvät. Enintään kolme uusinta yksilöllistä julkaisukorttia per kanava. Instagramissa pieni kuva, julkaisupäivä, lyhyt otsikko/ote ja linkki alkuperäiseen julkaisuun. Facebookissa päivämäärä, julkisen tekstin ensimmäinen kappale otsikkona, tiivis tekstikatkelma ja julkaisulinkki. Ei uutta sisällöntuotantoa tai muutoksia alkuperäisiin somejulkaisuihin.

## Tasakorkuiset palstat — v4-korjaus

V3 käytti Facebookille 530 px:n iframe-kehystä. Lapsikehys mittasi documentElement.scrollHeightin ja lisäsi 15 px; emoelementti lisäsi vielä 12 px. Mitta riippui kehysikkunan korkeudesta, ei vain varsinaisista korteista, joten alareunaan jäi tyhjää tilaa. Pelkkä molempien palstojen venyttäminen tähän korkeuteen ei korjaisi syytä.

V4 poistaa Facebook-kehyksen ja korkeuden postMessage-kuuntelijan tästä yhteisestä someosiosta. Molemmat tietolähteet haetaan suoraan samoista julkisista JSON-tiedostoista. Desktopissa ulkoruudukko venyttää palstat yhtä korkeiksi; molemmissa sama otsikko/lista/alalinkki-rakenne ja listan kolme tasakorkuista korttiriviä. Ei kiinteää palsta- tai iframe-korkeutta. Alle 701 px:n näytöillä palstat ovat allekkain ja korkeus seuraa omaa sisältöä. Molemmissa on Katso lisää -linkki ja samanmuotoinen lähde/päivitysrivi.

Vanha `facebook.html` säilyy erillisenä yhteensopivuussivuna, mutta etusivun uusi someosio ei lataa sitä. Muut iframe-upotukset (esimerkiksi BoxerBase) eivät muutu. Historiallista sisältöä tai syötetiedostoja ei poisteta. Facebook- ja Instagram-ylläpitotehtävät sekä niiden tietosopimukset säilyvät.

`docs/instagram.json` sisältää vain jo julkista @kehaketut-sisältöä; `docs/facebook.json` vain jo julkisen sivun sisältöä. Brändi 7632678, Instagram-käyttäjä kehaketut ja Facebook-sivu 160875127258478 tarkistetaan selaimessa. Julkaisupäivä on syötteen päivä, ei tekstissä mainittu kilpailupäivä. Tekstit lisätään textContentilla. Linkit rajataan HTTPS Instagram-/Facebook-osoitteisiin ilman userinfoa tai erikoisporttia. Kanavat latautuvat riippumatta toisistaan: toisen häiriö ei peitä toista. Ei Juicer-scriptiä, automaattista videolatausta, sisäistä vieritystä tai loputonta syötettä.

## Esikatselukuvat

`cache_instagram_thumbnails.py` noutaa korkeintaan kuusi jo julkista JPEG-esikatselua Metricoolin palauttamista Meta-CDN-osoitteista. Sallitut CDN:t, HTTPS, kokoraja, JPEG-tunnisteet, uudelleenohjausten tarkistus ja atominen tallennus. Tämä on rajattu siirtotarkistus, ei täydellinen kuvatiedostodekoodaus. Aiempi onnistunut kuva säilyy lataushäiriössä. Selaimen kuva tulee vain omasta `assets/instagram/<julkaisukoodi>.jpg`-polusta. Jos kuva puuttuu, kortti näyttää neutraalin Reel/kuva-tunnisteen ja toimivan julkaisulinkin, ei rikkinäistä kuvasymbolia. V4-asettelukorjaus ei korvaa tai muuta lähdekuvia.

Pages-työnkulku tekee kuvahaun ennen julkaisua ja säilyttää kuvat versionhallinnassa. Julkaisulista päivitetään erillisellä Metricool-yhteyttä käyttävällä ajastetulla ylläpitotehtävällä. Pelkkä Pages-cron ei löydä uusia Instagram-julkaisuja: se päivittää jo listattujen julkaisujen kuvat ja julkaisee tiedostot. Uuden listan päivittyminen riippuu Metricool-datan saatavuudesta ja ajastetun tehtävän onnistumisesta.

## Instagram-päivityssopimus (ennallaan)

Kirjoita vain `docs/instagram.json` nykyisen SHA:n suojauksella. Lue oikean brändin Instagram reels- ja posts-analytiikka; älä käytä luonnoksia, tarinoita tai toisen tilin aineistoa. Yhdistä, poista duplikaatit, järjestä uusin ensin ja säilytä enintään kuusi. Näkymä näyttää enintään kolme. `title` ja `excerpt` ovat lyhyitä uskollisia otteita julkisesta kuvatekstistä, eivät uusia tulosväitteitä. `image_source` on palvelun julkinen kuvalinkki, ei API/OAuth-tunnus. Ei henkilökohtaisia tilitietoja tai analytiikkalukuja julkiseen syötteeseen.

Jos haku epäonnistuu tai ei anna luotettavaa aineistoa, pidä viimeinen hyvä syöte. Älä tyhjennä listaa yksittäisen virheen vuoksi. Vahvistetusti poistettua julkaisua ei säilytetä nostona. Tämä tehtävä ei luo uusia somejulkaisuja.

## Testauksen rajaus

V4: `node --check docs/social-embed.js` ja 24 paikallista Chromium-skenaariota läpäisty. Leveydet 1600/1200/900/768/701/700/390/320 px; desktopissa panelien, korttirivien ja alalinkkien korkeus/sijainti mitattu, alareunan tyhjä tila rajattu normaaliksi paddingiksi. Toistuvat leveysmuutokset eivät kasvata osiota. Lisäksi riippumattomat syötevirheet, väärä brändi kummallakin kanavalla, turvattomat linkit/duplikaatit/HTML-teksti, rikkinäinen kuva, puuttuva mount, uudelleenalustus, eri julkaisumäärät ja suurempi tekstikoko testattu. Testi käyttää synteettistä sisältöä ja pikkukuvaa; se ei ole live-Yhdistysavain-selaintesti. Ajettava testi: `qa/check_social_layout.py` (Playwright/Chromium, erillinen vapaaehtoinen kehitystesti, ei uusia tuotantoriippuvuuksia).

V3:n historialliset testit: 12 kuvavälimuistin yksikkötestiä ja selaintestit 1200/768/390/320 px. Facebook oli siinä vain staattinen testisisältö, joten oikean iframe-korkeusvirheen toistuminen jäi tuolloin havaitsematta. Tämä rajaus korjataan v4:ssä poistamalla kehysriippuvuus.

Juicer-tilausta ei ostettu tai peruttu. Seuran vanha sisältö, Facebook-automaatio, uutiset ja media-vastaanotin säilyvät ennallaan.
