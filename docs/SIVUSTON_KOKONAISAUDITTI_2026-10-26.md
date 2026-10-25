# Kehä-Ketut – koko sivuston katselmus ja premium-uudistuksen eteneminen
**26.10.2026 · kehaketut.fi**

Tämän työn tavoite on yhdenmukainen puna-valko-grafiitti-ilme jokaiselle julkiselle sivulle. Sivusto on Yhdistysavaimessa; uusi yhteinen tyylitiedosto, mallisivut ja julkisten sivujen auditointi ovat GitHubissa. Varsinaisia Yhdistysavaimen tekstejä ei voi tästä reposta päivittää suoraan.

**Todentamisen rajaus:** Julkinen navigaatio ja tärkeimmät sisältösivut käytiin läpi. Osa alasivuista ei auennut hakupalvelun välimuistista; niiden yksityiskohtia ei arvailla. GitHub Actionsiin lisätty bounded public crawl täydentää listauksen enintään 90 julkisen sivun osalta, robots.txt:tä kunnioittaen. Ajo- ja virheloki on varmistettava julkaisun jälkeen.

## P0 – havaittu korjattava sisältö

| Osio | Löydös | Toimenpide |
| --- | --- | --- |
| Etusivu | Kilpailuista Ajankohtaista-osioon puuttunut puna-harmaa viiva | CSS-korjaus docs/news-embed.js -tiedostossa valmisteltu. Tarkista julkaisun jälkeen |
| Etusivu, vanha teksti | Vanhemmassa verkkohakukopiossa esiintyi 25.8.2026 kurssi-ilmoitus, mutta 59 sivun uusin tarkistus ei enää löytänyt tätä päivää. Sen sijaan väärä väite tulosten automaattisen päivityksen puuttumisesta löytyi edelleen | Älä poista jo poistunutta kurssia uudestaan. Korjaa vanha automaatioväite alkuperäiseen Yhdistysavaimen osioon sisältötasolla, ei vain CSS-piilotuksella |
| Yhteystiedot | Kaupungin nimi kirjoitettu "Rihimäki" | Korjaa Riihimäeksi vasta, kun postitusosoite on varmistettu |
| Hinnastot ja lisenssit | Kolmessa harjoitusryhmässä vanhoja lisenssiohjeita, hinnastoja ja viittaus vuoteen 2018 | Varmista kauden 2026–2027 hinnat, SuomiSport-lisenssit, maksutavat, harjoitusajat Tomilta, Pepeltä ja ryhmävastaavilta |
| Kilpailijasivut | Vain viisi henkilöesittelyä, osin vanhoja ottelumääriä; BoxerBase-profiileja yhdeksän | Tarkista aktiiviset urheilijat ja sarjat valmentajalta. Käytä live-kortteja, älä arvaa koko otteluhistoriaa |

## Julkisen sivurakenteen tarkastettavat alueet

### Etusivu
Hyväksi koettu tumma yläkuva/hero, kilpailukortit, kolmen uutisen nostot, urheilijakortit sekä yhteinen Instagram/Facebook ovat nykyisen designin esikuvia. Puuttuva erotin palautetaan. Vanhat etusivun HTML-kappaleet pitää siivota Yhdistysavaimessa, jotta ne eivät jää teksti-indeksointiin.

### Harjoittelu
Pääsivulla on kolme ryhmää. Valmis uusi ryhmäkorttipohja: embed/YHDISTYSAVAIN_HARJOITTELU_PREMIUM.html.

- Miesten kuntonyrkkeily: esittely, hinnat ja lisenssit, harjoitusajat.
- Naisten kuntonyrkkeily: esittely, hinnat ja lisenssit, harjoitusajat. Julkisen aikataulusivun tiistai 18–19.30; sunnuntai ehdollisena. Tarkista ennen uusimista.
- Kilpailija-/Harrastajaryhmä: esittely, hinnat ja lisenssit, harjoitusajat sekä Tuloksia-arkisto.

Kolmen ryhmän maksut ovat erisuuruisia. Sivut kertovat miesten/naisten jäsenmaksusta 30 € ja 80 €/kausimaksusta sekä vanhoista 15/45 € lisensseistä. **Näitä ei vahvistettu nykyisiksi hinnoiksi**. Uudessa sivupohjassa ei siksi kovakoodata hintoja.

### Kilpailijat
Pääsivun viisi esittelyä: Ilo Grönroos, Kosmo Grönroos, Maarjo Ranne, Josias Ndikumana ja Daniela Taskila. Kaikilla oma sivu, vanhoja otteluselostuksia/videoita ja eräillä vanhentuneita tilastoja. Rakenne yhtenäiseksi: esittely, mahdollinen luvallinen kuva, ajantasainen lähdekortti, vanhat ottelukertomukset historian osana. Älä väitä automaattisesti kaikkea BoxerBase-listan dataa täydelliseksi.

### Uutiset
Yhdistysavaimen oma arkisto säilyy. Etusivulla kolme uusinta toimituksellista uutista ja hyväksytyt kohderyhmät (kilpa, juniorit, kunto, naiset, koko seura). Vanhoja 2025 ja 2026 kurssi- sekä vuosikokousuutisia ei julkaista uudelleen someen.

### Seura
Uusi premium-yleissivun linkkikorttipohja: embed/YHDISTYSAVAIN_SEURA_PREMIUM.html. Säilytettävät alasivut: Seuran historia, Hall of Fame ja viisi henkilöä (Kalevi Tervalahti, Markku Sarasto, Niko Bitter, Pasi Silvennoinen, Risto Grönroos), Martti Markuksen muistolle, Seuran SM-mitalistit ja TUL-mestarit sekä Seuravaatteet. Vanhat tulos- ja henkilösaavutukset säilytetään muuttumattomina, esitystä kehitetään.

### Historiallinen Tuloksia-arkisto
Kilpailuryhmän Tuloksia-haarassa 18 erillistä vuosittaista sivua 2002–2019. Vuoden 2002 sisältö tarkistettu; se on yksityiskohtaista seuran historiaa. Ei poisteta eikä virheellisesti yhdistetä nykyiseen BoxerBase-hakuun. Valmis moderni vuosivalikko: embed/YHDISTYSAVAIN_TULOSARKISTO_PREMIUM.html. Suositus: linkki arkistoon Seura-osiosta, nykyiset kilpailut eri osiossa.

### Liity mukaan
Jäseneksi liittymisen natiivi Yhdistysavain-lomake säilytetään koskemattomana. Yläpuolelle parempi ohje ja Harjoittelu-linkki: embed/YHDISTYSAVAIN_LIITY_PREMIUM.html. Maksuhinnastoa ei monisteta liittymissivulle, vaan ajantasaiset hinnat pysyvät ryhmäsivuilla.

### Yhteystiedot
Esitetään yksi selkeä yhteystietokokonaisuus: virallinen seurasähköposti, puheenjohtaja, valmentajat, sali, postitusosoite ja kartta. Varmista yhteyshenkilöt ja korjaa kirjoitusvirhe. Sisällöntuotantopostia kehaketut.aineisto@gmail.com ei käytetä jäsenasioiden osoitteena.

### Sivuston yleisasetukset
Alatunnisteen someikonit lisätään vain vahvistettuihin seuran kanaviin (Facebook, Instagram ja myöhemmin YouTube/TikTok). Sivukohtaiset metaotsikot, metakuvaukset ja metakuvat tarkistetaan etenkin Harjoittelu-, Kilpailijat-, Liity mukaan-, Seura- ja Yhteystiedot-sivuilta. Saavutettavuus, kuva-alt-tekstit, lomakkeiden toimivuus, mobiili, sivuston nopeus ja kontrasti testataan julkisessa esikatselussa.

## Yhteinen toteutus

**GitHubin design system:** docs/rkk-premium-site.css. Siinä on brändisävyt, typografia, premium-kortit, CTA, erotin, tabularakenne ja historiallinen vuosivalikko.

**Yhdistysavain Plus / Premium:** Lisää koodieditorin head-osioon yksi linkki:
<link rel="stylesheet" href="https://glesima.github.io/kehaketut-feed/rkk-premium-site.css?v=1">
Koodieditorin nykyinen saatavuus pitää tarkistaa käyttäjän Yhdistysavain-tililtä, ja koodi tulee ottaa käyttöön varovasti.

**Yhdistysavain Start:** Ulkoasu → Tyylit säätää globaalit fontit, värit, rivivälit, osiovälit ja painikkeet. Erilliset HTML-osat voivat ladata saman CSS:n lokaalisti. Start ei tarjoa koodieditoria.

**Tämä dokumentti ei väitä, että Yhdistysavaimen kaikki sivut on jo korvattu.** Vanhojen tekstien toimittaminen ja julkaiseminen tapahtuvat Yhdistysavaimen ylläpidossa vaiheittain. Automaattinen julkinen sivuinventaario tuottaa tarkemman URL-kohtaisen raportin erilliseen tiedostoon docs/SIVUSTON_AUTOMAATTINEN_AUDITTI.md.

Lähteet: https://www.kehaketut.fi/ , https://www.kehaketut.fi/harjoittelu/ , https://www.kehaketut.fi/kilpailijat/ , https://www.kehaketut.fi/yhteystiedot/ , https://ohjeet.yhdistysavain.fi/kotisivut/ulkoasu/ , https://ohjeet.yhdistysavain.fi/kotisivut/osiot/koodieditori/ .
