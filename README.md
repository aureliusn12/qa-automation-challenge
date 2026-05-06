# QA Automation Challenge

[![QA Pipeline](https://github.com/YOUR_USERNAME/qa-automation-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/qa-automation-challenge/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Selenium](https://img.shields.io/badge/selenium-4.18-green)
![pytest](https://img.shields.io/badge/pytest-7.4-orange)

Projeto de automação de testes com duas suítes independentes no mesmo repositório:

- **API Automation** — REST API (Swagger Petstore)
- **Web Automation** — E2E (SauceDemo) com Page Object Model

---

## Tecnologias

| Categoria | Tecnologia |
|-----------|------------|
| Linguagem | Python 3.11 |
| Framework | pytest 7.4 |
| Automação API | requests, jsonschema, Faker, python-dotenv |
| Automação Web | Selenium 4, webdriver-manager |
| Padrão Web | Page Object Model (POM) |
| Padrão API | Service Layer Pattern |
| Qualidade | flake8 |
| Relatórios | pytest-html, allure-pytest |
| CI/CD | GitHub Actions |

---

## Arquitetura

```
qa-automation-challenge/
│
├── api_tests/
│   ├── tests/           → Casos de teste (test_pet, test_user, test_store)
│   ├── services/        → Service Layer — encapsula chamadas HTTP
│   │   ├── base_service.py      → Injeção de RequestHelper
│   │   ├── pet_service.py       → CRUD /pet
│   │   ├── user_service.py      → CRUD /user + login
│   │   └── store_service.py     → Inventory + Orders
│   ├── schemas/         → JSON Schema para validação de contrato
│   ├── fixtures/        → Fixtures de dados reutilizáveis
│   ├── utils/
│   │   ├── request_helper.py    → HTTP client com logging centralizado
│   │   └── logger.py
│   ├── data/
│   │   └── generators.py        → Faker: Pet, User, Order dinâmicos
│   └── conftest.py      → Services (session-scoped) + recursos (function-scoped)
│
├── web_tests/
│   ├── tests/
│   │   ├── test_login.py        → Login positivo e negativo
│   │   ├── test_cart.py         → Gerenciamento do carrinho
│   │   └── test_checkout_e2e.py → Fluxo completo de compra
│   ├── pages/           → Page Object Model
│   │   ├── base_page.py         → Waits, click, type, screenshot
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   ├── checkout_step_one_page.py
│   │   ├── checkout_step_two_page.py
│   │   └── checkout_complete_page.py
│   ├── fixtures/        → Page Object factories
│   ├── utils/
│   │   ├── driver_factory.py    → Chrome com suporte a headless
│   │   └── logger.py
│   ├── data/
│   │   └── test_data.py         → Credenciais e dados de teste
│   └── conftest.py      → driver fixture + logged_in_driver + screenshot on failure
│
├── .github/
│   └── workflows/
│       └── ci.yml       → lint → api-tests | web-tests (paralelo)
│
├── conftest.py          → sys.path setup para imports absolutos
├── pytest.ini
└── requirements.txt
```

---

## Page Object Model

Cada página da aplicação tem uma classe dedicada. Locators são atributos da classe. Os testes nunca interagem com o Selenium diretamente.

```
Test → InventoryPage.add_product("Sauce Labs Backpack")
     → BasePage.click((By.ID, "add-to-cart-sauce-labs-backpack"))
     → WebDriverWait.until(element_to_be_clickable)
     → element.click()
```

**BasePage** fornece os blocos fundamentais:

| Método | Comportamento |
|--------|--------------|
| `find(locator)` | Aguarda presença com `WebDriverWait` |
| `find_clickable(locator)` | Aguarda elemento clicável |
| `click(locator)` | Espera clicável, depois clica |
| `type_text(locator, text)` | Limpa e digita |
| `is_visible(locator)` | Retorna `bool` — nunca levanta exceção |
| `take_screenshot(name)` | Salva em `screenshots/` |

---

## Pré-requisitos

- Python 3.11+
- Google Chrome instalado
- pip atualizado

---

## Instalação

```bash
git clone https://github.com/YOUR_USERNAME/qa-automation-challenge.git
cd qa-automation-challenge

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
cp .env.example .env
```

---

## Executando os Testes

### API Tests

```bash
# Toda a suíte
pytest api_tests/tests/ -v

# Por módulo
pytest api_tests/tests/test_pet.py -v
pytest api_tests/tests/test_user.py -v
pytest api_tests/tests/test_store.py -v

# Com relatório HTML
pytest api_tests/tests/ -v --html=reports/api-report.html --self-contained-html
```

### Web Tests

```bash
# Toda a suíte
pytest web_tests/tests/ -v

# Headless (para CI ou sem interface)
HEADLESS=true pytest web_tests/tests/ -v

# Por arquivo
pytest web_tests/tests/test_login.py -v
pytest web_tests/tests/test_cart.py -v
pytest web_tests/tests/test_checkout_e2e.py -v

# Com relatório HTML
pytest web_tests/tests/ -v --html=reports/web-report.html --self-contained-html
```

### Todas as suítes

```bash
pytest api_tests/tests/ web_tests/tests/ -v
```

---

## Cobertura de Testes

### API — Swagger Petstore (`https://petstore.swagger.io/v2`)

| Arquivo | Classe | Cenários |
|---------|--------|----------|
| `test_pet.py` | `TestPetCreate` | create 200, schema, name/status match, integer id |
| | `TestPetRead` | get by id, 404 not found, findByStatus filter |
| | `TestPetUpdate` | update 200, name change, schema |
| | `TestPetDelete` | delete 200, deleted → 404, nonexistent → 404 |
| `test_user.py` | `TestUserCreate` | create 200, response code, múltiplos users |
| | `TestUserRead` | get 200, schema, username/email match, 404 |
| | `TestUserSession` | login 200, token no response |
| | `TestUserUpdate` | update 200, email persiste |
| | `TestUserDelete` | delete 200, deleted → 404, nonexistent → 404 |
| `test_store.py` | `TestStoreInventory` | 200, schema, dict não vazio, valores int |
| | `TestStoreOrder` | place order, schema, status, petId, get, delete |

### Web — SauceDemo (`https://www.saucedemo.com`)

| Arquivo | Classe | Cenários |
|---------|--------|----------|
| `test_login.py` | `TestLogin` | login ok, título, locked user, credenciais vazias |
| `test_cart.py` | `TestCart` | add 1/2 produtos, remover, contagem, nome no carrinho |
| `test_checkout_e2e.py` | `TestCheckoutE2E` | fluxo completo, header, validações de campos obrigatórios |

---

## Pipeline CI/CD

```
push/PR
   │
   ├── lint (flake8)
   │      │
   ├──────┼─── api-tests (ubuntu, Python 3.11)
   │      │         └── artifact: api-report.html
   │      │
   └──────┴─── web-tests (ubuntu, Chrome headless)
                     ├── artifact: web-report.html
                     └── artifact: failure-screenshots (somente em falha)
```

---

## Estratégia de Testes

| Princípio | Implementação |
|-----------|--------------|
| Independência | Cada teste cria e limpa seus próprios dados via fixtures com `yield` |
| Dinamismo | Faker elimina conflitos de ID/username entre execuções paralelas |
| Waits inteligentes | `WebDriverWait` + `expected_conditions` — zero `time.sleep()` |
| Validação de contrato | `jsonschema.validate()` valida estrutura além do status code |
| Rastreabilidade | Screenshot automático no teardown do `driver` fixture em caso de falha |
| Separação de responsabilidades | Testes não conhecem Selenium nem `requests` diretamente |
