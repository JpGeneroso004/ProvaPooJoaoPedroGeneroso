# 🎪 Art.Tendas — Sistema de Gestão de Eventos

Sistema web completo para gerenciar eventos, inventário de tendas e conjuntos de palco/piso da empresa Art.Tendas, desenvolvido com Python e Django.

---

## 📋 O que o programa faz

- **Gestão de Eventos** — cadastrar, editar e acompanhar eventos com data, local, cliente e status
- **Inventário de Tendas** — controle das tendas (3×3 a 10×10 m) com código gerado automaticamente, tipo e status
- **Conjuntos de Palco/Piso** — gerenciar conjuntos de 1 a 30 placas com status de disponibilidade
- **Mapa Interativo** — visualização geográfica dos eventos (OpenStreetMap / Leaflet)
- **Dashboard (Início)** — painel com estatísticas, próximos eventos e eventos em andamento

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.12 (recomendado) instalado com "Add Python to PATH" marcado

### Passo a passo

```bash
# 1. Entrar na pasta do projeto
cd ProvaJP

# 2. Instalar dependências
pip install django pillow

# 3. Criar o banco de dados
python manage.py makemigrations inventario
python manage.py makemigrations eventos
python manage.py migrate

# 4. Popular com dados de demonstração
python manage.py seed_data

# 5. Iniciar o servidor
python manage.py runserver
```

Acesse **http://127.0.0.1:8000** no navegador.

---

## 🧩 Conceitos de Orientação a Objetos utilizados

### 1. Classes e Objetos
Três classes principais representam as entidades do sistema:
- `Tenda` — representa uma tenda do estoque com tamanho, tipo e status
- `ConjuntoPalco` — representa um conjunto de palco/piso com N placas
- `Evento` — representa um evento com cliente, datas e equipamentos alocados

### 2. Herança
Todas as classes herdam de `django.db.models.Model`, que fornece os comportamentos base de persistência, consulta e validação. O campo customizado `DataBRField` herda de `forms.Field` para criar um widget de data próprio (DD/MM/AAAA).

### 3. Encapsulamento
Métodos internos encapsulam lógica que não deve ser exposta diretamente:
- `get_status_class()` — encapsula a lógica de mapeamento de status para classe CSS
- `total_tendas()` e `total_placas()` — encapsulam o cálculo de equipamentos de um evento
- `save()` sobrescrito em `Tenda` — encapsula a geração automática do código (T-001, T-002...)

### 4. Polimorfismo
O método `get_resumo()` existe nas três classes com comportamentos distintos:

```python
# Tenda
def get_resumo(self):
    return f'Tenda {self.codigo} | {self.get_tamanho_display()} {self.get_tipo_display()} | {self.get_status_display()}'

# ConjuntoPalco
def get_resumo(self):
    return f'{self.nome} | {self.quantidade_placas} placa(s) | {self.get_status_display()}'

# Evento
def get_resumo(self):
    return f'Evento: {self.nome} | Cliente: {self.cliente} | {self.data_inicio} → {self.data_fim} | {self.get_status_display()}'
```

O mesmo nome de método, chamado em objetos diferentes, produz resultados diferentes — polimorfismo em ação.

### 5. Composição e Associação entre classes
`Evento` se associa a `Tenda` e `ConjuntoPalco` via relacionamento ManyToMany — um evento pode ter várias tendas e vários conjuntos, e cada tenda/conjunto pode pertencer a vários eventos. Isso é composição real entre objetos do domínio.

### 6. Sobrescrita de método (Override)
- `Tenda.save()` sobrescreve o `save()` herdado de `Model` para adicionar a geração automática de código antes de salvar
- `DataBRField.to_python()` sobrescreve o método da classe pai para converter três campos (dia/mês/ano) em um objeto `date` do Python

---

## 🗂️ Estrutura do projeto

```
ProvaJP/
├── core/               # Configurações Django (settings, urls, wsgi)
├── eventos/            # App de eventos (models, views, forms, urls)
│   ├── fields.py       # Campo de data customizado (DataBRField)
│   └── management/     # Comando seed_data para dados de demo
├── inventario/         # App de inventário (models, views, forms, urls)
├── templates/          # Templates HTML (base, eventos, inventário)
├── static/             # CSS, JS e imagens
├── manage.py
└── requirements.txt
```

---

Desenvolvido por João Pedro Generoso — Prova de POO
