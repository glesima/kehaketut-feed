# Kehä-Ketut: yksityinen MP4-vastaanoton tekninen inventaario

**Vaihe:** 26.10.2026 paikallisesti testattu prototyyppi. Ei julkaise, siirrä, jaa tai muokkaa tiedostoja; ei ole Dropboxin 24/7-tausta-agentti.

`filming_intake.py` inventoi yhden yksityisen paikallisen videokansion, joka voidaan tulevaisuudessa synkronoida Dropboxin `/RKK`-kansiosta. Raportti havainnoi MP4-keston, kuvan koon, ruutunopeuden, ääniraidan, SHA-256-tunnisteen sekä ehdotetut metadata- ja ottelukytkennät. Raportissa mikään ei saa tilaa automaattisesti julkaisukelpoinen: kuvausluvat, junioreiden suostumukset, julkaistut ottelufaktat ja kohdekanavat varmennetaan erillisessä luotetussa palvelussa.

## Asennus

Python 3.10+ ja `ffprobe` (FFmpeg) sekä paikallinen _yksityinen_ kansio, jossa vain luvallista mediaa. Ei maksettuja pilvipalveluja.

Esimerkkikomennot:

```bash
python3 scripts/media/filming_intake.py \
  --folder "$HOME/Dropbox/RKK" \
  --assignments "$HOME/.config/rkk/private_bout_assignments.json" \
  --published-ledger "$HOME/.config/rkk/private_published_bouts.json" \
  --output "$HOME/.local/share/rkk/private_intake_report.json"
```

**Tiedostojen ollessa suuria ja vasta latautumassa** oletusarvoinen 60 sekunnin tiedoston viimeisen muokkauksen jälkeen odottaminen estää käsittelyn liian varhain. Tuotannossa tulee lisäksi käyttää kirjoituksen jälkeisen tiedostokoon pysyvyyden tarkistusta ja Dropbox-synkronoinnin valmistumissignaalia, koska pilottiversio ei ole tiedostojärjestelmän taustavahti.

`private_bout_assignments.json` on manuaalisesti/luotetulla vastaanottolomakkeella vahvistettu lähdetiedoston → tapahtuma/ottelunumero/kategoria -kartta. Esim.:

```json
{
  "camera001.mp4": {
    "event_id": "testevent123",
    "bout_id": "16",
    "kind": "full_bout",
    "provided_by": "club_admin_confirmed"
  },
  "phone001.mp4": {
    "event_id": "testevent123",
    "bout_id": "16",
    "kind": "interview_post",
    "provided_by": "club_admin_confirmed"
  }
}
```

Kentän `approved` tai `permission_granted` lisääminen tänne **ei valtuuta julkaisemiseen**. Virallinen tulos ja lupa tarkastetaan aina riippumattomasta oikeusrekisteristä. Valtuutuksia, henkilötietoja, raakavideoita ja varsinaista `private_intake_report.json`-tiedostoa **ei saa lisätä julkiseen GitHub-repositorioon**.

`private_published_bouts.json` voi sisältää jo julkaistujen ottelutunnisteiden listan, esimerkki:

```json
{"published_bouts":[{"event_id":"testevent123","bout_id":"16"}]}
```

Tämä on tässä toteutuksessa yksinkertainen **varoitus**, ei täydellinen tapahtuma+sisältöversio+kanava -atominen lukitus. Varsinainen julkaisuledger toteutetaan erikseen ennen automaattista somejakelua. Saman ottelun eri journalistista haastattelujuttua voidaan myöhemmin julkaista uutena konseptina, mutta vanhoja ottelukoosteita ei pidä kopioida automaattisesti.

## Lähtö- ja seuraava vaihe

- Tulo: yksi kansio paikallisia MP4-tiedostoja, vapaaehtoinen vahvistettu kuvaus-/ottelumetadata ja julkaisutieto.
- Lähtö: yksityinen `private_intake_report.json`, `publication_ready: false`.
- Tila `WAIT_FOR_UPLOAD_TO_SETTLE` tarkoittaa, että tiedostoa ei vielä avata; `MISSING_EXPLICIT_EVENT_AND_BOUT_MAPPING` kertoo puuttuvasta ottelu-ID:stä; `ALREADY_HAS_PUBLISHED_BOUT_CONTENT_REVIEW_REUSE` estää automaattisen saman ottelun uudelleenkierrättämisen. `INDEPENDENT_FILMING_AND_PUBLICATION_RIGHTS_CHECK_REQUIRED` vaatii erillisen luotetun luvan.
- Kun raportti on valmis, ihminen tai tuleva yksityinen palvelin voi luoda `event_recap.py`-manifestin ja ajaa paikallisen leikkeiden analyysin ja TV-koosteen. Nykyinen ohjelma ei automaattisesti lähetä syötteitä `event_recap.py`-renderöintiin.
- Viimeinen avoin työ on **toimiva** media-upload/Metricool-julkaisusilta ja kanavakohtainen julkisen julkaisun onnistumisvahvistus. Instagramin `Auto publish=OFF` havaittiin aiemmin todellisena ongelmana; suositus on `true` ja vahvistus Instagramin omasta julkisesta URL:sta.

## Paikallinen testi 26.10.2026

- `python3 -m unittest -v test_filming_intake` – 10/10.
- Käytännön testissä kaksi Dropboxista yksityiseen työtilaan kopioitua jo julkaistua otteluvideota: 8:05 / 848×476 / ei audioa ja 6:14 / 848×478 / audio. Molemmille löydettiin käyttäjän vahvistama ottelunumero (16 ja 33), ja mukana ollut julkaisuledger palautti varoituksen jo julkaistusta ottelumateriaalista. Ei uutta julkaisua, ei muutosta alkuperäisiin Dropbox-tiedostoihin.

