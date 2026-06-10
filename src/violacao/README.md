# Desafio SOLID - Sistema de E-commerce

## 📋 Descrição do Desafio

Este diretório contém um sistema de e-commerce incompleto que **viola deliberadamente** múltiplos princípios SOLID para fins educacionais.

Seu objetivo é:

1. **Analisar** o código existente em `src/violacao/`
2. **Identificar** quais princípios SOLID estão sendo violados
3. **Refatorar** o código seguindo os princípios SOLID
4. **Mover** as correções para `src/solucao/`
5. **Executar os testes** para garantir que o comportamento foi preservado

---

## 📁 Estrutura do Projeto

```
solid-design/
├── src/
│   ├── violacao/
│   │   ├── __init__.py
│   │   ├── ecommerce.py          # Sistema com violações SOLID
│   │   ├── main.py               # Demonstração do sistema
│   │
│   └── solucao/                 # SEU TRABALHO: Refatoração aqui
│       ├── __init__.py
│       └── ecommerce.py         # Sistema refatorado (SOLID)
│
├── tests/
│   └── test_ecommerce.py       # Testes que validam o comportamento
└── docs/
    ├── fundamentos-design-solid.md
    ├── index.md
    └── slides-solid.md
```

---

## 🔍 Violações Identificadas

### Sistema de E-commerce (src/violacao/ecommerce.py)

#### 1. **Classe `Produto`** - Violação de SRP
- ❌ Gerencia dados do produto
- ❌ Valida preço
- ❌ Calcula desconto
- ❌ Persiste em banco de dados
- ❌ Registra logs

**Solução**: Separar em classes especializadas (Validador, CalculadorDesconto, Repositório, etc)

#### 2. **Classe `Pedido`** - Violação de SRP e DIP
- ❌ Gerencia itens do pedido
- ❌ Calcula total
- ❌ Processa pagamento
- ❌ Envia e-mails
- ❌ Persiste em banco
- ❌ Gera relatórios

**Solução**: Usar injeção de dependência e separar responsabilidades

#### 3. **Método `Pedido.processar_pagamento()`** - Violação de OCP
- ❌ Usa if/elif para cada método de pagamento
- ❌ Adicionar novo método = modificar a classe existente

**Solução**: Usar polimorfismo com classes abstratas

#### 4. **Classe `Estoque`** - Violação de SRP
- ❌ Gerencia quantidade em estoque
- ❌ Valida disponibilidade
- ❌ Persiste em banco
- ❌ Envia alertas
- ❌ Registra movimentações

**Solução**: Separar responsabilidades

#### 5. **Classe `SistemaNotificacao`** - Violação de ISP
- ❌ Interface genérica com múltiplos métodos
- ❌ Classes são forçadas a usar métodos que não precisam

**Solução**: Segregar em interfaces específicas

#### 6. **Classe `GerenciadorPedidos`** - Violação de DIP
- ❌ Altamente acoplada a implementações concretas
- ❌ Difícil de testar (não pode usar mocks)

**Solução**: Depender de abstrações, não de implementações

---

## 🧪 Como Usar os Testes

### Executar testes do código original (com violações)

```bash
python tests/test_ecommerce.py
```

Este comando executará todos os testes para validar que o sistema funciona conforme esperado.

### Executar testes do código refatorado (sua solução)

```bash
python tests/test_ecommerce.py
```

Sua tarefa é criar uma versão refatorada que **passa em todos os testes** mantendo o comportamento do sistema.

---

## 🚀 Passo a Passo

### 1. Analise o código violado

```bash
# Leia o arquivo ecommerce.py em src/violacao/
# Observe os comentários indicando as violações SOLID
```

### 2. Execute o sistema original

```bash
cd src/violacao
python main.py
```

Veja como o sistema funciona com o código acoplado.

### 3. Execute os testes

```bash
python tests/test_ecommerce.py
```

Todos os 16 testes devem passar. Estes são os requisitos que sua solução deve manter.

### 4. Crie a estrutura da solução

```bash
mkdir ../solucao
```

Se preferir, você pode usar os mesmos testes compartilhados em `tests/test_ecommerce.py` sem copiar o arquivo.

### 5. Refatore o código

Crie `src/solucao/ecommerce.py` refatorando as classes:

**Exemplo de refatoração** (não é código completo, apenas ilustração):

```python
# ANTES (SRP violado - múltiplas responsabilidades)
class Pedido:
    def processar_pagamento(self, metodo):
        if metodo == "cartao":
            # lógica
        elif metodo == "boleto":
            # lógica

# DEPOIS (SRP aplicado - responsabilidades separadas)
from abc import ABC, abstractmethod

class MetodoPagamento(ABC):
    @abstractmethod
    def processar(self, pedido):
        pass

class PagamentoCartao(MetodoPagamento):
    def processar(self, pedido):
        # lógica do cartão

class PagamentoBoleto(MetodoPagamento):
    def processar(self, pedido):
        # lógica do boleto

class Pedido:
    def __init__(self, metodo_pagamento: MetodoPagamento):
        self.metodo_pagamento = metodo_pagamento
    
    def processar_pagamento(self):
        self.metodo_pagamento.processar(self)  # OCP: aberto para extensão!
```

### 6. Execute os testes na sua solução

```bash
python tests/test_ecommerce.py
```

Todos os testes devem passar!

### 7. Crie um Pull Request

Quando terminar:

1. Crie uma branch: `git checkout -b feature/refatoracao-seu-nome`
2. Faça commit das mudanças
3. Faça push: `git push origin feature/refatoracao-seu-nome`
4. Abra um Pull Request com a descrição das refatorações realizadas

---

## 📋 Checklist de Refatoração

- [ ] **SRP**: Cada classe tem uma única responsabilidade
- [ ] **OCP**: Sistema aberto para extensão, fechado para modificação
- [ ] **LSP**: Herança aplicada corretamente (se usada)
- [ ] **ISP**: Interfaces são específicas, não genéricas
- [ ] **DIP**: Código depende de abstrações, não de implementações
- [ ] **Testes**: Todos os 16 testes passam
- [ ] **Funcionalidade**: O sistema funciona igual ao original
- [ ] **Documentação**: Código comentado explicando as melhorias

---

## 💡 Dicas

1. **Use classes abstratas** (`ABC` do módulo `abc`)
2. **Injeção de dependência** para desacoplar classes
3. **Interfaces segregadas** para responsabilidades específicas
4. **Polimorfismo** em vez de if/elif
5. **Composição** em vez de herança quando apropriado

---

## 📚 Referências

Consulte o arquivo `docs/fundamentos-design-solid.md` para exemplos e explicações detalhadas de cada princípio SOLID.

---

## ❓ Dúvidas?

Se tiver dúvidas sobre os princípios SOLID, revise:
- Cada violação está documentada com comentários no código
- A documentação em `docs/fundamentos-design-solid.md`
- Os exemplos de código em cada seção do guia

**Bom trabalho! 🚀**
