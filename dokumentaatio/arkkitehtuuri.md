# Rakenne

```mermaid
 classDiagram
 
 	class Multiple_UI_Classes{
  }
  
  class Multiple_DB_Classes{
  }
  
	class TripTrackerService{
  }
  
  class ProfileRepository{
  }
  
  class TripRepository{
  }
  
  class Trip{
  }
  
  TripTrackerService ..> TripRepository
  TripTrackerService ..> ProfileRepository
  TripRepository ..> Trip
  Multiple_UI_Classes ..> TripTrackerService
  Multiple_UI_Classes ..> Trip
  TripRepository ..> Multiple_DB_Classes
  ProfileRepository ..> Multiple_DB_Classes
```

# Käyttöliittymä
Käyttöliittymä koostuu kolmesta luokasta: UI, ProfileView ja TripView. UI on käyttöliittymän kokonaisuudesta vastaava luokka, jonka start-metodilla käynnistetään käyttöliittymä. Kaksi muuta luokkaa edustavat ohjelman kahta eri näkymää: profiilit ja matkat. Kumpikin luokka vastaa täysin omasta näkymästään ja UI-luokka hallitsee mikä näkymä on millonkin näkyvillä. Sovelluslogiikka on pyritty irrottamaan käyttöllittymästä. Käyttöliittymä kutsuu TripTrackerService-luokan metodeja tämän saavuttamiseksi.

# Logiikka
Sovelluslogiikasta vastaa ensisijaisesti TripTrackerService-luokka, joka tarvittaessa kutsuu muiden luokkien funktioita. Ajatuksena on, että TripTrackerService-luokan metodit ovat ainoita sovelluksen toiminnallisuuteen liittyviä metodeja, joita käyttöliittymän tarvitsee kutsua. Luokka itsessään hyödyntää konstruktoriin injektoituja ProfileRepository- ja TripRepository-luokkia tietojen tallentamista ja noutamista varten. Luokkien tarkemmat suhteet näkyvät yllä olevassa rakennekaaviossa.

# Tietojen tallennus
ProfileRepository- ja TripRepository-luokat vastaavat tietojen pysyväistallennuksesta. Molemmat hyödyntävät yhteistä SQLite tietokantaa. Tiedostonimi määritellään .env tiedostossa. TripTrackerService:llä on oma välimuisti, jossa valitut matkat säilötään niin kauan kun valinta ei muutu. Tämä välttää turhia tietokantahakuja.

# Toiminnallisuudet

## Profiilin valitsemisen sekvenssikaavio
Kaaviota on yksinkertaistettu käyttöliittymän osalta ja kaikki käyttöliittymään liittyvät luokat on yhdistetty. Kaaviossa näkyy hyvin välimuistin toiminta.
```mermaid
 sequenceDiagram
 
 actor User
 User ->> UI_classes : Valitse profiili 1
 
 UI_classes ->> TripTrackerService : select_profile(1)
 TripTrackerService ->> TripTrackerService : select_time_range()
 TripTrackerService -->> UI_classes : 
 UI_classes ->> UI_classes : _print_statistics()
 UI_classes ->> TripTrackerService : get_statistics()
 TripTrackerService ->> TripTrackerService : _update_cache()
 TripTrackerService ->> TripRepository : find_by_profile(1, None, None)
 TripRepository ->> Trip : Useita konstruktori-kutsuja
 Trip -->> TripRepository : Luotu Trip-olio
 TripRepository -->> TripTrackerService : Lista Trip-olioita
 TripTrackerService -->> UI_classes : Lasketut tilastot
 UI_classes ->> UI_classes : _print_trips()
 UI_classes ->> TripTrackerService : get_trips()
 TripTrackerService ->> TripTrackerService : _update_cache()
 TripTrackerService -->> UI_classes : Lista Trip-olioita
```

## Matkan lisäämisen sekvenssikaavio
Kaaviota on yksinkertaistettu käyttöliittymän osalta ja kaikki käyttöliittymään liittyvät luokat on yhdistetty. Kaaviossa näkyy hyvin välimuistin toiminta.
```mermaid
 sequenceDiagram
 
 actor User
 User ->> UI_classes : Luo uusi matka
 
 UI_classes ->> TripTrackerService : valid_time("2022-01-01 00:00")
 TripTrackerService -->> UI_classes : True
 UI_classes ->> TripTrackerService : valid_time("2022-01-01 01:00")
 TripTrackerService -->> UI_classes : True
 UI_classes ->> TripTrackerService : add_trip("Matka", "2022-01-01 00:00", "2022-01-01 01:00", 1000)
 TripTrackerService ->> TripTrackerService : valid_time("2022-01-01 00:00")
 TripTrackerService -->> TripTrackerService : True
 TripTrackerService ->> TripTrackerService : valid_time("2022-01-01 01:00")
 TripTrackerService -->> TripTrackerService : True
 TripTrackerService ->> TripRepository : add(1, "Matka", "2022-01-01 00:00", "2022-01-01 01:00", 1000)
 TripRepository -->> TripTrackerService : 
 TripTrackerService -->> UI_classes : 
 
 UI_classes ->> UI_classes : _print_statistics()
 UI_classes ->> TripTrackerService : get_statistics()
 TripTrackerService ->> TripTrackerService : _update_cache()
 TripTrackerService ->> TripRepository : find_by_profile(1, "2022-01-01 00:00", "2022-01-01 01:00")
 TripRepository ->> Trip : Useita konstruktori-kutsuja
 Trip -->> TripRepository : Luotu Trip-olio
 TripRepository -->> TripTrackerService : Lista Trip-olioita
 TripTrackerService -->> UI_classes : Lasketut tilastot
 UI_classes ->> UI_classes : _print_trips()
 UI_classes ->> TripTrackerService : get_trips()
 TripTrackerService ->> TripTrackerService : _update_cache()
 TripTrackerService -->> UI_classes : Lista Trip-olioita
```
