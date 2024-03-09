# magento-data-api-generator
Generates Magento Data API Getters and Setters. 

## Description
Are you tired having to create Magento data interface files and the implementation files over and over again? I am too.
This script is for you. If you have the sample JSON code, you just need to create a YAML file (sample provided) and paste the JSON there.
Run the script and it will generate all the interface files and the implementations for you based on the JSON code you provide.
The interface files will be put into app/code/Vendor/MyModule/Api/Data/YourClassInterface.php and the implementation file will be put into app/code/Vendor/MyModule/Service/Data/YourClass.php

## Usage
Clone or copy the project to [MAGENTO_ROOT]/tools/magento-data-api-generator
```
$ cd /home/username/YourMagentoRoot/
$ mkdir tools && cd tools
$ git clone https://github.com/yohanespradono/magento-data-api-generator.git
$ cd magento-data-api-generator
$ pip3 install pyyaml
$ python generate.py [YOUR_YAML_FILE]
```

Example:

`python generate.py order.yml`


## YAML FILE

```yaml
\Vendor\MyModule:
  path: app/code/Vendor/MyModule
  classes:
    - name: OrderRequest
      data: {JSON}
    - name: OrderItem
      data: {JSON}
    - name: Coordinate
      data: {JSON}
```

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

## Limitations
This script doesn't currently generate the \<preference\> in the di.xml. You still have to do it manually.

