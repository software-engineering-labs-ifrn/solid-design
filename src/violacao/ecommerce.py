"""
SISTEMA DE E-COMMERCE COM VIOLAÇÕES DE SOLID
============================================

Este módulo contém uma implementação de um sistema de e-commerce
que VIOLA deliberadamente vários princípios SOLID para fins educacionais.

Violações identificadas:
- SRP (Single Responsibility Principle)
- OCP (Open/Closed Principle)
- DIP (Dependency Inversion Principle)
"""


class Produto:
    """Classe para gerenciar produtos.
    
    VIOLAÇÃO DE SRP: Esta classe tem múltiplas responsabilidades:
    - Gerenciar dados do produto
    - Validar preço
    - Calcular desconto
    - Registrar em banco de dados
    """
    
    def __init__(self, id_produto, nome, preco):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.estoque = 0
        self.desconto = 0
    
    def validar_preco(self):
        """Validação de preço - misturada com a entidade"""
        if self.preco < 0:
            raise ValueError("Preço não pode ser negativo!")
        return True
    
    def aplicar_desconto(self, percentual):
        """Cálculo de desconto - responsabilidade de negócio misturada"""
        if percentual < 0 or percentual > 100:
            raise ValueError("Desconto deve estar entre 0 e 100%")
        self.desconto = percentual
    
    def salvar_no_banco(self):
        """Persistência no banco - TOTALMENTE ACOPLADO à classe Produto!"""
        # Simulando conexão direta ao banco de dados
        print(f"[BD] Salvando produto {self.nome} ao preço {self.preco}")
        return True
    
    def registrar_log(self, mensagem):
        """Logging - mais uma responsabilidade misturada"""
        print(f"[LOG] {mensagem}")
    
    def get_preco_final(self):
        """Cálculo de preço com desconto"""
        return self.preco * (1 - self.desconto / 100)


class Pedido:
    """Classe para gerenciar pedidos.
    
    VIOLAÇÃO DE SRP e DIP: Esta classe faz TUDO:
    - Gerencia itens do pedido
    - Calcula total
    - Processa pagamento
    - Envia e-mail
    - Persiste no banco
    - Gera relatórios
    
    VIOLAÇÃO DE OCP: Mudanças em métodos de pagamento exigem modificação desta classe
    """
    
    def __init__(self, id_pedido, cliente):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.itens = []
        self.pagamento_metodo = None
        self.email_enviado = False
    
    def adicionar_item(self, produto, quantidade):
        """Adiciona um item ao pedido"""
        self.itens.append({
            "produto": produto,
            "quantidade": quantidade,
            "preco_unitario": produto.get_preco_final()
        })
    
    def calcular_total(self):
        """Calcula o total do pedido"""
        return sum(item["preco_unitario"] * item["quantidade"] for item in self.itens)
    
    def processar_pagamento(self, metodo_pagamento):
        """
        VIOLAÇÃO DE OCP: Se aparecer um novo método de pagamento (Pix, Criptomoeda, etc),
        esta função inteira precisa ser modificada!
        """
        self.pagamento_metodo = metodo_pagamento
        
        if metodo_pagamento == "cartao_credito":
            print(f"[PAGAMENTO] Processando cartão de crédito para {self.cliente}")
            # Lógica de pagamento de cartão
            return True
        
        elif metodo_pagamento == "boleto":
            print(f"[PAGAMENTO] Gerando boleto para {self.cliente}")
            # Lógica de geração de boleto
            return True
        
        elif metodo_pagamento == "transferencia":
            print(f"[PAGAMENTO] Gerando dados para transferência para {self.cliente}")
            # Lógica de transferência
            return True
        
        else:
            raise ValueError(f"Método de pagamento {metodo_pagamento} não suportado!")
    
    def enviar_confirmacao_email(self):
        """
        VIOLAÇÃO DE SRP: Envio de e-mail misturado com lógica de pedido.
        VIOLAÇÃO DE DIP: Acoplado diretamente ao serviço de e-mail.
        """
        total = self.calcular_total()
        print(f"[EMAIL] Enviando confirmação para {self.cliente}")
        print(f"[EMAIL] Pedido #{self.id_pedido}")
        print(f"[EMAIL] Total: R$ {total:.2f}")
        self.email_enviado = True
    
    def salvar_pedido_banco(self):
        """
        VIOLAÇÃO DE SRP: Persistência misturada com lógica de negócio.
        Se mudar o banco de dados, precisamos modificar esta classe!
        """
        total = self.calcular_total()
        print(f"[BD] Inserindo pedido #{self.id_pedido} na tabela pedidos")
        print(f"[BD] Cliente: {self.cliente}, Total: R$ {total:.2f}")
        
        for item in self.itens:
            print(f"[BD] Inserindo item: {item['produto'].nome} x {item['quantidade']}")
    
    def finalizar_pedido(self):
        """
        VIOLAÇÃO DE SRP: Este método coordena múltiplas responsabilidades.
        Se qualquer uma das etapas falhar, o estado fica inconsistente.
        """
        print(f"\n>>> Finalizando pedido #{self.id_pedido}")
        
        # Calcula total
        total = self.calcular_total()
        print(f"Total: R$ {total:.2f}")
        
        # Processa pagamento (acoplado!)
        if not self.processar_pagamento(self.pagamento_metodo or "cartao_credito"):
            raise Exception("Falha no processamento do pagamento")
        
        # Salva no banco (acoplado!)
        self.salvar_pedido_banco()
        
        # Envia e-mail (acoplado!)
        self.enviar_confirmacao_email()
        
        # Gera relatório (acoplado!)
        self.gerar_relatorio_vendas()
        
        print(">>> Pedido finalizado com sucesso!\n")
    
    def gerar_relatorio_vendas(self):
        """
        VIOLAÇÃO DE SRP: Geração de relatórios misturada com lógica de pedido.
        """
        print(f"[RELATÓRIO] Pedido #{self.id_pedido}")
        print(f"[RELATÓRIO] Cliente: {self.cliente}")
        print(f"[RELATÓRIO] Itens: {len(self.itens)}")
        print(f"[RELATÓRIO] Total: R$ {self.calcular_total():.2f}")


class Estoque:
    """Classe para gerenciar estoque.
    
    VIOLAÇÃO DE SRP: Múltiplas responsabilidades:
    - Gerenciar quantidade em estoque
    - Validar disponibilidade
    - Persistir no banco
    - Enviar alertas
    - Registrar movimentações
    """
    
    def __init__(self):
        self.produtos_estoque = {}
        self.limite_minimo = 10
    
    def adicionar_estoque(self, produto, quantidade):
        """Adiciona quantidade ao estoque"""
        if produto.id_produto not in self.produtos_estoque:
            self.produtos_estoque[produto.id_produto] = 0
        
        self.produtos_estoque[produto.id_produto] += quantidade
        print(f"[ESTOQUE] Adicionado {quantidade} unidades de {produto.nome}")
        
        # Salva direto no banco (acoplamento!)
        self._atualizar_banco_estoque(produto)
    
    def remover_estoque(self, produto, quantidade):
        """Remove quantidade do estoque"""
        if produto.id_produto not in self.produtos_estoque:
            raise ValueError(f"Produto {produto.nome} não existe no estoque")
        
        if self.produtos_estoque[produto.id_produto] < quantidade:
            raise ValueError(f"Estoque insuficiente de {produto.nome}")
        
        self.produtos_estoque[produto.id_produto] -= quantidade
        print(f"[ESTOQUE] Removido {quantidade} unidades de {produto.nome}")
        
        # Salva direto no banco (acoplamento!)
        self._atualizar_banco_estoque(produto)
        
        # Verifica se precisa alertar (acoplamento!)
        if self.produtos_estoque[produto.id_produto] < self.limite_minimo:
            self._enviar_alerta_estoque_baixo(produto)
    
    def verificar_disponibilidade(self, produto, quantidade):
        """Verifica se há estoque disponível"""
        return self.produtos_estoque.get(produto.id_produto, 0) >= quantidade
    
    def _atualizar_banco_estoque(self, produto):
        """Atualiza estoque no banco - acoplamento direto!"""
        quantidade = self.produtos_estoque.get(produto.id_produto, 0)
        print(f"[BD] Atualizando estoque do produto {produto.nome}: {quantidade}")
    
    def _enviar_alerta_estoque_baixo(self, produto):
        """Envia alerta quando estoque baixo - acoplamento!"""
        print(f"[ALERTA] Estoque baixo para {produto.nome}!")
        print(f"[EMAIL] Enviando notificação ao gerente de estoque")


class SistemaNotificacao:
    """Classe para enviar notificações.
    
    VIOLAÇÃO DE ISP: Interface genérica demais com métodos não utilizados.
    VIOLAÇÃO DE SRP: Gerencia múltiplos canais de comunicação.
    """
    
    def __init__(self):
        self.canal_email = "smtp.gmail.com"
        self.canal_sms = "provider.sms.com"
        self.canal_push = "firebase.com"
    
    def enviar_email(self, destinatario, assunto, corpo):
        """Envia e-mail - misturado com outros canais"""
        print(f"[EMAIL] Para: {destinatario}")
        print(f"[EMAIL] Assunto: {assunto}")
        print(f"[EMAIL] Corpo: {corpo}")
    
    def enviar_sms(self, telefone, mensagem):
        """Envia SMS - misturado com outros canais"""
        print(f"[SMS] Para: {telefone}")
        print(f"[SMS] Mensagem: {mensagem}")
    
    def enviar_push(self, usuario_id, titulo, mensagem):
        """Envia notificação push - misturado com outros canais"""
        print(f"[PUSH] Para usuário: {usuario_id}")
        print(f"[PUSH] Título: {titulo}")
        print(f"[PUSH] Mensagem: {mensagem}")
    
    def enviar_notificacao(self, tipo, **kwargs):
        """
        VIOLAÇÃO DE OCP: Cada novo canal de notificação exige uma mudança aqui!
        """
        if tipo == "email":
            self.enviar_email(kwargs.get("destinatario"), 
                            kwargs.get("assunto"), 
                            kwargs.get("corpo"))
        elif tipo == "sms":
            self.enviar_sms(kwargs.get("telefone"), 
                          kwargs.get("mensagem"))
        elif tipo == "push":
            self.enviar_push(kwargs.get("usuario_id"), 
                           kwargs.get("titulo"), 
                           kwargs.get("mensagem"))
        else:
            raise ValueError(f"Tipo de notificação {tipo} não suportado")


class GerenciadorPedidos:
    """Classe gerenciadora de pedidos.
    
    VIOLAÇÃO DE SRP: Coordena múltiplas responsabilidades.
    VIOLAÇÃO DE DIP: Altamente acoplada a classes concretas.
    """
    
    def __init__(self):
        self.pedidos = {}
        self.numero_pedido = 0
        # Acoplamento direto com classes concretas
        self.estoque = Estoque()
        self.notificacao = SistemaNotificacao()
    
    def criar_pedido(self, cliente):
        """Cria um novo pedido"""
        self.numero_pedido += 1
        pedido = Pedido(self.numero_pedido, cliente)
        self.pedidos[self.numero_pedido] = pedido
        return pedido
    
    def processar_pedido_completo(self, pedido):
        """
        Processa todo o fluxo de um pedido.
        VIOLAÇÃO DE SRP: Coordena múltiplas responsabilidades que deveriam estar separadas.
        """
        print(f"\n=== Processando Pedido Completo ===")
        
        # Valida pedido
        if not pedido.itens:
            raise ValueError("Pedido sem itens!")
        
        # Verifica estoque (acoplado!)
        for item in pedido.itens:
            if not self.estoque.verificar_disponibilidade(item["produto"], item["quantidade"]):
                raise ValueError(f"Estoque insuficiente para {item['produto'].nome}")
        
        # Remove do estoque (acoplado!)
        for item in pedido.itens:
            self.estoque.remover_estoque(item["produto"], item["quantidade"])
        
        # Finaliza pedido (acoplado!)
        pedido.finalizar_pedido()
        
        # Envia notificações (acoplado!)
        self.notificacao.enviar_email(
            pedido.cliente,
            "Pedido Confirmado",
            f"Seu pedido #{pedido.id_pedido} foi confirmado!"
        )
        
        print("=== Pedido Processado ===\n")
    
    def listar_pedidos(self):
        """Lista todos os pedidos"""
        print(f"\nTotal de pedidos: {len(self.pedidos)}")
        for id_pedido, pedido in self.pedidos.items():
            print(f"Pedido #{id_pedido}: Cliente {pedido.cliente}, Total: R$ {pedido.calcular_total():.2f}")
        print()
