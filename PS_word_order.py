#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
import string


class PS_word_order(object):
        def __init__(self, ps_tree):
                self.ps_tree=ps_tree

        def ps_word_order(self):
            index=0
            word_posn={}
            for word in self.ps_tree.split():
                    index=index+1
                    word_posn[word]=index
            return word_posn

        def ps_node_order(self):
            token=0
            node_address={}
            for word in self.ps_tree.split():
                if not word==']':
                        token=token+1
                        flag=0
                        for char in word:
                            if char=='[':
                                flag=flag+1
                            else:
                                flag=flag

                        if not flag==0:
                            node=string.replace(word, '[.', '')
                        else:
                            node=string.replace(word, '\\texthindi{', '')
                            node=string.replace(node, '}', '')

                        node_address[node]=token
            
            return node_address

        def ps_terminal(self):
            token=0
            node_address={}
            for word in self.ps_tree.split():
                    if not word==']':
                        flag=0
                        for char in word:
                            if char=='[':
                                flag=flag+1
                            else:
                                flag=flag

                        if flag==0:
                            token=token+1
                            node=string.replace(word, '\\texthindi{', '')
                            node=string.replace(node, '}', '')
                            node_address[token]=node
            
            return node_address
                        
                    
                        
                    
                    
