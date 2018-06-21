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


class Sanity_checks(object):
    def __init__(self, ds_tree, ps_tree):
        self.ds_tree=ds_tree
        self.ps_tree=ps_tree
    def terminal_match(self):
        flag_value=0
        status=True
        DS_terminal={}
        posn=0
        DS_term_String=''
        for chunk in self.ds_tree:
            for node in chunk:
                if not node.getLemma()=='((':
                    posn=posn+1
                    nodename=node.getName()
                    nodename=string.replace(nodename, 'ठ', 'प')
                    DS_terminal[posn]=nodename
                    DS_term_String=DS_term_String+' '+nodename
                    
        extract=PS_word_order(self.ps_tree)
        terminal_nodes=extract.ps_terminal()
        ordered_nodes=sorted(terminal_nodes.items(), key=itemgetter(0))
        PS_terminal={}
        PS_term_Str=''
        index=0
        for node in ordered_nodes:
            flag=0
            for char in node[1]:
                if char=='*':
                    flag=flag+1
                else:
                    flag=flag
            if flag==0:
                index=index+1
                PS_terminal[index]=node[1]
                PS_term_Str=PS_term_Str+' '+node[1]

        ordered_DS_terminal=sorted(DS_terminal.items(), key=itemgetter(1))

        ls_index=[]
        for node in ordered_DS_terminal:
            ls_index.append(node[0])
        indicator=0
        table_terminal=''
        for i in range(1, max(ls_index)+1):
            table_terminal=table_terminal+'\n'+str(i)+'\t\t'+DS_terminal[i]+'\t\t\t\t'+PS_terminal[i]
            if not DS_terminal[i]==PS_terminal[i]:
                flag_value=flag_value+1

        if flag_value==0:
            status=True
        else:
            status=False

        return [table_terminal, status]

    def first_modifier_match(self):
        extract=PS_word_order(self.ps_tree)
        node_order=extract.ps_word_order()
        n=0
        for node in node_order.keys():
            if node=='[.S' or node=='[.S-NN' or node=='[.S-NF' or node=='[.S**' or node=='[.S-NN**' or node=='[.S-NF**':
                token=node_order[node]
                for nodename in node_order.keys():
                    if node_order[nodename]==token+1:
                        first_mod=nodename
                if first_mod=='[.NP-SUBJ' or first_mod=='[.CCP-SUBJ' or first_mod=='JJP-SUBJ' or first_mod=='NULL__CCP-SUBJ':
                    n=n+1
            else:
                n=n
        return n
                
        
        
    

            
