# Document properties
__author__ = [ 'Pereira']
__copyright__ = 'Copyright_2022'
__credits__ = __author__
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = __author__[0]	# Responsável por manter o programa funcionando
__email__ = 'jv.pereiracastro2002@gmail.com'

from tkinter import *

class transition():
	'''
	TRANSIÇÃO DE TELA
	Função: mover uma tela ja colocada (com o método place) para as coordenadas dadas.
	Caso o widget a ser movido tenha sido colocado (place) utilizando rel em qualquer uma das variaveis de posicao, deverá ser dado em rel também para o método.

	Exemplo de uso:
		primeiro = Frame(root)
		primeiro.place(relx=.3,y=50,relwidth=.3, heigh=100)
		
		transition(root, frame=primeiro, relx=.2, y=80, relwidth=.5, heigh=200)

	Atributos:
		origem: É a tela na qual o widget está colocado. Exemplo: Tk(), Frame, Canvas, etc.
		frame: É o widget a ser deslocado. É necessário que o widget tenha sido colocado usando place antes da execução.
		x ou relx: Posição final do objeto em x. Pode ser relativa, ou simples.
		y ou rely: Posição final do objeto em y. Pode ser relativa, ou simples.
		width ou relwidth: Dimensão em x (largura) final do objeto. Pode ser relativa, ou simples.
		heigh ou relheigh: Dimensão em y (altura) final do objeto. Pode ser relativa, ou simples.
		duration_frames: É a duração em quantidade de frames que durará o objeto. Valor padrão = 120 frames.
		duration_btw_frames: É a duração entre cada frame. É dada em milissegundos. Valor padrão = 5.
	'''
	def __init__(self, origem, **kwargs):
		self.kwargs = kwargs
		self.origem = origem
		# duração entre frames
		if 'duration_btw_frames' in self.kwargs:
			self.time_frame = self.kwargs['duration_btw_frames']
		else:
			self.time_frame = 5

		# frame de origem
		if 'frame' in self.kwargs:
			self.frame = self.kwargs['frame']
		else:
			print("Erro: variavel 'frame' não definida.")
			return None

		# declara frame inicial
		self.frameAtual = 0

		# qtd de frames
		if 'duration_frames' in self.kwargs:
			self.frameFinal = int(self.kwargs['duration_frames'])
		else: 
			self.frameFinal = 120

		# avancado 
		self.avancado = [0,0,0,0]
		self.vMov2 = [0,0,0,0]
		self.aceleracaoMov2 = [0,0,0,0]

		self.__read_positions()

		self.__aceleration()

		self.__update()
	def __read_positions(self):
		'''
		Este método lê e guarda em listas as posições finais e iniciais do widget a ser deslocado.

		None -> None
		'''
		# encontra a posicao inicial do objeto, sem estar formatada
		pos = self.frame.place_info()

		# formata kwargs para aceitar heigh e height
		if 'relheigh' in self.kwargs or 'heigh' in self.kwargs:
			newDict = []
			for k, v in self.kwargs.items():
				if k == 'relheigh' or k == 'heigh':
					if k == 'heigh':
						newDict.append(['height', v])
					else:
						newDict.append(['relheight', v])
				else:
					newDict.append([k,v])
		self.kwargs = dict(newDict)

		posFinal = [0,0,0,0]
		posInicial = [0,0,0,0]
		modelos = ['','','','']
		listaPosicoes = ['x','y','width','height']
		for i in range(len(listaPosicoes)):
			# valida casos zerados
			if pos['rel%s'%(listaPosicoes[i])] == '0' and pos['%s'%(listaPosicoes[i])] == '0':
				if 'rel%s'%(listaPosicoes[i]) in self.kwargs:
					modelos[i] = 'relativo'
					posFinal[i] = float(self.kwargs['rel%s'%(listaPosicoes[i])])
				else:
					modelos[i] = 'simples'
					posFinal[i] = int(self.kwargs['%s'%(listaPosicoes[i])])
			else:
				if pos['rel%s'%(listaPosicoes[i])] != '0' and pos['rel%s'%(listaPosicoes[i])] != '':
					posInicial[i] = float(pos['rel%s'%(listaPosicoes[i])])

					# final
					modelos[i] = 'relativo'
					if 'rel%s'%(listaPosicoes[i]) in self.kwargs:
						posFinal[i] = float(self.kwargs['rel%s'%(listaPosicoes[i])])
					else:
						posFinal[i]	= posInicial[i]
				else:
					posInicial[i] = int(pos['%s'%(listaPosicoes[i])])

					# final
					modelos[i] = 'simples'
					if '%s'%(listaPosicoes[i]) in self.kwargs:
						posFinal[i] = int(self.kwargs['%s'%(listaPosicoes[i])])
					else:
						posFinal[i]	= posInicial[i]
		
		self.inicial = posInicial
		self.modelos = modelos
		self.final = posFinal
	def __aceleration(self):
		'''
		Este método realiza o calculo e encontra a aceleração do widget para o movimento dado.

		None -> None
		'''
		# define e encontra a aceleração para o dado sistema de coordenadas
		self.aceleracao = [0,0,0,0]
		for i in range(4):
			self.aceleracao[i] = ((self.final[i] - self.inicial[i])/2)*2/((self.frameFinal/2)**2)
	def __update(self):
		'''
		Este método executa a modificação da posição do frame. É executado até que o contabilize a quantidade dada de duration_frame, ou 120 caso não seja dada nenhuma quantidade.

		None -> None
		'''
		# pos do novo frame
		pos = [0,0,0,0]

		# analisa se ja passou da metade do trajeto
		if self.frameAtual <= self.frameFinal/2:
			for i in range(4):
				# movimento 1 - subir velocidade
				pos[i] = self.inicial[i] + self.aceleracao[i]*(self.frameAtual**2)/2

				# analisa se terminou o movimento 1, caso sim, define variaveis para o movimento 2 e inicia-o
				if self.frameAtual == self.frameFinal/2:
					# x na posicação do meio
					self.avancado[i] = pos[i]

					# velocidade nova
					self.vMov2[i] = self.aceleracao[i]*self.frameAtual

					# novo contador de frame 
					self.frameMov2 = 0

					# nova aceleração
					self.aceleracaoMov2[i] = (self.final[i] - (self.inicial[i]+(self.final[i] - self.inicial[i])/2) - self.vMov2[i]*self.frameAtual)*2/((self.frameFinal/2)**2)
		else:
			for i in range(4):
				# movimento 2
				pos[i] = self.avancado[i] +self.vMov2[i]*self.frameMov2 + self.aceleracaoMov2[i]*(self.frameMov2**2)/2
			self.frameMov2 += 1

		# encontra o sistema certo de place de acordo se for relativo ou simples
		if self.modelos[0] == 'relativo' and self.modelos[1] == 'relativo':
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'relativo':
				self.frame.place(relx=pos[0], rely=pos[1], relwidth=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'simples':
				self.frame.place(relx=pos[0], rely=pos[1], relwidth=pos[2],heigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'relativo':
				self.frame.place(relx=pos[0], rely=pos[1], width=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'simples':
				self.frame.place(relx=pos[0], rely=pos[1], width=pos[2],heigh=pos[3])
		if self.modelos[0] == 'relativo' and self.modelos[1] == 'simples':
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'relativo':
				self.frame.place(relx=pos[0], y=pos[1], relwidth=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'simples':
				self.frame.place(relx=pos[0], y=pos[1], relwidth=pos[2],heigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'relativo':
				self.frame.place(relx=pos[0], y=pos[1], width=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'simples':
				self.frame.place(relx=pos[0], y=pos[1], width=pos[2],heigh=pos[3])
		if self.modelos[0] == 'simples' and self.modelos[1] == 'relativo':
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'relativo':
				self.frame.place(x=pos[0], rely=pos[1], relwidth=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'simples':
				self.frame.place(x=pos[0], rely=pos[1], relwidth=pos[2],heigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'relativo':
				self.frame.place(x=pos[0], rely=pos[1], width=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'simples':
				self.frame.place(x=pos[0], rely=pos[1], width=pos[2],heigh=pos[3])
		if self.modelos[0] == 'simples' and self.modelos[1] == 'simples':
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'relativo':
				self.frame.place(x=pos[0], y=pos[1], relwidth=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'relativo' and self.modelos[3] == 'simples':
				self.frame.place(x=pos[0], y=pos[1], relwidth=pos[2],heigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'relativo':
				self.frame.place(x=pos[0], y=pos[1], width=pos[2],relheigh=pos[3])
			if self.modelos[2] == 'simples' and self.modelos[3] == 'simples':
				self.frame.place(x=pos[0], y=pos[1], width=pos[2],heigh=pos[3])

		# incrementa variavel e roda novamente
		self.frameAtual += 1
		if self.frameFinal >= self.frameAtual:
			self.origem.after(self.time_frame, self.__update)
		else:
			return None
	def info():
		'''
		Retorna informações da classe.
		'''
		print(transition.__doc__)