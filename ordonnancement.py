#!/usr/bin/env python

""" Classe Ordonnancement """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019 - novembre 2020'
__version__ = '0.2'

import job









class Ordonnancement():

    # constructeur pour un ordonnancement vide
    def __init__(self, nombre_machines):
        # liste des jobs dans l'ordre où ils doivent être ordonnancés
        self.sequence = [] 

        # nombre de machines utilisées
        self.nombre_machines = nombre_machines

        # durée de l'ordonnancement, c'est-à-dire date de fin de la dernière
        # opération exécutée
        self.duree = 0 

        # pour chaque machine, date à partir de laquelle on peut exécuter une
        # nouvelle opération.
        # Les machines sont numérotées à partir de 0
        self.date_disponibilite = [0 for i in range(self.nombre_machines)]


    def afficher(self):
        print("Ordre des jobs :", end='')
        for job in self.sequence:
            print(" ",job.numero," ", end='')
        print()
        for job in self.sequence:
            print("Job", job.numero, ":", end='')
            for machine in range(self.nombre_machines):
                print(" op", machine, 
                      "à t =", job.date_debut[machine],
                      "|", end='')
            print()
        print("Cmax =", self.duree)



    #####################
    # exo 2 :  A REMPLIR
    #####################
    def ordonnancer_job(self, job):
        self.sequence.append(job)

        # IF 1 JOB : 
        if(len(self.sequence)==1):
            job.date_debut[0]=0
            for m in range(1,self.nombre_machines):
                job.date_debut[m] = job.date_debut[m-1] + job.duree_operation[m-1]
        # ELSE >= 2 JOB : 
        else :
            job.date_debut[0] = self.sequence[-2].date_debut[0] + self.sequence[-2].duree_operation[0]
            for m in range (1,self.nombre_machines):
                job.date_debut[m] = max(self.sequence[-2].date_debut[m] + self.sequence[-2].duree_operation[m],
                              job.date_debut[m-1] + job.duree_operation[m-1])
            
        #job.duree = job.date_debut[-1] + job.duree_operation[-1] 



    #####################
    # exo 3 :  A REMPLIR
    #####################
    def ordonnancer_liste_job(self, liste_jobs):
        for j in liste_jobs : 
            self.ordonnancer_job(j)
        self.duree = liste_jobs[-1].date_debut[-1] + liste_jobs[-1].duree_operation[-1]
    
        

# Pour tester
if (__name__ == "__main__"):
    """
    a = job.Job(1,[1,1,1,10,1])
    b = job.Job(2,[1,10,1,1,1])
    c = job.Job(3,[10,1,1,1,1])
    a.afficher()
    b.afficher()
    c.afficher()
    l = [a,b,c]
    ordo = Ordonnancement(5)
    ordo.ordonnancer_liste_job(l)
    ordo.sequence
    ordo.afficher()
    a.afficher()
    b.afficher()
    c.afficher()
    """
    a = job.Job(0,[5,9,8,10,1])
    b = job.Job(2,[9,4,5,8,6])
    a.afficher()
    b.afficher()
    #l = [a,b]
    l = [b,a]
    ordo = Ordonnancement(5)
    ordo.ordonnancer_liste_job(l)
    ordo.sequence
    ordo.afficher()
    a.afficher()
    b.afficher()
    