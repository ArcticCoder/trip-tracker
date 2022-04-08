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
