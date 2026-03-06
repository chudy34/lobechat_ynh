# LobeHub v2 — Full Self-Hosted Stack

LobeHub v2 to kompletna platforma AI Agent Workspace z pełnym backendem serwerowym.

## Stack (v2.1.38)

| Usługa | Obraz Docker | Rola |
|--------|-------------|------|
| **LobeHub** | `lobehub/lobehub:latest` | Główna aplikacja (Next.js 16 + React 19) |
| **ParadeDB** | `paradedb/paradedb:latest-pg17` | PostgreSQL 17 + pgvector + pg_search (RAG) |
| **RustFS** | `rustfs/rustfs:latest` | S3-compatible storage (nowy w v2, zastąpił MinIO) |
| **Redis** | `redis:7-alpine` | Cache sesji i rate limiting |
| **SearXNG** | `searxng/searxng:latest` | Wbudowana prywatna wyszukiwarka |

## Co nowego w v2 vs v1

- **Brak osobnego Casdoor** — autentykacja wbudowana w NextAuth (prostszy setup)
- **RustFS zamiast MinIO** — lżejszy, szybszy S3-compatible storage napisany w Rust
- **ParadeDB zamiast pgvector** — PostgreSQL z pełnotekstowym wyszukiwaniem i wektorami
- **Telegram bot access** — nowe w v2.1.38
- **Group Chat + Multi-Agent** — orkiestracja wielu agentów
- **MCP Marketplace** — 10,000+ pluginów
- **GPT-5.4, Gemini 3.1** — wsparcie najnowszych modeli

## Funkcje

- ✅ Multi-user z serwerową bazą danych
- ✅ Knowledge Base (RAG) — upload PDF, Word, TXT, i chat z dokumentami
- ✅ 50+ dostawców LLM (OpenAI, Claude, Gemini, Ollama, DeepSeek, Groq...)
- ✅ MCP Marketplace (10,000+ pluginów)
- ✅ Multi-agent orkiestracja
- ✅ Artifacts (kod, wykresy, dokumenty)
- ✅ Generowanie obrazów
- ✅ TTS / STT
- ✅ Wbudowany web search (SearXNG)
- ✅ File uploads do 200MB
- ✅ Sync między urządzeniami

## Wymagania

- min. 2GB RAM (zalecane 4GB)
- min. 5GB wolnego miejsca
- Docker
- YunoHost 11.2+
- amd64 lub arm64
