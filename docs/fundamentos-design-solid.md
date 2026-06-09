# Princípios SOLID: Engenharia de Software e Design de Código

Bem-vindo ao guia prático sobre os **Princípios SOLID**. No desenvolvimento de software, escrever código que apenas "funciona" não é o suficiente. À medida que os sistemas crescem, códigos mal estruturados tornam-se rígidos, frágeis e difíceis de manter.

Os princípios SOLID resolvem esse problema, servindo como pilares para a criação de sistemas com alta **coesão** e baixo **acoplamento**.

> 💡 **O que é SOLID?**
> SOLID é um acrônimo mnemônico introduzido por Robert C. Martin (Uncle Bob) que reúne 5 práticas recomendadas de design de software orientado a objetos.

---

## O Acrônimo SOLID

1. **S**ingle Responsibility Principle *(Princípio da Responsabilidade Única)*
2. **O**pen/Closed Principle *(Princípio do Aberto/Fechado)*
3. **L**iskov Substitution Principle *(Princípio da Substituição de Liskov)*
4. **I**nterface Segregation Principle *(Princípio da Segregação de Interfaces)*
5. **D**ependency Inversion Principle *(Princípio da Inversão de Dependência)*

---

### 1. Single Responsibility Principle (SRP)

> *"Uma classe deve ter um, e apenas um, motivo para mudar."*

Uma classe deve ser especialista em uma única coisa. Se uma classe possui múltiplas responsabilidades, ela se torna acoplada e qualquer alteração em uma regra de negócio pode quebrar outra parte do sistema involuntariamente.

#### ❌ Violação do SRP

Imagine uma classe `Pedido` que gerencia os dados da compra, calcula o desconto e salva os dados no banco de dados:

```python
class Pedido:
    def __init__(self, itens):
        self.itens = itens

    def calcular_total(self):
        # Lógica de cálculo
        pass

    def salvar_banco_dados(self):
        # Lógica de conexão e persistência SQL (Violação!)
        print("Salvando no banco de dados...")
```

Por que está errado? Se a forma de salvar no banco mudar (ex: de SQL para NoSQL), a classe `Pedido` precisa ser alterada. Se a regra de cálculo mudar, ela também muda.

#### ✔️ Solução Aplicando SRP

Separamos a entidade de negócio da persistência de dados:

```python
class Pedido:
    def __init__(self, itens):
        self.itens = itens

    def calcular_total(self):
        pass

class PedidoRepository:
    def salvar(self, pedido: Pedido):
        # Responsável apenas pela persistência
        print("Salvando no banco de dados...")
```

---

### 2. Open/Closed Principle (OCP)

> "Entidades de software (classes, módulos, funções) devem estar abertas para extensão, mas fechadas para modificação."

Você deve ser capaz de adicionar novos comportamentos ou funcionalidades ao sistema sem precisar alterar o código original que já está testado e funcionando.

#### ❌ Violação do OCP

Uma classe de processamento de pagamentos que usa estruturas condicionais (`if/else`) para cada novo método de pagamento adicionado:

```python
class ProcessadorDePagamento:
    def processar(self, pedido, tipo_pagamento):
        if tipo_pagamento == "boleto":
            # Lógica do boleto
            pass
        elif tipo_pagamento == "cartao_credito":
            # Lógica do cartão
            pass
        # Toda vez que surgir um novo método (ex: Pix), precisaremos MODIFICAR esta classe.
```

#### ✔️ Solução Aplicando OCP

Utilizamos abstração (interfaces ou classes abstratas) para permitir a extensão do comportamento através do polimorfismo:

```python
from abc import ABC, abstractmethod

class MetodoPagamento(ABC):
    @abstractmethod
    def pagar(self, pedido):
        pass

class PagamentoPix(MetodoPagamento):
    def pagar(self, pedido):
        # Nova funcionalidade adicionada por EXTENSÃO
        print("Pagamento via Pix processado.")

class ProcessadorDePagamento:
    def processar(self, pedido, metodo: MetodoPagamento):
        metodo.pagar(pedido)  # Fechado para modificação
```

---

### 3. Liskov Substitution Principle (LSP)

> "Classes derivadas devem poder ser substituídas por suas classes bases sem que o comportamento do programa seja corrompido."

Formulado por Barbara Liskov, este princípio garante que a herança seja usada de forma correta. Se a classe `B` herda de `A`, então qualquer lugar que aceite `A` deve aceitar `B` sem lançar exceções inesperadas ou mudar o comportamento esperado.

#### ❌ Violação do LSP (O clássico caso do Retângulo e Quadrado)

Matematicamente, um quadrado é um retângulo. Mas no design de código, herdar `Quadrado` de `Retangulo` quebra expectativas:

```python
class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def set_largura(self, largura):
        self.largura = largura

    def set_altura(self, altura):
        self.altura = altura

    def calcular_area(self):
        return self.largura * self.altura

class Quadrado(Retangulo):
    def set_largura(self, largura):
        self.largura = largura
        self.altura = largura  # Força os lados a serem iguais

    def set_altura(self, altura):
        self.largura = altura
        self.altura = altura
```

Por que está errado? Se uma função recebe um `Retangulo` e altera sua largura para 5 e altura para 4, ela espera que a área seja 20. Se passarmos um `Quadrado` por polimorfismo, a área será 16. O comportamento foi corrompido.

#### ✔️ Solução Aplicando LSP

A herança foi mal aplicada. Se as assinaturas ou comportamentos diferem na prática, os objetos não compartilham a mesma relação hierárquica direta. Devemos criar abstrações mais genéricas ou utilizar composição:

```python
from abc import ABC, abstractmethod

class FormaGeometrica(ABC):
    @abstractmethod
    def calcular_area(self):
        pass

class Retangulo(FormaGeometrica):
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def calcular_area(self):
        return self.largura * self.altura

class Quadrado(FormaGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def calcular_area(self):
        return self.lado ** 2
```

---

### 4. Interface Segregation Principle (ISP)

> "Muitas interfaces específicas são melhores do que uma interface única e geral."

Os clientes (classes que implementam ou usam interfaces) não devem ser forçados a depender de métodos que não utilizam. Interfaces gigantes geram acoplamento desnecessário.

#### ❌ Violação do ISP

Uma interface de controle de dispositivos para uma casa inteligente:

```python
from abc import ABC, abstractmethod

class DispositivoInteligente(ABC):
    @abstractmethod
    def ligar(self):
        pass

    @abstractmethod
    def desligar(self):
        pass

    @abstractmethod
    def ajustar_temperatura(self):
        pass  # Nem todo dispositivo tem temperatura
```

Se criarmos uma classe `LampadaInteligente` herdando dessa interface, seremos obrigados a implementar `ajustar_temperatura()`, gerando um método vazio ou que lança uma exceção.

#### ✔️ Solução Aplicando ISP

Dividimos a interface genérica em interfaces menores e especializadas:

```python
from abc import ABC, abstractmethod

class Ligavel(ABC):
    @abstractmethod
    def ligar(self):
        pass

    @abstractmethod
    def desligar(self):
        pass

class Termostativel(ABC):
    @abstractmethod
    def ajustar_temperatura(self):
        pass

class Lampada(Ligavel):
    def ligar(self):
        print("Lâmpada ligada")

    def desligar(self):
        print("Lâmpada desligada")
```

---

### 5. Dependency Inversion Principle (DIP)

> "Dependa de abstrações, não de implementações concretas."

Módulos de alto nível (as regras de negócio principais) não devem depender de módulos de baixo nível (detalhes como banco de dados, bibliotecas de terceiros ou envio de e-mails). Ambos devem depender de abstrações.

#### ❌ Violação do DIP

Uma classe de negócio `GerenciadorDeNotificacoes` que depende diretamente de uma classe concreta de envio de SMS:

```python
class ServicoSMS:
    def enviar_sms(self, mensagem):
        print(f"SMS enviado: {mensagem}")

class GerenciadorDeNotificacoes:
    def __init__(self):
        self.servico = ServicoSMS()  # Alto nível dependendo diretamente do baixo nível!

    def notificar_usuario(self, mensagem):
        self.servico.enviar_sms(mensagem)
```

Por que está errado? Se o sistema decidir mudar o canal de comunicação para e-mail ou WhatsApp, teremos que modificar a classe de alto nível `GerenciadorDeNotificacoes`.

#### ✔️ Solução Aplicando DIP

Introduzimos uma abstração intermediária (interface). A classe de negócio depende apenas dessa abstração, e quem injeta a implementação real é quem instancia o fluxo (Injeção de Dependência):

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem):
        pass

class ServicoSMS(Notificador):
    def enviar(self, mensagem):
        print(f"SMS: {mensagem}")

class ServicoEmail(Notificador):
    def enviar(self, mensagem):
        print(f"E-mail: {mensagem}")

class GerenciadorDeNotificacoes:
    # O módulo de alto nível agora recebe uma abstração
    def __init__(self, notificador: Notificador):
        self.notificador = notificador

    def notificar_usuario(self, mensagem):
        self.notificador.enviar(mensagem)
```

---

## 🚀 Desafio Prático do Módulo

Navegue até a pasta `src/violacao/` deste repositório. Você encontrará o código de um sistema de e-commerce incompleto que viola gravemente múltiplos princípios SOLID descritos neste guia.

Sua missão:

- Analise os arquivos e identifique quais princípios estão sendo violados.
- Crie uma branch com o nome `feature/refatoracao-seu-nome`.
- Refatore o sistema movendo as correções para a pasta `src/solucao/`.
- Certifique-se de executar os testes automatizados contidos na pasta `tests/` para validar se as regras de negócio permanecem intactas após suas mudanças.
- Abra um Pull Request para consolidação da entrega!
