# Tehtävä 1 - Monopoli

```mermaid
 classDiagram
	

	class Noppa

  Pelaaja ..> Noppa : Liiku
	Pelaaja "1" -- "1" Pelinappula
	class Pelaaja

	Pelilauta "1" *-- "40" Peliruutu
	class Pelilauta

	
	Peliruutu "1" -- "1" Peliruutu : Seuraava ruutu
	class Peliruutu
  
  Pelinappula "1" -- "1" Peliruutu
	class Pelinappula

```
