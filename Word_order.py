#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join


class Word_order(object):
        def __init__(self, tree):
                self.tree=tree

        def order(self):
                index=0
                address={}
                for chunk in self.tree:
                        index=index+1
                        ChunkName=chunk.getName()
                        address[ChunkName]=index
                return address

        def node_order(self):
                index=0
                address={}
                for chunk in self.tree:
                        for node in chunk:
                                index=index+1
                                NodeName=node.getName()
                                address[NodeName]=index

                return address
