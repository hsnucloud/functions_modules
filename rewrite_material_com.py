"""
To rewrite the semiconductor material name with specific composition fraction
ex:
Al(x)Ga(y)In(1-x-y)As
x = 0.1
y = 0.3
rewrite as
Al(0.1)Ga(0.3)In(0.6)As

"""


def rewriteMaterial(material_name, x, y):
    input_name = material_name
    input_name = input_name.split(')')
    for index, string in enumerate(input_name):
        if not index == len(input_name) - 1:
            input_name[index] = input_name[index] + ')'
    found1 = []
    for string in input_name:
        a = re.findall('[(](.*?)[)]', string)
        if not a == []:
            found1.append(a[0])
        else:
            found1.append("")
    found_num1 = deepcopy(found1)
    for j in range(len(found_num1)):
        found_num1[j] = re.sub('x', '%f' % x, found_num1[j])
        found_num1[j] = re.sub('y', '%f' % y, found_num1[j])
        try:
            found_num1[j] = round(eval(found_num1[j]), 2)

        except:
            found_num1[j] = found_num1[j]
    for j in range(len(found_num1) - 1, -1, - 1):
        for index in range(len(input_name) - 1, -1, - 1):
            input_name[index] = re.sub(r'%s' % found1[j], '%s' % found_num1[j], input_name[index])
        if found_num1[j] == 0.0:
            input_name[j] = ''
        elif found_num1[j] == 1.0:
            input_name[j] = input_name[j].split('(')[0]
        material = ''
        for string in input_name:
            material += string
    return material