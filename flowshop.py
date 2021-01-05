#!/usr/bin/env python

"""Résolution du flowshop de permutation : 

 - par l'algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019 - Novembre 2020'
__version__ = '0.2'

import job
import ordonnancement
import sommet
import time

# On utilise une file de priorité pour les sommets : on peut
# ainsi accéder à tout moment au sommet de plus petite évaluation
import heapq

# valeurt maximale d'un entier
MAXINT = 10000

class Flowshop():
    def __init__(self, nombre_jobs=0, nombre_machines=0, liste_jobs=None):

        # nopbre de jobs pour le problème
        self.nombre_jobs = nombre_jobs

        # nombre de machines pour le problème
        self.nombre_machines = nombre_machines

        # ensemble des jobs pour le problème (l'ordre n'est pas important)
        self.liste_jobs = liste_jobs


    def definir_par_fichier(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline() 
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nombre_jobs = int(l[0])
        self.nombre_machines = int(l[1])
       
        self.liste_jobs = []
        for i in range(self.nombre_jobs):
            ligne = fdonnees.readline() 
            l = ligne.split()
            # on transforme la suite de chaînes de caractères représentant
            # les durées des opérations en une liste d'entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.liste_jobs.append(j)
        # fermeture du fichier
        fdonnees.close()
        
    
    #####################
    # exo 4 :  A REMPLIR
    #####################
    def ordre_NEH(self):
        """renvoie la liste des jobs ordonnée selon NEH"""
    	
        # on commencer par trier les jobs selon leurs durées 
        # décroissantes
        l = [job for job in self.liste_jobs]
        
        # STEP 1 
        l = sorted(l, key=lambda job:job.duree, reverse=True)
        p = [j.duree for j in l]
        #print(p)
        m = [j.numero for j in l]
        #print(m)
       # print("\n")
        # A REMPLIR
        seq_NEH = [l.pop(0)]
        
        # PAS BON 
        
        for job in l : 
            
            c_min = 10000000
            
            for i in range (0, len(seq_NEH)+1):
                l_int = seq_NEH.copy()
                l_int.insert(i,job)
                
                
                ordo = ordonnancement.Ordonnancement(self.nombre_machines)
                ordo.ordonnancer_liste_job(l_int)
                c = ordo.duree
                
                #print([j.numero for j in l_int], c )
                
                if(c< c_min):
                    c_min = c
                    insert = i
            
            seq_NEH.insert(insert,job)
            #print("On garde : ", [j.numero for j in seq_NEH])
                     
        return seq_NEH


    #####################
    # exo 5 :  A REMPLIR
    #####################
    # calcul de r_kj en tenant compte d'un ordo en cours
    def date_dispo(self, ordo, machine, job):
        
        #   r_{k,j} avec :
        # - machine Mk : k in {0,nombre_machines - 1}
        # - job j : j in {0, nombres_jobs - 1}
        # r représente la date à laquelle une machine j peut démarrer pour le job j 
        
        date_machine_job = 0

        # si première machine  : 
        
        if (machine == 0 ):
            return date_machine_job
        
        """
        # Date de début du job j sur la machine k
        for j in ordo.sequence : 
            if(j==job):
                date_machine_job = j.date_debut[machine] 
        
        
        
        for j in ordo.sequence : 
            print(j)
            if (j == job) : 
                break

            date_machine_job += j.duree_operation[machine]
        """
        m=0
        while m != machine : 
            date_machine_job += job.duree_operation[m]
            m+=1

            

        
        return date_machine_job

    #####################
    # exo 5 :  A REMPLIR
    #####################
    # calcul de q_kj en tenant compte d'un ordo en cours
    def duree_latence(self, ordo, machine, job):
        
        #   q_{k,j} :
        # - machine Mk : k in {0,nombre_machines - 1}
        # - job j : j in {0, nombres_jobs - 1}
        # Lorsqu’un job j est terminé sur une machine Mk il reste à exécuter les
        # opérations de j sur les machines suivantes, ce qui représente une durée
        
        q_machine_job = 0
        
        # si dernière machine
        if machine == self.nombre_machines - 1:
            return q_machine_job
        
        """
        # Temps d'exécution du job j sur les machines suivantes
        for j in ordo.sequence : 
            if(j == job):
                date_debut = j.date_debut[machine] + j.duree_operation[machine]
                date_fin = j.date_debut[self.nombre_machines - 1]+j.duree_operation[self.nombre_machines - 1]
        q_machine_job = date_fin - date_debut
        

        """
        isTerminated = False
        
        m = 0
        while m != machine:
            m+=1
        m+=1
        while m < self.nombre_machines : 
            q_machine_job +=job.duree_operation[m]
            m+=1
            
        """
        for j in ordo.sequence :
            
            if (j==job):
                isTerminated = True
                
            if(isTerminated == True):
                q_machine_job +=j.duree_operation[machine]
            
"""
        
        
        return q_machine_job



    #####################
    # exo 5 :  A REMPLIR
    #####################
    # calcul de la somme des durées des opérations d'une liste
    # exécutées sur une machine donnée
    def duree_jobs(self, machine, liste_jobs):
        duree = 0
        for j in liste_jobs : 
            duree += j.duree_operation[machine]
            
        return duree


    #####################
    # exo 5 :  A REMPLIR
    #####################
    # calcul de la borne inférieure 
    # en tenant compte d'un ordonnancement en cours
    def borne_inf(self, ordo, liste_jobs):
       
        # Exemple 1 :
        # 4 jobs / 5 machines 
        
        ordo.ordonnancer_liste_job(liste_jobs)
        borne_inf = 0
        
        LBk = list()
        for machine in range (self.nombre_machines) : # 0 à nombre_machines - 1
            # On fixe la machine k 
            r = list()
            q = list()
            duree_machine = self.duree_jobs(machine, liste_jobs)
            #print("Durée machine %s : " %machine, duree_machine)
            for j in ordo.sequence : 
                r.append(self.date_dispo(ordo,machine,j))
                q.append(self.duree_latence(ordo,machine,j))
                #print("\t", "Job %s : " %j.numero ,self.date_dispo(ordo,machine,j) ,self.duree_latence(ordo,machine,j) )
            LB = min(r)+min(q)+duree_machine
            #print("LBk = ",LB)
            LBk.append(LB)
                
       
        
        borne_inf = max(LBk)
             
        return borne_inf


    #####################
    # exo 6 :  A REMPLIR
    #####################
    # procédure par évaluation et séparation
    def evaluation_separation(self):

        
        # calcul d'une borne supérieure initiale par l'algo NEH
        # on récupère l'ordre NEH
        l_NEH = self.ordre_NEH()
        # on crée un ordonnancement
        ordo = ordonnancement.Ordonnancement(self.nombre_machines)
        # selon l'ordre NEH
        ordo.ordonnancer_liste_job(l_NEH)
        # on initialise la valeur de la borne sup avec la durée NEH
        borne_sup = ordo.duree
        print("Borne sup de départ =",borne_sup)
        # on mémorise l'ordonnancement de départ
        liste_sup = [j for j in l_NEH]

        # file de priorité pour l'arbre de recherche
        arbre = []
        
        # création de la racine
        ordo = ordonnancement.Ordonnancement(self.nombre_machines)
        borne_inf = self.borne_inf(ordo, l_NEH)  
        print("Borne inf de départ =",borne_inf)
        # le premier sommet est numéroté 1
        numero = 1
        # le premier sommet ne contient aucun jobn placés
        s = sommet.Sommet([], l_NEH, borne_inf, numero)   # S0

        # on ajoute ce sommet dans la file de priorité
        heapq.heappush(arbre, s)                         # F 
        
        
        current_solution = sommet.Sommet(l_NEH, 0, borne_inf, 0)
        current_solution.evaluation = borne_sup
        # Iterate while some vertices remain
        while arbre != []:
            # This will return the next vertex to be examined, and the choice of 
            # queuing structure will change the resulting order
            current_vertex = arbre.pop() # numéro = 1 / l_NEH
            #print([i.numero for i in current_solution.places], current_solution.evaluation)
            if current_vertex.non_places == [] : # On a une solution
                # Testing if it is better or not : 
                if current_vertex.__lt__(current_solution):
                    print("*****************************")
                    print("Solution : ",[i.numero for i in current_vertex.places ], current_vertex.evaluation )
                    print("*****************************")
                    current_solution = current_vertex
            
            for vertex in current_vertex.non_places:
                # Tests whether the current vertex is in the list of explored vertices
                if vertex not in current_vertex.places :
                    # Mark the current_vertex as explored and remove the current_vertex as unexplored 
                    save_places = current_vertex.places.copy()
                    save_places.append(vertex)
                    save_non_places = current_vertex.non_places.copy()
                    save_non_places.remove(vertex)
                    """
                    print("current vertex = ", [i.numero for i in save_places],
                           [i.numero for i in save_non_places])
                    """
                    for neighbor in save_non_places :
                    # We push all unexplored neighbors to the queue

                        numero+=1
                        neighbor_places = save_places.copy()
                        neighbor_places.append(neighbor)
                        neighbor_non_places = save_non_places.copy()
                        neighbor_non_places.remove(neighbor)
                        
                        ordo_neighbor = ordonnancement.Ordonnancement(self.nombre_machines)
                        borne_inf_neighbor = self.borne_inf(ordo_neighbor, neighbor_places)  
                        
                        
                        # On ajoute que si c'est inférieur à la borne inf 
                        if borne_inf_neighbor<current_solution.evaluation:
                            evaluation_neighbor = ordo_neighbor.duree
                            s_neighbor = sommet.Sommet(neighbor_places, neighbor_non_places , evaluation_neighbor, numero) 
                            """
                            print("\t neighbor vertex = ", [i.numero for i in s_neighbor.places],
                                 [i.numero for i in s_neighbor.non_places],borne_inf_neighbor,evaluation_neighbor )
                            """
                            heapq.heappush(arbre, s_neighbor)
                         
            #print("---------")
        borne_sup = current_solution.evaluation
        liste_sup = current_solution.places
        return borne_sup, liste_sup


# Pour tester
if __name__ == "__main__":
    print("JEU 1 :")
    start = time.perf_counter()
    prob = Flowshop()
    prob.definir_par_fichier("jeu1.txt")
    o = ordonnancement.Ordonnancement(prob.nombre_machines)
    #print([i.numero for i in prob.liste_jobs])
    print("Borne inf :", prob.borne_inf(o,prob.liste_jobs))

    print("Ordo NEH :")
    l = prob.ordre_NEH()
    for i in l:
        print(i.numero," ", end="")

    print()
    b, l = prob.evaluation_separation()
    print("Ordonnancement optimal :")
    for i in l:
        print(i.numero,' ',end="")
    print("de durée",b)
    elapsed = time.perf_counter()
    elapsed = elapsed - start
    print ("Time spent in solving is: %s" %(elapsed))

    
    print()
    print("JEU 2 :")
    start = time.perf_counter()
    prob = Flowshop()
    prob.definir_par_fichier("jeu2.txt")
    o = ordonnancement.Ordonnancement(prob.nombre_machines)
    print("Borne inf :", prob.borne_inf(o,prob.liste_jobs))

    print("Ordo NEH :")
    l = prob.ordre_NEH()
    for i in l:
        print(i.numero," ", end="")

    print()
    b, l = prob.evaluation_separation()
    print("Ordonnancement optimal :")
    for i in l:
        print(i.numero,' ',end="")
    print("de durée",b)
    elapsed = time.perf_counter()
    elapsed = elapsed - start
    print ("Time spent in solving is: %s s" %(elapsed))