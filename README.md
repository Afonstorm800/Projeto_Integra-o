# Projeto de Integração de Sistemas

Projeto completo de integração de sistemas de informação com suporte a processamento de dados, serialização, controle de jobs, acesso a APIs remotas, operações de banco de dados e visualização de resultados.

## 📋 Características

Este projeto implementa todos os requisitos essenciais de um sistema de integração:

### ✅ Processamento de Dados com Expressões Regulares
- Normalização de textos e dados
- Limpeza e validação de dados
- Composição e transformação de dados
- Normalização de CPF, CNPJ, telefones, CEP
- Mascaramento de dados sensíveis

### ✅ Serialização de Dados
- Importação/Exportação de **JSON**
- Importação/Exportação de **XML**
- Importação/Exportação de **YAML**
- Conversão entre formatos

### ✅ Sistema de Jobs e Controle de Processos
- Orquestração de workflows
- Gerenciamento de dependências entre jobs
- Pipeline de execução
- Controle de processos múltiplos

### ✅ Acesso a Serviços Remotos
- Cliente HTTP genérico com retry
- Exemplos de APIs públicas
- Suporte a autenticação (Token, API Key)
- Integração com GitHub, APIs de clima, dados aleatórios, etc.

### ✅ Operações de Banco de Dados
- Suporte a SQLite, PostgreSQL, MySQL (via SQLAlchemy)
- Operações CRUD completas
- **Joins** entre tabelas
- **Agrupamentos** (GROUP BY)
- **Lookups** e enriquecimento de dados
- Integração com Pandas DataFrames

### ✅ Operações sobre Valores
- Transformações de valores
- Agregações estatísticas
- Conversão de unidades
- Cálculos de porcentagem e crescimento
- Aplicação de fórmulas
- Normalização e interpolação

### ✅ Sistema de Logging
- Logging configurável
- Suporte a arquivo e console
- Context managers para operações
- Rastreamento de duração de operações

### ✅ Dashboard de Visualização
- Gráficos de linha, barra, pizza
- Scatter plots e heatmaps
- Histogramas e box plots
- Tabelas interativas
- Geração de HTML estático
- Servidor Flask para dashboards interativos

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais
- `requests` - Cliente HTTP para APIs
- `pyyaml` - Suporte a YAML
- `lxml` - Processamento de XML
- `pandas` - Manipulação de dados
- `sqlalchemy` - ORM e acesso a bancos de dados
- `plotly` - Visualizações interativas
- `flask` - Servidor web para dashboards

## 📚 Estrutura do Projeto

```
Projeto_Integra-o/
├── src/
│   ├── data_processing/     # Processamento de dados com RE
│   │   ├── __init__.py
│   │   └── processor.py
│   ├── serialization/       # Import/Export JSON, XML, YAML
│   │   ├── __init__.py
│   │   └── handler.py
│   ├── jobs/                # Controle de Jobs e Pipelines
│   │   ├── __init__.py
│   │   └── controller.py
│   ├── api/                 # Cliente de APIs remotas
│   │   ├── __init__.py
│   │   └── client.py
│   ├── database/            # Operações de banco de dados
│   │   ├── __init__.py
│   │   └── manager.py
│   ├── utils/               # Utilitários (logging, operações)
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── operations.py
│   └── dashboard/           # Visualização de dados
│       ├── __init__.py
│       └── generator.py
├── examples/
│   └── complete_example.py  # Exemplo completo
├── data/                    # Dados gerados
├── requirements.txt         # Dependências
└── README.md               # Esta documentação
```

## 💡 Exemplos de Uso

### 1. Processamento de Dados com Expressões Regulares

```python
from src.data_processing import DataProcessor

processor = DataProcessor()

# Normalizar texto
text = "  Hello   World!  @#$  "
normalized = processor.normalize_text(text)
print(normalized)  # "hello world"

# Validar email
email = "user@example.com"
is_valid = processor.validate_pattern(email, 'email')
print(is_valid)  # True

# Normalizar CPF
cpf = "12345678901"
formatted = processor.normalize_cpf(cpf)
print(formatted)  # "123.456.789-01"

# Mascarar dados sensíveis
sensitive = "My email is john.doe@example.com"
masked = processor.mask_sensitive_data(sensitive, 'email')
print(masked)  # "My email is jo***@example.com"
```

### 2. Serialização de Dados

```python
from src.serialization import SerializationHandler

handler = SerializationHandler()

data = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
}

# Exportar para JSON
handler.export_json(data, 'users.json')

# Exportar para XML
handler.export_xml(data, 'users.xml')

# Exportar para YAML
handler.export_yaml(data, 'users.yaml')

# Importar de JSON
imported = handler.import_json('users.json')

# Converter entre formatos
handler.convert('users.json', 'users_converted.xml')
```

### 3. Sistema de Jobs e Pipelines

```python
from src.jobs import Job, Pipeline

def load_data(context):
    return {"records": [1, 2, 3, 4, 5]}

def process_data(context):
    records = context['job_load_result']['records']
    return {"processed": [x * 2 for x in records]}

def save_data(context):
    processed = context['job_process_result']['processed']
    return {"saved_count": len(processed)}

# Criar pipeline
pipeline = Pipeline("data_pipeline")

# Adicionar jobs com dependências
pipeline.add_job(Job("load", load_data))
pipeline.add_job(Job("process", process_data, depends_on=["load"]))
pipeline.add_job(Job("save", save_data, depends_on=["process"]))

# Executar pipeline
result = pipeline.run()
status = pipeline.get_status_summary()
```

### 4. Acesso a APIs Remotas

```python
from src.api import APIClient, PublicAPIExamples

# Usar cliente genérico
client = APIClient("https://api.example.com")
data = client.get("/endpoint")

# Usar exemplos de APIs públicas
user = PublicAPIExamples.get_github_user("torvalds")
print(f"Name: {user['name']}")

rates = PublicAPIExamples.get_exchange_rates('USD')
print(f"EUR: {rates['rates']['EUR']}")

random_user = PublicAPIExamples.get_random_user()
```

### 5. Operações de Banco de Dados

```python
from src.database import DatabaseManager, DataOperations

# Conectar ao banco
db = DatabaseManager('sqlite:///example.db')

# Criar tabela
db.execute_query("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        category TEXT
    )
""")

# Inserir dados
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics"}
]
db.bulk_insert("products", products)

# Selecionar dados
electronics = db.select("products", conditions={"category": "Electronics"})

# Agrupar dados
grouped = db.group_by(
    "products",
    group_columns=["category"],
    agg_columns={"price": "AVG"}
)

# Joins
joined = db.join("table1", "table2", on="id", join_type="inner")

# Operações avançadas
ops = DataOperations(db)
lookup_result = ops.lookup("main_table", "lookup_table", "id", "id", ["name", "description"])
```

### 6. Operações sobre Valores

```python
from src.utils import ValueOperations

ops = ValueOperations()

# Transformar valor
rounded = ops.transform(42.567, "round", {"decimals": 2})

# Agregar valores
values = [10, 20, 30, 40, 50]
avg = ops.aggregate(values, "avg")

# Aplicar fórmula
data = {"a": 10, "b": 20, "c": 5}
result = ops.apply_formula(data, "(a + b) * c")

# Converter unidades
meters = ops.convert_units(100, "cm", "m")

# Calcular porcentagem
percentage = ops.calculate_percentage(25, 100)

# Taxa de crescimento
growth = ops.calculate_growth_rate(100, 150)
```

### 7. Dashboard de Visualização

```python
from src.dashboard import DashboardGenerator

dashboard = DashboardGenerator()

# Dados de exemplo
sales_data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'sales': [1200, 1400, 1100, 1600]
}

# Criar gráfico de linha
line_chart = dashboard.create_line_chart(
    sales_data,
    x='month',
    y='sales',
    title='Monthly Sales'
)
dashboard.add_figure(line_chart)

# Criar gráfico de pizza
category_data = {
    'category': ['Electronics', 'Furniture', 'Clothing'],
    'revenue': [45000, 25000, 15000]
}
pie_chart = dashboard.create_pie_chart(
    category_data,
    labels='category',
    values='revenue',
    title='Revenue by Category'
)
dashboard.add_figure(pie_chart)

# Gerar dashboard HTML
dashboard.generate_dashboard_html('dashboard.html')
```

### 8. Sistema de Logging

```python
from src.utils import setup_logging, get_logger, LogContext

# Configurar logging
setup_logging(log_file='app.log', level=logging.INFO)
logger = get_logger('MyApp')

# Usar context para operações
with LogContext(logger, "Data Processing"):
    # Código aqui será logado com início, fim e duração
    process_data()
```

## 🎯 Exemplo Completo

Execute o exemplo completo que demonstra todas as funcionalidades:

```bash
python examples/complete_example.py
```

Este exemplo executa:
1. Processamento de dados com expressões regulares
2. Serialização em JSON, XML e YAML
3. Controle de jobs e pipeline
4. Acesso a APIs remotas
5. Operações de banco de dados
6. Operações sobre valores
7. Geração de dashboards
8. Pipeline de integração completo

## 📊 Visualização de Resultados

Após executar os exemplos, você encontrará os seguintes arquivos na pasta `data/`:

- `dashboard.html` - Dashboard com gráficos interativos
- `integration_dashboard.html` - Dashboard do pipeline de integração
- `users.json`, `users.xml`, `users.yaml` - Dados serializados
- `example.db` - Banco de dados SQLite com exemplos
- `integration.log` - Arquivo de log das operações

Abra os arquivos `.html` no navegador para visualizar os dashboards interativos!

## 🔧 Configuração

### Variáveis de Ambiente

Você pode criar um arquivo `.env` para configurações:

```
# Configurações de API
OPENWEATHER_API_KEY=your_api_key_here

# Configurações de Banco de Dados
DATABASE_URL=sqlite:///data/app.db

# Configurações de Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Bancos de Dados Suportados

O projeto suporta diversos bancos via SQLAlchemy:

```python
# SQLite
db = DatabaseManager('sqlite:///path/to/database.db')

# PostgreSQL
db = DatabaseManager('postgresql://user:pass@localhost/dbname')

# MySQL
db = DatabaseManager('mysql://user:pass@localhost/dbname')
```

## 📝 Funcionalidades por Módulo

### data_processing
- ✅ Normalização de texto
- ✅ Validação de padrões (email, CPF, CNPJ, telefone, etc.)
- ✅ Extração com regex
- ✅ Substituição de padrões
- ✅ Limpeza de dados
- ✅ Composição de templates
- ✅ Mascaramento de dados sensíveis

### serialization
- ✅ JSON: import/export
- ✅ XML: import/export
- ✅ YAML: import/export
- ✅ Conversão entre formatos
- ✅ Serialização de strings

### jobs
- ✅ Definição de jobs
- ✅ Pipelines com dependências
- ✅ Controle de execução
- ✅ Status e monitoramento
- ✅ Gerenciamento de contexto
- ✅ ProcessController para múltiplos pipelines

### api
- ✅ Cliente HTTP genérico
- ✅ Suporte a GET, POST, PUT, DELETE, PATCH
- ✅ Retry automático com backoff
- ✅ Autenticação (Bearer Token, API Key)
- ✅ Exemplos de APIs públicas

### database
- ✅ CRUD completo
- ✅ Joins entre tabelas
- ✅ Group By com agregações
- ✅ Lookups
- ✅ Integração com Pandas
- ✅ Bulk operations
- ✅ Operações avançadas de dados

### utils
- ✅ Sistema de logging configurável
- ✅ LogContext para rastreamento
- ✅ Operações sobre valores
- ✅ Agregações estatísticas
- ✅ Conversão de unidades
- ✅ Cálculos matemáticos
- ✅ Transformações de dados

### dashboard
- ✅ Gráficos de linha
- ✅ Gráficos de barra
- ✅ Gráficos de pizza
- ✅ Scatter plots
- ✅ Heatmaps
- ✅ Histogramas
- ✅ Box plots
- ✅ Tabelas
- ✅ Geração de HTML
- ✅ Servidor Flask

## 🤝 Contribuindo

Este é um projeto acadêmico. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Projeto desenvolvido para a disciplina de Integração de Sistemas de Informação.

## 👨‍💻 Autor

Desenvolvido como parte do projeto da disciplina de integração de sistemas de informação.
