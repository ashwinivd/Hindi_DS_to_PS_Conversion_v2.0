
#-*- coding: UTF-8 -*-
# filename   : Phrases.py
# author     : Himanshu Yadav
# last update: 7/13/2016
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
import string
from operator import itemgetter


############################## Begin: class Phrases ##############################

 
class Phrase(object):
    # initializes 'Phrase' from 'tree' and 'ChunkName'
    # tree: one of the tree line from SSF treelist
    # Chunkname: Name of the chunk from chunklist in the tree
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)        # calls 'Word_order' class which allocates unique id to each chunk according to linear word order

    
    # draws terminal nodes for any chunk (e.g. splits phrasal NP node into NNP and PSP terminal nodes)
    # chunk: any chunk from chunk-list in a tree
    def terminal_nodes(self, chunk, node_id):
        all_t_node={}
        n=0
        for node in chunk:
            t_node={}
            morph=[]
            if node.getLemma()=='((':
                no_entry=''
            else:
                node_PC=node.getPos()
                t_parent_id=node_id
                n=n+1
                t_node_id=1000+(t_parent_id*10)+n
                node_name=node.getName()
                node_name=string.replace(node_name, 'ठ', 'प')
                morph=node.getAF()
                node_type='Terminal-Node'
                linear_id=self.check.node_order()[node.getName()]
                t_node[node_name]=[t_parent_id, t_node_id, node_PC+' '+node_name, morph, node_type, linear_id]
                all_t_node=dict(all_t_node.items()+t_node.items())
                all_t_node=dict(all_t_node)
                all_t_node.update(t_node)
        return all_t_node

    # draws internal phrase structure for a given phrase.
    # uses modifier-modified relation given in DS treebank to identify head child of a phrase.
    # takes takes head_child as a chunk to draw phrase structure of non-head children
    def phrase(self, chunk, node_id):
        head_child={}
        ChunkName=chunk.getName()
        Chunk_PC=chunk.getPos()
        parent_chunk=chunk
        head_parent_id=node_id
        head_node_id=self.check.order()[ChunkName]
        head_node_name=ChunkName
        morph=[]
        head_node_type='Head-Child'
        #head_child[Chunk_PC]=[head_parent_id, head_node_id, head_node_name, morph, head_node_type]
        head_child_terminal=self.terminal_nodes(chunk, head_node_id)
        dict_head=dict(head_child.items()+head_child_terminal.items())
        dict_head=dict(head_child)
        dict_head.update(head_child_terminal)
        all_dict_non_head={}
        for chunk in self.tree.getChildren(ChunkName):
            non_head={}
            dict_non_head={}
            for node in chunk:
                if node.getLemma()=='((':
                    linear_id=self.check.node_order()[node.getName()]
                    
            if chunk.getPos()=='VGF' or chunk.getPos()=='NULL__VGF' or chunk.getPos()=='NULL__VGNN' or chunk.getPos()=='NULL__VGNF' or chunk.getPos()=='VGNF' or chunk.getPos()=='VGNN':
                child=' flag '+str(self.check.order()[chunk.getName()])
                all_dict_non_head[child]=[node_id, self.check.order()[chunk.getName()], 'flag', [], 'Embedded-Clause', linear_id]
            else:
                non_head_parent_id=node_id
                non_head_node_name=chunk.getName()
                morph=[]
                non_head_node_type='Non-Head-Child'
                if not self.tree.getChildren(chunk.getName()):
                    non_head_node_id=self.check.order()[non_head_node_name]
                    non_head[chunk.getName()]=[non_head_parent_id, non_head_node_id, chunk.getPos(), morph, non_head_node_type, linear_id]
                    non_head_terminal=self.terminal_nodes(chunk, non_head_node_id)
                    dict_non_head=dict(non_head.items()+non_head_terminal.items())
                    dict_non_head=dict(non_head)
                    dict_non_head.update(non_head_terminal)
                    
                else:
                    non_head_node_id=self.check.order()[non_head_node_name]
                    non_head[chunk.getName()]=[non_head_parent_id, non_head_node_id, chunk.getPos(), morph, non_head_node_type, linear_id]
                    child_non_head=self.phrase(chunk, non_head_node_id)
                    dict_non_head=dict(non_head.items()+child_non_head.items())
                    dict_non_head=dict(non_head)
                    dict_non_head.update(child_non_head)
            all_dict_non_head=dict(all_dict_non_head.items()+dict_non_head.items())
            all_dict_non_head=dict(all_dict_non_head)
            all_dict_non_head.update(dict_non_head)
                    
        all_dict_non_head=dict(all_dict_non_head.items()+dict_head.items())
        all_dict_non_head=dict(all_dict_non_head)
        all_dict_non_head.update(dict_head)
        
        return all_dict_non_head
        
############################## End  : class Phrase   ###############################
    
############################## Begin: class Fragments ##############################
# It applies the fragmention process on a given clause and fragments it into predicate, arguments and adjuncts for distinction.

class Fragments(object):
    # initializes the Fragments from 'tree' and 'pred'
    # pred: head-chunk of the clause for which fragments are to be separated 
    def __init__(self, tree, pred):
        self.tree=tree
        self.pred=pred
        self.Pred_P=self.pred.getName()
        self.check=Word_order(self.tree)
        self.create=Phrase(self.tree)

    # returns predicate and its word order position
    def predicate(self):
        Pred={}
        dict_pred={}
        Pred_PC=self.pred.getPos()
        pred_node_id=self.check.order()[self.pred.getName()]
        pred_parent_id=pred_node_id+200
        pred_node_name=self.pred.getName()
        morph=[]
        pred_node_type='Head-of-Clause'
        for node in self.pred:
            if node.getLemma()=='((':
                linear_id=self.check.node_order()[node.getName()]
        Pred[pred_node_name]=[pred_parent_id, pred_node_id, Pred_PC, morph, pred_node_type, linear_id]
        pred_terminal=self.create.terminal_nodes(self.pred, pred_node_id)
        dict_pred=dict(Pred.items()+pred_terminal.items())
        dict_pred=dict(Pred)
        dict_pred.update(pred_terminal)

        return dict_pred 

    # returns a dictionary of arguments with their word-order positions
    # we have at this level defined some basic labels like NP-SUBJ, NP-OBJ-1, NP-SUBJ-Dative etc. to ditinguish between arguments

    def fragments(self):
        parent_id=self.check.order()[self.pred.getName()]+200
        dict_frag={}
        dict_n_frag={}
        frag={}
        for chunk in self.tree.getChildren(self.pred.getName()):
            node_PC=chunk.getPos()
            node_name=chunk.getName()
            morph=[]
            for nodename in chunk:
                if nodename.getLemma()=='((':
                    linear_id=self.check.node_order()[nodename.getName()]
            if node_PC=='VGF' or node_PC=='NULL__VGF' or node_PC=='NULL__VGNN' or node_PC=='NULL__VGNF' or node_PC=='VGNF' or node_PC=='VGNN':
                Frag=' flag '+str(self.check.order()[chunk.getName()])
                dict_n_frag[Frag]=[parent_id, self.check.order()[chunk.getName()], 'flag', [], 'Embedded-Clause', linear_id]
            else:
                if (chunk.isChild('k1', self.Pred_P)):
                    if self.tree.existChild('k1s', self.Pred_P):        
                        Frag=node_PC
                        node_type='Copula-Subject'
                        if not self.tree.getChildren(node_name):
                            node_id=self.check.order()[node_name]
                            frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                            frag_terminal=self.create.terminal_nodes(chunk, node_id)
                            dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                            dict_frag=dict(dict_frag)
                            dict_frag.update(frag)
                            dict_frag.update(frag_terminal)
                        else:
                            node_id=self.check.order()[node_name]
                            frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                            dict_child=self.create.phrase(chunk, node_id)
                            dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                            dict_frag=dict(dict_frag)
                            dict_frag.update(frag)
                            dict_frag.update(dict_child)
                    else:
                        Frag=node_PC+'-SUBJ'
                        node_type='Grammatical-Subject'
                        if not self.tree.getChildren(node_name):
                            node_id=self.check.order()[node_name]
                            frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                            frag_terminal=self.create.terminal_nodes(chunk, node_id)
                            dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                            dict_frag=dict(dict_frag)
                            dict_frag.update(frag)
                            dict_frag.update(frag_terminal)
                        else:
                            node_id=self.check.order()[node_name]
                            frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                            dict_child=self.create.phrase(chunk, node_id)
                            dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                            dict_frag=dict(dict_frag)
                            dict_frag.update(frag)
                            dict_frag.update(dict_child)

                elif (chunk.isChild('k4', self.Pred_P) or chunk.isChild('k2g', self.Pred_P)):
                    Frag=node_PC+'-OBJ-2'
                    node_type='Secondary-Object'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                    
                elif chunk.isChild('k4a', self.Pred_P):
                    Frag=node_PC+'-SUBJ-Dat'
                    node_type='Dative-Subject'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                        
                       
                elif chunk.isChild('pk1', self.Pred_P):
                    Frag=node_PC+'-SUBJ'
                    node_type='Grammatical-Causal-Subject'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                            
                elif chunk.isChild('jk1', self.Pred_P):
                    Frag=node_PC+'-J-SUBJ'
                    node_type='Caused-Subject'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                        
                elif (chunk.isChild('k2', self.Pred_P) or chunk.isChild('k2p', self.Pred_P)):
                    Frag=node_PC+'-OBJ-1'
                    node_type='Grammatical-Object'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                            

                elif chunk.isChild('k2s', self.Pred_P):
                    Frag=node_PC+'-OBJ-Comp'
                    node_type='Object-Complement'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
                            
                elif chunk.nameEquals('BLK'):
                    SYM='|'

                else:
                    Frag=node_PC
                    node_type='Adjunct'
                    if not self.tree.getChildren(node_name):
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        frag_terminal=self.create.terminal_nodes(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+frag_terminal.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(frag_terminal)
                    else:
                        node_id=self.check.order()[node_name]
                        frag[node_name]=[parent_id, node_id, Frag, morph, node_type, linear_id]
                        dict_child=self.create.phrase(chunk, node_id)
                        dict_frag=dict(dict_frag.items()+frag.items()+dict_child.items())
                        dict_frag=dict(dict_frag)
                        dict_frag.update(frag)
                        dict_frag.update(dict_child)
        dict_frag=dict(dict_frag.items()+dict_n_frag.items())
        dict_frag=dict(dict_frag)
        dict_frag.update(dict_n_frag)

        return dict_frag
    
