# HY-OhTe - Vili Sinervä

Vili Sinervän **OhTE** kurssin *git repositoirio*. Projektina matkojen seuranta sovellus.

## Dokumentaatio
[Arkkitehtuuri](https://github.com/ArcticCoder/trip-tracker/blob/master/dokumentaatio/arkkitehtuuri.md)

[Changelog](https://github.com/ArcticCoder/trip-tracker/blob/master/dokumentaatio/changelog.md)

[Tuntikirjanpito](https://github.com/ArcticCoder/trip-tracker/blob/master/dokumentaatio/tuntikirjanpito.md)

[Vaatimusmäärittely](https://github.com/ArcticCoder/trip-tracker/blob/master/dokumentaatio/vaatimusmaarittely.md)

## Komennot

### Asennus ja käyttö
1. Asenna riippuvuudet:
```bash
poetry install
```

2. Valmistele sovellus (**POISTAA OLEMASSAOLEVAN TIETOKANNAN**):
```bash
poetry run invoke build
```

3. Käynnistä (Ensimmäisen kerran jälkeen suorita suoraan tällä):
```bash
poetry run invoke start
```

### Testaus ja kehitys:
Pylintin suoritus
```bash
poetry run invoke lint
```

autopep8 koodin muotoilu
```bash
poetry run invoke format
```

Testien suoritus
```bash
poetry run invoke test
```

Testikattavuus raportin luominen (index.html, löytyy *htmlcov* kansiosta)
```bash
poetry run invoke coverage-report
```
