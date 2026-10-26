> **YHTEINEN UUSI SUUNTA 26.10.2026:** Käyttäjä nimenomaisesti haluaa **poistaa jokaisen yksittäisen videon ennakkotarkistuksen normaalilta julkaisupolulta**, jolloin etukäteen valtuutettujen videoiden julkaiseminen etenee automaattisesti. Alkuperäinen alla kuvattu manuaalinen hyväksyntä säilyy vain tarvittaessa poikkeuspolkuna (puuttuvat kuva-/musiikkioikeudet, alaikäisen lupa, ristiriitaiset tulokset, huono tekninen laatu). Tekniset perustat [PR #18](https://github.com/glesima/kehaketut-feed/pull/18) ja jatko [issue #19](https://github.com/glesima/kehaketut-feed/issues/19). Automaattisen livejulkaisun jatkuva yksityinen palvelin ei ole vielä käytössä; ei saa väittää että pelkkä PR laukaisisi postauksia. 

# Kehä-Ketut – raakavideosta julkaisuvalmiiksi Reels/Shorts-videoksi

**26.10.2026.** Käyttäjän 26.10. kysymykseen "miten raakavideosta tulee hieno käsitelty video ja järkevä postaus". Tämä dokumentti on toteutusmäärittely ja pilotin ohje, **ei väite, että automaattinen tuotantoputki olisi jo käytössä**.

## Päätökset ja todellinen nykytila

- Kohdekanavat ovat oikean seuran **Facebook, Instagram @kehaketut ja käyttäjän vahvistama oikea YouTube-kanava** Metricool-brändissä **7632678**. **TikTok myöhemmin**.
- Facebookin uutisten RSS Autolist **`RKK | Seurauutiset | Facebook`** on käyttäjän mukaan tallennettu ja ajastettu **tiistaisin ja torstaisin klo 18 Europe/Helsinki**. Autolist on enabled; RSS-historian tuonti OFF, uusi sisältö disabled, Repeat OFF. Ensimmäisen uuden artikkelin todellinen disabled-jonotesti vielä tekemättä.
- RSS-lista **ei leikkaa videoita eikä tuota Reel/Shorts-julkaisuja**. Videoille erillinen hyväksyttävä tuotantopolku.
- Julkinen Yhdistysavain-sivusto, GitHubin kilpailukortit ja Instagramin Juicer-upotus ovat jo käytössä erillisillä rajapinnoilla.
- Dropboxin videovastaanottokansiota/file request -linkkiä, valmiiksi ajavaa videoeditorin automaatiota, hyväksyntäbackendiä tai AI:n itsenäisesti toteuttamaa multimodaalista leikkausta **ei ole vielä otettu käyttöön**.
- Instagramin ja YouTuben toimiva kanavayhteys ei itsessään vahvista valmiita videojulkaisuja: ensimmäinen tarkistettu testijulkaisu tehdään erikseen.

## Käyttökokemus: mitä lähettäjä tekee

**Pienin paketti**: 1–3 MP4-raakavideota (mieluiten yksi ottelu per tiedosto) sekä lyhyt tapahtumatieto. Käyttäjä voi toimittaa videon suoraan keskusteluun, jos tiedostokoko sallii, tai myöhemmin yksityisen Dropbox File Request -linkin kautta. Videot eivät päädy julkiseen GitHubiin. Dropbox-kansion ja julkisen lähetyslinkin perustaminen vaatii erillisen valtuutuksen.

Videon mukana tarvittavat tiedot:
- **Aihe**: kilpailu / harjoitukset / leiri / seuran tapahtuma.
- **Milloin ja missä** tapahtui (vain varmennetut tiedot).
- **Keitä videolla on**, jos heitä saa nimetä; mikä oli kilpailun todellinen tulos, jos tulos mainitaan.
- **Kuvaajan/julkaisun käyttöoikeudet**: erityisesti alaikäiset, muut ottelijat, musiikki, kisajärjestäjän mahdolliset rajoitukset.
- **Mahdollinen toive**: painotetaanko harjoitustunnelmaa, tekniikkaa, urheilijaa vai kilpailupäivän yhteenvetoa; onko tietty aikakohta ehdottomasti mukana tai pois.

Jos tietoa puuttuu, julkaisu estetään kyseiseltä osalta ja AI:n tekstiehdotuksessa käytetään vain varmennettuja seikkoja. Älä päättele otteluvoittoa kameran hurrauksesta, henkilöiden nimeä ulkonäöstä tai kuuluvan puheen oikeaa transkriptiota pelkästä huonosta äänestä.

## Vaiheittainen prosessi ja vastuu

| Vaihe | Tekniikka / ehdotus | Tarkistus | Tuloste |
|---|---|---|---|
| 1. Vastaanotto | yksityinen media-kansio, uusi job ID, alkuperäiset tiedostot muuttumattomina | oikeudet, metadata, sala-/henkilötietojen käsittely | `INCOMING` + media manifest |
| 2. Analyysi | videon esikatselu, aikaleimat, kohtausrajat, halutessa AI scene-by-scene / puheen litterointi | nyrkkeilyssä AI ehdottaa, valmentaja vahvistaa osumat ja oleelliset hetket | 5–8 ehdokasleikkeen aikaleimat |
| 3. Käsikirjoitus | koukku → tapahtuman tunnus → 3–5 toimintaleikettä → tunnelma → loppu-CTA | ei väärää tulosta, ei taktisesti arkaluontoisia sekvenssejä | 20–40 s edit decision list |
| 4. Editointi | FFmpeg / editori: tarkka leikkaus, tarvittaessa vakautus, 9:16 rajaus, lievä värikorjaus, äänentaso, brändigrafiikka, lopputunnus | tarkista ottelijat rajauksen aikana; ei tekaistuja lyöntejä | 1080×1920 H.264 MP4 |
| 5. Grafiikka & äänet | RKK #B91C2B + #171A1F + valkoinen, logo, selkeät nimitiedot, äänet ja mahdollinen lisensoitu musiikki | oikeudet, tekstien oikeellisuus; ei epäselvän puheen keksittyjä tekstityksiä | reel-videomaster + kansikuva |
| 6. Julkaisutekstit | yksi faktalista → kolme eri kanavatekstiä ja metatiedot | tapahtumatiedot ja nimet lähteestä/valmentajalta, inhimillinen kieli | Facebook/IG/YouTube-paketti |
| 7. Hyväksyntä | **pilottina** yksityinen esikatselu ja manuaalinen tarkistus; myöhemmin oma kirjautuva hyväksyntäpalvelin | yksi nimetty hyväksyjä Gleb/Pepe/Erika; kilpailuleikkeissä valmentajan faktatarkistus, kuvaoikeus | `APPROVED` ja versioloki |
| 8. Jakelu | Metricool Planner: IG Reel, FB Reel, YouTube Short, tarvittaessa kanavakohtaiset julkaisuajat ja kuvatekstit | oikean brändin tilit ja asetukset ennen ajastusta | ajastetut julkaisut |
| 9. Seuranta | Metricoolin julkaisutilat + someanalytiikka + julkinen sivusto/Juicer | virheitä ei uudelleenjulkaista tuplana; ei suoraa automaattista Yhdistysavain-artikkelia | onnistumistiedot, tarvittaessa tarkistus |

### Yhden 30 sekunnin videon rakenne

- 0–3 s: vahvin aito kohta heti alkuun (ei välttämättä pitkä animoitu intro).
- 3–7 s: lyhyt seuran tunnus, oikea kilpailu/paikka/päivä.
- 7–23 s: 3–4 kiinnostavaa todellista toimintakohtaa.
- 23–27 s: tunnelma, joukkue tai valmentaja, jos kuvattuja henkilöitä saa julkaista.
- 27–30 s: logo ja `kehaketut.fi`, mahdollinen todellinen ja varmistettu tulosteksti.

Pystysuunta 9:16, 1080×1920, H.264 MP4 + AAC; tarvittaessa YouTubeen / valmennusarkistoon erillinen 16:9 leike, ei pakoteta vaakakuvaa huonosti keskeltä rajattuna. Kuvan alkuperäinen laatutaso ja kuvanpeitto voivat rajoittaa 9:16-leikkausta. Musiikin oikeudet tarkistetaan erikseen kanavakohtaisesti: Instagramin kirjasto ei lähtökohtaisesti anna oikeutta samaan kappaleeseen YouTubessa.

**Ei generatiivisia ihmisten liikkeitä, tuloksia, kommentteja tai osumia eikä pitkän taktisen analyysivideon julkaisemista.**

## Esimerkki julkaisupaketista – vain mallitekstit

Yhdestä hyväksytystä kilpailukoosteesta syntyy samasta faktalistasta:
- **Instagram Reel**: 1 koukku + lyhyt tapahtumakuvaus + kannustava mutta asiallinen loppu + 3–5 perusteltua hashtagia.
- **Facebook Reel**: hieman kontekstia paikalliselle yleisölle, tarvittaessa linkki seuran ajankohtaiseen uutiseen tai harjoittelusivulle.
- **YouTube Short**: hakukelpoinen otsikko alle 100 merkkiä + 1–3 virkkeen videokuvaus, event/paikka ja mahdollinen lisensoitu äänitieto.

Mallin neutraali otsikko: `Kehä-Ketut kehässä – kilpailupäivän kohokohtia`.
Mallin neutraali teksti: `Kehä-Ketut oli mukana kilpailupäivän tunnelmassa. Tässä muutama hetki kehän tapahtumista ja joukkueen matkasta. Kiitos valmentajille, järjestäjille ja kaikille mukana olleille! 🥊 #KehäKetut #Nyrkkeily #Riihimäki`.
**Korvaa mallin kilpailuviittaus ja muut väitteet vain oikeista lähdetiedoista.** Todellisessa julkaisutekstissä mainitaan nimet/tulos vain, jos ne on varmennettu ja julkaisuun hyväksytty.

## Mitä Metricool voi ja ei voi tehdä

- Metricoolin omassa editorissa voi leikata/splitata videota, rajata kuvakokoa, säätää värejä, käyttää logoa/grafiikkaa ja ajastaa FB/IG/YouTube. Se **ei automaattisesti tarkoita älykästä nyrkkeilyn kohokohtien löydintä ja valmista ammattimontaasia**. Varsinainen raakavideosta videomasteriksi -putki tehdään erillisenä.
- Metricool tukee eri kanavien tekstien ja asetusten muokkaamista erikseen.
- Metricoolin **Send for review** -hyväksyntätoiminto vaatii sen nykyohjeen mukaan **Advanced/Custom**-tilauksen. **Ei oleteta, että yhdistyksellä olisi maksullinen tilaus**. Ensimmäinen pilotti: esitarkastus yksityisesti + julkaisu vain käyttäjän nimenomaisen hyväksynnän jälkeen. Myöhempi vahva, yksilölliseen passkey-tunnukseen perustuva hyväksyntäpalvelin on dokumentoitu erikseen.
- Tätä varten ei tarvitse ottaa TikTokia käyttöön, ei myöskään Yhdistysavaimen kalliimpaa versiota.

## Toteutuksen pilotti – hyväksymisehdot

1. Ota ensimmäiseksi 1 **luvalla käytettävä raakavideo**, mielellään yksi ottelu / treeni.
2. Talteen alkuperäinen täydessä laadussa yksityisesti; tee 5–8 aikaleimattua kohokohtaehdotusta, joista valmentaja voi korjata valinnan.
3. Renderöi 20–40 sekunnin MP4, 9:16, oikea RKK-logo ja yhtenäinen ulkoasu, sekä 9:16-kansikuva.
4. Tuota kolme **erilaista** mutta samoihin faktoihin perustuvaa julkaisutekstiä: Facebook, Instagram, YouTube (+ YouTube-otsikko). Korjauksista uusi luonnosversio.
5. Esikatsele ja hyväksytä. Älä ajasta tai julkaise väärille tileille; ensimmäinen pilotti julkaistaan vasta erikseen päätettäessä.
6. Seuraa kaikkien kolmen kanavan julkaisun onnistumista ja sivuston mahdollisia näyttösyötteitä, älä väitä verkkosivun YouTube-nostoa olevan käytössä ennen sen erillistä testausta.
7. Mittaa laatu (luettavuus, leikkaus, ottelijoiden näkyvyys, oikeudet), tarvittavat ihmiskorjaukset ja tulkintavirheet ennen kuin automatisoit lisää.

Työvaiheet `RECEIVED → RIGHTS_CHECK → CLIPS_PROPOSED → EDIT_DRAFT → FACTS_AND_RIGHTS_REVIEW → APPROVED → SCHEDULED → PUBLISHED`. Muutos hyväksyttyyn videoon tai tekstiin = uusi hyväksyntä.

## Lähteet

- [Metricool: median editointi](https://help.metricool.com/edit-images-and-videos-while-scheduling-your-content-wputz)
- [Metricool: kanavakohtaiset formaatit](https://help.metricool.com/scheduling-and-posting-options-by-social-network-cwmb3)
- [Metricool: YouTube-julkaisu](https://help.metricool.com/schedule-and-publish-on-youtube-gof0k)
- [Metricool: postauksen hyväksyntä ja maksullisuus](https://help.metricool.com/how-to-send-posts-for-review-with-metricools-approval-system-yvdr0)
- [Repo: olemassa oleva suunnitelma](SISALTOTUOTANTO_VIDEO_JA_UUTISAUTOMAATIO_2026-10-25.md)
- [Repo: mediavastaanoton turvallisuus](TURVALLINEN_SISALTOVASTAANOTTO_2026-10-25.md)
