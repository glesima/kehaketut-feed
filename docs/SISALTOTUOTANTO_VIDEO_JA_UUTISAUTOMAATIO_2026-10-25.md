# Kehä-Ketut: uutisten, otteluvideoiden ja somejulkaisujen automaatio
**Toteutussuunnitelma 25.10.2026. Tämä ei tarkoita, että alla luetellut uudet integraatiot olisivat jo käytössä.**

## 1. Tavoite ja lähtötilanne

Yksi helppo tapa toimittaa uutisaihe, ottelutulos, harjoituskuva tai MP4-video. Tekoäly rakentaa siitä tavallisen seuran uutisen, kuvituksen, somekuvatekstin ja/tai lyhyen ottelukoosteen. Käyttäjä/valmentaja hyväksyy sisällön ennen julkaisua. Julkaisuja ei lähetetä vääriin Facebook-/Instagram-tileihin.

**Nykyisin jo käytössä**:
- Yhdistysavaimen verkkosivut ja julkinen Uutiset-arkisto, kolmen uusimman uutisen korttinosto GitHub-syötteestä.
- GitHub Actions / Python rajatusti seuraa oikeaa BoxerBase-seuraa neljä kertaa vuorokaudessa; uudet kilpailut eivät vielä löydy kattavasti.
- Instagram @kehaketut:n Juicer-kuvavirta verkkosivulla.
- Metricool-brändi Riihimäen Kehä-Ketut (ID 7632678), yhteydet Facebook-sivulle 160875127258478 ja Instagramiin @kehaketut; Facebook-korttivirran erillinen tietosyöte.
- YouTube-kanava on seuran mukaan olemassa, mutta sitä **ei ole yhdistetty Metricool-brändiin**. Kanavan URL/omistus/oikeudet pitää varmistaa, ei arvata.
- BoxRec on poistettu eikä kuulu suunnitelmaan.

**Tämän suunnitelman prioriteetti:** vähentää hallituksen ja valmentajien toistuvaa editointi- ja julkaisutyötä, säilyttää oikeat faktat ja juniorien kuvien julkaisuluvat.

## 2. Sisääntulo: yksi kanava uutisille, yksi isoille kuville/videoille

### Tekstit ja pienet kuvat

Seuran julkinen yhteysosoite on nykyisin `riihimaenkehaketut@gmail.com`. Tätä voidaan käyttää sisältövihjeiden vastaanottamiseen, **jos yhdistyksen sähköpostitilin ylläpitäjät antavat siihen oikeudet**; nykyistä käyttäjän henkilökohtaista Gmail-liitosta ei oleteta samaksi tiliksi.

Lähettäjä lisää aiheen:
- `[RKK-UUTINEN]` – harjoituskuuluminen / kurssi / kokous / tiedote.
- `[RKK-KILPAILU]` – osallistuminen, kilpailun paikka ja ajankohta, valmentajan vahvistamat osallistujat.
- `[RKK-KUVA]` – 3–5 harjoituskuvaa, joihin on julkaisuluvat.

Viestissä riittävät tapahtuma, päivämäärä, paikka, osallistujat ja mitä voidaan julkaista. Tekoäly valmistelee valmiin tekstin ilman keksittyjä tuloksia. Edistynyt ratkaisu käsittelee vain luotettujen lähettäjien viestit ja merkitsee muut tarkistettaviksi.

### Pitkät otteluvideot ja suuremmat tiedostot

Suositeltu reitti on *yksityinen Dropbox-kansio + erillinen Dropbox File Request -lähetyslinkki*. Hallituksen/valmennuksen jäsen voi lähettää videot linkin kautta ilman yhteisen tallennustilin kirjautumistunnuksia. Dropbox-yhteys on saatavilla, mutta **kansiota ja lähetyslinkkiä ei ole luotu**: kohdepolku ja linkin luominen vahvistetaan erikseen, ettei mitään avointa vastaanotto-osoitetta synny ilman lupaa.

Tiedostot jaetaan tiloihin `incoming/`, `approved/`, `private-full-bouts/`, `public-clips/` ja `archive/` (ehdotus, ei vielä luotu). YouTubeen ei lähetetä automaattisesti täysiä otteluita.

## 3. Uutisen julkaisukanava ja Yhdistysavaimen rajoite

**Vahvistettu Yhdistysavain-toiminto:** `Uutiset → Lisää uutinen`; uutiset voi ajastaa ja niistä voi tarjota RSS-syötteen. Suoraan sähköpostilla tapahtuvaa natiiviartikkelin julkaisu-API:a ei ole varmistettu tai löydetty Yhdistysavaimen dokumentaatiosta. Tätä ei saa luvata.

**Vaihe 1, pienin työmäärä:** sähköpostiviesti / kuvapaketti -> tekoälyn toimitettu valmis uutisluonnos -> ylläpitäjä julkaisee yhden kerran Yhdistysavaimessa -> automaattinen kolmen uutisen etusivunosto toimii jo nykyisellä GitHub-syötteellä. Tiedon keskitetty virallinen uutisarkisto säilyy.

**Vaihe 2, vaihtoehtoinen aidosti automaattinen etusivujulkaisu:** hyväksytty sähköpostiuutinen luodaan suoraan Github Pages -pohjaiseen omaan uutisvarastoon. Nykyinen etusivun uutiswidget voi yhdistää sen Yhdistysavaimen julkiseen uutisarkistoon, deduplikoida ja järjestää. Tällöin Yhdistysavaimen alkuperäinen `/uutiset/`-arkisto **ei päivity automaattisesti**, ellei myöhemmin toteuteta erillistä sallittua kirjoitusreittiä. Valinta tehdään tietoisesti: ei rikota kahden uutisarkiston johdonmukaisuutta.

Julkaisun tilat: `received`, `drafted`, `needs_facts`, `approved`, `published`, `rejected`. Uutisen kirjoittajalle selkeät lähetys- ja palautemallit, mutta ei salaista hyväksyntätokenia sähköpostin aiheessa.

## 4. BoxerBase -> automaattinen kilpailu- ja ottelu-uutinen

### Kilpailua ENNEN
1. Löydä uusi tapahtuma oikean seuran julkisista ja sallituista BoxerBase-tiedoista (määrittely: `AUTOMAATTISET_OTTELUT_2026-10-25.md`).
2. Erota avoin ilmoittautuminen, valmentajan vahvistama osallistuminen, vahvistettu ottelupari ja julkinen ottelulista.
3. Jos lähde ei yksiselitteisesti vahvista seuran lähtijöitä, valmentaja Tomi saa lyhyen tarkistusluonnoksen. **Älä ilmoita nimiä arvauksena.**
4. Valmistele lyhyt ennakkouutinen: kilpailun nimi, päivä, paikkakunta, seuran ilmoittamat osallistujat ja lähde. Julkaistaan vain hyväksynnällä.

### Kilpailun JÄLKEEN
1. Lisää etusivun tuloskortit ilman hyväksyntää vain varmistetuille julkisille voitoille/tappioille (nykyisen tulosyötteen periaate).
2. Luo yhdestä tapahtumasta yksi lyhyt uutisluonnos: ottelijoiden nimet, painoluokat vain jos todettu lähteessä, vastustajat, lopputulokset, päivämäärä ja lähdelinkki.
3. Älä tee yhtä uutista jokaisesta ottelusta tai duplikaattia julkaisukorjauksista. Jos tulos myöhemmin muuttuu, ilmoita korjauksesta ja päivitä olemassa oleva luonnos / julkaisu.
4. Ei automaattista facebook-/instagram-julkaisua ilman hyväksyntää. Jos muutama ottelu puuttuu, raportti merkitään keskeneräiseksi.

## 5. Videosisältö: valmennuksen arkisto ja julkinen markkinointisisältö erikseen

### Valmennuksen arkisto
- Täydet MP4-ottelut valmennuksen suljettuun Dropbox-kansioon, joka ei ole yleisölle jaossa.
- YouTuben `Unlisted` ei ole yksityinen: linkin saanut voi jakaa sen. Jos YouTubeen tuodaan täysiä otteluita, `Private` ja nimetty pääsy; parempi käyttää seuran erikseen hallittua yksityistä arkistoa.
- Taltiointiin ja jakoon tarvittavat oikeudet tarkistetaan; varsinkin alaikäisten kilpailijoiden kuvaoikeudet.

### Julkinen 20–40 sekunnin ottelu- tai kilpailukooste
1. Materiaalin vastaanotto (esimerkiksi 1–3 videotiedostoa kilpailusta).
2. AI analysoi lyhyitä kohtauksia ja ehdottaa 4–8 lyhyttä näyttävää segmenttiä. Pitkistä videoista arvio voi olla epätarkempi, joten suosi ensin 1 ottelua / tiedosto ja päävalmentajan nopeaa valintaa.
3. Valmennukselle merkittävä täysi ottelumateriaali EI mene julkaisuun. Älä näytä pitkiä yhtenäisiä eriä, toistuvia taktisia heikkouksia, sparritaktiikoita tai valmentajan ohjeita.
4. Alkuun 2–3 sekunnin logo/otsikko; 3–5 lyhyttä toimintapätkää; väliin tunnelma-/huoltokuvaa; lopussa ottelun virallinen tulos, jos se on todella tarkistettu.
5. Tekninen leikkaus tehdään deterministisesti FFmpegillä: 1080×1920 (9:16), tarvittaessa 1080×1350 (4:5) valokuvajulkaisu, tekstitykset, tilastokortit, brändivärit #B91C2B, #171A1F, #FFFFFF ja seuran logo.
6. Ihminen hyväksyy leikkeet, reiluuden ja kuvaoikeudet ennen julkaisua. Ei tekoälyn luomia tekaistuja iskuja, väärää ottelutulosta tai sekoitettuja vastustajia.
7. Eri musiikkiresurssit: Instagram-Reeliin Meta/Metricoolin käyttöön sallima musiikki; YouTubeen YouTube Audio Library tai erikseen monikanavaiseen käyttöön lisensoitu musiikki. Älä siirrä Instagramissa lisättyä lisenssimusiikkia sellaisenaan YouTubeen.
8. Julkaistaan Metricoolista Instagramiin, Facebookiin ja YouTubeen. YouTube-kanava tulee ensin yhdistää seuran olemassa olevaan Metricool-brändiin.
9. YouTuben lyhyiden videoiden remix-asetukset kannattaa tarkistaa, ja pitkien otteluiden julkaisun oletus on ei julkinen.

**Pilotin onnistuminen:** 2 otteluvideota -> 1 hyväksytty noin 30 sekunnin Reels/Shorts-sisältö, 1 soveltuva kansikuva, 2–3 alustakohtaista kuvatekstiä. Tavoite on minimoida käyttäjän aktiivinen editointiaika, ei luvata tiettyä valmistumisaikaa. Ensimmäisessä pilotissa ei tehdä automaattista lähetystä.

## 6. Instagramin säännölliset harjoituskuvat

1. Hallituksen jäsen ottaa harjoitusillasta 3–5 laadukasta kuvaa; kuvissa olevien henkilöiden, etenkin alaikäisten, julkaisuun on seuran ohjeiden mukainen lupa.
2. Lähettää kuvat samaan sisältövastaanottoon; kohde `[RKK-KUVA]` sekä päivämäärä.
3. Automaatio tarkistaa peruslaadun, pystyasettelun, kohtuullisen valaistuksen ja mahdolliset kaksoiskuvat, valitsee 1–4 parasta sekä tekee seuran väreihin sopivan kohtuullisen otsake-/kuvagrafiikan.
4. AI tuottaa 1–3 lauseen luontevan suomenkielisen tekstin (ei ylitsepursuavaa markkinointikieltä), mahdollisen paikkamerkinnän, 2–4 relevanttia hashtagia.
5. Metricooliin syöttö ja hyväksyntä; Instagram voi julkaista Reelsin äänellä Metricoolin käyttöön sallitusta musiikkikirjastosta, kun yhteys tapahtuu Facebookin kautta. Tavallisiin kuviin ei lisätä musiikkia väkisin.
6. Juicer tuo varsinaisen Instagram-julkaisun nykyiselle seuran sivustolle omalla päivityssyklillään. Nettisivun HTML-koodia ei muokata.
7. Pienin laadukas tahti: yksi harjoituskuuluminen viikossa / kilpailukooste kilpailun jälkeen. Parempi muutama hyvä julkaisu kuin päivittäinen heikkolaatuinen automaattiviestintä.

## 7. Metricool-kanavien tila ja mahdollisuudet (tarkistettu 25.10.2026)

Yhdistetty brändi: **Riihimäen Kehä-Ketut**, Metricool ID 7632678.
- Facebook: sivu 160875127258478, yhdistetty.
- Instagram: @kehaketut, yhdistetty.
- YouTube: **ei yhdistetty** kyseiseen Metricool-brändiin; seuran kanavan nimeä / tunnistetta ei ole varmistettu.
- Metricoolin ajastimessa voi rajata oikeat tileille lähetettävät julkaisut ja kirjoittaa erillisen teksti-/videoversion kanavaa kohti.
- Metricoolissa on sisäänrakennettu kuva-/videoeditori ja mahdollisuus ajastaa Reels-videoita Metan sallimalla musiikilla, kun Instagramin yhteys on muodostettu Facebookin kautta.
- YouTube Shortsien ajastus on tuettu kanavan yhdistämisen jälkeen.
- Metricool RSS Autolist voi tuoda Yhdistysavaimen uutis-RSS:n automaattisesti postausjonoon. **Add disabled posts** sallii aloittaa hyväksyttävistä ehdotuksista, ei suoraan hallitsemattomasta autopostauksesta. Asetusten saatavuus riippuu tilauksesta.
- Metricoolin varsinaiset reviewer-/approvalSystem-työnkulut voivat vaatia Advanced-/Custom-tilausta. Ilmaisversion perusluonnosta / käsin hyväksyttävää julkaisua voi käyttää alkuun.

Lähteet: 
- https://help.metricool.com/schedule-and-post-on-instagram-6b6q5
- https://help.metricool.com/how-to-add-audio-to-your-instagram-reels-from-metricool-2o2ks
- https://help.metricool.com/schedule-and-publish-on-youtube-gof0k
- https://help.metricool.com/edit-images-and-videos-while-scheduling-your-content-wputz
- https://help.metricool.com/how-to-link-an-rss-feed-to-an-autolist-ank6m
- https://ohjeet.yhdistysavain.fi/kotisivut/osiot/uutislista/
- https://support.google.com/youtube/answer/157177

## 8. Varmistus, tietoturva ja vastuut

- Seuran kuvaus- ja julkaisuohje / juniorien suostumukset, valmennuksen harkinta videoiden julkisuudesta.
- Kuka tahansa voi ehdottaa uutista, mutta vain hyväksytyistä lähteistä tuleva faktatieto menee tarkistusjonoon. Vältä haitallisten lähettäjien pääsy automaattiseksi julkaisijaksi.
- Tapahtumien ja ottelijoiden nimet/tulokset tarkistetaan BoxerBase-lähteen vahvistetuista tiedoista. Ilmoittautuminen ei ole sama kuin osallistuminen tai vahvistettu ottelu.
- TikTokin, YouTuben, Instagramin ja Facebookin erilaiset musiikki- ja julkaisuoikeudet tarkistetaan ennen julkaisua.
- Mitään API-salaisuuksia tai täysiä otteluvideoita ei talleteta GitHubin julkiseen `docs/`-hakemistoon.
- Vastuuroolit: hallitus/Pepe = uutiset ja ehdotukset; Tomi = ottelijoiden, kilpailujen ja taktiikkaherkkien videoiden tarkistus; tekninen ylläpito = media-ajot, tallennus, someliitännät, ajastukset ja häiriötilanteet; julkaisemisesta vastaava henkilö = lopullinen hyväksyntä.
- Toteutuksessa auditoitava kirjaus: kuka lähetti, mistä lähteestä tiedot tulivat, kuka hyväksyi, milloin julkaistiin, mitä alustaa käytettiin.
- Ei automaattista julkaisemista muiden henkilökohtaisten/yritysten kanavien kautta. Varmista tilien tunnisteet joka julkaisuajossa.

## 9. Tekninen toteutusjärjestys

**P0 – valmis tehtäväksi seuraavaksi**
1. Nykyisen BoxerBase-event discoveryn parannus ja virallisen tuloksen luotettava ilmestyminen etusivulle (erillinen määrittely: `docs/AUTOMAATTISET_OTTELUT_2026-10-25.md`).
2. Yhdistysavaimen RSS käyttöön, mikäli uutisen tekijät haluavat automaattiset somenostot; Metricool RSS Autolist -testi vain Kehä-Kettujen brändillä, uusilla posteilla `disabled`-tila.
3. Määritetään videon julkaisukäytäntö ja valmennuksen hyväksyntä sekä yhdistetään oikea seuran YouTube-kanava Metricooliin. Tilien hallintaan tarvitaan käyttäjän kirjautuminen.

**P1 – ensimmäinen sisältöautomaatiopilotti**
4. Kun käyttöoikeudet on vahvistettu, luo Dropbox File Request -lähetyslinkki videoille ja kuville ja tee `incoming`-hakemisto yksityiseen tilaan.
5. Yksi pilottitapahtuma: kaksi raakavideota -> automaattinen kohokohtien ehdotus -> FFmpeg-kokoonpano -> visuaalinen hyväksyntä -> Metricool-luonnos Instagram/Facebook/YouTube-kanaville.
6. Sisältöviestin muoto (Gmail) -> tekoälyn uutisluonnos -> tarkistus -> nykyinen Yhdistysavain-uutisen julkaisu.

**P2 – myöhempi automatisointi**
7. Saapuvan Gmail-/tiedostosyötteen seuranta ja hyväksymispolku; estä julkiset julkaisut luvattomista lähteistä.
8. Vaihtoehtoinen GitHub Pagesin oma uutisvarasto, jos halutaan todellinen sähköposti -> etusivun julkaisu ilman Yhdistysavaimen editoria. Selkeä tieto siitä, etteivät nämä artikkelit automaattisesti mene Yhdistysavaimen omaan uutisarkistoon.
9. Virallisen BoxerBase-kilpailun ajastettu ennakkouutisluonnos sekä toteutuneiden ottelujen yhteinen jälkiuutis- ja somekoosteluonnos, vain luotettavin lähtein.
10. Uusien kuvien säännöllinen RKK-julkaisuprosessi; materiaalin automaattinen laatu-/käyttölupaseula ja eri kanavien formaattien varmistus.
11. Mittaa tuotetut julkaisut, käyttäjän aktiivinen aika / julkaisu, tiliriskit ja hyväksymisprosentti. Paranna tästä, älä kytke sokkona täydellistä autopostausta.

## 10. Julkaisemisen hyväksymiskriteerit

- 1 sähköpostiviestistä muodostuu virheetön uutisluonnos ilman keksittyjä faktoja.
- 1 pilottiotteluvideosta 20–40 sekunnin kooste, jonka Tomi tai muu valmentaja hyväksyy eikä se vuoda täyttä ottelua.
- Seuran juniorien kuvia ei julkaista ilman asianmukaisia lupia.
- Yhtä kilpailun virallista tulosta käytetään vain kerran eikä hävinnyttä tulosta luoda; korjaus päivittää olemassa olevan merkinnän.
- Sisältöä ei julkaista vahingossa väärän henkilökohtaisen tai yrityksen somen tilille.
- Valmennuksen hyväksynnän jälkeen julkaisu onnistuu sivuille / Metricooliin / YouTubeen ilman 3–4 eri palvelussa toistuvaa manuaalista tekstinsyöttöä.

**Tämä dokumentti on suunnitelma. Gmailista Yhdistysavaimeen suoraa automaattista natiiviartikkelijulkaisua, YouTube-yhdistämistä tai videoiden automaattista leikkausputkea EI ole vielä tehty.**
