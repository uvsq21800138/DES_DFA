# Python[version]
from os.path import isfile, join
import StrBinaire as SB 
import DES
import math

## Variables globales
Chex = ""		# claire en hexadecimal
Jhex = ""		# chiffre juste en hexadecimal
Ihex = []		# liste des chiffres en hexadecimal
Claire = ""	  	# claire en binaire
Juste = ""	  	# chiffre juste en binaire
Injustes = {}   # chiffre injuste en binaire
JP = ""		 	# juste permuté
JbL = ""		# bloc L du juste
JbR = ""		# bloc R du juste
JRi = ""		# bloc input Sbox du juste
SO = {}			# seulement les sortie de Sbox fauté
FI = {}			# seulement les fautes en entrée de Sbox
NbF = []		# nombre de faute par Sbox
K16 = ""		# clé partielle K16
MK = ""			# clé maitre
MKP = {}		# clé maitre complete

# Récupère les donnees en entrée et les convertie en string binaire 
def Input_attaque():
	global Chex, Jhex, Ihex, Claire, Juste, Injustes
	# recuperation du fichier input et liste sortie
	filename = "input.txt"
	chiffres = {}
	# si le nom est bien représenté, on récupère les données
	if isfile(join(filename)):
		# lecture du fichier
		f1 = open(filename, 'r').readlines()
		Chex = f1[0].replace(" ", "").replace('\n','')
		Jhex = f1[1].replace(" ", "").replace('\n','')
		Claire = SB.taille(format(int(Chex,16),"b"),64)
		Juste = SB.taille(format(int(Jhex,16),"b"),64)
		i = 2
		for line in f1 :
			if line != f1[0] and line != f1[1]:
				hexa = line.replace(" ", "").replace('\n','')
				Ihex.append(hexa)
				Injustes[hexa] = SB.taille(format(int(hexa,16),"b"),64)

# Ecrit la liste des résultat de l'attaque
def Output_attaque():
	filename = "output.txt"
	f = open(filename, 'w')
	f.write("K16 : "+K16+"\n")
	f.write("Master key : "+MK+"\n")
	f.write("\nKeys\n")
	(keys, cd)= DES.key_shedule(MK)
	f.write(' '+cd+'\n')
	for key in keys:
		f.write(key+'\n')
	f.write("\nMaster Key potentiel bin\n")
	for i in range(int(math.pow(2,int(8)))):
		k = format(i,"b")
		k = SB.taille(k,8)
		f.write(k+' '+MKP[k]+'\n')
	
	f.write("\nMaster Key potentiel hex\n")
	for i in range(int(math.pow(2,int(8)))):
		k = format(i,"b")
		k = SB.taille(k,8)
		f.write(format(int(MKP[k],2),"x").upper()+'\n')
	f.close()

# Ecrit la solution MK avec les claire et chiffré utilisé (pour tester)
def Output_solution(k, chiffre):
	filename = "solution.txt"
	f = open(filename, 'a')
	if(chiffre == Juste):
		f.write("Voici la solution :\n")
		f.write("Claire :\t"+Claire+"\n")
		f.write("Chiffre :\t"+chiffre+"\n")
		f.write("Master key:"+MKP[k]+"\n")
		f.write("Claire  (h):\t"+format(int(Claire,2),"x").upper()+"\n")
		f.write("Chiffre (h):\t"+format(int(chiffre,2),"x").upper()+"\n")
		f.write("Master key (h): "+format(int(MKP[k],2),"x").upper()+"\n\n")
	else : 
		f.write("Aucune solution n'a ete trouve.\n\n")
	f.close()

# Initie les valeurs du problème sur le chiffre juste
def init_juste():
	global JP, JbL, JbR, JRi
	JP = DES.permute(DES.IP,Juste)
	JbL = SB.part(JP,0,32,64)
	JbR = SB.part(JP,1,32,64)
	
	###### Fonction F ######
	# expension
	JER = DES.permute(DES.E,JbR)
	JRi = SB.coupe(JER,8,6,48)

# Génère les valeurs du problème sur les chiffres injustes
def faute_chiffre(chiffre, injuste):
	global FI, SO
	P = DES.permute(DES.IP,injuste)
	bL = SB.part(P,0,32,64)
	bR = SB.part(P,1,32,64)
	
	# Xor pour les alpha et les fautes
	Alpha = SB.str_xor(JbL,bL)
	Faute = SB.str_xor(JbR,bR)

	###### Fonction F ######
	# P-1 sur alpha
	iPA = DES.permute(DES.iP,Alpha)
	
	# expension
	ER = DES.permute(DES.E,bR)
	EF = DES.permute(DES.E,Faute)
   
	# split des boites S
	iPAi = SB.coupe(iPA,8,4,32)
	Ri = SB.coupe(ER,8,6,48)
	Fi = SB.coupe(EF,8,6,48)
	k = chiffre
	SO[k] = []
	FI[k] = []
	
	## Recherche sur les boite S
	for n in range(8):
		if Fi[n] != "000000":
			SO[k].append(iPAi[n])
			FI[k].append(Fi[n]) 
		else :
			SO[k].append("")
			FI[k].append("") 

# Compte le nombre de fautes par bloc S
def compte_faute():
	global NbF
	NbF = [0,0,0,0,0,0,0,0]
	for c in Ihex:
		for n in range(8) :
			if FI[c][n] != "":
				NbF[n] +=1

''' Autre méthode
def methode_G():
	Gi = [{},{},{},{},{},{},{},{}]
	for i in range(int(math.pow(2,int(6)))):
		k = format(i,"b")
		k = SB.taille(k,6)
		for n in range(8) :
			for c in Ihex:
				if FI[c][n] != "":
					RxK = SB.str_xor(JRi[n],k)
					RxKxF = SB.str_xor(RxK,FI[c][n])
					# Gi(f,k)
					sbi = SB.str_xor(DES.Sbox(n,RxK),DES.Sbox(n,RxKxF))
					if sbi == SO[c][n]:
						if k not in Gi[n].keys() :
							Gi[n][k] = [c]
						else : 
							Gi[n][k].append(c)
	Res = []
	for n in range(8) :
		for k in Gi[n].keys() :
			if len(Gi[n][k]) == NbF[n] :
				Res.append([n,k])
	return Res
'''

# Rassemble les 2⁶ morceaux de K16 pour chaque bloc s'il corresponde à la sortie P-1(alpha)
def methode_K():
	Ki = [{},{},{},{},{},{},{},{}]
	for i in range(int(math.pow(2,int(6)))):
		k = format(i,"b")
		k = SB.taille(k,6)
		for c in Ihex:
			for n in range(8) :
				if FI[c][n] != "":
					RxK = SB.str_xor(JRi[n],k)
					RxKxF = SB.str_xor(RxK,FI[c][n])
					# Gi(f,k)
					sbi = SB.str_xor(DES.Sbox(n,RxK),DES.Sbox(n,RxKxF))
					if sbi == SO[c][n]:
						if k not in Ki[n].keys() :
							Ki[n][k] = 1
						else : 
							Ki[n][k] += 1
	Res = []
	for n in range(8) :
		for k in Ki[n] :
			if Ki[n][k] == NbF[n]:
				Res.append(k)
	return Res

# Génère les clé maitre possible avec la matrice MK créé avec methode_K()
def genere_maitre_p():
	global MKP
	for i in range(int(math.pow(2,int(8)))):
		k = format(i,"b")
		k = SB.taille(k,8)
		m = ""
		n = ""
		cmpt = 0
		for j in range(len(MK)):
			if MK[j] in ['0','1','_'] :
				m += MK[j]
			else :
				m += k[cmpt]
				cmpt += 1
		j = 0
		while j <len(m):
			tmp = 0
			for t in range(7):
				n += m[j+t]
				if m[j+t] == '1' :
					tmp += 1
			if m[j+7] == '_':
				n += str((tmp+1)%2)
				j += 8
			else :
				n += '-'
				j += 8
		MKP[k] = n

# Attaque par faute pour construire la clé maitre 
#	il y a 8 bits manquants car la clé maitre fait 56 bits et la clé partielle fait 48 bits
def attaque_faute():
	global K16, MK
	## Initie les valeurs sur Juste
	init_juste()

	## Récupère les fautes en entrée et les sorties fautés de Sbox
	for c in Ihex:
		faute_chiffre(c,Injustes[c])
	
	## Compte le nombre de faute par Sbox
	compte_faute()
	
	## Résoud le systeme
	# Compte le nombre de fois où les morceaux de k sont solutions bloc par bloc
	K16 = "".join(methode_K())
	MK = DES.key_master(K16)
	genere_maitre_p()
	Output_attaque()
	
# Main à exécuter
def main():
	# Récupère les clés maitres potentielles avec les fautes sur le dernier tour
	Input_attaque()	
	attaque_faute()
	
	# Chiffre avec les clés maitres potentielles et teste si elle donne le chiffré juste
	chiffre = ""
	i = 0
	while chiffre != Juste and i<int(math.pow(2,int(8))):
		k = format(i,"b")
		k = SB.taille(k,8)
		chiffre = DES.chiffre(Claire, MKP[k])
		i += 1
	
	# Imprime la solution et un message si il n'y en a pas.
	if chiffre == Juste :
		Output_solution(k, chiffre)
	else :
		print("Aucune solution n'a été trouvé.")

	
if __name__=="__main__":
	main()
