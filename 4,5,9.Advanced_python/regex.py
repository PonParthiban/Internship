import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
print(is_valid_email("parthi2006@gmail.com"))
print(is_valid_email("parthiaa.gmail.com"))
 
#findall()
text = "The rain in Spain stays mainly in the plain."
pattern = '\d+'
matches = re.findall(pattern, text)
print(matches)

#compile()
pattern = re.compile('[a-e]')
match1 = (pattern.findall(text))
print(match1)

p = re.compile('\d')
print(p.findall("I went to him at 11 A.M. on 4th July 1886"))
p = re.compile('\d+')
print(p.findall("I went to him at 11 A.M. on 4th July 1886"))

p = re.compile('\w')
print(p.findall("He said * in some_lang."))
p = re.compile('\w+')
print(p.findall("I went to him at 11 A.M., he \
said *** in some_language."))
p = re.compile('\W')
print(p.findall("he said *** in some_language."))

p = re.compile('ab*')
print(p.findall("ababbaabbb"))

#split() - re.split(pattern, string, maxsplit=0, flags=0)
text = "The rain in Spain stays mainly in the plain."
pattern = r'\s+'
result = re.split(pattern, text)
print(result)
