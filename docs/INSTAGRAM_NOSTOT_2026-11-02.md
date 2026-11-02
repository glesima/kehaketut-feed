# Tiiviit Instagram-nostot ilman Juiceria

## Toteutus

`social-embed.js` v3 korvaa aiemman Juicer-upotuksen. Sama Yhdistysavaimen `rkk-social-unified`-elementti ja script-osoite säilyvät. Enintään kolme uusinta yksilöllistä julkaisukorttia: pieni kuva, päivämäärä, lyhyt otsikko/ote ja linkki alkuperäiseen Instagram-julkaisuun. Ei automaattista videolatausta, sisäistä vieritysikkunaa tai loputonta syötettä. Facebook-kehys säilyy rinnalla; puhelinleveydellä palstat ovat allekkain. Instagram-julkaisuja ei poisteta eikä tilejä muuteta.

`docs/instagram.json` sisältää vain jo julkista @kehaketut-sisältöä. Brändi 7632678 ja käyttäjätunnus tarkistetaan sekä päivityksessä että selaimessa. Julkaisupäivä ei ole tekstissä mainittu kilpailupäivä. Selaimessa tekstisisältö lisätään textContentilla, ei HTML:nä. Linkit rajataan Instagramin p/reel/tv-osoitteisiin.

## Esikatselukuvat

`cache_instagram_thumbnails.py` noutaa korkeintaan kuusi jo julkista JPEG-esikatselua Metricoolin palauttamista Meta-CDN-osoitteista. Sallitut CDN:t, HTTPS, kokoraja, JPEG-tunnisteet, uudelleenohjausten tarkistus ja atominen tallennus. Tämä on rajattu siirtotarkistus, ei täydellinen kuvatiedostodekoodaus. Aiempi onnistunut kuva säilyy lataushäiriössä. Selaimen kuva tulee vain omasta `assets/instagram/<julkaisukoodi>.jpg`-polusta. Jos kuva puuttuu, kortti näyttää neutraalin Reel/kuva-tunnisteen ja toimivan julkaisulinkin, ei rikkinäistä kuvasymbolia.

Pages-työnkulku tekee kuvahaun ennen julkaisua ja säilyttää kuvat versionhallinnassa. Julkaisulista päivitetään erillisellä Metricool-yhteyttä käyttävällä ajastetulla ylläpitotehtävällä. Pelkkä Pages-cron ei löydä uusia Instagram-julkaisuja: se päivittää jo listattujen julkaisujen kuvat ja julkaisee tiedostot. Uuden listan päivittyminen riippuu Metricool-datan saatavuudesta ja ajastetun tehtävän onnistumisesta.

## Päivityssopimus

Kirjoita vain `docs/instagram.json` nykyisen SHA:n suojauksella. Lue oikean brändin Instagram reels- ja posts-analytiikka; älä käytä luonnoksia, tarinoita tai toisen tilin aineistoa. Yhdistä, poista duplikaatit, järjestä uusin ensin ja säilytä enintään kuusi. Näkymä näyttää enintään kolme. `title` ja `excerpt` ovat lyhyitä uskollisia otteita julkisesta kuvatekstistä, eivät uusia tulosväitteitä. `image_source` on palvelun julkinen kuvalinkki, ei API/OAuth-tunnus. Ei henkilökohtaisia tilitietoja tai analytiikkalukuja julkiseen syötteeseen.

Jos haku epäonnistuu tai ei anna luotettavaa aineistoa, pidä viimeinen hyvä syöte. Älä tyhjennä listaa yksittäisen virheen vuoksi. Vahvistetusti poistettua julkaisua ei säilytetä nostona. Tämä tehtävä ei luo uusia somejulkaisuja.

## Testauksen rajaus

Paikallisesti 12 kuvavälimuistin yksikkötestiä läpäistiin. Chromium-testit 1200, 768, 390 ja 320 px: kolme korttia, ei vaakaylivuotoa tai duplikaatteja, ei videosoitinta tai Juicer-pyyntöjä. Lisäksi syötteen virhe, väärä brändi, rikkoutunut kuva, turvaton linkki ja HTML-tekstin turvallinen näyttö testattu. Layout-testi käytti synteettisiä esikatselukuvia ja Facebookin staattista testisisältöä: tämä ei yksin ole oikean Yhdistysavain-sivun live-selaintesti. Pages-ajon ja oikeiden kuvien tulos varmennetaan julkaisun jälkeen.

Juicer-tilausta ei ostettu tai peruttu. Seuran vanha sisältö, Facebook-automaatio, uutiset ja media-vastaanotin säilyvät ennallaan.
