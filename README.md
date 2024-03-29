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

### Rollen
- Projektmanager: Marius
- SCRUM Master: Veronika
- Entwickler: Sebastian

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

Aufgabenverteilung Sprint 4:
- Marius: Implementierung von neuen Events + Optimierung der Datenbank (in ständiger Absprache mit Sebastian)
- Sebastian: Implementierung Lobby-Interface, Alpha-Version (erste Muliplayer Spiel ermöglichen)
- Veronika: Player optimieren + KI Implementierung anfangen

### Week 5

### Rollen
- Projektmanager: Veronika
- SCRUM Master: Sebastian
- Entwickler: Marius

#### 5. Sprint (01.03.2024 - 08.03.2024)
Erfüllte Aufgaben von Sprint 4:
- Marius: Neue Events implementiert, Datenbank optimiert, Chat Messaging, Client-Server-Kommunikation optimiert, große Fehler gefixt
- Sebastian: Lobby-Interface implementiert
- Veronika: Player und GameLogik optimiert, KI Implementierung angefangen

Anmerkungen:
- Implementierung der Alpha-Version wird wegen Krankheit auf nächsten Sprint verschoben

Aufgabenverteilung Sprint 5:
- Marius: Netzwerk Tests schreiben
- Sebastian: Frontend von Multiplayer implementieren
- Veronika: KI fertig implementieren

### Week 6

### Rollen
- Projektmanager: Sebastian
- SCRUM Master: Marius
- Entwickler: Veronika

#### 6. Sprint (08.03.2024 - 12.03.2024)
Erfüllte Aufgaben von Sprint 5:
- Marius: Netzwerk Tests
- Sebastian: Frontend von Multiplayer
- Veronika: KI fertig

Aufgabenverteilung Sprint 6:
- Alle: Präsenz-Termin, in dem Netzwerk-Kommunnikation und KI Player gemerged werden

### Week 7

### Rollen
- Projektmanager: Marius
- SCRUM Master: Veronika
- Entwickler: Sebastian

#### 7. Sprint (12.03.2024 - 19.03.2024)
Erfüllte Aufgaben von Sprint 6:
- Alle: Alles gemerged und Bugs gefixt

Aufgabenverteilung Sprint 8:
- Marius: Leaderboard, Statistiken implementieren, Username 
- Sebastian: Username UI, Game Play Settings, Statistiken UI, Global Error Pop-up
- Veronika: Unit Tests für Winner-Erkennung. Tests für die KIs, KI Optimierung

### Week 8

### Rollen
- Projektmanager: Veronika
- SCRUM Master: Sebastian
- Entwickler: Marius

#### 8. Sprint (19.03.2024 - 21.03.2024)
Erfüllte Aufgaben von Sprint 8:


Aufgabenverteilung Sprint 9:
Alle: Bugfixes
- Marius: Präsi
- Sebastian: Präsi
- Veronika: Dokumentation fertig


# Codebase

## Requirements
- Python 3.10
- `sudo apt install sqlite3 -y`
- `pip3 install -r requirements.txt`

*`pip3 uninstall socketio` if installed, because it conflicts with python-socketio*

## Running the code
- python3 main.py
