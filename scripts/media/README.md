# Kehä-Ketut: raakavideosta tarkastettavaan Reels/Shorts-koosteeseen

Tämä yksittäisen videon testattu, toistettava **paikallinen pilotointityökalu** leikkaa ennakkoon ihmisen valitsemat jaksot ja luo samasta lähdemateriaalista videon, kansikuvan sekä renderöinnin metatiedot. Se käyttää aidosti seuran logoa ja tuttuja puna–valko–grafiitti-värejä.

## Rajaukset

- **Ei julkaise tai ajasta** mitään Facebookiin, Instagramiin, YouTubeen, Metricooliin eikä Yhdistysavaimeen.
- Ei tee teknisesti luotettavaa **automaattista osumien/otteluvoittojen tulkintaa**: tärkeät 4–8 klippiä hyväksyy valmentaja. `clips` ilmoitetaan JSON-manifestissa ja ne voivat olla eri pituisia.
- Ei generoi tekaistuja ottelutilanteita eikä muuta todellista lopputulosta.
- Säilyttää alkuperäisen raakavideon koskemattomana. Älä kopioi yksityisiä raakavideoita, hyväksymättömiä juniorikuvia tai käyttöoikeudellisia alkuperäislogoja julkiseen GitHubiin. Hae seuran hyväksytty logo omaan yksityiseen työtilaan.

## Vaaditaan

Python 3.10+, Pillow, ffmpeg ja ffprobe. Linuxissa asenna tarvittaessa `sudo apt install ffmpeg fonts-noto-core` ja `python3 -m pip install Pillow` virtuaaliympäristöön. Ilmaisilla paikallisilla työkaluilla ei synny uusia videopalvelujen tilausmaksuja.

## Ajo

```bash
python3 scripts/media/build_reel.py \
  --source "/polku/ottelu.mp4" \
  --logo "/polku/Keha-Ketut-logo-header-HD.png" \
  --manifest "scripts/media/example_manifest_hameenlinna_20261024.json" \
  --output-dir "/polku/yksityiseen/valmistuvat"
```

Varmista, että kyseisen videon ja sen julkaisemiseen tarvittavat oikeudet ovat kunnossa ennen käyttöä. Jos haluat ensin katsoa pelkän kansikuvan ja tarkistaa manifestin ilman MP4:n renderöintiä, lisää `--dry-run`.

## Manifestaation perustiedot

`date`, `place`, `red`, `blue`, `division`, `result` kirjoitetaan tarkistetusta lähteestä. `clips` sisältää `start`, `duration` (sekuntia) ja `crop_x` (vasemman reunan vaakarajaus pikseleinä alkuperäisestä). Mukana on yksi aiemman oikean otteluvideon 8 leikkeen referenssimanifesti: **ei ole automaattisesti pätevä muulle videotiedostolle**.

Renderöinnin jälkeen käytä näitä toimituksellisina luonnoksina:

- `*_draft.mp4` — pystyvideo, 1080 × 1920 H.264/AAC.
- `kansikuva.jpg` — pystykansikuva.
- `render_metadata.json` — klippien aikaleimat, syötteen tarkistetut faktat ja muistutus hyväksyntätilasta.
- `ffmpeg.log` — ongelmatilanteiden tekninen loki.
- `instagram_luonnos.txt`, `facebook_luonnos.txt`, `youtube_luonnos.txt`, `somejulkaisut_luonnos.md` — turvalliset luonnokset **vain manifestin annetuista faktoista**. Lopulliset ihmiselle kirjoitetut tekstit voivat olla luontevammat.
- `private_segments/` — tekniset leikevälit ja välimontaasi, **sisältävät yksityistä kuvamateriaalia**. Säilytä vain yksityisessä kansiossa.

**Ennen Metricooliin viemistä**: tarkista että rajaus on hyvä myös mobiililla; näytetyt nimet, kisat ja tulokset pitävät paikkansa; kuvien ja äänien oikeudet ovat kunnossa; ja yksi valtuutettu henkilö hyväksyy lopullisen videon + kanavakohtaiset tekstiversiot. Musiikkia ei tässä lisätä. Facebookin erillinen RSS-autolista ei kuulu tähän videotyönkulkuun.

Tulevat vaiheet: yksityinen lähetyskansio, aikaleimoja ehdottava analyysimoduuli, hyväksyntäsivu, tekoälyn alustakohtaiset tekstit ja vasta sen jälkeen valvottu Metricool-ajastus.

## Tarkistetut testit 26.10.2026

Työkalun manifestin hyväksyntätestit 6/6 läpi sekä koko kuuden minuutin raakavideosta renderöity 32 s esimerkkikooste omassa yksityisessä testiympäristössä (myös MP4-dekoodaus tarkistettu). Työkalun renderöinti on kaksivaiheinen: ensin lähdemateriaalin aikaleimalliset leikkeet yksitellen nopeasti rajattuna, sitten valmis 9:16-kuva, tulos- ja logoelementit. Tämä vähentää pitkän videon moninkertaista dekoodausta.

Alkuperäinen henkilökohtainen video tai logo eivät ole tämän repositoryn mukana. Käytä niitä vain luvallisissa paikallisissa kansioissa.