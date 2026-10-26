> **TARKENNUS 26.10.2026 – Instagramin puuttuneen julkaisun syy tunnistettu:** Käyttäjä vahvisti, että Instagram Reel -julkaisun **Auto publish oli OFF**. Metricoolin virallisen ohjeen mukaan tämä käynnistää manuaalisen julkaisun ilmoituksella; tila `Sent` tarkoittaa vain ilmoituksen lähettämistä, ei Instagramissa julkaistua videota. Käyttäjä ei tehnyt erillistä mobiilijulkaisua, joten Reeliä ei näy profiilissa. Aiempi `PUBLISHED`-merkintä Metricool-liitännässä ei tässä tapauksessa ollut luotettava todiste Instagramissa näkyvästä postauksesta. **Älä diagnosoi tätä Meta-poistoksi tai tee tukeen eskalointia oletuksena.**
>
> **Korjauspolku:** Metricool Calendar → alkuperäinen Instagram-postaus → **Duplicate** → jätä kanavaksi **vain Instagram** (FB ja YouTube julkaistu jo) → **Auto publish ON** → tuleva aika → ajoita/julkaise. Jos alkuperäinen notifikaatio on käytettävissä, vaihtoehto on suorittaa julkaisu puhelimella. Kun manuaalinen notifikaatio on jo lähetetty, Metricoolin ohjeen mukaan alkuperäistä postausta ei enää voi vaihtaa automaattiseksi: tarvitaan duplikaatti. Aina julkaisun jälkeen varmista oikea Instagram Reel -URL/näkyvyys ennen kuin kirjataan `PUBLIC_VERIFIED` tai yritetään retry. Tulevien automaatioiden on pakotettava IG Reel `autoPublish=true` ja tarkistettava erikseen alkuperäisen kanavan näkyvyys.
>
> Lähde: https://help.metricool.com/why-does-my-post-appear-as-sent-in-metricool-and-not-auto-published-467xf ja https://help.metricool.com/why-cant-i-enable-auto-publishing-66gg0 .

# Kehä-Ketut – Metricool-luonnokset ja TV-tyylin V5-pilotti

**26.10.2026 · Työtila / julkaisut eivät ole julkisia.**

## Mitä käyttäjä todensi

- Metricoolin **Riihimäen Kehä-Ketut** -brändissä (ID `7632678`) tehtiin yksi monikanavainen Facebook Reel + Instagram Reel + YouTube Short -julkaisuehdotus. Tallennuksen jälkeen kalenterissa näkyi **kolme erillistä Draft-korttia** 26.10.2026 klo 11.39. Mitään ei julkaistu.
- Metricoolin **Template / Edit by network** sallii yhteisen sisällön muokkaamisen ennen tallennusta, mutta tallennettaessa syntyy **yksi erillinen julkaisu verkostoa kohti**; sen jälkeen jokainen muokkaus tehdään kanavakohtaisesti. Tämä on Metricoolin ilmoittama toimintamalli, ei käyttäjän virhe. Ohje: https://help.metricool.com/multiposting-edit-per-social-network-85out
- YouTuben otsikkoon oli aiemmasta ChatGPT:n kopiointiohjeesta tullut kirjaimellisia kenoviivoja `\|` ennen pystypalkkeja. **Kenoviivat eivät ole videon tai Metricoolin ominaisuus, vaan virheellistä otsikkotekstiä**. Korjaa YouTube-luonnos otsikkoon `Gleb Simanov vs Sampo Paananen – Hämeenlinna 2026` (ei kenoviivoja).
- `Publish date can't be a past date` näkyy 26.10. klo 11.39 luontiajankohdan jälkeen avatussa luonnoksessa. Draft-kortti on silti tallessa eikä mitään lähetetä automaattisesti; julkaisuaikaa muutetaan tulevaksi vasta, jos julkaisu oikeasti päätetään ajastaa.
- Kalliimpaa Metricoolin Posts Library -ominaisuutta ei oleteta käyttöön: se on maksullisille suunnitelmille. **MCP-yhteys** voi luoda eri kanaville omia postauksia/luonnoksia, mutta tämän keskustelun olemassa olevia kolme Draft-luonnosta ei pidä vahingossa korvata uusilla tai luoda duplikaatteja. Tässä vaiheessa avustetaan manuaalista editointia, myöhemmin voidaan kokeilla yhden toimituspaketin automaattista siirtoa luonnoksiksi. Ohje: https://help.metricool.com/more-scheduling-options-with-metricools-mcp-ylkdd

## V5 – erillinen TV-tyylisen ilmeen kokeilu

Käyttäjä pyysi ammattilaisemman televisiotuotannon tuntuista videota, mutta materiaalin alkuperäinen laatu asettaa rajat. Aiemmasta yksityisestä 6:06 MP4:stä valittuja samoja kahdeksaa todellista jaksoa käytettiin jo v4:ssä; uusi **V5 on vaihtoehtoinen vertailuversio, ei hyväksytty julkaisu eikä automaattinen korvaus Metricoolin luonnoksiin**.

**Valmistettu ja teknisesti tarkistettu** paikallisesti:
- 32 s / 1080×1920 / 25 fps / H.264 + AAC, 21,2 Mt.
- Oikea aiemmin tallennettu seuramerkki; TV-tyylinen yläotsake, punaisen ja sinisen kulman väliset tunnisteet, hillitty värikorjaus, todennettu tulos `Paananen voitti 5–0` lopussa sekä oma seuran lopputunnus.
- Ei keinotekoisia iskuja, valheellisia tuloksia, lisensoimattomia musiikkikappaleita tai lisättyä tekokatsomoääntä; alkuperäinen kehä-ääni säilytettiin.
- Pystyvideon alaosa pidetään vapaana olennaisista teksteistä, koska YouTube/Instagram/Facebook piirtävät nimensä, tekstinsä ja toimintopainikkeensa videon päälle.
- FFprobe todensi keston ja koon; koko MP4 purettiin onnistuneesti virheettömästi. Erillinen kansikuva, kuvallinen neljän ruudun vertailu sekä toimituspaketin ohjeet tehty; yksityinen V5 MP4 **on vain keskustelun tiedostossa, ei julkisessa GitHubissa**.

**Olennainen rehellinen laaturaja:** lähde on **848×478** ja kuvattu **yhdellä kaukaa kuvaavalla kameralla**. V5 nostaa graafisen editoinnin laatua, mutta 1080×1920 toimitusformaatti **ei tuo aitoa 1080p-erottelukykyä**. Todellinen broadcast-taso edellyttää parempaa kuvauskalustoa ja kuvakulmia.

## Seuraava tuotannon laatutasoa nostava suunnitelma

1. **Kuvaus**: mieluiten yksi jatkuva laaja kuva + toinen lähempää, vakaat jalustat, parempi sijainti kehän tasolla, 4K/25 tai 50 fps sisävalaistuksen ja välkynnän mukaan, äänelle oma keruu. Älä häiritse ottelua, noudata järjestäjän lupia.
2. **Valikointi**: ihminen vahvistaa merkittävimmät jaksot; tuleva AI-liike/kohtausehdotus ei saa luokitella osumia pisteiksi eikä keksiä urheilusuorituksia.
3. **Editointi**: 1–2 s hook, 20–35 s rytmitetyt tilanteet, maltillinen slow motion vain kun alkuperäinen ruutunopeus sallii, ammattimainen värikorjaus ja äänen tasaus, yhtenäiset turvallisille alueille sijoitetut grafiikat, todennettu tulos ja seuran tunnus.
4. **Yhden lähteen julkaisupaketti**: tuota MP4 + kansikuva + IG / FB / YT -tekstit kokonaan valmiiksi ennen Metricoolia. Kanavakohtaiset tekstikentät ja asetukset kerran, tallennus Draft-kortteihin. Tallennettuja Draft-kortteja ei voi enää muuttaa yhtenä yhdistettynä templaatina.
5. **Hyväksyntä**: käyttäjä/valtuutettu hallituksen hyväksyjä + tarvittaessa valmentaja tarkistaa videon; mitään ei aikatauluteta tai julkaista ennen erillistä lupaa. Laadulliset muutokset, myös mahdollisen V5-videon vaihto luonnoksiin, edellyttävät ensin hyväksyntää.
6. **Lisäkustannukset**: paikallinen FFmpeg+Pillow toimii ilman uusia videoeditointitilauksia. Maksullisia generatiivisia videotoimintoja tai automaattista julkaisualustaa ei hankita pelkän pilotin vuoksi. Mittaa palaute ja kuvan laatu ensin.

## Viralliset ohjeet

- https://help.metricool.com/multiposting-edit-per-social-network-85out
- https://help.metricool.com/edit-images-and-videos-while-scheduling-your-content-wputz
- https://help.metricool.com/posts-library-u05cj
- https://help.metricool.com/more-scheduling-options-with-metricools-mcp-ylkdd
- [Videopilotti ja fakta-aineisto](VIDEOPILOTTI_HAMEENLINNA_2026-10-26.md)
- [Shorts-safezone-korjaus PR #15](https://github.com/glesima/kehaketut-feed/pull/15)
- [Varsinainen videoiden työnkulku](VIDEOTUOTANTO_RAAKAVIDEOSTA_JULKAISUUN_2026-10-26.md)
