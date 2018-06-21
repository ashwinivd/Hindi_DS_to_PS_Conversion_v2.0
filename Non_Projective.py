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
from operator import itemgetter




class Non_projectivity(object):
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)
        
    def nP_detect(self, child_child):
        flag1='None'
        flag2='None'
        flag3='None'
        flag4='None'
        flag5='None'
        flag6='None'
        flag7='None'
        l_count=0

        value=False
        side=''
        
        
        ls_order=[]
        for node in child_child:
            ls_order.append(node[1])
            node_chunk=self.tree.getChunk(node[0])
        
        level=''
        grandparent=''
        ggparent=''
        gggparent=''
        ggggparent=''
        gggggparent=''
        ggggggparent=''
        gggggggparent=''

        for chunk in self.tree:
            if node_chunk.isChild(None, chunk.getName()):
                parent=chunk
                for chunkk in self.tree:
                    if parent.isChild(None, chunkk.getName()):
                        grandparent=chunkk
                        if parent.getPos()=='VGF' or parent.getPos()=='NULL__VGF': 
                            level1='Inter-clausal'
                        elif parent.getPos()=='VGNN' or parent.getPos()=='VGNF' or parent.getPos()=='NULL__VGNN' or parent.getPos()=='NULL__VGNF':
                            level1='Inter-clausal(NF)'
                        else:
                            level1='Intra-clausal'
                        for chunkkk in self.tree:
                            if grandparent.isChild(None, chunkkk.getName()):
                                ggparent=chunkkk
                                if grandparent.getPos()=='VGF' or grandparent.getPos()=='NULL__VGF': 
                                    level2=level1+' + Inter-clausal'
                                elif grandparent.getPos()=='VGNN' or grandparent.getPos()=='VGNF' or grandparent.getPos()=='NULL__VGNN' or grandparent.getPos()=='NULL__VGNF':
                                    level2=level1+' + Inter-clausal(NF)'
                                else:
                                    level2=level1+' + Intra-clausal'
                                for chunkkkk in self.tree:
                                    if ggparent.isChild(None, chunkkkk.getName()):
                                        gggparent=chunkkkk
                                        if ggparent.getPos()=='VGF' or ggparent.getPos()=='NULL__VGF': 
                                            level3=level2+' + Inter-clausal'
                                        elif ggparent.getPos()=='VGNN' or ggparent.getPos()=='VGNF' or ggparent.getPos()=='NULL__VGNN' or ggparent.getPos()=='NULL__VGNF':
                                            level3=level2+' + Inter-clausal(NF)'
                                        else:
                                            level3=level2+' + Intra-clausal'
                                        for chunkkkkk in self.tree:
                                            if gggparent.isChild(None, chunkkkkk.getName()):
                                                ggggparent=chunkkkkk
                                                if gggparent.getPos()=='VGF' or gggparent.getPos()=='NULL__VGF': 
                                                    level4=level3+' + Inter-clausal'
                                                elif gggparent.getPos()=='VGNN' or gggparent.getPos()=='VGNF' or gggparent.getPos()=='NULL__VGNN' or gggparent.getPos()=='NULL__VGNF':
                                                    level4=level3+' + Inter-clausal(NF)'
                                                else:
                                                    level4=level3+' + Intra-clausal'
                                                for chunkkkkkk in self.tree:
                                                    if ggggparent.isChild(None, chunkkkkkk.getName()):
                                                        gggggparent=chunkkkkkk
                                                        if ggggparent.getPos()=='VGF' or ggggparent.getPos()=='NULL__VGF': 
                                                            level5=level4+' + Inter-clausal'
                                                        elif ggggparent.getPos()=='VGNN' or ggggparent.getPos()=='VGNF' or ggggparent.getPos()=='NULL__VGNN' or ggggparent.getPos()=='NULL__VGNF':
                                                            level5=level4+' + Inter-clausal(NF)'
                                                        else:
                                                            level5=level4+' + Intra-clausal'
                                                        for chunkkkkkkk in self.tree:
                                                            if gggggparent.isChild(None, chunkkkkkkk.getName()):
                                                                ggggggparent=chunkkkkkkk
                                                                if gggggparent.getPos()=='VGF' or gggggparent.getPos()=='NULL__VGF':
                                                                    level6=level5+' + Inter-clausal'
                                                                elif gggggparent.getPos()=='VGNN' or gggggparent.getPos()=='VGNF' or gggggparent.getPos()=='NULL__VGNN' or gggggparent.getPos()=='NULL__VGNF':
                                                                    level6=level5+' + Inter-clausal(NF)'
                                                                else:
                                                                    level6=level5+' + Intra-clausal'
                                                                for chunkkkkkkkk in self.tree:
                                                                    if ggggggparent.isChild(None, chunkkkkkkkk.getName()):
                                                                        gggggggparent=chunkkkkkkkk
                                                                        if ggggggparent.getPos()=='VGF' or ggggggparent.getPos()=='NULL__VGF': 
                                                                            level7=level6+' + Inter-clausal'
                                                                        elif ggggggparent.getPos()=='VGNN' or ggggggparent.getPos()=='VGNF' or ggggggparent.getPos()=='NULL__VGNN' or ggggggparent.getPos()=='NULL__VGNF':
                                                                            level7=level6+' + Inter-clausal(NF)'
                                                                        else:
                                                                            level7=level6+' + Intra-clausal'

        if grandparent:
            parent_posn={}
            parent_posn[grandparent.getName()]=self.check.order()[grandparent.getName()]
            for chunk in self.tree.getChildren(grandparent.getName()):
                parent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_parent=sorted(parent_posn.items(), key=itemgetter(1))
            for child in ordered_parent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag1='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag1='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag1='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag1='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag1='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag1='max3'

        if ggparent:
            gparent_posn={}
            gparent_posn[ggparent.getName()]=self.check.order()[ggparent.getName()]
            for chunk in self.tree.getChildren(ggparent.getName()):
                gparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_gparent=sorted(gparent_posn.items(), key=itemgetter(1))
            for child in ordered_gparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag2='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag2='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag2='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag2='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag2='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag2='max3'

        if gggparent:
            ggparent_posn={}
            ggparent_posn[gggparent.getName()]=self.check.order()[gggparent.getName()]
            for chunk in self.tree.getChildren(gggparent.getName()):
                ggparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_ggparent=sorted(ggparent_posn.items(), key=itemgetter(1))
            for child in ordered_ggparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag3='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag3='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag3='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag3='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag3='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag3='max3'
        if ggggparent:
            gggparent_posn={}
            gggparent_posn[ggggparent.getName()]=self.check.order()[ggggparent.getName()]
            for chunk in self.tree.getChildren(ggggparent.getName()):
                gggparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_gggparent=sorted(gggparent_posn.items(), key=itemgetter(1))
            for child in ordered_gggparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag4='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag4='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag4='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag4='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag4='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag4='max3'

        if gggggparent:
            ggggparent_posn={}
            ggggparent_posn[gggggparent.getName()]=self.check.order()[gggggparent.getName()]
            for chunk in self.tree.getChildren(gggggparent.getName()):
                ggggparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_ggggparent=sorted(ggggparent_posn.items(), key=itemgetter(1))
            for child in ordered_ggggparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag5='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag5='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag5='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag5='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag5='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag5='max3'

        if ggggggparent:
            gggggparent_posn={}
            gggggparent_posn[ggggggparent.getName()]=self.check.order()[ggggggparent.getName()]
            for chunk in self.tree.getChildren(ggggggparent.getName()):
                gggggparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_gggggparent=sorted(gggggparent_posn.items(), key=itemgetter(1))
            for child in ordered_gggggparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag6='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag6='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag6='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag6='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag6='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag6='max3'

        if gggggggparent:
            ggggggparent_posn={}
            ggggggparent_posn[gggggggparent.getName()]=self.check.order()[gggggggparent.getName()]
            for chunk in self.tree.getChildren(gggggggparent.getName()):
                ggggggparent_posn[chunk.getName()]=self.check.order()[chunk.getName()]
            
            head_posn=self.check.order()[parent.getName()]
            ordered_ggggggparent=sorted(ggggggparent_posn.items(), key=itemgetter(1))
            for child in ordered_ggggggparent:
                if child[1]<head_posn:
                    if min(ls_order)<child[1]:
                        flag7='min1'                    
                        if len(child_child)>1:
                            if child_child[1][1]<child[1]:
                                flag7='min2'
                                if len(child_child)>2:
                                    if child_child[2][1]<child[1]:
                                        flag7='min3'

                elif child[1]>head_posn:
                    if max(ls_order)>child[1]:
                        flag7='max1'
                        if len(child_child)>=2:
                            if child_child[len(child_child)-2][1]>child[1]:
                                flag7='max2'
                                if len(child_child)>=3:
                                    if child_child[len(child_child)-3][1]>child[1]:
                                        flag7='max3'


        nP_child1='-'
        nP_child2='-'
        nP_child3='-'
        attach_node=''

        if flag1=='min1' and flag2=='None':
            value=True
            side='LEFT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag1=='min2' and flag2=='None':
            value=True
            side='LEFT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]

        if flag1=='min3' and flag2=='None':
            value=True
            side='LEFT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]

        if flag1=='max1' and flag2=='None':
            value=True
            side='RIGHT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag1=='max2' and flag2=='None':
            value=True
            side='LEFT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]

        if flag1=='max3' and flag2=='None':
            value=True
            side='LEFT'
            l_count=1
            level=level1
            attach_node=grandparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]




        if flag2=='min1' and flag3=='None':
            value=True
            side='LEFT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag2=='min2' and flag3=='None':
            value=True
            side='LEFT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    

        if flag2=='min3' and flag3=='None':
            value=True
            side='LEFT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]

        if flag2=='max1' and flag3=='None':
            value=True
            side='RIGHT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag2=='max2' and flag3=='None':
            value=True
            side='LEFT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    

        if flag2=='max3' and flag3=='None':
            value=True
            side='LEFT'
            l_count=2
            level=level2
            attach_node=ggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]

        if flag3=='min1' and flag4=='None':
            value=True
            side='LEFT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag3=='min2' and flag4=='None':
            value=True
            side='LEFT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]

        if flag3=='min3' and flag4=='None':
            value=True
            side='LEFT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]

        if flag3=='max1' and flag3=='None':
            value=True
            side='RIGHT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag3=='max2' and flag3=='None':
            value=True
            side='LEFT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    
        if flag3=='max3' and flag4=='None':
            value=True
            side='LEFT'
            l_count=3
            level=level3
            attach_node=gggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]

        if flag4=='min1' and flag5=='None':
            value=True
            side='LEFT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag4=='min2' and flag5=='None':
            value=True
            side='LEFT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    

        if flag4=='min3' and flag5=='None':
            value=True
            side='LEFT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]


        if flag4=='max1' and flag5=='None':
            value=True
            side='RIGHT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag4=='max2' and flag5=='None':
            value=True
            side='LEFT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                
        if flag4=='max3' and flag5=='None':
            value=True
            side='LEFT'
            l_count=4
            level=level4
            attach_node=ggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]

        if flag5=='min1' and flag6=='None':
            value=True
            side='LEFT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag5=='min2' and flag6=='None':
            value=True
            side='LEFT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    

        if flag5=='min3' and flag6=='None':
            value=True
            side='LEFT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]


        if flag5=='max1' and flag6=='None':
            value=True
            side='RIGHT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag5=='max2' and flag6=='None':
            value=True
            side='LEFT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                
        if flag5=='max3' and flag6=='None':
            value=True
            side='LEFT'
            l_count=5
            level=level5
            attach_node=gggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]


        if flag6=='min1' and flag7=='None':
            value=True
            side='LEFT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag6=='min2' and flag7=='None':
            value=True
            side='LEFT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    

        if flag6=='min3' and flag7=='None':
            value=True
            side='LEFT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]


        if flag6=='max1' and flag7=='None':
            value=True
            side='RIGHT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag6=='max2' and flag7=='None':
            value=True
            side='LEFT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                
        if flag6=='max3' and flag7=='None':
            value=True
            side='LEFT'
            l_count=6
            level=level6
            attach_node=ggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]


        if flag7=='min1':
            value=True
            side='LEFT'
            l_count=7
            level=level7
            attach_node=gggggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    nP_child1=nodename

        if flag7=='min2':
            value=True
            side='LEFT'
            l_count=7
            level=level7
            attach_node=gggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    

        if flag7=='min3':
            value=True
            side='LEFT'
            l_count=7
            level=level7
            attach_node=gggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==min(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i+1][0]
                    nP_child3=child_child[i+2][0]


        if flag7=='max1':
            value=True
            side='RIGHT'
            l_count=7
            level=level7
            attach_node=ggggggparent.getName()
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    nP_child1=nodename

        if flag7=='max2':
            value=True
            side='LEFT'
            l_count=7
            level=level7
            attach_node=gggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                
        if flag7=='max3':
            value=True
            side='LEFT'
            l_count=7
            level=level7
            attach_node=gggggggparent.getName()
            for i in range(0, len(child_child)):
                if child_child[i][1]==max(ls_order):
                    nP_child1=child_child[i][0]
                    nP_child2=child_child[i-1][0]
                    nP_child3=child_child[i-2][0]

        return [value, side, nP_child1, nP_child2, nP_child3, l_count, level, attach_node]

    

    def nP_subtrees(self, chunk, dict_nP):
        ChunkName=chunk.getName()
        dict_child={}
        nnp=0
        if not self.tree.getChildren(ChunkName):
            nnp=nnp+0
        else:
            for child in self.tree.getChildren(ChunkName):
                child_P=child.getName()
                if not self.tree.getChildren(child_P):
                    nnp=nnp+0
                else:
                    child_child=self.nP_subtrees(child, dict_nP)[0]
                    n_dict_nP=self.nP_subtrees(child, dict_nP)[1]
                    dict_nP=dict(dict_nP.items()+n_dict_nP.items())
                    dict_nP=dict(dict_nP)
                    dict_nP.update(n_dict_nP)
                    if self.nP_detect(child_child)[0]:
                        side=self.nP_detect(child_child)[1]
                        nP_child1=self.nP_detect(child_child)[2]
                        nP_child2=self.nP_detect(child_child)[3]
                        nP_child3=self.nP_detect(child_child)[4]
                        depth=self.nP_detect(child_child)[5]
                        levels=self.nP_detect(child_child)[6]
                        attach_node=self.nP_detect(child_child)[7]
                        dict_nP[nP_child1]=[side, nP_child2, nP_child3, depth, levels, attach_node]
                        
                child_Posn=self.check.order()[child_P]
                dict_child[child_P]=child_Posn
        ordered_child=sorted(dict_child.items(), key=itemgetter(1))
        return [ordered_child, dict_nP]

    def intervener(self, nP_child1):
        n=0
        dict_chunk={}
        for chunc in self.tree:
            n=n+1
            dict_chunk[chunc.getName()]=n
            if self.tree.getChunk(nP_child1).isChild(None, chunc.getName()):
                parent_ch1=chunc

        edgeD=0
        ej=dict_chunk[nP_child1]
        ei=dict_chunk[parent_ch1.getName()]
        dict_span=[]
        if ej>ei:
            for i in range(ei+1, ej+1):
                for nodu in dict_chunk.keys():
                    if dict_chunk[nodu]==i:
                        dict_span.append(nodu)

        else:
            for i in range(ej, ei):
                for nodu in dict_chunk.keys():
                    if dict_chunk[nodu]==i:
                        dict_span.append(nodu)
        
        nc=0
        ic={}
        parent_node1=''
        attach_posn=''
        for nod1 in dict_span:
            if not self.tree.getChunk(nod1).isChild(None, parent_ch1.getName()):
                comp_sign=0
                for nod2 in dict_span:
                    if self.tree.getChunk(nod1).isChild(None, nod2):
                        comp_sign=comp_sign+1
                    else:
                        comp_sign=comp_sign
                if comp_sign==0:
                    edgeD=edgeD+1
                    nc=nc+1
                    for parnt in self.tree:
                        if self.tree.getChunk(nod1).isChild(None, parnt.getName()):
                            parent_node1=parnt.getName()

                    attach_posn=parent_node1
                    ic[nod1]=[attach_posn]
                    
                else:
                    edgeD=edgeD
            else:
                edgeD=edgeD

        return [edgeD, ic]

    def nP_tree(self, pred):
        dict_nP=self.nP_subtrees(pred, {})[1]
        return dict_nP

    






                                    
