import re
txt = '''
{number section}
num=1
{text section}
txt="2
MR=P,FR=N"
'''
# object = re.compile( ur"(?:(?P<name>[^MR=\n]+)=(?P<value>[^\n]+))+", re.S | re.U )
object = re.compile( ur"(?:(?P<name>[MR=\n]+)=(?P<value>[^\n]+))", re.S | re.U )
result = object.finditer( txt )
group_name_by_index = dict( [ (v, k) for k, v in object.groupindex.items() ] )
print group_name_by_index
for match in result :
  for group_index, group in enumerate( match.groups() ) :
    if group :
      print "text: %s" % group
      print "group: %s" % group_name_by_index[ group_index + 1 ]
      print "position: %d, %d" % match.span( group_index + 1 )
      
a = "TR000     MR=P, FR=N, MM=P, FM=P"     
regex = re.compile(r'''
    [\S]+=                # a key (any word followed by a colon)
    (?:
                       # then a space in between
        (?!\S+=)\S+       # then a value (any word not followed by a colon)
    )+                    # match multiple values if present
    ''', re.VERBOSE)

x = '''CS ID=123 HD=CT NE="HI THERE"'''
print re.findall("""\w+="[^"]*"|\w+='[^']*'|\w+=\w+|\w+""", x)