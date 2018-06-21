#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from Rule_Selection import *
from Phrases import *
import string
from Non_Projective import *


class Join_clauses(object):
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)

    def join_clauses(self, i_ChunkName, i_clause):
        clause=i_clause
        for chunk in self.tree.getChildren(i_ChunkName):
            ChunkName=chunk.getName()
            if chunk.getPos()=='VGF' or chunk.getPos()=='NULL__VGF' or chunk.getPos()=='NULL__VGNN' or chunk.getPos()=='NULL__VGNF' or chunk.getPos()=='VGNF' or chunk.getPos()=='VGNN':
                draw_PS=Rule_selection(self.tree, chunk)
                parent_id=clause[' flag '+str(self.check.order()[ChunkName])][0]
                emb_clause=draw_PS.rule_selection(parent_id)
                n_flag=0
                for node in emb_clause:
                    if emb_clause[node][2]=='flag':
                        n_flag=n_flag+1
                    else:
                        n_flag=n_flag
                if not n_flag==0:
                    emb_clause=self.join_clauses(ChunkName, emb_clause)
                    del clause[' flag '+str(self.check.order()[ChunkName])]
                    clause=dict(clause.items()+emb_clause.items())
                    clause=dict(clause)
                    clause.update(emb_clause)
                else:
                    del clause[' flag '+str(self.check.order()[ChunkName])]
                    clause=dict(clause.items()+emb_clause.items())
                    clause=dict(clause)
                    clause.update(emb_clause)
            else:
                clause=self.join_clauses(ChunkName, clause)
                
        return clause
            


class PStrees(object):
    def __init__(self, tree):
        self.tree=tree
        self.handle=Non_projectivity(self.tree)
        self.check=Word_order(self.tree)
    def pstree(self):
        for chunk in self.tree:
            if not chunk.getDrel():
                if not chunk.getDMrel():
                    pred=chunk
                    ChunkName=pred.getName()
                    get=Join_clauses(self.tree)
                    draw_PS=Rule_selection(self.tree, pred)
                    clause=draw_PS.rule_selection(0)
                    #PS_tree=''
                    PS_tree=get.join_clauses(ChunkName, clause)


        if self.handle.nP_tree(pred):
            dict_nP=self.handle.nP_tree(pred)
            for arc in dict_nP:
                if dict_nP[arc][1]=='-' and dict_nP[arc][2]=='-':
                    if not self.tree.getChunk(arc).getPos()=='VGF' or self.tree.getChunk(arc).getPos()=='NULL__VGF' or self.tree.getChunk(arc).getPos()=='NULL__VGNN' or self.tree.getChunk(arc).getPos()=='NULL__VGNF' or self.tree.getChunk(arc).getPos()=='VGNN' or self.tree.getChunk(arc).getPos()=='VGNF':
                        attach_node=dict_nP[arc][5]
                        if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                            new_parent_id=PS_tree[attach_node][0]
                        else:
                            new_parent_id=PS_tree[attach_node][1]  
                            
                        old_parent_id=PS_tree[arc][0]
                        empty_name_POS=self.tree.getChunk(arc).getPos()+'**'
                        empty_name=self.tree.getChunk(arc).getName()+'**'
                        PS_tree[empty_name]=[old_parent_id, 1000+self.check.order()[arc], empty_name_POS, [], 'Empty_Node', PS_tree[arc][5]]
                        PS_tree[arc][0]=new_parent_id
                        PS_tree[arc][2]=empty_name_POS
                    else:
                        attach_node=dict_nP[arc][5]
                        if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                            new_parent_id=PS_tree[attach_node][0]
                        else:
                            new_parent_id=PS_tree[attach_node][1]   
                        old_node_id=PS_tree[arc][1]+300
                        old_parent_id=PS_tree['S-'+str(old_node_id)][0]
                        empty_name_POS=PS_tree['S-'+str(old_node_id)][2]+'**'
                        empty_name=PS_tree['S-'+str(old_node_id)][2]+'**'+str(old_node_id)
                        PS_tree[empty_name]=[old_parent_id, 1000+old_node_id, empty_name_POS, [], 'Empty_Node', PS_tree['S-'+str(old_node_id)][5]]
                        PS_tree['S-'+str(old_node_id)][0]=new_parent_id
                        PS_tree['S-'+str(old_node_id)][2]=empty_name_POS

                else:
                    if not self.handle.intervener(arc)[0]==1:
                        if not self.tree.getChunk(arc).getPos()=='VGF' or self.tree.getChunk(arc).getPos()=='NULL__VGF' or self.tree.getChunk(arc).getPos()=='NULL__VGNN' or self.tree.getChunk(arc).getPos()=='NULL__VGNF' or self.tree.getChunk(arc).getPos()=='VGNN' or self.tree.getChunk(arc).getPos()=='VGNF':
                            attach_node=dict_nP[arc][5]
                            if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                                new_parent_id=PS_tree[attach_node][0]
                            else:
                                new_parent_id=PS_tree[attach_node][1]
                            old_parent_id=PS_tree[arc][0]
                            empty_name_POS=self.tree.getChunk(arc).getPos()+'**'
                            empty_name=self.tree.getChunk(arc).getName()+'**'
                            PS_tree[empty_name]=[old_parent_id, 1000+self.check.order()[arc], empty_name_POS, [], 'Empty_Node', PS_tree[arc][5]]
                            PS_tree[arc][0]=new_parent_id
                            PS_tree[arc][2]=empty_name_POS
                        else:
                            attach_node=dict_nP[arc][5]
                            if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                                new_parent_id=PS_tree[attach_node][0]
                            else:
                                new_parent_id=PS_tree[attach_node][1]
                            old_node_id=PS_tree[arc][1]+300
                            old_parent_id=PS_tree['S-'+str(old_node_id)][0]
                            empty_name_POS=PS_tree['S-'+str(old_node_id)][2]+'**'
                            empty_name=PS_tree['S-'+str(old_node_id)][2]+'**'+str(old_node_id)
                            PS_tree[empty_name]=[old_parent_id, 1000+old_node_id, empty_name_POS, [], 'Empty_Node', PS_tree['S-'+str(old_node_id)][5]]
                            PS_tree['S-'+str(old_node_id)][0]=new_parent_id
                            PS_tree['S-'+str(old_node_id)][2]=empty_name_POS
                    else:
                        ic=self.handle.intervener(arc)[1]
                        for broker in ic:
                            attach_node=ic[broker][0]
                            move_C=broker
                        if not self.tree.getChunk(move_C).getPos()=='VGF' or self.tree.getChunk(move_C).getPos()=='NULL__VGF' or self.tree.getChunk(move_C).getPos()=='NULL__VGNN' or self.tree.getChunk(move_C).getPos()=='NULL__VGNF' or self.tree.getChunk(move_C).getPos()=='VGNN' or self.tree.getChunk(move_C).getPos()=='VGNF':
                            if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                                new_parent_id=PS_tree[attach_node][0]
                            else:
                                new_parent_id=PS_tree[attach_node][1] 
                            old_parent_id=PS_tree[move_C][0]
                            empty_name_POS=self.tree.getChunk(move_C).getPos()+'**'
                            empty_name=self.tree.getChunk(move_C).getName()+'**'
                            PS_tree[empty_name]=[old_parent_id, 1000+self.check.order()[move_C], empty_name_POS, [], 'Empty_Node', PS_tree[move_C][5]]
                            PS_tree[move_C][0]=new_parent_id
                            PS_tree[move_C][2]=empty_name_POS
                        else:
                            if self.tree.getChunk(attach_node).getPos()=='VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGF' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNN' or self.tree.getChunk(attach_node).getPos()=='NULL__VGNF' or self.tree.getChunk(attach_node).getPos()=='VGNN' or self.tree.getChunk(attach_node).getPos()=='VGNF':
                                new_parent_id=PS_tree[attach_node][0]
                            else:
                                new_parent_id=PS_tree[attach_node][1] 
                            old_node_id=PS_tree[move_C][1]+300
                            old_parent_id=PS_tree['S-'+str(old_node_id)][0]
                            empty_name_POS=PS_tree['S-'+str(old_node_id)][2]+'**'
                            empty_name=PS_tree['S-'+str(old_node_id)][2]+'**'+str(old_node_id)
                            PS_tree[empty_name]=[old_parent_id, 1000+old_node_id, empty_name_POS, [], 'Empty_Node', PS_tree['S-'+str(old_node_id)][5]]
                            PS_tree['S-'+str(old_node_id)][0]=new_parent_id
                            PS_tree['S-'+str(old_node_id)][2]=empty_name_POS
                            
        else:
            PS_tree=PS_tree

        return [PS_tree, clause]

            
        
