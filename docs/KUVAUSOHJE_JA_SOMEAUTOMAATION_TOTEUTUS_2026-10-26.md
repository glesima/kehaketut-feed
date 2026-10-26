# Kehä-Ketut – kilpailuvideoiden kuvausohje ja automaatioon siirtyminen

**Päivitetty 26.10.2026.** Ohje seuran hallitukselle, kilparyhmälle, valmentajille ja kuvaajille. Tämä on käytännön toimintamalli ja tuotantosuunnitelma. Yksittäisten kilpailujen kuvausluvat, alaikäisten julkaisuluvat, ottelutiedot ja julkaisupolku tarkistetaan sovituin menettelyin. Julkaisuoikeus ei synny pelkästä Dropboxiin lähettämisestä.

## 1. Todellinen lähtötilanne

- Kahden valmiin julkaisusisällön (Gleb Simanov, sekä Simo Pöyry + Kosmo Grönroos) videot ovat **julkisina Facebookissa, Instagramissa ja YouTubessa**. Kolmen kanavan julkaisuketju on siis toimivaksi osoitettu manuaalisen käyttöliittymän kautta.
- Simo/Kosmo-koosteen julkaisu 26.10.2026 klo 14.28: Facebook https://facebook.com/reel/2256449974919826 ; Instagram https://www.instagram.com/reel/De9SHpJCSff/ ; YouTube https://www.youtube.com/watch?v=6qVfWB5ft7M .
- Glebin julkaisut: Facebook https://facebook.com/reel/1123183827112227 ; Instagram https://www.instagram.com/reel/De9QLdAkr_o/ ; YouTube https://www.youtube.com/shorts/NABfEb7SoxQ .
- **Tarkennus YouTubeen:** Simo/Kosmo-video lähetettiin Metricoolista asetuksella `type=video` eikä `type=short`; 39 s 9:16 -materiaalin voi YouTube käsitellä Shortsina, mutta julkaisuasetusten on jatkossa oltava yksiselitteisesti `short`, ja oma Shorts-näkymä tarkistetaan.
- Aiempien Reelsien Instagram-julkaisuvika oli `Auto publish=OFF`: Metricool lähetti manuaalisen julkaisuilmoituksen, ei julkista Instagram-julkaisua. Uusi IG-versio julkaistiin kytkimellä ON ja on näkyvissä. Jatkossa **autoPublish=true**, eikä ilmoituksen `Sent` saa tarkoittaa onnistunutta julkista julkaisua.
- Käytössä GitHubin 3 moduulia: `scripts/media/suggest_clips.py` (liikepohjaiset ehdotukset, eivät osumien arviot), `build_reel.py --style broadcast` (yksi ottelu) ja `event_recap.py` (1–12 ottelun yhteiskooste). Vaativat vielä hallitusti toimitetut MP4:t, oikeat lähdetiedot ja oikeustarkistukset; **24/7 Dropbox → media → Metricool automaattinen julkaisu ei ole valmis**.
- Dropboxin `/RKK`-kansiossa on tällä tarkistuskerralla **vain kaksi 24.10. kilpailun MP4:tä**. Ne vastaavat Simo Pöyryn ja Kosmo Grönroosin otteluita ja on jo käytetty yhteisjulkaisuun. Niistä ei automaattisesti tehdä uusia saman sisältöisiä videoita.
- Metricool Free: **20 todellisuudessa julkaistua postausta kalenterikuukaudessa**; luonnokset eivät vie kiintiötä, ajastettujakin voi olla yli 20 mutta kuukauden aikana julkaistaan enintään 20. Sama video kolmessa verkostossa käyttää kolme julkaisua. Tarkista käyttöliittymän laskuri. Lähde: https://help.metricool.com/main-differences-between-free-and-paid-plans-bl0v9 . MCP on Free-tasolla, mutta itsenäinen pitkäikäinen taustajulkaisu ei synny ChatGPT-yhteyden olemassaolosta. Suora HTTP API vaatii korkeampaa tilausta.

## 2. Kuvaajien yhden kilpailupäivän kuvauslista

**A. Ottelun dokumentointikamera (ensisijainen, tärkein aineisto)**
1. Pyydä järjestäjän kuvauslupa, kuvaa sallitusta turvallisesta paikasta, älä estä tuomareita, huoltajia tai ottelun kulkua.
2. Vakaa jalusta tai tukeva paikka kehän sivussa/viistosti nurkasta; mieluiten hieman kehäkoroketta ylempää ja niin, että molemmat ottelijat mahtuvat kuvaan koko ajan. Älä tee jatkuvaa äkkizoomausta.
3. Kuvataan **koko ottelu yhtenäisenä tallenteena**: ottelijoiden sisääntulo tai kuulutus ennen aloitusta, kaikki erät ja mahdollinen virallinen tuloskuulutus. Älä katkaise tallennusta kesken erien.
4. Puhelin vaakaan **16:9**, mieluiten **4K, 25/50 fps** jos kuva pysyy hyvälaatuisena; muuten 1080p. Suomen sisävaloissa kokeile välkkymätön 25/50 fps ja riittävän lyhyt suljinaika. Pidä tarkennus/valotus vakaana. Älä käytä digitaalista zoomia.
5. Tarkista akku, tallennustila, linssi ja ensimmäiset 5 s ääntä/kuvaa. **Kehän oma ääni** talteen. Älä lisää musiikkia alkuperäiseen tiedostoon.

**B. Toinen kamera / puhelin – some- ja tunnelmakuvat**
1. Ota erilliset **pystysuuntaiset 9:16** klipit puhelimella (mieluiten 4K/25–50fps), kukin 5–12 sekunnin rauhallinen otto; anna kuvalla alussa/lopussa 1–2 s ylimääräistä leikkausvaraa.
2. Kuvaa luvallisesti: salin yleiskuva ja kehän valmistelut, kädet/hanskat ja kengät, lämmittely, valmentajan ja urheilijan yhteinen hetki, nousu kehään, kulman tunnelma, yleisön reaktio, **virallinen tuloskuulutus**, urheilijan/pienen ryhmän kuva ottelun jälkeen.
3. Tee myös 2–3 laajaa vaakakuvaa arkistoa varten; valokuva seuran joukkueesta jos henkilöt haluavat näkyä.
4. Älä kuvaa pukuhuoneita, alaikäisten yksityisiä hetkiä, loukkaantumista lähikuvana tai luottamuksellista taktiikkapalaveria. Huumori saa olla hyväntahtoista; ei vastustajan, tappion tai juniorin kustannuksella.

**C. Pika-haastattelut (suostumuksella)**
- **Ennen ottelua:** 10–20 s, rauhallisessa paikassa. Kysymykset: ”Millä fiiliksillä kehään?” ja ”Mitä haluaisit saada ottelusta irti?” Ei keksittyjä lupauksia voitosta.
- **Ottelun jälkeen:** 15–30 s, vasta kun urheilija on valmis puhumaan. Kysymykset: ”Mitä ottelusta jäi mieleen?”, ”Mikä onnistui tai mitä opit?” ja ”Mitä kohti harjoittelet seuraavaksi?”. Anna myös mahdollisuus kieltäytyä. Pidä tappioiden käsittely asiallisena.
- **Valmentajalta:** 10–20 s: ”Mikä oli päivän tärkein oppi?” tai ”Mistä joukkueen suorituksessa voi olla tyytyväinen?” Ei yksityiskohtaisia salaisia taktiikoita.
- Pidä puhelin pystyssä, kamera silmien tasolla, kohde riittävässä valossa, ääntä tarkkaileva kuvaaja mahdollisimman lähellä; tarvittaessa edullinen kaulusmikrofoni. Kuvaa kysymystä seuraava vastaus kokonaisena.

## 3. Toimitusohje kuvaajalle

- **Alkuperäiset MP4-tiedostot** Dropboxiin tai seuran erilliseen vastaanottolinkkiin **ilman WhatsAppin pakkausta**. WhatsApp-ryhmässä voi lähettää tiedon, että materiaali on tulossa, ei isoa raakavideota.
- Merkitse samaan viestiin: kilpailu ja päivämäärä, ottelijat, tieto onko **koko ottelu** / **pystyklippi** / **haastattelu** / **kuva**, kuvaaja sekä kuvaus-/julkaisulupatilanne. Yhdistä video BoxerBase-ottelunumeroon jos se tiedetään; älä arvaa.
- Suositeltu nimeäminen (ei pakko nimetä puhelimessa heti): `2026-11-06_SM_bout-123_kokonainen_kuvaaja.mp4`, `2026-11-06_SM_bout-123_haastattelu-jalkeen.mp4`. Puhelimen alkuperäinen nimi sallitaan, kun mukana on erillinen tunnistusviesti.
- **Yhteistä avointa Dropbox File Request -linkkiä ei ole vielä luotu.** Sen perustaminen vaatii erillisen valtuutuksen tarkkaan vastaanottokansioon. Siihen asti laitteelta jo pääsevä ylläpitäjä voi tallentaa omat tiedostonsa `/RKK`-kansioon ja muut pyytävät lähetysohjeet.
- Kuvaajalla ei tule olla yleisiä Dropbox-jako-/kirjautumisoikeuksia. Pidä raakavideo yksityisessä kansiossa, eikä julkisen Github Pagesin `docs/`-hakemistossa.

## 4. Julkaisukanavat ja sisältömuodot

| Formaatti | Pituussuositus | Milloin |
| --- | --- | --- |
| RKK Broadcast / kilpailukooste | 30–75 s | yksi yhteinen kooste saman tapahtuman seuran ottelijoista, yleensä 1 julkaisu/tapahtuma |
| RKK Kulissien takana | 20–45 s | lämmittely, matkakuulumiset, haastattelut, salin arki, erillinen näkökulma |
| RKK Pilke silmäkulmassa | 10–25 s | hyvänmielinen oikeasti hauska harjoitustilanne, ei lavastettua ottelutulosta |
| Pidempi dokumentti | 2–5 min | kun on useita hyvin kuvattuja kohtauksia ja kiinnostavia haastatteluja; oma erillinen julkaisu harkitusti |

- Pääformaatti 9:16, H.264 MP4, AAC. Yksi yhteinen master ja alustakohtaiset tekstiversiot. YouTube type short kun tavoite on Shorts.
- Ei joka saman otteluvideon kolmea tai viittä eri julkaisua ilman omaa journalistista näkökulmaa.
- **Julkaisujen oikeuksista pidetään ennakkorekisteriä**, erityisesti lasten kuvista, eikä osallistujan Dropbox-linkki anna julkaisuoikeutta. Koulutus ja kuvausohje henkilöstölle; alaikäisen kieltäytyminen kunnioitetaan.

## 5. Automaatiorata (nykytila vs tavoitteet)

1. **Intake:** Dropboxiin ladattu tiedosto saadaan paikalliseen yksityiseen synkronointikansioon; työ käynnistyy vain valmiista tiedostosta. Paikallinen inventointiraportti tunnistaa MP4:n keston, koon, tekniset ominaisuudet, hashin ja puuttuvan ottelutunnisteen. Tiedostonimeen piilotettuja merkityksiä ei arvata.
2. **Match:** tieto `event_id + bout_id` saadaan kuvaajan lomakkeesta tai hallitusti yhdistetystä merkinnästä ja tarkistetaan BoxerBasen virallisiin julkaistuihin tuloksiin. Ei kasvojen automaattista identifiointia.
3. **Rights:** hyväksytyssä yksityisessä rekisterissä kuvaajan/järjestäjän lupa, urheilijat/huoltajan suostumus, ääni ja kohdekanavat; muuten HOLD, ei julkaista.
4. **Edit:** valitse useita katsojalle ymmärrettäviä otoksia, poista tuomarivälähdykset ja toistuva materiaali; leikkeiden laatupisteet vaativat jatkokehitystä. TV-grafiikat, seuramerkki, musiikin oikeudet, lopputulokset.
5. **Publish:** vakaasti saatavilla oleva yksityisen median jakelureitti tai hyväksytty latauspalvelu, kolme kanavakohtaista julkaisua, **Auto publish ON**, YouTube **short**. API vs MCP-taustajulkaisu on yhä tekninen avoin valinta.
6. **Verify:** jokaisen kanavan julkinen URL ja kanavasivu, oikeat mediat ja tulos, mahdolliset virheet. Kerran julkaistusta tapahtuma + sisältöversio + kanava -yhdistelmästä pysyvä ledger. Älä uusintajulkaise onnistunutta kanavaa.
7. **Insights:** 48 h / 7 vrk katseluaika, katselun säilyminen, jakojen ja kommenttien määrä, sekä uuden sisällön vaikutus seuran näkyvyyteen.

**Pysyvän ennakkovaltuutuksen tavoitteena nollakosketus**, mutta tämä edellyttää toimivaa luotettua kuvaoikeus- ja lähdetietorekisteriä. Ei vedetä käyttäjän automaatiopyynnöstä johtopäätöstä, että kaikki avoimesta linkistä saapuvat videot voisi julkaista suoraan.

## 6. Mitä tarvitaan seuraavaksi käytännössä

- Kaksi roolia: kuvausvastuullinen koko ottelulle, toinen kuvaa pystysuuntaiset tunnelmat/haastattelut. Jos on vain yksi henkilö, **koko ottelu ensin**.
- Hallituksen yhteinen päätös kuvauslupien kirjaamisesta, kuvaajien perehdytyksestä ja tapahtumakohtaisen materiaalin toimitustavasta.
- Yksi uusi kilpailutapahtuma ja vähintään 2 eri raakavideota sekä haastattelut testiksi.
- Rakennetaan paikallinen media-inventaario/valmiustarkistus ja sen jälkeen vastaanottokansio + julkaisusilta. Tämä asiakirja ei tarkoita, että ne olisi jo tuotantoon yhdistetty.
- GitHubin projektitehtävä: https://github.com/glesima/kehaketut-feed/issues/19 .

## Virallisia ulkoisia lähteitä

- Metricool julkaisun tekniset vaatimukset: https://help.metricool.com/publishing-requirements-for-images-and-videos-from-metricool-vfc8n
- Metricool Instagram autojulkaisu: https://help.metricool.com/schedule-and-post-on-instagram-6b6q5
- Metricool MCP/tilausrajat: https://help.metricool.com/mcp-limits-and-plan-requirements-h72jg
- YouTube Shorts: https://support.google.com/youtube/answer/15424877
- NSPCC Child Protection in Sport Unit kuvausohje: https://sport.nspcc.org.uk/help-advice/topics/photography/

## Viestintälinjauksen tarkennus 26.10.2026 – vähemmän käsityötä kuvaajille

- Käyttäjä on Riihimäen Kehä-Kettujen **tiedotus-/mediavastaava**, ei automaattisesti kaikkien ottelujen kamerakuvaaja. Ottelijoiden ja huoltajien itse kuvaamat videot ovat ensisijainen raakamateriaali; viestintävastaava hoitaa editoinnin/julkaisujen koordinoinnin. Älä edellytä kahta kameraa tai erillistä kuvaajaa joka kisaan. **Yksi hyvä kokonainen ottelu vaakaan** riittää; lyhyet pystysuuntaiset tunnelma- ja vapaaehtoiset haastattelupätkät ovat arvokasta lisämateriaalia.
- Hallitukselle ja kilparyhmälle annetaan **lyhyet, neutraalit WhatsApp-viestit**, ei ylivirittyneitä juhlapuheita eikä koristeellisia AI-symboleja.
- **Älä jaa Dropboxin tavallista muokattavaa /RKK-kansiota kaikille kuvaajille.** Perusta sen sijaan erilliseen sovittuun tulokansioon **Dropbox File Request**, jolla kuka tahansa linkin saanut voi ladata alkuperäisiä tiedostoja ilman Dropbox-kirjautumista mutta ei näe muiden tiedostoja tai arkistoa. Esimerkkikohde `/RKK/Uudet_videot`, **ei vielä luotu eikä tiedostopyyntölinkkiä ole olemassa**; Dropbox-kansion ja tiedostopyynnön perustaminen vaatii erillisen käyttäjän hyväksynnän. Tilin tallennustila ja latausrajat varmistetaan; Dropbox Basic/Plus/Family file request max 2GB/tiedosto, ylemmissä paketeissa 250GB.
- Varavaihtoehto on **WhatsAppiin lähettäminen asiakirjana/tiedostona**, ei media-/galleriavideona. WhatsAppin tavalliset HD-videotkaan eivät takaa alkuperäistä laatua. WhatsAppin tiedostoraja 2 GB. Oletuksena ensisijainen File Request helpottaa automaatiota.
- Kuvaajalle riittää **kilpailu, ottelijat, päivämäärä, materiaalityyppi**, ja kuvaus/julkaisulupien mukainen toiminta. Puhelimen alkuperäinen tiedostonimi hyväksytään, jos mukana lähetetään tekstimuotoinen selite. Tapahtuman ja ottelun tarkka `bout_id` voidaan täydentää luotetusta virallisesta lähteestä; älä vaadi kuvaajaa tuntemaan BoxerBasea.
- Seuraavassa viestissä ryhmään annetaan vasta **oikea ja tarkistettu Dropbox-upload-URL**, ei epävirallista tavallisen kansiojaon linkkiä.

Lähteet: https://help.dropbox.com/share/create-file-request ; https://help.dropbox.com/share/received-file-request ; https://faq.whatsapp.com/453914586839706/ .
