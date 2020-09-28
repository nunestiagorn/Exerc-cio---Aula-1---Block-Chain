import os
import hashlib


class Bloco:

	def __init__(self, origem, destino, hash_anterior=None):
		self.origem = origem
		self.destino = destino
		self.hash_anterior = 'Vazio' if hash_anterior is None else hash_anterior
		self.hash = self.gerar_hash()
		self.mensagem = ''

	def __str__(self):
		text = '''Origem: {}\nDestino: {}\nMensagem: Ola {}. Meu nome é {}\nHash: {}\nHash Anterior: {}\n'''
		return text.format(self.origem, self.destino, self.origem, self.destino, self.hash, self.hash_anterior)

	def gerar_hash(self):
		
		text = 'Origem: {}\nDestino: {}\nMensagem: Ola {}. Meu nome é {}.\n'.format(self.origem, self.destino, self.destino, self.origem)

		return hashlib.sha256(text.encode()).hexdigest()


def cria_blocos(nomes):

	blocos = []
	for n1, n2 in zip(nomes[:-1], nomes[1:]):
		bloco = Bloco(n1, n2)
		if len(blocos) > 0:
			bloco.hash_anterior = blocos[-1].hash
		blocos.append(bloco)

	bloco = Bloco(n2, nomes[0], blocos[-1].hash)
	blocos.append(bloco)
	blocos[0].hash_anterior = blocos[-1].hash

	return blocos


def valida_blocos(blocos):

	hash_anterior = None
	for i, b in enumerate(blocos):

		b2 = blocos[i-1]
		if b.hash_anterior == b2.hash:
			print('Bloco', i, 'OK')
			#print(b)
			#print('-----')
		else:
			print('Bloco:', i)
			print('Hash anterior encontrada:', b.hash_anterior)
			print('Hash correta:', b2.hash)
			return False
	return True


def salva_bloco(bloco, i):

	if not os.path.exists('blocos'):
		os.makedirs('blocos')

	with open('blocos/Bloco_{}.txt'.format(i+1), 'w') as f:
		f.write(bloco.__str__())

def parse_linha(linha):

	return linha.replace('\n', '').split(' ')[-1]


def le_bloco(arquivo):

	with open(arquivo, 'r') as f:
		origem = parse_linha(f.readline())
		destino = parse_linha(f.readline())
		f.readline() #mensagem
		f.readline() #hash atual
		hash_anterior = parse_linha(f.readline())

		bloco = Bloco(origem, destino, hash_anterior)
	return bloco


if __name__ == '__main__':

	nomes = ['Chase', 'Rennie', 'Franklin', 'Huynh', 'England', 'Lugo', 'Rodrigues', 'Betts', 'Cummings', 'Irwin', 'Nixon', 'Higgins', 'Cook', 'Ross', 'Eaton', 'Fountain']

	# cria blocos a partir da lista de nomes
	blocos = cria_blocos(nomes)

	# valida a lista de blocos
	print('BLOCOS 1', valida_blocos(blocos))

	# salva os blocos em arquivos texto
	for i, b in enumerate(blocos):
		salva_bloco(b, i)

	# le do arquivo e guarda os blocos numa lista
	blocos2 = []
	index = 0
	arquivo = 'blocos/Bloco_{}.txt'.format(index+1)
	while os.path.exists(arquivo):
		b = le_bloco(arquivo)
		blocos2.append(b)
		index += 1
		arquivo = 'blocos/Bloco_{}.txt'.format(index+1)
		
	# valida a lista de blocos
	print('BLOCOS 2', valida_blocos(blocos2))
