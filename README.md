# Hindi_DS_to_PS_Conversion_v2.0
This version of conversion algorithm handles non-projective trees. In addition to generating phrase structure trees for projective dependencies, the current version also converts the non-projective dependencies. This version of the our algorithm successfully converts 98.2% of the dependency trees.

Also current version provides with two type of outputs - bracketted phrase structure tree and dictionary format tree (having an entry for each node).

Like previous version, the algorithm can be run with input SSF format of Hindi-urdu Dependency Treebank. It will generate Phrase structure trees for the corresponding dependency trees.  Please see <a href="http://ceur-ws.org/Vol-1779/10yadav.pdf">this paper</a> and <a href="https://osf.io/925x3/">this abstract</a> for more details.  

I have given a sample file of dependency trees that can be used as an input. conversion.py is the main module which takes dependency tree as input (in the format given in sample_input file) and prints output PS trees (in form of bracketted notation or dictionary format based on your choice).
