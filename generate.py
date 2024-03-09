import yaml
import sys
import os
import os.path
from string import Template

file = sys.argv[1]
content = None
root_path = '../../'
ifContent = """<?php

namespace ${namespace}\Api\Data;

interface ${className}Interface
{
${fileContent}
"""
ifTemplate = Template(ifContent)
dataContent = """<?php

namespace ${namespace}\Service\Data;

use Magento\Framework\Model\AbstractModel;
use ${namespace}\Api\Data\${className}Interface;

class ${className} extends AbstractModel implements ${className}Interface 
{
"""

dataTemplate = Template(dataContent)

def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def lower_first_letter(s):
    return s[0].lower() + s[1:]

def getTypes(attribute, value, types):
    if isinstance(value, str):
       paramType = declaredType = 'string'
    elif isinstance(value, float):
       paramType = declaredType = 'float'
    elif isinstance(value, int):
       paramType = declaredType = 'int'
    elif isinstance(value, dict):
       paramType = declaredType = 'object'
    elif isinstance(value, list):
       paramType = declaredType = 'array'
    if types.get(attribute):
       Type = types.get(attribute)
       paramType = Type
       bracket = Type[-2:]
       if bracket == '[]':
          declaredType = 'array'
       else:
          declaredType = 'object'
    nullable = ''
    if attribute in classData['nullable']: nullable = '?'
    if not declaredType == 'mixed':
        declaredType = nullable + declaredType
    return paramType, declaredType, nullable

with open(file) as stream:
    try:
        content = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for namespace in content:
    path = content[namespace]['path']
    iface_path = content[namespace]['iface_path']
    impl_path = content[namespace]['impl_path']
    print('Check path')
    if os.path.isdir(root_path + path) == False:
        print(f'Directory {path} doesn\'t exist')
        quit()

    ifDir = root_path + path + '/' + iface_path
    implDir = root_path + path + '/' + impl_path
    if os.path.isdir(ifDir) == False:
        print(f'Directory {ifDir} doesn\'t exist')
        print('Creating directory')
        os.makedirs(ifDir)
    if os.path.isdir(implDir) == False:
        print(f'Directory {implDir} doesn\'t exist')
        print('Creating directory')
        os.makedirs(implDir)

    classes = content[namespace]['classes']
    for classData in classes:
        className = classData['name']
        nullableFields = classData['nullable']
        if not classData.get('type') is None:
            types = classData.get('type')
            print(types)

        fileContent = ''
        for attribute, value in classData['data'].items():
            constName = attribute.upper()
            constValue = attribute
            fileContent += '    const ' + constName + ' = \'' + constValue + '\';' + f"\n"
        
        # Interface Setters
        for attribute, value in classData['data'].items():
            nullable = ''
            if attribute in classData['nullable']: nullable = '?'
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)

            paramType, declaredType, nullable = getTypes(attribute, value, types)

            phpdoc = '''
    /**
     * @param ${nullable}${paramType} ${variableName}
     * @return $$this
     */
'''
            phpdoc= Template(phpdoc)
            phpdoc = phpdoc.substitute({'variableName': variableName, 'paramType':  paramType, 'nullable':nullable})

            fileContent += phpdoc
            fileContent += '    public function set' + MethodName + '('+declaredType+' ' + variableName + '): '+className+'Interface;' + f"\n"

        # Interface Getters
        for attribute, value in classData['data'].items():
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)

            paramType, declaredType, nullable = getTypes(attribute, value, types)

            phpdoc = '''
    /**
     * @return ${nullable}${paramType}
     */
'''
            phpdoc= Template(phpdoc)
            phpdoc = phpdoc.substitute({'variableName': variableName, 'paramType':  paramType, 'nullable': nullable})

            fileContent += phpdoc
            fileContent += '    public function get' + MethodName + '(): '+ declaredType + ';' + f"\n"

        fileContent += '}'

        # create interface file
        print('Create data interface')
        filePath = root_path + ifDir + className + 'Interface.php'
        print(filePath)
        f = open(filePath, "w")
        fileContent = ifTemplate.substitute({ 'className': className, 'fileContent': fileContent, 'namespace': namespace.strip('\\') })

        f.write(fileContent)
        f.close()


        # Implementation Classes

        # header
        fileContent = dataTemplate.substitute({ 'className': className, 'fileContent': fileContent, 'namespace': namespace.strip('\\') })

        # Implementation setters
        setterTemplate = '''
    /**
     * @inheritDoc
     */
    public function set${MethodName}(${declaredType} ${variableName}): ${returnType}
    {
        return $$this->setData(self::${constName}, ${variableName});
    }
'''
        setterTemplate = Template(setterTemplate)

        for attribute, value in classData['data'].items():
            constName = attribute.upper()
            constValue = attribute
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)

            paramType, declaredType, nullable = getTypes(attribute, value, types)

            fileContent += setterTemplate.substitute({'MethodName': MethodName, 'variableName': variableName, 'constName': constName, 'returnType': className + 'Interface', 'declaredType':declaredType})

        # Implementation getters
        getterTemplate = '''
    /**
     * @inheritDoc
     */
    public function get${MethodName}(): ${declaredType}
    {
        return $$this->getData(self::${constName});
    }
'''
        getterTemplate = Template(getterTemplate)
        for attribute, value in classData['data'].items():
            constName = attribute.upper()
            constValue = attribute
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)

            paramType, declaredType, nullable = getTypes(attribute, value, types)

            fileContent += getterTemplate.substitute({'MethodName': MethodName, 'variableName': variableName, 'constName': constName, 'declaredType': declaredType})


        fileContent += '}'


        # create implementation file
        print('Create implementation class')
        filePath = root_path + implDir + + className + '.php'
        print(filePath)
        f = open(filePath, "w")

        f.write(fileContent)
        f.close()