---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #0f172a
color: #f8fafc
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    padding: 40px;
  }
  h1, h2 { color: #ffffff; }
  h3 { color: #34d399; }
  footer { color: #64748b; font-size: 0.5em; }
  section.lead h1 { text-align: left; }
  span.highlight { color: #34d399; font-weight: bold; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; text-align: center; }
  .card { background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #34d399; }
  .card-bad { border-left-color: #ef4444; }
  .roi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; font-size: 0.6em; }
  .roi-card { background: #1e293b; padding: 10px; border-radius: 6px; }
---

<!-- Title Slide -->
### Instituto Federal do Rio Grande do Norte — Campus Parnamirim
# Além da Sintaxe: <span class="highlight">Construindo Aplicações Robustas</span>
#### SOLID: A Arte do Design de Software

**Curso:** Superior de Tecnologia em Sistemas para Internet  
**Prof.** Daniel Aguiar | daniel.aguiar@ifrn.edu.br  
github.com/daguiardev

---

## Agenda da Aula

<div class="grid-4" style="margin-top: 40px;">
  <div class="card">
    <h3>⚠️</h3>
    <strong>1. Problema</strong>
    <p style="font-size: 0.7em; color: #94a3b8;">O caos do código acoplado.</p>
  </div>
  <div class="card">
    <h3>⏳</h3>
    <strong>2. Origem</strong>
    <p style="font-size: 0.7em; color: #94a3b8;">História e conceitos.</p>
  </div>
  <div class="card">
    <h3>💻</h3>
    <strong>3. Os 5 Pilares</strong>
    <p style="font-size: 0.7em; color: #94a3b8;">Análise prática do SOLID.</p>
  </div>
  <div class="card">
    <h3>📊</h3>
    <strong>4. ROI & Fim</strong>
    <p style="font-size: 0.7em; color: #94a3b8;">Retorno e revisão.</p>
  </div>
</div>

---

## ⚠️ O Sintoma: Código "Colcha de Retalhos"

<div class="grid-2">
  <div>
    <p style="border-left: 4px solid #f59e0b; padding-left: 15px; font-style: italic; color: #cbd5e1;">
      "Mudamos o formato do e-mail de notificação e as consultas ao banco de dados pararam de funcionar."
    </p>
    <p style="font-size: 0.8em; color: #94a3b8; margin-top: 20px;">
      À medida que o sistema cresce, pequenas alterações geram um efeito cascata imprevisível. O software perde flexibilidade e a equipe ganha medo de refatorar.
    </p>
  </div>
  <div class="grid-2" style="font-size: 0.7em;">
    <div class="card card-bad"><strong>Rigidez:</strong> Difícil de mudar.</div>
    <div class="card card-bad"><strong>Fragilidade:</strong> Quebra em locais aleatórios.</div>
    <div class="card card-bad"><strong>Imobilidade:</strong> Impossível reaproveitar.</div>
    <div class="card card-bad"><strong>Viscosidade:</strong> Gambiarras são mais fáceis.</div>
  </div>
</div>

---

## De onde surgiu o SOLID?

- **Robert C. Martin ("Uncle Bob")**: Compilou os princípios no início dos anos 2000.
- **Michael Feathers**: Popularizou o acrônimo.
- **Foco Central**: Mitigar problemas de design na Programação Orientada a Objetos (POO).

### Objetivos Primordiais
- **Manutenibilidade:** Facilitar correções e evolução do sistema.
- **Escalabilidade:** Permitir crescimento seguro do projeto.

---

## O Acrônimo Desmistificado

<div class="roi-grid" style="font-size: 0.75em; margin-top: 20px;">
  <div class="roi-card"><h2 style="color:#34d399; font-family:monospace;">S</h2><strong>Single Responsibility</strong><br>Uma única responsabilidade.</div>
  <div class="roi-card"><h2 style="color:#34d399; font-family:monospace;">O</h2><strong>Open / Closed</strong><br>Aberto a extensões, fechado a alterações.</div>
  <div class="roi-card"><h2 style="color:#34d399; font-family:monospace;">L</h2><strong>Liskov Substitution</strong><br>Subclasses seguras.</div>
  <div class="roi-card"><h2 style="color:#34d399; font-family:monospace;">I</h2><strong>Interface Segregation</strong><br>Interfaces enxutas.</div>
  <div class="roi-card"><h2 style="color:#34d399; font-family:monospace;">D</h2><strong>Dependency Inversion</strong><br>Dependa de abstrações.</div>
</div>

---

## S — Single Responsibility Principle (SRP)

> " Uma classe deve ter um, e apenas um, motivo para mudar."

```typescript
// Responsabilidades devidamente isoladas
class Pedido {
  private items: string[] = [];
  calcularTotal() { return this.items.length * 10; }
}

class PedidoRepository {
  salvar(pedido: Pedido) { /* conexão banco */ }
}

class NotificationService {
  enviarEmail(msg: string) { /* disparo e-mail */ }
}
```

---

## O — Open/Closed Principle (OCP)

> "Entidades devem estar abertas para extensão, mas fechadas para modificação."

```typescript
interface Frete { calcular(peso: number): number; }

class FretePAC implements Frete { calcular(p: number) { return p * 5; } }
class FreteSedex implements Frete { calcular(p: number) { return p * 15; } }

class CalculadoraFrete {
  calcular(frete: Frete, peso: number) { return frete.calcular(peso); }
}
```

---

## L — Liskov Substitution Principle (LSP)

> "Classes derivadas devem poder ser substituídas por suas classes base."

```typescript
class Ave { comer() { return "comendo"; } }

class AveQueVoa extends Ave { voar() { return "voando"; } }

class Pinguim extends Ave {
  // Pinguim não herda voar() incorretamente. Evita bugs inesperados.
  nadar() { return "nadando"; }
}
```

---

## I — Interface Segregation Principle (ISP)

> "Uma classe não deve ser forçada a depender de interfaces que não utiliza."

```typescript
interface Trabalhavel { trabalhar(): void; }
interface Comivel { comer(): void; }

class Humano implements Trabalhavel, Comivel {
  trabalhar() {}
  comer() {}
}

class Robo implements Trabalhavel {
  trabalhar() {} // Não é forçado a implementar "comer()"
}
```

---

## D — Dependency Inversion Principle (DIP)

> "Dependa de abstrações, não de implementações."

```typescript
interface Database { connect(): void; }

class MySQLConnection implements Database { connect() { /* ... */ } }

class SistemaPrincipal {
  // O sistema depende do contrato (Interface), não do driver rígido do banco
  constructor(private db: Database) {}
}
```

---

## O Retorno do Investimento (ROI) do SOLID

- Flexibilidade: O design SOLID dita como seu software reage a mudanças.
- Maturidade Prática: Evite over-engineering; aplique conforme a necessidade.
- Padrão de Mercado: Clean Architecture e DDD fundamentam-se nesses pilares.

---

## Obrigado!

"Escrever código limpo é um ato de respeito pelo próximo desenvolvedor."  
✉️ daniel.aguiar@ifrn.edu.br  
💻 github.com/daguiardev

---