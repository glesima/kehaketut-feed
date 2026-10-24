# Kehä-Ketut: ajastettava kilpailu- ja kuvasyöte v1

Tämä on **asennettava toteutusprototyyppi**, ei vielä julkaistu integraatio.
Koodi on testattu paikallisilla fixtures-esimerkeillä. Internet-yhteyttä
BoxerBaseen tai Instagramiin ei ole voitu testata tästä suoritusympäristöstä.

## Mitä ratkaisu tekee

- Python lukee BoxerBasen julkisen seuraprofiilin sekä ottelijoiden profiilit:
  ottelumäärät, voitot, tappiot ja BoxerBase-linkit.
- Hakee tunnettujen tapahtumien julkiset ottelulistat, etsii seuran nyrkkeilijät
  ja selvittää virallisen tuloksen ottelun omalta sivulta. Löytää lisäksi enintään
  kahdeksan tapahtumaa Suomen BoxerBasen etusivun julkisista linkeistä.
  **Se ei vielä löydä kaikkia mahdollisia uusia tapahtumia eikä takaa
  ilmoittautuneiden osallistujien automaattista löytämistä**.
- Säilyttää edellisen onnistuneen päivityksen, jos yksittäinen sivu antaa virheen.
- Osaa lukea Instagramin uusimmat kuvat virallisen Meta API:n kautta vain, kun
  erikseen valtuutettu `@kehaketut`-tunniste on lisätty salaisuutena.
  Jos token kuuluu väärälle tilille, Instagram-haku keskeytyy.
- JSON-syötettä lukeva HTML näyttää tulokset, nyrkkeilijät, kuvavirran
  ja henkilökohtaiset tilastot upotettavissa, responsiivisissa iframe-näkymissä.
- Ensimmäisessä vaiheessa GitHub Actions ajaa paikalliset testit ja julkaisee aloitustietosyötteen vain pyydettäessä. Ajastettu BoxerBase-haku otetaan käyttöön vasta erillisen tarkistuksen ja palveluntarjoajan ehtojen varmistamisen jälkeen.

## Miten kytket sen käyttöön (GitHub Pages)

1. Luo erillinen julkinen GitHub-repositorio, esimerkiksi `kehaketut-feed`.
   Julkinen repo on tarpeen, jos käytössä on tavallinen GitHub Free + Pages.
2. Lähdekoodi on siirretty repositorioon GitHub-yhteyden avulla. Tarkista tiedostot ja ota Actions käyttöön.
3. Aseta **Settings → Pages → Build and deployment → Source: GitHub Actions**. Julkaisutyönkulku käyttää `actions/deploy-pages`-toimintoa.
4. Aja ensimmäisen kerran **Actions → Kehä-Ketut feed - manual verification → Run workflow**. Tämä ajaa testit ja julkaisee tämänhetkisen *esimerkkitietoaineiston*; se ei vielä hae BoxerBasea verkosta.
5. Tarkista, että `https://glesima.github.io/kehaketut-feed/widget.html?view=boxers`
   toimii ja näyttää päivityspäivän.
6. HTML-katkelmissa on jo oikea GitHub-tilin nimi `glesima` ja ehdotettu
   repo `kehaketut-feed`. Liitä katkelmat Yhdistysavaimen **HTML-koodia**-osioihin
   vasta, kun Github Pages -osoite oikeasti avautuu.
7. Ennen nykyisten staattisten tuloskorttien poistamista tarkista vähintään kaksi
   eri tapahtumaa ja usean nyrkkeilijän luvut.
8. Lisää halutessasi seuran ammattilais-Instagramin **virallisella Meta API:n
   kirjautumisvirralla** haettu, vain @kehaketut-tilin lukuoikeustunnus GitHub
   Actions Secret -kohtaan `INSTAGRAM_ACCESS_TOKEN`. Älä lähetä sitä chatissa
   tai lisää HTML-koodiin. Yhteys Metricooliin ei yksin tuota tällaista tokenia.

**Käyttöoikeus:** Varmista ensin BoxerBasen käyttöehdoista/palveluntarjoajalta
säännöllisen koneellisen tietojen haun sallittavuus. Skripti tarkistaa robots.txt:n
ja jättää hakematta, jos se estää noudon. Jos käyttöehto tai API on epäselvä,
pyydä kirjallinen lupa ennen automaattisen ajastuksen aktivointia.

**Helpompi Instagram-vaihtoehto:** Juicerin ilmainen Instagram Feed
on erillinen upotettava automaattinen kuvavirta, joka päivittyy noin kerran
vuorokaudessa. Yhdistä siihen vain @kehaketut, kopioi Juicerin tarjoama
widget-koodi Yhdistysavaimen HTML-osioon ja jätä se hoitamaan kuvavirta.
Juicer voi vaatia sosiaalisen median kirjautumisen / uudelleenvaltuutuksen.
Tämä on erillinen tili Metricoolista. https://www.juicer.io/instagram

**Instagram – oma API-polku:** Metricool Free-/Starter-yhteys ei tarjoa automaattiselle
ulkopuoliselle skriptille Metricool API:a. Viralliseen Instagram API:in tarvitaan
seuran ammattilaistilin valtuutus Meta-kehittäjäsovelluksessa ja mahdollisesti
lisäkäsittelyä oikeuksille. Medialinkit voivat vanhentua; päivitys korjaa niitä
vain, jos valtuutus toimii.

**Tietojen rajaus:** BoxerBasen profiilien ottelumäärät eivät välttämättä ole
koko uran ottelumääriä. Alustavia ilmoittautumisia ei näytetä vahvistettuina
otteluina. Sivu näyttää datan lähteen ja päivityspäivän. Alaikäisistä
näytetään vain julkinen nimi ja ottelutilasto, ei syntymävuotta.

## Kehityksessä / ei vielä valmista

- Automaattinen kaikkien BoxerBase-tapahtumien seurakohtainen osallistujahaku
  ilman virallista API:a, koska julkinen osallistujalista on sivutettu ja
  tapahtumatiedot julkaistaan vaiheittain.
- Sosiaalisen median autopostaus. Tämä ei lähetä julkaisuja Facebookiin
  eikä Instagramiin. Sosiaalisen median julkaisut tehdään erikseen Metricoolissa.
- Yhdistysavaimen Uutislistaan suoraan kirjoittaminen ei ole tässä käytössä.
  Aseta etusivun Uutislista → Asetukset → näytettävien uutisten määrä: **3**.

## Testaus

`python -m pip install -r requirements.txt`

`python -m unittest discover -s tests -v`

`python scripts/update.py` tarvitsee verkon ja sallivan robots.txt:n.

Tarkista, että `docs/data.json` ei koskaan sisällä API-tunnuksia tai
nuorten syntymävuosia.


## Käyttöönoton tilanne 25.10.2026

GitHub Actionsin ajastus julkaisee BoxerBase-profiilit, tulokset ja kolme uusinta uutista neljästi vuorokaudessa. Varmista lähteen käyttöehdot myös jatkossa; epäonnistunut päivitys säilyttää viimeisimmän kelvollisen aineiston. Instagram-kuvavirtaan ensisijainen ratkaisu on Juicerin Yhdistysavaimeen upotettu erillinen widget.

## Facebook-osio

Facebookin oma Page Plugin -iframe ei latautunut luotettavasti Yhdistysavaimessa.
Oma `docs/facebook.html` näyttää pelkän julkisen Facebook-julkaisun tiivistelmän
ja linkin oikeaan julkaisuun. Ensimmäinen aineisto on haettu yhdistetyn
Metricool-brändin (id 7632678, Facebook-sivutunniste 160875127258478) kautta.
JSON-syöte `docs/facebook.json` vaatii erillisen säännöllisen päivityksen;
Github Actionsin BoxerBase-haussa ei ole Metricoolin API-avainta.
Älä käytä henkilökohtaisen tai yrityksen Facebook-tilin julkaisuja.
