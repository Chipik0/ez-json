# EZ - JSON
#### EZ - JSON provides tools for managing JSON files, simplifying the process of reading, saving and manipulating data stored in JSON format. This is the simplest module that will simplify working with dictionaries and JSON.

## Example usage
You can set the default value that will be returned if there is an error finding the keys.
##
```
if __name__ == '__main__':
    json_obj = JSON('NewJson.json', None)
    
    json_obj['Chips1.Chips2'] = 'Chips3'
    json_obj.save()
    print(json_obj)
```

- This code example will return a JSON file looking like this:

```
{
    "Chips1": {
        "Chips2": "Chips3"
    }
}
```
##
- Also, you can delete keys like this:
```
del json_obj['Chips1.Chips2']
```
->
```
{
    "Chips1": {}
}
```
##
- Also you can use "in" operator.
```
if 'Chips3' in json_obj['Chips1.Chips2']
    ...
```
##
