> **PÄIVITYS 26.10.2026:** Ensimmäinen Hämeenlinna-video on nyt julkaistu Facebookissa, Instagramissa ja YouTubessa; vanhempaa mainintaa kolmesta odottavasta Draftista ei enää tule pitää nykytilana. Käyttäjän uusi suunta on **yhden kilpailun usean ottelun yhteiskooste ja automaattinen julkaisu ilman joka videon tarkistusklikkausta silloin, kun oikeudet ja varmistetut faktat sallivat**. Tekninen offline-prototyyppi [PR #18](https://github.com/glesima/kehaketut-feed/pull/18) toteuttaa usean MP4:n koonnin, mutta yksityinen 24/7-julkaisukanava on vielä avoimessa [issue #19](https://github.com/glesima/kehaketut-feed/issues/19). 

# Kehä-Ketut – videot, jotka kiinnostavat myös katsojia

**26.10.2026 · kolme julkaisulinjaa ja maltillinen kokeilusuunnitelma.**
Tämä on toimituksellinen suunnitelma, ei automaattisen julkaisemisen lupa.

## Vakiotyyli ja kaksi rinnakkaista formaattia

| Formaatti | Miksi katsoa? | Kuvallinen toteutus | Huomautus |
|---|---|---|---|
| **RKK Broadcast** – kilpailukooste | Oikeat ottelutilanteet ja vahvistettu tulos | TV-tyyliset nimet, kulmavärit, vakaa rytmi, hillityt grafiikat | Ensimmäinen V5-video on hyväksytty sisällöllisesti. Pidetään tällaiset videot faktapohjaisina. |
| **RKK Kulissien takana** | Ihmiset, harjoittelun arki, joukkueen tunnelma | Lyhyet henkilökohtaiset aidot tilanteet, kevyet väliotsikot, oikea saliääni | Ei tarvitse aina voittotulosta, ei valmennuksen yksityisiä taktisia ohjeita. |
| **RKK Pilke silmäkulmassa** | Samaistuttava harrastajahuomio tai huvittava hetki | Nopeasti ymmärrettävä koukku, aidot reaktiot, hillitty tekstipointti | Ei tehdä huumoria vastustajasta, tappiosta tai juniorin kustannuksella. |

Kaikille yhteinen identiteetti: Kehä-Kettujen oikea seuramerkki, punainen #B91C2B, grafiitinmusta #171A1F, valkoinen ja sama fonttiperhe. Voidaan pitää hauskaa ilman, että seurasta tulee epävakava tai joka video näyttää eri tuotannolta.

## Ensimmäiset kolme kokeilua

1. **Broadcast – Hämeenlinna 24.10.2026**: Gleb Simanov – Sampo Paananen, 32 sekunnin V5. Nykyinen valmis pilotti, kolme oikeaa Metricool-luonnosta. V5 täytyy vaihtaa oikeaksi videoliitteeksi ennen julkaisemista. YouTuben otsikko on jo korjattu. Julkaisut ajastetaan/julkaistaan vasta käyttäjän vahvistamasta versiosta, ei vahingossa vanhasta V4:stä.
2. **Huumori – "Kun valmentaja sanoo: vielä yksi erä"**: noin 12–18 sekunnin harjoitusmateriaali, aito, sovittu tilanne sekä loppuun hymy/tunnelma. Saa olla hauska, muttei nöyryyttävä. Käytetään vain oikeasti tallennettua materiaalia, ei lavasteta ottelutulosta eikä generoida tekaistuja iskuja.
3. **Dokumentaarinen – "Mitä ennen ottelua tapahtuu?"**: 25–45 s valmistautumista, varusteita, salia, liikkuvia ihmisiä ja valmennuksen ajatuksia yleisellä tasolla; voi toimia ilman dramaattista lopputulosta.

### Kokeiden mittaus ilman ylitulkintaa

- Vertaa formaatteja **normaalistetuilla mittareilla**, esim. katselun keskipituus / katseluprosentti, loppuun asti katselut, jaot, tallennukset, kommenttien laatu ja uudet seuraajat per tavoitettu katsoja.
- Tarkista ensimmäinen havainto **48–72 h** julkaisusta ja uudelleen noin **7 päivän** kohdalla. Yksi video ei vielä todista, mikä toimii.
- 12 sekunnin huumorivideon katseluprosenttia ei pidä verrata mekaanisesti 32 sekunnin kilpailukoosteeseen ilman videon pituuden huomiointia.
- Kiinnitä huomiota yleisön ja seuran arvoihin: onnistunut huumori on helposti ymmärrettävää, lämminhenkistä ja totuudenmukaista.
- Älä julkaise samaa leikettä lukuisina peräkkäisinä versioina vain kokeilun nimissä; mieluummin kolme sisällöllisesti erilaista laadukasta videota.

## Yhden videon tuleva automaatiopolku

`yksityinen raakavideo` → `suggest_clips.py` ehdottaa aktiivisia jaksoja → valmentaja tai ihminen tarkistaa kohtaukset ja julkaisuluvat → `build_reel.py` renderöi hyväksytyt leikkeet RKK-visuaalisuudella → valmiit FB/IG/YT-tekstit ja kansikuva → käyttäjän hyväksyntä → Metricool-draftit → julkaisu → analytiikka.

**Ei ole vielä automaattisesti valmis:** sosiaalisen median lopullinen hyväksyntä, tekoälyn semanttinen kohokohtavalinta, itsenäinen videoiden vastaanotto ja Metricooliin suoraan siirtäminen ilman saatavilla olevaa media-URL:ää. Tähän ei oleteta kalliimpaa Yhdistysavain- tai Metricool-tilausta.

[Videopilotin työnkulku](VIDEOTUOTANTO_RAAKAVIDEOSTA_JULKAISUUN_2026-10-26.md) · [TV-tyyli ja Metricool](VIDEON_TV_TYYLINEN_JATKO_JA_METRICOOL_DRAFT_2026-10-26.md)
