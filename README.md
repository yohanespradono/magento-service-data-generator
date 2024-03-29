# Magento Service Data Interface And Data Implementation Class Generator
Generates Magento service data interface files and the implementation data class files including the setters and getters.

## Description
Are you tired having to create Magento data interface files and the implementation files over and over again? I am too.
This script is for you. If you have the sample JSON code, you just need to create a YAML file (sample provided) and paste the JSON there.
Run the script and it will generate all the interface files and the implementations for you based on the JSON code you provide.
The interface files will be put into app/code/Vendor/MyModule/Api/Data/YourClassInterface.php and the implementation file will be put into app/code/Vendor/MyModule/Service/Data/YourClass.php

## Usage
Clone or copy the project to [MAGENTO_ROOT]/tools/magento-service-data-generator
```
$ cd /home/username/YourMagentoRoot/
$ mkdir tools && cd tools
$ git clone https://github.com/yohanespradono/magento-service-data-generator.git
$ cd magento-service-data-generator
$ pip3 install pyyaml
$ python generate.py [YOUR_YAML_FILE]
```

Example:

`python generate.py order.yml`


## YAML FILE
See [order.yml](order.yml) to see the example


## Warning
The sample above will override any files in
```
app/code/Vendor/MyModule/Api/Data/OrderRequestInterface.php
app/code/Vendor/MyModule/Api/Data/OrderItemInterface.php
app/code/Vendor/MyModule/Api/Data/CoordinateInterface.php
app/code/Vendor/MyModule/Service/Data/OrderRequest.php
app/code/Vendor/MyModule/Service/Data/OrderItem.php
app/code/Vendor/MyModule/Service/Data/Coordinate.php
```
Test it on your empty module first.

## Limitations
This script doesn't currently generate the \<preference\> in the di.xml. You still have to do it manually.

