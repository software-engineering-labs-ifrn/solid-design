"""
Demonstração do Sistema de E-commerce com Violações SOLID
========================================================

Este script demonstra o funcionamento do sistema de e-commerce
que viola os princípios SOLID e mostra os problemas que surgem.
"""

from ecommerce import Produto, Pedido, Estoque, GerenciadorPedidos


def main():
    print("=" * 60)
    print("SISTEMA DE E-COMMERCE COM VIOLAÇÕES SOLID")
    print("=" * 60)
    
    # Cria alguns produtos
    print("\n>>> Criando produtos...")
    notebook = Produto(1, "Notebook", 3000.00)
    notebook.aplicar_desconto(10)  # 10% de desconto
    
    mouse = Produto(2, "Mouse", 150.00)
    teclado = Produto(3, "Teclado", 300.00)
    
    # Salva produtos (acoplamento direto ao banco!)
    for produto in [notebook, mouse, teclado]:
        produto.salvar_no_banco()
        produto.registrar_log(f"Produto {produto.nome} criado com sucesso")
    
    # Gerencia estoque
    print("\n>>> Gerenciando estoque...")
    gerenciador = GerenciadorPedidos()
    
    gerenciador.estoque.adicionar_estoque(notebook, 5)
    gerenciador.estoque.adicionar_estoque(mouse, 20)
    gerenciador.estoque.adicionar_estoque(teclado, 15)
    
    # Cria pedido
    print("\n>>> Criando pedido...")
    pedido = gerenciador.criar_pedido("João Silva")
    pedido.pagamento_metodo = "cartao_credito"
    
    pedido.adicionar_item(notebook, 1)
    pedido.adicionar_item(mouse, 2)
    pedido.adicionar_item(teclado, 1)
    
    # Processa pedido (acoplamento em cascata!)
    print("\n>>> Processando pedido (mostra acoplamento em cascata)...")
    try:
        gerenciador.processar_pedido_completo(pedido)
    except Exception as e:
        print(f"ERRO ao processar pedido: {e}")
    
    # Lista pedidos
    gerenciador.listar_pedidos()
    
    # Demonstra a dificuldade de extensão (violação OCP)
    print("\n>>> Tentando adicionar novo método de pagamento...")
    print("PROBLEMA: Se quisermos adicionar Pix como método de pagamento,")
    print("temos que modificar a classe Pedido.processar_pagamento()!")
    print("Isso viola o Princípio Open/Closed (aberto para extensão, fechado para modificação)")
    
    # Demonstra estoque baixo
    print("\n>>> Simulando estoque baixo...")
    gerenciador.estoque.remover_estoque(notebook, 4)  # Deixa apenas 1 unidade


if __name__ == "__main__":
    main()
