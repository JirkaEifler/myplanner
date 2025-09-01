# MyPlanner

> Komplexní webová aplikace pro správu osobních úkolů vytvořená s Django a PostgreSQL

![License](https://img.shields.io/badge/license-Proprietary-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue)

## Přehled

MyPlanner je plnohodnotná aplikace pro správu úkolů, která kombinuje sílu Django server-side renderingu s moderní REST API architekturou. Aplikace umožňuje uživatelům organizovat svou práci prostřednictvím přizpůsobitelných seznamů úkolů, systémů priorit, tagování a integrovaných kalendářních událostí.

### Klíčové možnosti

- **Kompletní správa úkolů**: Vytváření, organizace a sledování úkolů s pokročilým filtrováním a vyhledáváním
- **Flexibilní organizace**: Vlastní seznamy a opakovaně použitelné barevně kódované tagy pro personalizovaný workflow
- **Řízení času**: Termíny splnění, připomínky a volitelná integrace kalendářních událostí
- **Duální architektura**: Tradiční webové rozhraní plus REST API pro budoucí mobilní/frontend integrace
- **Funkce pro spolupráci**: Komentáře k úkolům a sdílené organizační nástroje

## Funkcionalita

### 🔐 Autentifikace a bezpečnost
- Bezpečná registrace a autentifikace uživatelů pomocí vestavěného Django systému
- Session-based autentifikace s CSRF ochranou
- Řízení přístupu na základě rolí pro chráněné zdroje

### 📝 Správa úkolů
- **Kompletní CRUD operace**: Vytváření, čtení, aktualizace a mazání úkolů s komplexní validací formulářů
- **Správa stavu**: Real-time přepínání dokončení úkolů pomocí AJAX
- **Organizační nástroje**: Přiřazování úkolů do vlastních seznamů a aplikace více tagů
- **Systém priorit**: Víceúrovňové přiřazování priorit pro efektivní třídění úkolů
- **Sledování termínů**: Správa termínů splnění s vizuálními indikátory
- **Kolaborativní poznámky**: Připojování komentářů pro týmovou spolupráci nebo osobní poznámky

### 📂 Organizace seznamů
- **Vlastní seznamy**: Vytváření neomezených personalizovaných seznamů úkolů pro různé projekty nebo kontexty
- **Správa seznamů**: Úprava vlastností seznamů, zobrazení souhrnů úkolů a správa workflow specifických pro seznamy
- **Hierarchická organizace**: Organizace úkolů v rámci seznamů pro lepší projektové řízení

### 🏷️ Systém tagů
- **Flexibilní tagování**: Vytváření a opakované použití tagů napříč všemi úkoly
- **Vizuální organizace**: Barevně kódovaný systém tagů pro rychlou vizuální identifikaci
- **Správa tagů**: Centralizovaná administrace tagů s hromadnými operacemi

### ⚙️ Pokročilé nastavení
- **Administrace tagů**: Komplexní rozhraní pro správu tagů
- **Hromadné operace**: Výběr a mazání více tagů efektivně
- **Správa dat**: Nástroje pro údržbu čisté databáze

### ⏰ Systém připomínek
- **Vlastní připomínky**: Nastavení časově označených připomínek s personalizovanými poznámkami
- **Integrace s úkoly**: Přímé propojení mezi připomínkami a konkrétními úkoly
- **Správa připomínek**: Vytváření, úprava a mazání připomínek podle potřeby

### 📅 Integrace událostí
- **Kalendářní události**: Propojení úkolů s kalendářními událostmi včetně času začátku a konce
- **Správa událostí**: Kompletní CRUD operace pro plánování událostí
- **Prevence duplikátů**: Systém zabraňuje více událostem na úkol pro integritu dat

### 🔍 Pokročilé filtrování
- **Vícekriteriální vyhledávání**: Filtrování úkolů podle textového obsahu, přiřazení seznamu, úrovně priority a stavu dokončení
- **Filtrování podle tagů**: Výběr více tagů pro přesné vyhledání úkolů
- **Zobrazení výsledků**: Čisté, tabulkové prezentování filtrovaných výsledků

### 🌐 REST API
- **Kompletní API pokrytí**: Plné CRUD endpointy pro všechny hlavní entity (Seznamy, Úkoly, Připomínky, Události, Tagy)
- **Vyžadována autentifikace**: Bezpečný přístup k API s oprávněními založenými na uživatelích
- **Pokročilé funkce**: Vestavěné stránkování, možnosti vyhledávání a flexibilní řazení výsledků
- **Připraveno pro integraci**: Navrženo pro budoucí mobilní aplikace nebo React frontend integraci

## Technická architektura

### Backend stack
- **Framework**: Django 5.x s Django REST Framework
- **Databáze**: PostgreSQL 14+ (s SQLite fallback pro vývoj)
- **Autentifikace**: Vestavěný autentifikační systém Django
- **API**: RESTful API architektura s komplexní serializací

### Frontend implementace
- **Šablony**: Django template systém s vlastními template tagy a filtry
- **Stylování**: Vlastní CSS s principy responzivního designu
- **Interaktivita**: JavaScript pro AJAX funkcionalitu a dynamické uživatelské interakce
- **Uživatelský zážitek**: Postupné vylepšování s graceful degradation

### Zajištění kvality
- **Testovací framework**: Pytest s komplexním pokrytím testy
- **Test fixtures**: Předkonfigurovaná testovací data pro uživatele, úkoly a seznamy
- **Validace**: Validace formulářů a testování API endpointů

## Instalace a nastavení

### Požadavky

Ujistěte se, že vaše vývojové prostředí obsahuje:

- **Python**: Verze 3.11 nebo vyšší
- **PostgreSQL**: Verze 14 nebo vyšší (doporučeno)
- **Virtuální prostředí**: Python venv nebo virtualenv

### Rychlý start

1. **Nastavení repozitáře**
   ```bash
   git clone https://github.com/your-username/myplanner.git
   cd myplanner
   ```

2. **Konfigurace prostředí**
   ```bash
   # Vytvoření virtuálního prostředí
   python -m venv env
   
   # Aktivace virtuálního prostředí
   # Na macOS/Linux:
   source env/bin/activate
   # Na Windows:
   env\Scripts\activate
   ```

3. **Instalace závislostí**
   ```bash
   pip install -r requirements.txt
   ```

### Konfigurace databáze

#### Možnost A: PostgreSQL (doporučeno)

1. **Vytvoření databáze**
   ```sql
   -- V PostgreSQL konzoli
   CREATE DATABASE my_planner_db;
   ```

2. **Konfigurace prostředí**
   ```bash
   # Kopírování šablony prostředí
   cp .env.example .env
   ```

3. **Konfigurace nastavení databáze**
   
   Upravte soubor `.env` s vašimi PostgreSQL přihlašovacími údaji:
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=my_planner_db
   DB_USER=postgres
   DB_PASSWORD=vase_bezpecne_heslo
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

#### Možnost B: SQLite (fallback pro vývoj)

Pokud není nakonfigurován soubor `.env`, aplikace se automaticky přepne na SQLite s lokálním souborem `db.sqlite3` v kořenovém adresáři projektu.

### Inicializace aplikace

1. **Migrace databáze**
   ```bash
   python manage.py migrate
   ```

2. **Vytvoření administrátorského uživatele** (volitelné)
   ```bash
   python manage.py createsuperuser
   ```

3. **Vývojový server**
   ```bash
   python manage.py runserver
   ```

   Přístup k aplikaci na: `http://127.0.0.1:8000/`

## Struktura aplikace

### Trasy webového rozhraní

| Trasa | Popis |
|-------|-------|
| `/` | Úvodní stránka a autentifikace |
| `/app/tasks/` | Hlavní rozhraní pro správu úkolů |
| `/app/lists/` | Vytváření a správa seznamů |
| `/app/filters/` | Pokročilé nástroje pro filtrování úkolů |
| `/app/settings/` | Správa tagů a hromadné operace |
| `/admin/` | Django administrační rozhraní |

### REST API endpointy

Všechny API endpointy vyžadují autentifikaci a mají prefix `/api/`.

| Endpoint | Metody | Popis |
|----------|--------|-------|
| `/api/type-lists/` | GET, POST | Seznam a vytváření seznamů úkolů |
| `/api/type-lists/<id>/` | GET, PUT, PATCH, DELETE | Operace s jednotlivými seznamy |
| `/api/tasks/` | GET, POST | Seznam a vytváření úkolů |
| `/api/tasks/<id>/` | GET, PUT, PATCH, DELETE | Operace s jednotlivými úkoly |
| `/api/reminders/` | GET, POST | Seznam a vytváření připomínek |
| `/api/reminders/<id>/` | GET, PUT, PATCH, DELETE | Operace s jednotlivými připomínkami |
| `/api/events/` | GET, POST | Seznam a vytváření událostí |
| `/api/events/<id>/` | GET, PUT, PATCH, DELETE | Operace s jednotlivými událostmi |
| `/api/tags/` | GET, POST | Seznam a vytváření tagů |
| `/api/tags/<id>/` | GET, PUT, PATCH, DELETE | Operace s jednotlivými tagy |
| `/api-auth/` | GET, POST | DRF autentifikační rozhraní |

### Funkce API

- **Stránkování**: Konfigurovatelná velikost stránky pro velké datasety
- **Vyhledávání**: Full-text vyhledávání napříč relevantními poli
- **Řazení**: Flexibilní řazení výsledků podle více kritérií
- **Filtrování**: Filtrování založené na query parametrech

## Vývoj

### Struktura projektu

```
myplanner/
├── my_planner_project/          # Konfigurace Django projektu
│   ├── settings.py             # Nastavení aplikace
│   ├── urls.py                 # Konfigurace kořenových URL
│   └── wsgi.py                 # WSGI vstupní bod aplikace
├── planner/                    # Hlavní modul aplikace
│   ├── models.py              # Datové modely (Task, List, Tag, atd.)
│   ├── views_html.py          # Tradiční HTML views
│   ├── views.py               # REST API views
│   ├── forms.py               # Django formuláře pro HTML rozhraní
│   ├── serializers.py         # DRF serializery pro API
│   ├── urls_html.py           # URL vzory pro HTML rozhraní
│   ├── urls.py                # URL vzory pro API
│   ├── templatetags/          # Vlastní template filtry
│   ├── templates/planner/     # HTML šablony
│   ├── static/planner/        # CSS a JavaScript assety
│   └── tests/                 # Testovací sada
├── requirements.txt           # Python závislosti
├── manage.py                 # Django management script
└── README.md                 # Tento soubor
```

### Spouštění testů

Spuštění kompletní testovací sady:

```bash
pytest
```

Testovací sada zahrnuje:
- **Testování modelů**: Validace datových modelů a vztahů
- **Testování views**: Validace HTTP odpovědí pro HTML i API endpointy
- **Testování formulářů**: Validace vstupů a zpracování chyb
- **Integrační testování**: Validace end-to-end workflow

### Kvalita kódu

Projekt dodržuje Django best practices včetně:

- **Bezpečnost**: CSRF ochrana, prevence SQL injection, XSS mitigace
- **Výkon**: Optimalizované databázové dotazy a efektivní template rendering
- **Udržitelnost**: Jasné oddělení zodpovědností mezi HTML views a API endpointy
- **Škálovatelnost**: Database-agnostický design s PostgreSQL optimalizací

## Úvahy o nasazení

### Konfigurace bezpečnosti

Před nasazením do produkce:

1. **Správa tajného klíče**
   - Přesuňte `SECRET_KEY` do environment proměnných
   - Použijte kryptograficky bezpečné generování klíčů

2. **Debug konfigurace**
   - Nastavte `DEBUG = False` v produkčním nastavení
   - Nakonfigurujte vhodné `ALLOWED_HOSTS`

3. **Bezpečnost databáze**
   - Používejte silné, unikátní databázové přihlašovací údaje
   - Vyhněte se výchozím PostgreSQL uživatelům v produkci
   - Implementujte správnou síťovou bezpečnost pro přístup k databázi

### Optimalizace výkonu

- Nakonfigurujte servírování statických souborů pro produkci
- Implementujte databázové connection pooling
- Zvažte caching strategie pro často přistupovaná data
- Optimalizujte databázové dotazy s select_related/prefetch_related

## Přispívání

Toto je proprietární software. Pro pokyny k přispívání a licenční informace prosím kontaktujte autora.

## Licence

© 2025 Jiří Eifler. Všechna práva vyhrazena.

Tento projekt je proprietární software. Žádná část tohoto repozitáře nesmí být kopírována, upravována, distribuována nebo používána bez výslovného písemného povolení autora.

## Podpora

Pro technickou podporu nebo žádosti o nové funkce prosím kontaktujte vývojový tým prostřednictvím příslušných kanálů ustanovených pro tento projekt.