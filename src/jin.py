from jinja2 import Template

name = "Sasha"
age = 28

tm = Template("I'm {{ n }} {{ a }}").render(n=name, a=age)

print(tm)
