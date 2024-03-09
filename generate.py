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

with open(file) as stream:
    try:
        content = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for namespace in content:
    path = content[namespace]['path']
    print('Check path')
    if os.path.isdir(root_path + path) == False:
        print(f'Directory {path} doesn\'t exist')
        quit()

    ifDir = root_path + path + '/Api/Data'
    implDir = root_path + path + '/Service/Data'
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

        fileContent = ''
        for attribute, value in classData['data'].items():
            constName = attribute.upper();
            constValue = attribute;
            fileContent += '    const ' + constName + ' = \'' + constValue + '\';' + f"\n";
        
        # Interface Setters
        for attribute, value in classData['data'].items():
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)
            if isinstance(value, str):
               typ = 'string'
            elif isinstance(value, float):
               typ = 'float'
            elif isinstance(value, int):
               typ = 'int'

            phpdoc = '''
    /**
     * @param ${type} ${variableName}
     * @return $$this
     */
'''
            phpdoc= Template(phpdoc)
            phpdoc = phpdoc.substitute({'variableName': variableName, 'type':  typ})

            fileContent += phpdoc
            fileContent += '    public function set' + MethodName + '('+typ+' ' + variableName + '): '+className+'Interface;' + f"\n"

        # Interface Getters
        for attribute, value in classData['data'].items():
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)
            if isinstance(value, str):
               typ = 'string'
            elif isinstance(value, float):
               typ = 'float'
            elif isinstance(value, int):
               typ = 'int'

            phpdoc = '''
    /**
     * @return ${type}
     */
'''
            phpdoc= Template(phpdoc)
            phpdoc = phpdoc.substitute({'variableName': variableName, 'type':  typ})

            fileContent += phpdoc
            fileContent += '    public function get' + MethodName + '(): '+typ+';' + f"\n"

        fileContent += '}'

        # create interface file
        print('Create data interface')
        filePath = root_path + path  + '/Api/Data/' + className + 'Interface.php' 
        print(filePath)
        f = open(filePath, "w")
        fileContent = ifTemplate.substitute({ 'className': className, 'fileContent': fileContent, 'namespace': namespace.strip('\\') })

        f.write(fileContent)
        f.close()


        # Implementation Classes

        # header
        fileContent = dataTemplate.substitute({ 'className': className, 'fileContent': fileContent, 'namespace': namespace.strip('\\') })

        # setters
        setterTemplate = '''
    /**
     * @inheritDoc
     */
    public function set${MethodName}(${variableName}): ${type}
    {
        return $$this->setData(self::${constName}, ${variableName});
    }
'''
        setterTemplate = Template(setterTemplate)

        for attribute, value in classData['data'].items():
            constName = attribute.upper();
            constValue = attribute;
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)
            fileContent += setterTemplate.substitute({'MethodName': MethodName, 'variableName': variableName, 'constName': constName, 'type': className + 'Interface'})

        # getters
        getterTemplate = '''
    /**
     * @inheritDoc
     */
    public function get${MethodName}(): ${type}
    {
        return $$this->getData(self::${constName});
    }
'''
        getterTemplate = Template(getterTemplate)
        for attribute, value in classData['data'].items():
            constName = attribute.upper();
            constValue = attribute;
            MethodName = to_camel_case(attribute)
            variableName = '$'+lower_first_letter(MethodName)
            if isinstance(value, str):
               typ = 'string'
            elif isinstance(value, float):
               typ = 'float'
            elif isinstance(value, int):
               typ = 'int'
            fileContent += getterTemplate.substitute({'MethodName': MethodName, 'variableName': variableName, 'constName': constName, 'type': typ})


        fileContent += '}'


        # create implementation file
        print('Create implementation class')
        filePath = root_path + path  + '/Service/Data/' + className + '.php'
        print(filePath)
        f = open(filePath, "w")

        f.write(fileContent)
        f.close()