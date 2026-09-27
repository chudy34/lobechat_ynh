# LobeHub dla YunoHost

> Pakiet YunoHost dla [LobeHub](https://github.com/lobehub/lobehub). Ta instrukcja dotyczy instalacji z tego repozytorium.

## 🚀 Instalacja i aktualizacja na YunoHost

Zainstaluj lub zaktualizuj aplikację z głównej gałęzi pakietu:

```bash
sudo yunohost app install https://github.com/chudy34/lobechat_ynh
sudo yunohost app upgrade lobehub -u https://github.com/chudy34/lobechat_ynh
```

Przed aktualizacją instancji z danymi wykonaj kopię zapasową YunoHost i sprawdź, czy można ją odczytać. Pakiet korzysta z Docker CE i Compose v2. Instalator przygotowuje także PostgreSQL/ParadeDB, RustFS, Redis oraz SearXNG. Ustawienia i dane pozostają na serwerze YunoHost; to repozytorium zawiera tylko pliki pakietu.

### Co instaluje ten pakiet

| Składnik | Rola |
| --- | --- |
| LobeHub | Interfejs i funkcje agentów AI |
| PostgreSQL/ParadeDB | Baza danych i wyszukiwanie |
| RustFS | Przechowywanie plików |
| Redis | Usługi pomocnicze |
| SearXNG | Wyszukiwanie w sieci |

Ten pakiet nie konfiguruje automatycznie kluczy API dostawców modeli. Sposób podania klucza zależy od wybranego dostawcy i konfiguracji LobeHub.

### Ważne przy aktualizacji

Aktualizacje z tego repozytorium zmieniają pakiet YunoHost oraz przypięty obraz LobeHub. Dane są przechowywane w katalogu danych aplikacji na serwerze. Przed wdrożeniem nowej wersji na instancji z ważnymi danymi przetestuj ją na osobnej instancji i zachowaj działającą kopię zapasową.

---

<div align="center">

[![Baner LobeHub](https://github.com/user-attachments/assets/5f78ae58-ed4f-4d38-8037-96109fbba58c)](https://github.com/lobehub/lobehub/blob/canary/README.md)

**LobeHub — przestrzeń do tworzenia i organizowania agentów AI**

[Projekt główny](https://github.com/lobehub/lobehub) · [Dokumentacja](https://lobehub.com/docs) · [Wydania](https://github.com/lobehub/lobehub/releases)

</div>

Grafiki w dalszej części pochodzą z [README projektu LobeHub](https://github.com/lobehub/lobehub/blob/canary/README.md) i są ładowane z adresów projektu głównego. Ilustrują gałąź `canary`, więc mogą pokazywać funkcje lub wygląd nowsze od wersji zapakowanej dla YunoHost.

## Aktualna wersja upstream

- Repository: `https://github.com/lobehub/lobehub`
- Release: `v2.2.18`
- Docker image: `lobehub/lobehub:2.2.18`
- LobeHub version: `2.2.18`
- Licencja upstream: [LobeHub Community License](https://github.com/lobehub/lobehub/blob/v2.2.18/LICENSE)

## ✨ Funkcje LobeHub

LobeHub służy do tworzenia agentów AI i organizowania ich pracy w jednym miejscu. Opis poniżej streszcza [README projektu głównego](https://github.com/lobehub/lobehub/blob/canary/README.md).

### Operator — praca agentów w jednym miejscu

Możesz organizować zadania agentów, planować ich uruchomienia i przeglądać wyniki pracy.

![Widok operatora LobeHub](https://github.com/user-attachments/assets/7b08d6d9-9dff-4b06-a919-324630554509)

### Create — tworzenie agentów

Kreator agentów pomaga skonfigurować ich zadania, modele i narzędzia. LobeHub obsługuje różne modele i typy treści oraz umiejętności i wtyczki zgodne z MCP.

![Kreator agentów LobeHub](https://github.com/user-attachments/assets/949b8166-486d-4750-ad7a-cfe7bfcb84e3)

### Collaborate — współpraca agentów

Grupy agentów, strony, projekty i przestrzenie robocze pozwalają prowadzić pracę w uporządkowany sposób.

![Współpraca agentów w LobeHub](https://github.com/user-attachments/assets/e51526c6-e09c-4a5a-9cec-dcd3fd68a3a8)

### Evolve — pamięć i dopasowanie

Pamięć osobista pomaga agentom zachować kontekst. Użytkownik może przeglądać i edytować zapamiętane informacje.

![Pamięć osobista w LobeHub](https://github.com/user-attachments/assets/5c6e16f0-7f47-4baf-9aeb-3a00deb8ff5b)

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
