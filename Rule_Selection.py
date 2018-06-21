#!/usr/bin/python
#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Phrases import *
from operator import itemgetter
import string


class Rule_selection(object):
    def __init__(self, tree, pred):
        self.tree=tree
        self.pred=pred
        self.check=Word_order(self.tree)
        
    def rule_selection(self, parent_id):
        dict_S={}
        S_parent_id=parent_id
        S_node_id=self.check.order()[self.pred.getName()]+300
        VP_node_id=self.check.order()[self.pred.getName()]+200

        for nodes in self.pred:
            if nodes.getLemma()=='((':
                V_linear_id=self.check.node_order()[nodes.getName()]

        S_linear_id=V_linear_id

        S = {}
        VP = {}
        

        get=Fragments(self.tree, self.pred)
        create=Phrase(self.tree)
        Predicate=get.predicate()
        dict_frag=get.fragments()
        

        chunk_posn={}
        for chunk in self.tree.getChildren(self.pred.getName()):
            chunk_posn[chunk.getName()]=self.check.order()[chunk.getName()]
        ordered_frag=sorted(chunk_posn.items(), key=itemgetter(1))

        if ordered_frag:
            first_arg=ordered_frag[0][0]
            first_arg_index=self.check.order()[first_arg]
            for frag in dict_frag:
                if dict_frag[frag][1]==first_arg_index:
                    first_frag=frag
                    if dict_frag:
                        dict_frag[first_frag][0]=S_node_id

        SYM=''
        dict_sym={}
        for chunk in self.tree.getChildren(self.pred.getName()):
            if chunk.isChild('rsym', self.pred.getName()):
                sym_term=''
                sym_id=self.check.order()[chunk.getName()]
                for node in chunk:
                    if not node.getLemma()=='((':
                        sym_term=sym_term+' '+node.getName()
                    else:
                        sym_linear_id=self.check.node_order()[node.getName()]
                SYM="SYM"+sym_term
                dict_sym[chunk.getName()]=[S_node_id, sym_id, SYM, [], 'SYMBOL', sym_linear_id]

        if self.pred.getPos()=='VGF' or self.pred.getPos()=='NULL__VGF':
            VP['VP-'+str(VP_node_id)]=[S_node_id, VP_node_id, 'VP', [], 'Verb-Head', V_linear_id]
            S['S-'+str(S_node_id)]=[S_parent_id, S_node_id, 'S', [], 'Top-Node', S_linear_id]
            dict_S=dict(dict_S.items()+Predicate.items()+dict_frag.items()+VP.items()+S.items())
            dict_S=dict(dict_S)
            dict_S.update(Predicate)
            dict_S.update(dict_frag)
            dict_S.update(VP)
            dict_S.update(S)
            if not SYM=='':
                dict_S=dict(dict_S.items()+dict_sym.items())
                dict_S=dict(dict_S)
                dict_S.update(dict_sym)
        elif self.pred.getPos()=='VGNN' or self.pred.getPos()=='VGNF':
            VP['VP-'+str(VP_node_id)]=[S_node_id, VP_node_id, 'VP', [], 'Verb-Head', V_linear_id]
            S['S-'+str(S_node_id)]=[S_parent_id, S_node_id, 'S-'+self.pred.getPos()[2]+self.pred.getPos()[3], [], 'Top-Node', S_linear_id]
            dict_S=dict(dict_S.items()+Predicate.items()+dict_frag.items()+VP.items()+S.items())
            dict_S=dict(dict_S)
            dict_S.update(Predicate)
            dict_S.update(dict_frag)
            dict_S.update(VP)
            dict_S.update(S)
            if not SYM=='':
                dict_S=dict(dict_S.items()+dict_sym.items())
                dict_S=dict(dict_S)
                dict_S.update(dict_sym)
        elif self.pred.getPos()=='NULL__VGNF' or self.pred.getPos()=='NULL__VGNN':
            VP['VP-'+str(VP_node_id)]=[S_node_id, VP_node_id, 'VP', [], 'Verb-Head', V_linear_id]
            S['S-'+str(S_node_id)]=[S_parent_id, S_node_id, 'S-'+self.pred.getPos()[8]+self.pred.getPos()[9], [], 'Top-Node', S_linear_id]
            dict_S=dict(dict_S.items()+Predicate.items()+dict_frag.items()+VP.items()+S.items())
            dict_S=dict(dict_S)
            dict_S.update(Predicate)
            dict_S.update(dict_frag)
            dict_S.update(VP)
            dict_S.update(S)
            if not SYM=='':
                dict_S=dict(dict_S.items()+dict_sym.items())
                dict_S=dict(dict_S)
                dict_S.update(dict_sym)
        else:
            parent_new_id=self.check.order()[self.pred.getName()]
            dict_frag=get.fragments()
            for frags in dict_frag:
                dict_frag[frags][0]=parent_new_id
            S_node_id=parent_new_id
            S_linear_id=parent_new_id
            S[self.pred.getName()]=[S_parent_id, S_node_id, self.pred.getPos(), [], 'Top-Node', S_linear_id]
            pred_terminal=create.terminal_nodes(self.pred, parent_new_id)
            
            SYM=''
            dict_sym={}
            for chunk in self.tree.getChildren(self.pred.getName()):
                if chunk.isChild('rsym', self.pred.getName()):
                    sym_term=''
                    sym_id=self.check.order()[chunk.getName()]
                    for node in chunk:
                        if not node.getLemma()=='((':
                            sym_term=sym_term+' '+node.getName()
                        else:
                            sym_linear_id=self.check.node_order()[node.getName()]
                    SYM="SYM"+sym_term
                    dict_sym[chunk.getName()]=[S_node_id, sym_id, SYM, [], 'SYMBOL', sym_linear_id]

            dict_S=dict(dict_S.items()+pred_terminal.items()+dict_frag.items()+S.items())
            dict_S=dict(dict_S)
            dict_S.update(pred_terminal)
            dict_S.update(dict_frag)
            dict_S.update(S)
            if not SYM=='':
                dict_S=dict(dict_S.items()+dict_sym.items())
                dict_S=dict(dict_S)
                dict_S.update(dict_sym)

        return dict_S


        
