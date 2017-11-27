import requests


# ==================== Funcao para buscar periodos ==================== #
def busca_periodos():
    resultado = consultar('', '', '', '', '', 0)  # resultado da busca
    salvar_arquivo('periodos', resultado)  # salvando resultado da busca

    limpar_arquivo('periodos', 0)

    formato_desejado('periodos', 0)

    return


# ==================== Funcao para buscar marcas ==================== #
def busca_marcas():
    periodos = abre_arquivo('periodos')
    linha = periodos.readline()  # pegando a primeira linha do aquivo
    conteudo_linha = linha.split()  # pegando o conteudo da linha
    ultimo = conteudo_linha[0]  # pegando o codigo do ultimo priodo

    resultado = consultar(ultimo, '', '', '', '', 1)  # resultado da busca
    salvar_arquivo('marcas', resultado)  # salvando resultado da busca

    limpar_arquivo('marcas', 1)

    # formato_desejado('marcas', 1)

    return


# ==================== Funcao para buscar os modelos ==================== #
def busca_modelos():
    periodos = abre_arquivo('periodos')
    linha = periodos.readline()  # pegando a primeira linha do aquivo
    conteudo_linha = linha.split()  # pegando o conteudo da linha
    ultimo = conteudo_linha[0]  # pegando o codigo do ultimo priodo

    marcas = abre_arquivo('marcas')  # abrindo aquivo marcas

    for linha_m in marcas:  # percorrendo as linhas do arquivo
        conteudo = linha_m.split()  # pegando o conteúdo da linha

        marca = conteudo[0]

        resultado = consultar(ultimo, marca, '', '', '', 2)  # resultado da busca

        salvar_arquivo('modelos_da_' + conteudo[1], resultado)  # salvando resultado da busca

        limpar_arquivo('modelos_da_' + conteudo[1], 2)

        formato_desejado('modelos_da_' + conteudo[1], 2)

    return


# ==================== Funcao para buscar as versoes ==================== #
def busca_versao():
    periodos = abre_arquivo('periodos')
    linha = periodos.readline()  # pegando a primeira linha do aquivo
    conteudo_linha = linha.split()  # pegando o conteudo da linha
    ultimo = conteudo_linha[0]  # pegando o codigo do ultimo priodo

    marcas = abre_arquivo('marcas')  # abrindo aquivo marcas

    for linha_m in marcas:  # percorrendo as linhas do arquivo
        conteudo = linha_m.split()  # pegando o conteúdo da linha
        marca = conteudo[0]

        modelos = abre_arquivo('modelos_da_'+conteudo[1])
        for linha in modelos:
            conteudo_l = linha.split()
            modelo = conteudo_l[0]

            resultado = consultar(ultimo, marca, modelo, '', '', 3)  # resultado da busca

            salvar_arquivo(conteudo[1]+'_'+conteudo_l[1]+'_'+conteudo_l[0], resultado)  # salvando resultado da busca

            limpar_arquivo(conteudo[1]+'_'+conteudo_l[1]+'_'+conteudo_l[0], 3)

            formato_desejado(conteudo[1]+'_'+conteudo_l[1]+'_'+conteudo_l[0], 3)

    return


# ==================== Funcao para montar tabela para a busca fibal ==================== #
def tabela_de_busca():
    conteudo = []
    periodos = abre_arquivo('periodos')
    for linha_p in periodos:
        conteudo_p = linha_p.split()
        periodo = conteudo_p[0]

        marcas = abre_arquivo('marcas')  # abrindo aquivo marcas
        for linha_m in marcas:  # percorrendo as linhas do arquivo
            conteudo_m = linha_m.split()  # pegando o conteudo da linha
            marca = conteudo_m[0]

            modelos = abre_arquivo('modelos_da_'+conteudo_m[1])
            for linha_l in modelos:
                conteudo_l = linha_l.split()
                if len(conteudo_l) > 1:
                    modelo = conteudo_l[0]

                    versoes = abre_arquivo(conteudo_m[1]+'_'+conteudo_l[1]+'_'+modelo)
                    for linha_v in versoes:
                        conteudo_v = linha_v.split()
                        if len(conteudo_v) > 1:

                            conteudo.append(periodo+' '+marca+' '+modelo+' '+conteudo_v[0]+' '+conteudo_v[1]+'\n')

    reescrever('Tabela_busca_final', conteudo)

    return


# ==================== Funcao realizar a busca completa ==================== #
def busca_completa():
    arq = abre_arquivo('Tabela_busca_final')

    for linha in arq:
        conteudo = linha.split()
        tam = len(conteudo) - 1
        if tam > 1:
            periodo = conteudo[0]
            marca = conteudo[1]
            modelo = conteudo[2]
            ano = conteudo[3]
            combustivel = conteudo[4]

            resultado = consultar(periodo, marca, modelo, ano, combustivel, 4)

            salvar_arquivo(periodo+'_'+marca+'_'+modelo+'_'+ano+'_'+combustivel, resultado)
    return


# ==================== Funcao para realizar consultas na tabela fipe ==================== #
def consultar(periodo, marca, modelo, ano, combustivel, tipo):
    if tipo == 0:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Content-Length': '0',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'nvgt41729=1501801813993_1_0|0_0|0; sb_days=1501803588279; sback_total_sessions=3; '
                             '_spl_pv=50; '
                             'sback_browser=0-77194500'
                             '-149433865670a0f5d64a71e736c66730e10f4ac2c177f374ba13247355925911cc60bc7759-87849107'
                             '-179198170156-1503183381; sback_client=587f98b6becd8a73835ec19d; '
                             'sback_customer'
                             '=$2gSx80awQ1aNhDe50UayQTWSJDNVZnewlVZrVmSX1GMZBTawpEdHtUTwpmUSp1R21Ucy4WTXRESaRTaw5kQEhlT2$12; '
                             'sback_partner=false; nav41729=7620a5f92221c98be2ea833cf09|2_237; nvgc41729=0|0; '
                             '_ga=GA1.3.697912669.1498731358; _gid=GA1.3.1176072343.1503567970; _gat=1',
                   'Host': 'veiculos.fipe.org.br',
                   'Origin': 'http://veiculos.fipe.org.br',
                   'Referer': 'http://veiculos.fipe.org.br/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 '
                                 'Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}  # parametro padrao exigido pelo site para realizar a busca

        data = ''
        link = 'http://veiculos.fipe.org.br/api/veiculos/ConsultarTabelaDeReferencia'  # link para buscar os periodos

    elif tipo == 1:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Content-Length': '46',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'nvgt41729=1501801813993_1_0|0_0|0; sb_days=1501803588279; sback_total_sessions=3; _spl_pv=50; '
                             'sback_browser=0-77194500'
                             '-149433865670a0f5d64a71e736c66730e10f4ac2c177f374ba13247355925911cc60bc7759-87849107'
                             '-179198170156-1503183381; sback_client=587f98b6becd8a73835ec19d; '
                             'sback_customer'
                             '=$2gSx80awQ1aNhDe50UayQTWSJDNVZnewlVZrVmSX1GMZBTawpEdHtUTwpmUSp1R21Ucy4WTXRESaRTaw5kQEhlT2$12; '
                             'sback_partner=false; nav41729=7620a5f92221c98be2ea833cf09|2_237; '
                             '_ga=GA1.3.697912669.1498731358; _gid=GA1.3.1176072343.1503567970; nvgc41729=0|0',
                   'Host': 'veiculos.fipe.org.br',
                   'Origin': 'http://veiculos.fipe.org.br',
                   'Referer': 'http://veiculos.fipe.org.br/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101'
                                 'Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'codigoTabelaReferencia': periodo, 'codigoTipoVeiculo': '1'}
        link = 'http://veiculos.fipe.org.br/api/veiculos/ConsultarMarcas'

    elif tipo == 2:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Content-Length': '134',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'nvgt41729=1501801813993_1_0|0_0|0; sb_days=1501803588279; sback_total_sessions=3; _spl_pv=50;'
                             'sback_browser=0-77194500'
                             '-149433865670a0f5d64a71e736c66730e10f4ac2c177f374ba13247355925911cc60bc7759-87849107'
                             '-179198170156-1503183381; sback_client=587f98b6becd8a73835ec19d; '
                             'sback_customer'
                             '=$2gSx80awQ1aNhDe50UayQTWSJDNVZnewlVZrVmSX1GMZBTawpEdHtUTwpmUSp1R21Ucy4WTXRESaRTaw5kQEhlT2$12;'
                             'sback_partner=false; nav41729=7620a5f92221c98be2ea833cf09|2_237; '
                             '_ga=GA1.3.697912669.1498731358; _gid=GA1.3.1176072343.1503567970',
                   'Host': 'veiculos.fipe.org.br',
                   'Origin': 'http://veiculos.fipe.org.br',
                   'Referer': 'http://veiculos.fipe.org.br/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101'
                                 'Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'codigoTipoVeiculo': '1',
                'codigoTabelaReferencia': periodo,
                'codigoModelo': '',
                'codigoMarca': marca,
                'ano': '',
                'codigoTipoCombustivel': '',
                'anoModelo': '',
                'modeloCodigoExterno': '', }
        link = 'http://veiculos.fipe.org.br/api/veiculos/ConsultarModelos'

    elif tipo == 3:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Content-Length': '135',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'nvgt41729=1501801813993_1_0|0_0|0; sb_days=1501803588279; sback_total_sessions=3; '
                             '_spl_pv=50; '
                             'sback_browser=0-77194500'
                             '-149433865670a0f5d64a71e736c66730e10f4ac2c177f374ba13247355925911cc60bc7759-87849107'
                             '-179198170156-1503183381; sback_client=587f98b6becd8a73835ec19d; '
                             'sback_customer'
                             '=$2gSx80awQ1aNhDe50UayQTWSJDNVZnewlVZrVmSX1GMZBTawpEdHtUTwpmUSp1R21Ucy4WTXRESaRTaw5kQEhlT2$12;'
                             'sback_partner=false; nav41729=7620a5f92221c98be2ea833cf09|2_243; '
                             '_ga=GA1.3.697912669.1498731358; _gid=GA1.3.2113665792.1504114274; _gat=1; nvgc41729=0|0',
                   'Host': 'veiculos.fipe.org.br',
                   'Origin': 'http://veiculos.fipe.org.br',
                   'Referer': 'http://veiculos.fipe.org.br/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/60.0.3112.113 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'codigoTipoVeiculo': '1',
                'codigoTabelaReferencia': periodo,
                'codigoModelo': modelo,
                'codigoMarca': marca,
                'ano': '',
                'codigoTipoCombustivel': '',
                'anoModelo': '',
                'modeloCodigoExterno': '', }

        link = 'http://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModelo'

    elif tipo == 4:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Content-Length': '178',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'nvgt41729=1501801813993_1_0|0_0|0; sb_days=1501803588279; sback_total_sessions=3; '
                             '_spl_pv=50; '
                             'sback_browser=0-77194500'
                             '-149433865670a0f5d64a71e736c66730e10f4ac2c177f374ba13247355925911cc60bc7759-87849107'
                             '-179198170156-1503183381; sback_client=587f98b6becd8a73835ec19d; '
                             'sback_customer'
                             '=$2gSx80awQ1aNhDe50UayQTWSJDNVZnewlVZrVmSX1GMZBTawpEdHtUTwpmUSp1R21Ucy4WTXRESaRTaw5kQEhlT2$12; sback_partner=false; nav41729=7620a5f92221c98be2ea833cf09|2_243; _ga=GA1.3.697912669.1498731358; _gid=GA1.3.2113665792.1504114274; nvgc41729=0|0',
                   'Host': 'veiculos.fipe.org.br',
                   'Origin': 'http://veiculos.fipe.org.br',
                   'Referer': 'http://veiculos.fipe.org.br/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/60.0.3112.113 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        data = {'codigoTabelaReferencia': periodo,
                'codigoMarca': marca,
                'codigoModelo': modelo,
                'codigoTipoVeiculo': '1',
                'anoModelo': ano,
                'codigoTipoCombustivel': combustivel,
                'tipoVeiculo': 'carro',
                'modeloCodigoExterno': '',
                'tipoConsulta': 'tradicional', }

        link = 'http://veiculos.fipe.org.br/api/veiculos/ConsultarValorComTodosParametros'

    consulta = requests.post(link, data=data, headers=headers)  # realizando busca
    if consulta.status_code != 200:
        print('Erro ao acessar '+periodo+' '+marca+' '+modelo+' '+ano+' '+combustivel+' '+tipo)

    return consulta.text


# ==================== Funcao para retirar caracteres indesejados ==================== #
def limpar_arquivo(nome, tipo):
    arq = abre_arquivo(nome)  # abrindo aquivo
    linha = arq.readline()  # pegando a unica linha do aquivo
    conteudo_linha = linha.split()  # pegando o conteudo da linha
    novo_conteudo = []  # lista para formar o novo conteudo
    var = 0  # variavel para recorrer o conteudo

    if tipo == 0:
        max = 36

    elif (tipo == 1) or tipo == 2 or tipo == 3:
        max = len(conteudo_linha)  # variavel de controle do laço

    while var < max:  # laco para pegar percorrer o conteudo
        texto = conteudo_linha[var]  # texto recebe o conteudo de conteudo_linha
        texto = texto.replace('[', '')
        texto = texto.replace('{', '')
        texto = texto.replace('"', '')
        texto = texto.replace(':', ' ')
        texto = texto.replace(',', '')
        texto = texto.replace(']', '')
        texto = texto.replace('Mes', ' Mes')
        texto = texto.replace('Value', ' Value')
        texto = texto.replace('"Modelos":', '')
        texto = texto.replace('Siena', 'Siena ')
        texto = texto.replace('Uno', 'Uno ')
        texto = texto.replace('UNO', 'Uno ')
        texto = texto.replace('CRUZE', 'Cruze ')
        texto = texto.replace('ONIX', 'Onix ')
        texto = texto.replace('S10', 'S10 ')
        texto = texto.replace('Civic', 'Civic ')
        texto = texto.replace('CR-V', 'CR-V ')
        texto = texto.replace('Corolla', 'Corolla ')
        texto = texto.replace('Hilux', 'Hilux ')
        texto = texto.replace('AMAROK', 'AMAROK ')
        texto = texto.replace('Golf', 'GOLF ')
        texto = texto.replace('Gol', 'Gol ')
        texto = texto.replace('Gasolina', ' 1')
        texto = texto.replace('Álcool', ' 2')
        texto = texto.replace('Diesel', ' 3')
        texto = texto.replace('}', '\n')

        if var == max - 1:  # verifica se ultimo
            novo_conteudo.append(texto)  # aciciona o conteudo de texto a lista sem adicionar nova linha
        else:
            novo_conteudo.append(texto)  # aciciona o conteudo de texto a lista e adicionar nova linha

        var += 1  # incrementa a variavel de controle

    reescrever(nome, novo_conteudo)  # chama a funcao reescrever e passa o novo_conteudo de períodos
    return


# ==================== Funcao para deixar conteudo do arquivo na forma desejada ==================== #
def formato_desejado(nome, tipo):
    arq = abre_arquivo(nome)  # abrindo aquivo
    novo_conteudo = []  # lista para formar o novo conteudo

    if tipo == 0:
        cont = 0
        for linha in arq:  # laco para percorrer as linhas
            conteudo = linha.split()  # pegando conteudo da linha

            if cont == 35:  # Salvando somente os codigos dos periodos
                novo_conteudo.append(conteudo[1]+' '+conteudo[3])
                break
            else:
                novo_conteudo.append(conteudo[1]+' '+conteudo[3]+'\n')
            cont += 1

    elif tipo == 1:
        for linha in arq:  # laco para percorrer as linhas
            conteudo = linha.split()  # pegando conteudo da linha

            if conteudo[1] == 'Fiat':  # Salvando somente os codigos das marcas desejadas
                novo_conteudo.append(conteudo[3] + ' ' + conteudo[1]+'\n')
            elif conteudo[1] == 'GM-Chevrolet':
                novo_conteudo.append(conteudo[3] + ' ' + conteudo[1]+'\n')
            elif conteudo[1] == 'Honda':
                novo_conteudo.append(conteudo[3] + ' ' + conteudo[1]+'\n')
            elif conteudo[1] == 'Toyota':
                novo_conteudo.append(conteudo[3] + ' ' + conteudo[1]+'\n')
            elif conteudo[1] == 'VW-VolksWagen':
                novo_conteudo.append(conteudo[3] + ' ' + conteudo[1])
                break
    elif tipo == 2:
        for linha in arq:
            conteudo = linha.split()
            tam = len(conteudo) - 1

            if tam > 0:
                texto = conteudo[1]

                if (texto == 'Uno') or (texto == 'GrandSiena') or (texto == 'Siena') or (texto == 'Cruze') or (
                            texto == 'Onix') or (texto == 'S10') or (texto == 'Civic') or (texto == 'CR-V') or (
                            texto == 'Corolla') or (texto == 'Hilux') or (texto == 'AMAROK') or (texto == 'Gol') or (
                            texto == 'GOLF'):
                    if conteudo[4].isdigit():
                        novo_conteudo.append(conteudo[4]+' '+conteudo[1]+' '+conteudo[2]+'\n')
                    else:
                        novo_conteudo.append(conteudo[5] + ' ' + conteudo[1] + ' ' + conteudo[2] + '\n')
    elif tipo == 3:
        for linha in arq:
            conteudo = linha.split()
            tam = len(conteudo) - 1

            if tam > 0:
                novo_conteudo.append(conteudo[1] + ' ' + conteudo[2] + '\n')

    reescrever(nome, novo_conteudo)  # chama a funcao reescrever e passa o novo_conteudo
    return


# ==================== Funcao para criar e escrever arquivos txt ==================== #
def salvar_arquivo(nome, conteudo):
    with open(nome + '.txt', "w", encoding='UTF8') as arq:  # criando/abrindo arquivo
        arq.write(conteudo)  # salvando conteudo
    return ()


# ==================== Funcao para abrir arquivo txt ==================== #
def abre_arquivo(nome):
    arq = open(nome + '.txt', "r", encoding='UTF8')  # abrindo aquivo
    return arq  # retorna o arquivo


# ==================== Funcao para reescrever arquivo txt ==================== #
def reescrever(nome, conteudo):
    arq = open(nome + '.txt', "w", encoding='UTF8')  # abrindo aquivo
    arq.writelines(conteudo)  # reescreve o arquivo com o novo conteudo do arquivo
    return ()


# ==================== Funcao Main ==================== #
def main():
    # ====== Buscar ultimos 36 periodos e salvar no formato ID|Periodo =====#
    busca_periodos()

    # ====== Buscar as marcas desejadas e salvar no formato ID|Marca =====#
    busca_marcas()

    # ====== Buscar os modelos desejadas e salvar no formato ID|Modelo =====#
    busca_modelos()

    # ====== Buscar as versoes de cada modelo e salvar no formato ID|Versao =====#
    busca_versao()

    # ====== Monta a tabela para realizar busca final no formato ID_Periodo|ID_Marca|ID_Modelo|ID_Versao =====#
    tabela_de_busca()

    # ====== Realiza busca com todos os parametros =====#
    busca_completa()


main()
