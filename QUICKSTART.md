# Guia Rápido - Quick Start

## Instalação Rápida

```bash
# Clonar o repositório
git clone https://github.com/Afonstorm800/Projeto_Integra-o.git
cd Projeto_Integra-o

# Instalar dependências
pip install -r requirements.txt
```

## Teste Rápido

Execute o script de teste para verificar se tudo está funcionando:

```bash
python examples/test_system.py
```

## Uso Básico

### 1. Processamento de Dados

```python
from src.data_processing import DataProcessor

processor = DataProcessor()

# Normalizar texto
text = processor.normalize_text("  Hello   World!  ")
# Resultado: "hello world"

# Validar email
is_valid = processor.validate_pattern("user@example.com", 'email')
# Resultado: True

# Normalizar CPF
cpf = processor.normalize_cpf("12345678901")
# Resultado: "123.456.789-01"
```

### 2. Serialização

```python
from src.serialization import SerializationHandler

handler = SerializationHandler()

data = {"name": "Alice", "age": 30}

# Exportar para JSON
handler.export_json(data, 'output.json')

# Exportar para XML
handler.export_xml(data, 'output.xml')

# Exportar para YAML
handler.export_yaml(data, 'output.yaml')

# Converter entre formatos
handler.convert('output.json', 'output_converted.xml')
```

### 3. Pipeline de Jobs

```python
from src.jobs import Job, Pipeline

def meu_job(context):
    print("Executando job...")
    return {"status": "ok"}

pipeline = Pipeline("meu_pipeline")
pipeline.add_job(Job("job1", meu_job))
resultado = pipeline.run()
```

### 4. Acesso a APIs

```python
from src.api import PublicAPIExamples

# Buscar usuário do GitHub
user = PublicAPIExamples.get_github_user("torvalds")
print(user['name'])

# Buscar taxas de câmbio
rates = PublicAPIExamples.get_exchange_rates('USD')
print(rates['rates']['EUR'])
```

### 5. Banco de Dados

```python
from src.database import DatabaseManager

db = DatabaseManager('sqlite:///meu_banco.db')

# Criar tabela
db.execute_query("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        email TEXT
    )
""")

# Inserir dados
db.insert("usuarios", {"id": 1, "nome": "Alice", "email": "alice@example.com"})

# Buscar dados
usuarios = db.select("usuarios")
```

### 6. Operações sobre Valores

```python
from src.utils import ValueOperations

ops = ValueOperations()

# Arredondar
resultado = ops.transform(42.567, "round", {"decimals": 2})
# Resultado: 42.57

# Calcular média
media = ops.aggregate([10, 20, 30, 40], "avg")
# Resultado: 25

# Converter unidades
metros = ops.convert_units(100, "cm", "m")
# Resultado: 1.0
```

## Exemplo Completo

Um exemplo completo está disponível em `examples/complete_example.py`:

```bash
python examples/complete_example.py
```

Este exemplo demonstra:
- Processamento de dados com RE
- Serialização JSON/XML/YAML
- Pipeline de jobs
- Acesso a APIs remotas
- Operações de banco de dados
- Geração de dashboards

## Estrutura dos Dados

Todos os dados gerados ficam na pasta `data/`:
- Arquivos JSON, XML, YAML
- Bancos de dados SQLite
- Logs de execução
- Dashboards HTML

## Próximos Passos

1. Explore os exemplos em `examples/`
2. Leia a documentação completa no `README.md`
3. Adapte os módulos para seu caso de uso
4. Crie seus próprios pipelines de integração

## Suporte

Para dúvidas ou problemas:
1. Consulte o README.md completo
2. Verifique os exemplos
3. Execute os testes: `python examples/test_system.py`
