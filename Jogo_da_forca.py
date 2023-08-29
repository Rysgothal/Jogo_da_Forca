import os
import random

class JogoDaForca():
    def __init__(self):
        super().__init__()
        self.BaixarDependencias()
        self.BaixarArquivoTxtPalavras()
        self.Palavra = self.SortearUmaPalavra()
        self.Print = self.RetornarPalavraPrint(self.Palavra)
        self.PalavraLista = list(self.Palavra)
        self.PrintLista = list(self.Print.replace(' ', ''))
        self.Tentativas = 6
        self.ChutesAntigos = []

    def BaixarDependencias(self):   
        import pip
        
        try:
            import requests 
        except ModuleNotFoundError:
            pip.main(['install', "requests==2.31.0"])
            import requests

        try:
            import configparser
        except ModuleNotFoundError:
            pip.main(['install', 'configparser==6.0.0'])
            import configparser    

        self.vRequest = requests
        self.vIni = configparser.ConfigParser()

    def BaixarArquivoTxtPalavras(self):  
        vURL = "https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt"  # Link onde está o .txt
        vResponse = self.vRequest.get(vURL) 
        vArquivoExiste = os.path.exists('palavras.txt')

        if vArquivoExiste:            
            print('O arquivo de palavras para o jogos já existe, continuando...')
            return
        else:
            print('O arquivo de palavras para o jogos não existe, baixando...')

        if vResponse.status_code == 200:
            vArquivoTxt = vResponse.text  
            
            with open('palavras.txt', 'w') as vArquivo:
                vArquivo.write(vArquivoTxt)

            print("Palavras baixadas e salvas...\n")
        else:
            print("Falha ao baixar o arquivo, verifique...")
            exit()

    def SortearUmaPalavra(self):
        with open('palavras.txt', 'r') as vArquivo:
            vLinhas = vArquivo.readlines()

        vTotalLinhas = len(vLinhas)
        if vTotalLinhas > 0:
            vLinhaSelecionada = random.randint(0, vTotalLinhas - 1)
            vPalavraSelecionada = vLinhas[vLinhaSelecionada].strip()
            return vPalavraSelecionada
        else:
            print('Não foi possivel selecionar uma palavra, verifique...')
            exit()
    
    def RetornarPalavraPrint(self, pPalavra):
        vPrint = ' '.join(['_' if vLetra != ' ' else ' ' for vLetra in pPalavra])
        return vPrint
    
    def MostrarTituloJogo(self):
        print('============================================================')
        print('                        Jogo Da Forca                       ')
        print('============================================================')
        print('\n\t\t' + self.Print)
    
    def PegarChute(self):
        self.MostrarTituloJogo()

        if self.ChutesAntigos:
            print('\nChutes anteriores: ' + ', '.join(self.ChutesAntigos) + '.')
        
        self.Chute = input('\n Digite uma Letra: ')
        self.Chute = self.Chute.strip()

        while self.Chute == '': 
            self.Chute = input('Digite pelo menos 1 Letra: ')
            self.Chute = self.Chute.strip()

        while len(self.Chute) > 1: 
            self.Chute = input('Digite apenas 1 Letra: ')
            self.Chute = self.Chute.strip()

        while self.Chute in self.ChutesAntigos:
            self.Chute = input('A Letra informada já foi digitada, tente outra: ')
            self.Chute = self.Chute.strip()

    def RodarJogo(self):
        vPossuiChute = False  
        self.PegarChute()
        self.ChutesAntigos.append(self.Chute)    
        
        for i, vChar in enumerate(self.PalavraLista):
            if self.Chute != vChar:
                continue
            
            self.PrintLista[i] = self.Chute
            vPrintLista = ''.join(self.PrintLista)
            self.Print = ' '.join(vPrintLista)
            vPossuiChute = True

        if not '_' in self.Print:
            print(f'\nParabéns!!! \nVocê acertou a palavra: "{self.Palavra}".')
            vJogo.SalvarArquivoTentativas()
            exit()

        if not vPossuiChute:
            print(f'\nA letra: "{self.Chute}", não possui nessa Palavra.')
            self.Tentativas -= 1 
            print(f'Tentativas Restantes = {self.Tentativas}.')
            
            if self.Tentativas == 0:
                print(f'\nO número de tentaticas acabou, a palavra era "{self.Palavra}".')
                vJogo.SalvarArquivoTentativas()
                exit()
        else:            
            print(f'\nA letra: "{self.Chute}", possui nessa Palavra.')
            print(f'Tentativas Restantes = {self.Tentativas}.')
            
        self.RodarJogo()   

    def SalvarArquivoTentativas(self):
        print('Salvando historico do jogo...')
        vArquivo = 'Log.ini'

        if not os.path.exists(vArquivo):
            with open(vArquivo, 'w') as vINI:
                self.vIni.write(vINI)

        self.vIni.read(vArquivo)
        
        NumeroJogo = 1
        while self.vIni.has_section(f'jogo{NumeroJogo}'):
            NumeroJogo += 1
        
        self.vIni[f'jogo{NumeroJogo}'] = {'PALAVRA': self.Palavra, 'TENTATIVA': self.ChutesAntigos}
        
        with open('log.ini', 'w') as LogJogo:
            self.vIni.write(LogJogo)

vJogo = JogoDaForca()
vJogo.RodarJogo()