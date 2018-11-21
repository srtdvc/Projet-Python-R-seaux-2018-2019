#!/usr/bin/python
##
# TCP chat server
# port 1664
##
# coding : utf-8
from sys import argv 
from socket import *
from select import select
import os 

##POUR LANCER LE CHAT COTE SERVEUR ./chatp2p.py
##POUR LANCER LE CHAT COTE CLIENT ./chatp2p.py ipduserveur exemple pour le pc1 ./chatp2p.py 10.0.0.1 

if (len(argv))==2:
	print("Je suis client")
	stri="nc %s 1664" % argv[1]
	os.system(stri)
elif(len(argv)==1):
	s=socket(AF_INET, SOCK_STREAM)
	s.bind(('0.0.0.0', 1664))
	s.listen(5)
	socks={}
	banned_liste={}
	socks["serveur"]=s
	names={}
	identifier=False
	while True:
	  try:
	  	lin, lout, lex=select(socks.values(), [], []) 
	  	print ("select got %d read events" % (len(lin)))
	  except error :
		pass
	  else:

		  for t in lin:
		    if t==s: # this is an incoming connection
		      (c, addr)=s.accept()
		      msg="Hello, veuillez vous identifier SVP avec la commande START suivi de votre nickname :\n " 
		      socks[addr[0]]=c
		      banned_liste[addr[0]]=[]
		      c.send(msg.encode())	 	
		    else: # someone is speaking
		      who=t.getpeername()[0]
		      data=t.recv(1024)
		      if data:
			msg="%s: %s\n" % (who, data.strip())
		      else: # connection closed
			socks[who].remove(t)
			msg="Goodbye %s!\n" % (who,)
		      tab=msg.split(' ')
		      commande=tab[1].split('\'')
		      option=tab[1]
		      if option =="pm" and identifier and len(tab)>3:
			msg=""
			for chaine in tab[3:]:
				msg="%s %s" % (msg,chaine)
			for per in names.keys():
				if names[per] == who:
					msg="%s: %s\n" % (per,msg)
			if tab[2] in names.keys():
		      		personne=names[tab[2]]
				if who not in banned_liste[personne]:
		        		socks[personne].send(msg.encode())
				else :
					t.send("Vous etes bannis\n".encode())
			else:
				t.send("Erreur personne non existante\n".encode())
		      elif option =="bm":
			msg=""
			for chaine in tab[2:]:
				msg="%s %s" % (msg,chaine)
			for per in names.keys():
				if names[per] == who:
					msg="%s: %s\n" % (per,msg)
		      	for personne in socks.keys():
				if personne != "serveur" and (who not in banned_liste[personne]) :
					socks[personne].send(msg.encode())
		      elif option == "start": #Permet de demarrer une session cote client en faisant start nickname
			var=tab[2].split('\n')
			perss=var[0]
		      	names[perss]=who
			msg="________________________\nHello %s\n vous etes connecter avec les personnes suivantes : \n" % (tab[2],)
			for nom in names.keys():
				msg="%s %s\n" % (msg,nom)
			socks[addr[0]]=c
			banned_liste[addr[0]]=[]
			identifier=True
			c.send(msg.encode())
		      elif option == "list\n":#Permet d'afficher la liste des clients connectes
		      	stri="\n\n____________________\n\nLa liste des clients est de %s\n\n __________________\n\n" % (names.keys())
			socks[who].send(stri.encode())
		      elif option == "quit\n": #Permet de quitter le chat
			msg='Vous avez quitter\n'
			socks[who].send(msg)
			socks[who].shutdown(2)
			socks[who].close()
			continue 
		      elif option == "ban" and identifier : #Permet de bannir une personne sur le chat en faisant ban nickname
			var=tab[2].split('\n')
			perss=var[0]
			if perss in names.keys():
				personne=names[perss].split('\n')
				banned_liste[who].append(personne[0])
			else:
				t.send("Erreur personne non existante\n".encode())
		      elif option == "unban" and identifier : #Permet de retirer le ban sur une personne avec unban nickname
			var=tab[2].split('\n')
			perss=var[0]
			if perss in names.keys():
				personne=names[perss].split('\n')
				banned_liste[who].remove(personne[0]) 
			else:
				t.send("Erreur personne non existante\n".encode()) 
		      else:
			if not identifier:
				msg="Il faut s'identifier \n"
			else:
				msg="Commande erronee \n"
		      	t.send(msg.encode())	
else :
	print("\nFaux 2 parametres possible seulement ! \n")      



