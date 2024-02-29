# TicTacToe

## Week 1

### Rollen
- Projektmanager: Marius
- SCRUM Master: Veronika
- Entwickler: Sebastian

### Projektmanagement - @Marius
Anforderungen wurden vom Auftraggeber in Form eines PDF Dokuments definiert und an uns zusammen mit den Spielregeln übergeben.

Den Entwicklern wurden verschiedene Überaufgaben zugeordnet:
- Veronika: "AI" player, Dashboard
- Marius: Network (Chat, Game) und DB (SQLite)
- Sebastian: Game Engine (Rules und Player Management)

Ebenfalls wurde ein GitHub Repository erstellt und den Entwickler Berechtigungen zugeordnet.

### SCRUM Sprints - @Veronika
#### 1. Sprint (31.01.2024 - 07.02.2024)
Aufgabenverteilung Sprint 1:
- Marius: User Stories + Backlog 
- Sebastian: Klassendiagrammen erstellen
- Veronika: Scrum Dokumentation, Sequenzdiagramme erstellen

## Week 2

### Rollen
- Projektmanager: Veronika
- SCRUM Master: Sebastian
- Entwickler: Marius

#### 2. Sprint (07.02.2024 - 16.02.2024)
Erfüllte Aufgaben von Sprint 1:
- Marius: User Stories + Backlog
- Sebastian: Klassendiagramm erstellt, Menü implementiert
- Veronika: Sequenzdiagramme erstellt, Scrum Dokumentation (Gantt chart)

Aufgabenverteilung Sprint 2:
- Marius: Use Cases 1 und 3 
- Sebastian: Use Cases 2 erstellen, Menü implementieren 
- Veronika: Scrum Dokumentation, Use Cases 4 und 5 

## Week 3

### Rollen
- Projektmanager: Sebastian
- SCRUM Master: Marius
- Entwickler: Veronika

#### 3. Sprint (16.02.2024 - 23.02.2024)
Erfüllte Aufgaben von Sprint 2:
- Marius: Use Cases 1 und 3 erstellt
- Sebastian: Use Cases 2 erstellt, Menü implementiert
- Veronika: Use Cases 4 und 5 erstellt

Aufgabenverteilung Sprint 3:
- Marius: Network-Manager + Scrum
- Sebastian: Player-Management, Projektleitung
- Veronika: KI-Algorithmus implementieren

### Week 4

#### 4. Sprint (23.02.2024 - 01.03.2024)
Erfüllte Aufgaben von Sprint 3:
- Marius: Kommunikation
- Sebastian: Projektleitung, auf Marius gewartet
- Veronika: Player

Lessons learned:
- Sebastian musste auf Marius warten, was die Zeit verschwendet hat (Plannungsfehler)
- Marius hat einen PR gestellt, welcher eigentlich nicht gemerged werden sollte (Kommunikationsfehler)
- KI konnte nicht implementiert werden, da die von der Player-Klasse abhängt, die für später geplannt war (Plannungsfehler)
- Marius konnte Datenbank + Eventmanagement machen, was für den nächsten Sprint geplant war (Plannungsfehler)

Aufgabenverteilung Sprint 2:
- Marius: Implementierung von neuen Events + Optimierung der Datenbank (in ständiger Absprache mit Sebastian)
- Sebastian: Implementierung Lobby-Interface, Alpha-Version (erste Muliplayer Spiel ermöglichen)
- Veronika: Player optimieren + KI Implementierung anfangen

### Week 5

#### 5. Sprint (16.02.2024 - 23.02.2024)
Erfüllte Aufgaben von Sprint 1:
- Marius: Use Cases 1 und 3 erstellt
- Sebastian: Use Cases 2 erstellt, Menü implementiert
- Veronika: Use Cases 4 und 5 erstellt

Aufgabenverteilung Sprint 2:
- Marius: Network-Manager + Scrum
- Sebastian: Player-Management, Projektleitung
- Veronika: KI-Algorithmus implementieren

# Codebase

## Requirements
- Python 3.10
- `pip3 install -r requirements.txt`

## Running the code
- python3 main.py
