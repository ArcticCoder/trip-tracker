# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus mahdollistaa kuljettujen matkojen seurannan ja yksinkertaisen analyysin. Mahdollisia käyttökohteita ovat esimerkiksi juoksu- tai pyörälenkit. Sovellukseen voi luoda useamman profiilin eri henkilöiden tai saman henkilön eri tyyppisten matkojen erittelyä varten.

## Profiilit

Jokainen matka kuuluu tietylle profiilille. Tarkoituksena on ryhmitellä matkat käyttäjälle mielekkäällä tavalla. Mahdollisia profiileja olisi esimerkiksi *Matti - Maasto, Matti - Kaupunki, Maija - Juoksu*. **PROFIILIT EIVÄT OLE SALASANASUOJATTUJA:** Kyseessä on paikallinen sovellus, joten salasana ei tarjoaisi merkittävää yksityisyydensuojaa, tietoturvaa tai tiedon suojaa, ilman että itse tietokannan tiedot salataan. Tämä taas ei ole sovelluksen tarkoituksen kannalta välttämätöntä, eikä kurssin tavoitteiden kannalta mielekästä.

## Toiminnallisuus

- Pofiilinvalintaikkuna, jossa voidaan
	- Luoda uusi profiili
		- Nimen tulee olla uniikki
	- Poistaa olemassaoleva profiili
	- Valita tarkasteltava profiili, jonka jälkeen avautuu pääikkuna

- Pääikkuna, jossa voidaan
	- Tarkastella profiiliin liitettyjä matkoja
		- Oletuksena näkyy kaikki matkat kronologisessa järjestyksessä
		- Valinta voidaan rajata tietylle aikavälille
		- Matkoista näkyy
			- Nimi
			- Aloitusaika
			- Lopetusaika
			- Kesto
			- Pituus
			- Keskinopeus
	- Lisätä uusi matka, johon liittyy tiedot
		- Nimi
		- Aloitusaika
		- Lopetusaika
		- Pituus
	- Poistaa matkoja
	- Laskea ja tarkastella valituista matkoista erinnäisiä tilastoja
		- Keskimääräinen kesto
		- Keskimääräinen pituus
		- Keskimääräinen nopeus
	- Piirtää matkojen (numeerisista) tiedoista ja niistä laskettavista arvoista kuvaajia
		- Kuvaaja valittujen matkojen kestoista/pituuksista/keskinopeuksista ajan myötä
	- Palata profiilinvalintaan
