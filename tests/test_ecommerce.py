"""
Testes do Sistema de E-commerce
==============================

Testes que validam as regras de negócio do sistema.
Use estes testes para garantir que a refatoração mantém
o comportamento esperado do sistema.
"""

import sys
import os

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecommerce import Produto, Pedido, Estoque, GerenciadorPedidos


def test_produto_criacao():
    """Testa a criação de um produto"""
    print("[TESTE] Criação de Produto")
    produto = Produto(1, "Notebook", 3000.00)
    assert produto.id_produto == 1
    assert produto.nome == "Notebook"
    assert produto.preco == 3000.00
    print("✓ PASSOU\n")


def test_produto_validacao_preco():
    """Testa a validação de preço negativo"""
    print("[TESTE] Validação de Preço Negativo")
    produto = Produto(1, "Produto", -100)
    try:
        produto.validar_preco()
        assert False, "Deveria ter lançado exceção"
    except ValueError:
        print("✓ PASSOU\n")


def test_produto_desconto():
    """Testa aplicação de desconto"""
    print("[TESTE] Aplicação de Desconto")
    produto = Produto(1, "Produto", 100.00)
    produto.aplicar_desconto(10)
    assert produto.get_preco_final() == 90.00
    print("✓ PASSOU\n")


def test_pedido_criacao():
    """Testa a criação de um pedido"""
    print("[TESTE] Criação de Pedido")
    pedido = Pedido(1, "Cliente Teste")
    assert pedido.id_pedido == 1
    assert pedido.cliente == "Cliente Teste"
    assert len(pedido.itens) == 0
    print("✓ PASSOU\n")


def test_pedido_adicionar_item():
    """Testa adicionar item ao pedido"""
    print("[TESTE] Adicionar Item ao Pedido")
    pedido = Pedido(1, "Cliente Teste")
    produto = Produto(1, "Notebook", 3000.00)
    
    pedido.adicionar_item(produto, 1)
    assert len(pedido.itens) == 1
    print("✓ PASSOU\n")


def test_pedido_calcular_total():
    """Testa cálculo do total do pedido"""
    print("[TESTE] Cálculo do Total do Pedido")
    pedido = Pedido(1, "Cliente Teste")
    
    produto1 = Produto(1, "Produto A", 100.00)
    produto2 = Produto(2, "Produto B", 200.00)
    
    pedido.adicionar_item(produto1, 2)  # 200
    pedido.adicionar_item(produto2, 1)  # 200
    
    total = pedido.calcular_total()
    assert total == 400.00, f"Total deveria ser 400.00, mas foi {total}"
    print("✓ PASSOU\n")


def test_pedido_total_com_desconto():
    """Testa cálculo do total com desconto aplicado"""
    print("[TESTE] Cálculo do Total com Desconto")
    pedido = Pedido(1, "Cliente Teste")
    
    produto = Produto(1, "Notebook", 1000.00)
    produto.aplicar_desconto(20)  # 20% de desconto = 800
    
    pedido.adicionar_item(produto, 1)
    
    total = pedido.calcular_total()
    assert total == 800.00, f"Total deveria ser 800.00, mas foi {total}"
    print("✓ PASSOU\n")


def test_estoque_adicionar():
    """Testa adicionar quantidade ao estoque"""
    print("[TESTE] Adicionar Estoque")
    estoque = Estoque()
    produto = Produto(1, "Produto", 100.00)
    
    estoque.adicionar_estoque(produto, 10)
    assert estoque.verificar_disponibilidade(produto, 10)
    print("✓ PASSOU\n")


def test_estoque_remover():
    """Testa remover quantidade do estoque"""
    print("[TESTE] Remover Estoque")
    estoque = Estoque()
    produto = Produto(1, "Produto", 100.00)
    
    estoque.adicionar_estoque(produto, 10)
    estoque.remover_estoque(produto, 5)
    
    assert estoque.produtos_estoque[produto.id_produto] == 5
    print("✓ PASSOU\n")


def test_estoque_insuficiente():
    """Testa remoção com estoque insuficiente"""
    print("[TESTE] Remoção com Estoque Insuficiente")
    estoque = Estoque()
    produto = Produto(1, "Produto", 100.00)
    
    estoque.adicionar_estoque(produto, 5)
    
    try:
        estoque.remover_estoque(produto, 10)
        assert False, "Deveria ter lançado exceção"
    except ValueError as e:
        assert "insuficiente" in str(e).lower()
        print("✓ PASSOU\n")


def test_gerenciador_criar_pedido():
    """Testa criação de pedido pelo gerenciador"""
    print("[TESTE] Criar Pedido pelo Gerenciador")
    gerenciador = GerenciadorPedidos()
    
    pedido1 = gerenciador.criar_pedido("Cliente 1")
    pedido2 = gerenciador.criar_pedido("Cliente 2")
    
    assert len(gerenciador.pedidos) == 2
    assert pedido1.id_pedido == 1
    assert pedido2.id_pedido == 2
    print("✓ PASSOU\n")


def test_processamento_pagamento_cartao():
    """Testa processamento de pagamento com cartão"""
    print("[TESTE] Processamento de Pagamento com Cartão")
    pedido = Pedido(1, "Cliente")
    
    resultado = pedido.processar_pagamento("cartao_credito")
    assert resultado is True
    assert pedido.pagamento_metodo == "cartao_credito"
    print("✓ PASSOU\n")


def test_processamento_pagamento_boleto():
    """Testa processamento de pagamento com boleto"""
    print("[TESTE] Processamento de Pagamento com Boleto")
    pedido = Pedido(1, "Cliente")
    
    resultado = pedido.processar_pagamento("boleto")
    assert resultado is True
    assert pedido.pagamento_metodo == "boleto"
    print("✓ PASSOU\n")


def test_pagamento_invalido():
    """Testa pagamento com método inválido"""
    print("[TESTE] Pagamento com Método Inválido")
    pedido = Pedido(1, "Cliente")
    
    try:
        pedido.processar_pagamento("criptomoeda_inexistente")
        assert False, "Deveria ter lançado exceção"
    except ValueError as e:
        assert "não suportado" in str(e).lower()
        print("✓ PASSOU\n")


def test_pedido_sem_itens():
    """Testa processamento de pedido sem itens"""
    print("[TESTE] Processamento de Pedido sem Itens")
    gerenciador = GerenciadorPedidos()
    pedido = gerenciador.criar_pedido("Cliente")
    
    try:
        gerenciador.processar_pedido_completo(pedido)
        assert False, "Deveria ter lançado exceção"
    except ValueError as e:
        assert "sem itens" in str(e).lower()
        print("✓ PASSOU\n")


def test_fluxo_completo():
    """Testa o fluxo completo: criar, adicionar itens, processar"""
    print("[TESTE] Fluxo Completo de Pedido")
    gerenciador = GerenciadorPedidos()
    
    # Cria produtos
    notebook = Produto(1, "Notebook", 3000.00)
    mouse = Produto(2, "Mouse", 150.00)
    
    # Adiciona ao estoque
    gerenciador.estoque.adicionar_estoque(notebook, 5)
    gerenciador.estoque.adicionar_estoque(mouse, 20)
    
    # Cria pedido
    pedido = gerenciador.criar_pedido("João Silva")
    pedido.pagamento_metodo = "cartao_credito"
    
    pedido.adicionar_item(notebook, 1)
    pedido.adicionar_item(mouse, 2)
    
    # Calcula total esperado
    total_esperado = (3000.00 * 1) + (150.00 * 2)
    assert pedido.calcular_total() == total_esperado
    
    # Processa pedido
    gerenciador.processar_pedido_completo(pedido)
    
    # Verifica que o pedido foi adicionado
    assert len(gerenciador.pedidos) == 1
    
    print("✓ PASSOU\n")


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES DO SISTEMA DE E-COMMERCE")
    print("=" * 60 + "\n")
    
    tests = [
        test_produto_criacao,
        test_produto_validacao_preco,
        test_produto_desconto,
        test_pedido_criacao,
        test_pedido_adicionar_item,
        test_pedido_calcular_total,
        test_pedido_total_com_desconto,
        test_estoque_adicionar,
        test_estoque_remover,
        test_estoque_insuficiente,
        test_gerenciador_criar_pedido,
        test_processamento_pagamento_cartao,
        test_processamento_pagamento_boleto,
        test_pagamento_invalido,
        test_pedido_sem_itens,
        test_fluxo_completo,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FALHOU: {str(e)}\n")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTADO: {passed} PASSOU, {failed} FALHOU")
    print("=" * 60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
