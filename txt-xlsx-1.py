import pandas as pd
import numpy as np

arquivoProdutos = 'txt/produtos.txt'
arquivoVendas = 'txt/vendas.txt'
arquivoXlsx = 'xlsx/relatorio.xlsx'
dadosProduto = open(arquivoProdutos, 'r')
dadosProduto = dadosProduto.readlines()
vendasProdutos = open(arquivoVendas, 'r')
vendasProdutos = vendasProdutos.readlines()

def dfProdutos():
    infoProdutos = []
    for i in dadosProduto:
        i = i.strip('\n')
        cd = i.split(' ')
        infoProdutos.append(cd)
    dfProdutos = pd.DataFrame(infoProdutos, columns=['Código', 'Produto', 'valor'])
    return dfProdutos

def dfVendas():
    dadosVenda = []
    for i in vendasProdutos:
        i = i.strip('\n')
        cd = i.split(' ')
        dadosVenda.append(cd)
    dfVendas = pd.DataFrame(dadosVenda, columns=['Código', 'Data'])
    return dfVendas

dadosProdutos = dfProdutos()
dadosVendas = dfVendas()

def buscaProdutos(itemBusca):
    df_mask = dadosProdutos['Código'] == itemBusca
    positions = np.flatnonzero(df_mask)
    filtered_df = dadosProdutos.iloc[positions]

    return filtered_df


def codigosUnicos():
    cd = dadosVendas['Código'].unique()
    cd = sorted(cd)
    return cd

cdUnico = codigosUnicos()

def datasUnicas():
    dt = dadosVendas['Data'].unique()
    dt = sorted(dt)
    return dt

dtUnica = datasUnicas()

def gerarArquivos():
    with pd.ExcelWriter(arquivoXlsx) as writer:
        for dt in dtUnica:
            codigos = []
            nomes = []
            valores = []
            qtdV = []
            vlVenda = []
            for cd in cdUnico:
                df_mask = (dadosVendas['Código'] == cd) & (dadosVendas['Data'] == dt)
                positions = np.flatnonzero(df_mask)
                filtered_df = dadosVendas.iloc[positions]
                rsP = buscaProdutos(cd)
                qtdVendas = len(filtered_df)
                valorT = rsP['valor'].to_string(index=False)
                nomeT = rsP['Produto'].to_string(index=False)
                totalVendas = qtdVendas * float(valorT)
                codigos.append(cd)
                nomes.append(nomeT)
                valores.append(valorT)
                qtdV.append(qtdVendas)
                vlVenda.append(totalVendas)
            dados = {'Codigo': codigos, 'Produto': nomes, 'Valor': valores, 'Qtd Vendido': qtdV, 'Valor vendas': vlVenda}
            dadosInserir = pd.DataFrame(data=dados)
            dadosInserir.to_excel(writer, sheet_name=dt)
gerarArquivos()