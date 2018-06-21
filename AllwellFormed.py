#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from Clause_joining import *
import string
from PS_word_order import *
from operator import itemgetter
from Sanity_Checks import *


class AllWellFormed(object):
    def __init__(self, tree, ps_S):
        self.tree=tree
        self.ps_S=ps_S
    def allwellFormedtrees(self):
        n_PS_tree_Subj=0
        n_DS_tree_Subj=0
        n_DS_tree_OBJ_1=0
        n_PS_tree_OBJ_1=0
        n_DS_tree_SUBJ_Dat=0
        n_PS_tree_SUBJ_Dat=0
        n_DS_tree_OBJ_2=0
        n_PS_tree_OBJ_2=0
        n_DS_tree_OBJ_Comp=0
        n_PS_tree_OBJ_Comp=0
        flag_duplicate=True
        flag_arg=True
        flag_clause=True
        flag_termmatch=True
        flag_wellformed=True
        nn_pred=0
        nn_clause=0
        n_pred=0
        flagvalue=True

        for chunk in self.tree:
            if chunk.getPos()=='VGF' or chunk.getPos()=='NULL__VGF' or chunk.getPos()=='VGNN' or chunk.getPos()=='VGNF' or chunk.getPos()=='NULL__VGNN' or chunk.getPos()=='VGNF':
                nn_pred=nn_pred+1
                for child in self.tree.getChildren(chunk.getName()):
                    if child.isChild('k1', chunk.getName()):
                        if not self.tree.existChild('k1s', chunk.getName()):
                            if not (child.getPos()=='VGF' or child.getPos()=='NULL__VGF' or child.getPos()=='VGNN' or child.getPos()=='VGNF'):
                                n_DS_tree_Subj=n_DS_tree_Subj+1
                    if child.isChild('k2', chunk.getName()) or child.isChild('k2p', chunk.getName()):
                        if not (child.getPos()=='VGF' or child.getPos()=='NULL__VGF' or child.getPos()=='VGNN' or child.getPos()=='VGNF'):
                            n_DS_tree_OBJ_1=n_DS_tree_OBJ_1+1
                    if child.isChild('k4a', chunk.getName()):
                        if not (child.getPos()=='VGF' or child.getPos()=='NULL__VGF' or child.getPos()=='VGNN' or child.getPos()=='VGNF'):
                            n_DS_tree_SUBJ_Dat=n_DS_tree_SUBJ_Dat+1
                    if child.isChild('k4', chunk.getName()) or child.isChild('k2g', chunk.getName()):
                        if not (child.getPos()=='VGF' or child.getPos()=='NULL__VGF' or child.getPos()=='VGNN' or child.getPos()=='VGNF'):
                            n_DS_tree_OBJ_2=n_DS_tree_OBJ_2+1
                    if child.isChild('k2s', chunk.getName()):
                        if not (child.getPos()=='VGF' or child.getPos()=='NULL__VGF' or child.getPos()=='VGNN' or child.getPos()=='VGNF'):
                            n_DS_tree_OBJ_Comp=n_DS_tree_OBJ_Comp+1
        
        for chunk in self.tree:
            if not chunk.getDrel():
                if not chunk.getDMrel():
                    n_pred=n_pred+1

        if n_pred==1:
            PS_tree=self.ps_S
            for word in PS_tree.split():
                if word=='[.NP-OBJ-1' or word=='[.CCP-OBJ-1' or word=='[.JJP-OBJ-1' or word=='[.NULL__CCP-OBJ-1' or word=='[.NULL__NP-OBJ-1':
                    n_PS_tree_OBJ_1=n_PS_tree_OBJ_1+1
                if word=='[.NP-SUBJ' or word=='[.CCP-SUBJ' or word=='[.JJP-SUBJ' or word=='[.NULL__CCP-SUBJ' or word=='[.NULL__NP-SUBJ':
                    n_PS_tree_Subj=n_PS_tree_Subj+1
                if word=='[.NP-SUBJ-Dat' or word=='[.CCP-SUBJ-Dat' or word=='[.JJP-SUBJ-Dat' or word=='[.NULL__CCP-SUBJ-Dat' or word=='[.NULL__NP-SUBJ-Dat':
                    n_PS_tree_SUBJ_Dat=n_PS_tree_SUBJ_Dat+1
                if word=='[.NP-OBJ-2' or word=='[.CCP-OBJ-2' or word=='[.JJP-OBJ-2' or word=='[.NULL__CCP-OBJ-2' or word=='[.NULL__NP-OBJ-2':
                    n_PS_tree_OBJ_2=n_PS_tree_OBJ_2+1
                if word=='[.NP-OBJ-Comp' or word=='[.CCP-OBJ-Comp' or word=='[.JJP-OBJ-Comp' or word=='[.NULL__CCP-OBJ-Comp' or word=='[.NULL__NP-OBJ-Comp':
                    n_PS_tree_OBJ_Comp=n_PS_tree_OBJ_Comp+1
                if word=='[.S' or word=='[.S-NN' or word=='[.S-NF' or word=='[.S**' or word=='[.S-NN**' or word=='[.S-NF**':
                    nn_clause=nn_clause+1

            DS_term_String=''
            for chunk in self.tree:
                for node in chunk:
                    if not node.getLemma()=='((':
                        DS_term_String=DS_term_String+' '+node.getName()

            terminal=[]
            for word in PS_tree.split():
                if not word==']':
                    flag=0
                    for char in word:
                        if char=='[':
                            flag=flag+1
                        else:
                            flag=flag
                    if flag==0:
                        terminal.append(word)

            do=Sanity_checks(self.tree, PS_tree)
            try:
                if len(set(terminal))==len(terminal):
                    flag_duplicate=True
                else:
                    flag_duplicate=False
                    
                if n_DS_tree_Subj==n_PS_tree_Subj and n_DS_tree_OBJ_1==n_PS_tree_OBJ_1 and n_DS_tree_SUBJ_Dat==n_PS_tree_SUBJ_Dat and n_DS_tree_OBJ_2==n_PS_tree_OBJ_2 and n_DS_tree_OBJ_Comp==n_PS_tree_OBJ_Comp:
                    flag_arg=True
                else:
                    flag_arg=False
                    
                if nn_pred==nn_clause:
                    flag_clause=True
                else:
                    flag_clause=False
                    
                if do.terminal_match()[1]==False:
                    flag_termmatch=False
                else:
                    flag_termmatch=True
            except KeyError:
                flag_termmatch=False
        else:
            flagvalue=False

        return [flag_duplicate, flag_arg, flag_clause, flag_termmatch]
            
