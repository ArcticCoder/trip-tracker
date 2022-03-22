# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus mahdollistaa kuljettujen matkojen seurannan ja yksinkertaisen analyysin. Mahdollisia käyttökohteita ovat esimerkiksi juoksu- tai pyörälenkit. Sovellukseen voi luoda useamman profiilin eri henkilöiden tai saman henkilön eri tyyppisten matkojen erittelyä varten.

## Profiilit

Jokainen matka kuuluu tietylle profiilille. Tarkoituksena on ryhmitellä matkat käyttäjälle mielekkäällä tavalla. Mahdollisia profiileja olisi esimerkiksi *Matti - Maasto, Matti - Kaupunki, Maija - Juoksu*. **PROFIILIT EIVÄT OLE SALASANASUOJATTUJA:** Kyseessä on paikallinen sovellus, joten salasana ei tarjoaisi merkittävää yksityisyydensuojaa, tietoturvaa tai tiedon suojaa, ilman että itse tietokannan tiedot salataan. Tämä taas ei ole sovelluksen tarkoituksen kannalta välttämätöntä, eikä kurssin tavoitteiden kannalta mielekästä.

## Toiminnallisuus

### Ydin

Pofiilinvalintaikkuna, jossa voidaan
 - Luoda uusi profiili tai vaihtaa profiilin nimi
	 - Nimen tulee olla uniikki
 - Poistaa olemassaoleva profiili
 - Valita tarkasteltava profiili, jonka jälkeen avautuu pääikkuna

Pääikkuna, jossa voidaan
 - Tarkastella profiiliin liitettyjä matkoja
	 - Oletuksena näkyy kaikki matkat kronologisessa järjestyksessä, mutta valinta voidaan rajata tietylle aikavälille
	 - Matkoista näkyy (ainakin)
		 - Nimi
		 - Aloitusaika
		 - Lopetusaika
		 - Kesto
		 - Pituus
		 - Keskinopeus
 - Lisätä uusi matka, johon liittyy tiedot
	 - Nimi
	 - Aloitusaika
	 - Lopetusaika (mahdollisesti vaihtoehtona myös suoraan matkan kesto)
	 - Pituus
 - Poistaa matkoja
 - Laskea ja tarkastella valituista matkoista erinnäisiä tilastoja. Esimerkiksi:
	 - Keskimääräinen kesto
	 - Keskimääräinen pituus
	 - Keskimääräinen nopeus
 - Piirtää matkojen (numeerisista) tiedoista ja niistä laskettavista arvoista kuvaajia. Esimerkiksi:
	 - Kuvaaja valittujen matkojen kestoista/pituuksista/keskinopeuksista ajan myötä
 - Palata profiilinvalintaan

### Mahdollisuuksien ja tarpeiden mukaan lisättävät (karkeassa prioriteettijärjestyksessä)

 - Lisää vaihtoehtoja matkojen järjestämiselle esimerkiksi keston mukaan
 - (Lähes varmasti lisättävä) Mahdolllisuus sovittaa esimerkiksi suora yllä mainittuihin kuvaajiin, jotta kehityksen suunta ja tahti on selvempää
 - Liukuvan keskiarvon laskeminen ja piirtäminen kuvaajiin
 - Lisää vaihtoehtoja matkojen rajaamiselle esimerkiksi matkan, ajan tai keston mukaan
 - Olisi mahdollisesti kiinnnostavaa voida valita kaksi (tai useampi) profiilia samanaikaisesti ja vertailla niitä tilastojen ja kuvaajien avulla.
 - Uusia laskettavia tilastoja ja piirrettäviä kuvaajia on mahdollista keksiä liki loputtomasti, joten niitä lisätään mahdollisuuksien mukaan.
 - Valittujen matkojen tallentaminen esimerkiksi .csv tiedostoon
