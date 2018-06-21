import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from ssf_api import *
from Clause_joining import *
from Word_order import *
from AllwellFormed import *
from Non_Projective import *


def getAllChildren(tree, node_id):
    for node in tree:
        child={}
        if node[1][0]==node_id:
            child[node[1][1]]=node[0]
    return child

def construct_bracket(ps_tree, parent_id):
    dict_S={}
    for node in ps_tree:
        if ps_tree[node][0]==parent_id:
            node_id=ps_tree[node][1]
            store_S=' [.'+ps_tree[node][2]
            child_S=construct_bracket(ps_tree, node_id)
            child_S_f=''
            for nodez in child_S:
                child_S_f=child_S_f+nodez[0]
            store_S=store_S+child_S_f+' ]'
            linear_index=ps_tree[node][5]
            dict_S[store_S]=linear_index

    ordered_S=sorted(dict_S.items(), key=itemgetter(1))
    
    return ordered_S 

SSF_DIR ="../HDTB_pre_release_version_0.05/InterChunk/SSF/utf/Training/"

print 'Please type 0 for bracketted tree output and 1 for dictionary tree output'
flag = input()
for filename in listdir(SSF_DIR):
    ssf = SSF(SSF_DIR+filename)
    for tree in ssf.getTrees():
        for chunk in tree:
            if not chunk.getDrel():
                if not chunk.getDMrel():
                    pred=chunk
        
        get=PStrees(tree)
        ps_tree=get.pstree()[1]
        PS_tree=get.pstree()[0]

        S=''
        node_S=construct_bracket(PS_tree, 0)
        node_S_f=''
        for nodename in node_S:
            node_S_f=node_S_f+nodename[0]
        S=S+node_S_f
        
        if flag==0:
            print '\n\n'+S+'\n\n'
        elif flag==1:
            print '\n\n'+str(PS_tree)
        else:
            print 'Invalid input! Please give 0 for bracketted tree output or 1 for dictionary tree output'
            flag = input()
            if flag==0:
                print '\n\n'+S+'\n\n'
            elif flag==1:
                print '\n\n'+str(PS_tree)
