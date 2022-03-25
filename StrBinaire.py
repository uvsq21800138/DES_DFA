# Python[version]

## opération sur binaire au format string

# opération xor sur les char binaire
def xor(x, y):
	if x in ["0","1"] and y in ["0","1"] :
		if x != y:
			return "1"
		else :
			return "0"
	return "X"

# opération xor sur les string binaire
def str_xor(x, y):
	res = ""
	if len(x) == len(y):
		for i in range(len(x)):
			res += xor(x[i],y[i])
	return res

# complete l'écriture binaire jusqu'à la bonne taille
def taille(word, t):
	tmp1 = word
	while len(tmp1) < t :
		tmp1 = '0'+tmp1
	return tmp1

# coupe le mot word en nb parts d'épaisseur ep (t = nb*ep)
def coupe(word, nb, ep, t):
	l = []
	if nb*ep == t: 
		for i in range(nb):
			j = int(i)*int(ep)
			e = word[j:j+ep]
			l.append(e)
	return l

# renvoie la ieme part d'épaisseur ep (t >= (i+1)*ep)
def part(word, i, ep, t):
	if (i+1)*ep <= t: 
		j = int(i*ep)
		return word[j:j+ep]
	return ""

## int(word, 2) string binaire --> int
## format(int,"b") string binaire <-- int
## int(word, 16) string hexa --> int
## hex(int) string hexa <-- int	
