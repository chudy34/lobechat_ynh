# LobeHub for YunoHost

## Instalacja i aktualizacja

To repozytorium jest pakietem instalacyjnym [LobeHub](https://github.com/lobehub/lobehub) dla YunoHost. Instalacja i aktualizacja z głównej gałęzi pakietu:

```bash
sudo yunohost app install https://github.com/chudy34/lobechat_ynh
sudo yunohost app upgrade lobehub -u https://github.com/chudy34/lobechat_ynh
```

Przed aktualizacją instancji z danymi wykonaj kopię zapasową YunoHost i sprawdź, czy można ją odczytać. Pakiet korzysta z Docker CE i Compose v2. Instalator przygotowuje także PostgreSQL/ParadeDB, RustFS, Redis oraz SearXNG. Ustawienia i dane pozostają na serwerze YunoHost; to repozytorium zawiera tylko pliki pakietu.

## Aktualna wersja upstream

- Repository: `https://github.com/lobehub/lobehub`
- Release: `v2.2.18`
- Docker image: `lobehub/lobehub:2.2.18`
- LobeHub version: `2.2.18`
- Licencja upstream: [LobeHub Community License](https://github.com/lobehub/lobehub/blob/v2.2.18/LICENSE)

## Czym jest LobeHub

LobeHub służy do tworzenia agentów AI i organizowania ich pracy w jednym miejscu. Według [README projektu głównego](https://github.com/lobehub/lobehub#readme) obejmuje między innymi:

- budowanie agentów oraz korzystanie z różnych modeli i typów treści;
- łączenie agentów z umiejętnościami i wtyczkami zgodnymi z MCP;
- współpracę wielu agentów w grupach, stronach, projektach i przestrzeniach roboczych;
- planowanie uruchomień oraz pamięć agenta, którą użytkownik może przeglądać i edytować.

Do korzystania z wybranego dostawcy modeli może być potrzebny jego klucz API. Pełny opis funkcji i aktualne wymagania są w [dokumentacji LobeHub](https://lobehub.com/docs). Instrukcje wdrożenia przez Vercel lub zwykły Docker z README upstream dotyczą innych metod instalacji; na YunoHost używaj poleceń powyżej.

## Jak pakiet śledzi upstream

Pakiet uruchamia oficjalny obraz Docker LobeHub w wersji zapisanej w `conf/docker-compose.yml`. Pliki specyficzne dla YunoHost, w tym skrypty instalacji, aktualizacji, kopii i przywracania, są utrzymywane tutaj. Nie są automatycznie zastępowane plikami z projektu głównego.

Workflow [Update LobeHub upstream](.github/workflows/update-upstream.yml) sprawdza codziennie najnowsze stabilne wydanie LobeHub. Gdy ukaże się nowa wersja, `tools/update-upstream` aktualizuje numer pakietu, tag obrazu i informacje o wydaniu w tym README. Przed zapisaniem zmiany workflow sprawdza konfigurację Compose, przywracanie SQL oraz dostępność wszystkich obrazów na `amd64` i `arm64`. Jeśli kontrola nie przejdzie, aktualizacja nie jest publikowana.

Aktualizację można też przygotować ręcznie:

```bash
tools/update-upstream
```

Zmiany działania aplikacji w nowym wydaniu upstream mogą wymagać osobnej adaptacji pakietu YunoHost. Wynik automatycznych kontroli nie zastępuje próby aktualizacji na instancji testowej przed wdrożeniem na serwerze z danymi.

## Odnośniki do projektu głównego

- [Repozytorium i pełne README](https://github.com/lobehub/lobehub)
- [Dokumentacja samodzielnego hostowania](https://lobehub.com/docs/self-hosting/platform/docker-compose)
- [Dokumentacja konfiguracji](https://lobehub.com/docs)
- [Lista wydań](https://github.com/lobehub/lobehub/releases)
