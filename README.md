# magento-data-api-generator
Generates Magento Data API Getters and Setters

## Usage
Clone or copy the project to [MAGENTO_ROO]/tools/magento-data-api-generator
```
$ cd ./tools/magento-data-api-generator
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

See order.yml to see the example
