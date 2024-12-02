# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:08:49 2024

@author: lenovo
"""
import numpy as np
class QuantumCircuit:
    def __init__(self,n_q): #n_q=nombre de qubits
        self.n_q=n_q
        self.tab_stbl=np.zeros((2*n_q,2*n_q),dtype=int)
        self.phase=np.zeros(2*n_q,dtype=int)
        self.portes=[]
    
    
        for i in range(n_q):
            self.tab_stbl[i,i+n_q]=1
        
    def ajouter_porte(self,porte,*qubits):
        self.portes.append((porte,qubits))
       
    def executer(self):
        for porte, qubits in self.portes:
            if porte=="h":
                self.appliquer_h(*qubits)
            elif porte=="s":
                self.appliquer_s(*qubits)
            elif porte=="cx":
                self.appliquer_cx(*qubits)
            else: 
                raise ValueError(f"Porte Inconnue :{porte}")
    
    def appliquer_h(self,q_cible):    
        for i in range(len(self.tab_stbl)):
            self.tab_stbl[i,q_cible],self.tab_stbl[i,q_cible+self.n_q]=\
                self.tab_stbl[i,q_cible+self.n_q],self.tab_stbl[i,q_cible]
                                                            
    def appliquer_s(self,q_cible):
    
        for i in range(len(self.tab_stbl)):
            self.tab_stbl[i,q_cible]^=self.tab_stbl[i,q_cible+self.n_q]
    
    
    def appliquer_cx(self,q_controle,q_cible):
        
        for i in range(len(self.tab_stbl)):
            self.tab_stbl[i,q_cible]^=self.tab_stbl[i,q_controle]
            self.tab_stbl[i,q_controle+self.n_q]^=self.tab_stbl[i,q_cible+self.n_q]
    
    
    
    def afficher_stabilisateurs(self):
      
        print("Stabilisateurs :")
        for i in range(len(self.tab_stbl)):
            x=''.join(map(str,self.tab_stbl[i,:self.n_q]))
            z=''.join(map(str,self.tab_stbl[i,self.n_q]))
            print(f"Stabilisateur{i+1}:X={x},Z={z},Phase={self.phases[i]}")
    
    
    
