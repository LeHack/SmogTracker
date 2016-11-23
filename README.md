# SmogTracker

## System do zbierania i manipulowania danymi pozyskanymi z systemów zewnętrznych w czasie rzeczywistym.

Autorzy: Łukasz Hejnak, Piotr Skurski

## Instalacja (za pierwszym razem, potem tylko kroki 2, 4, 7 i 8):
0. Upewnij się, że masz python3 (3.4.3) oraz pip 7.1.0 zainstalowany (i skonfigurowany by używał python3)
1. sudo pip install virtualenv
2. git clone git@github.com:LeHack/SmogTracker
3. cd SmogTracker
4. virtualenv .
5. source bin/activate
6. pip install Django==1.10.3
7. dodaj nową domenę (np. smogtracker.pl) w /etc/hosts wskazującą na 127.0.0.100, np.
        sudo echo "127.0.0.100   smogtracker.pl" >> /etc/hosts
8. python manage.py runserver smogtracker.pl:8000
9. wejdź na smogtracker.pl:8000
10. ???
11. profit $$$
