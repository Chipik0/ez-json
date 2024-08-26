import json
from typing import Any, Iterator, Tuple

def loadJson(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    except FileNotFoundError:
        print(f'Warning: The file at "{path}" was not found. Created new empty dict.')
        return {}
    
    except json.JSONDecodeError:
        print(f'Error: The file at "{path}" could not be decoded as JSON. Created new empty dict.')
        return {}
    
    except Exception as e:
        print(f'An unexpected error occurred while loading JSON from "{path}": {e}. Created new empty dict.')
        return {}

def writeJson(data, path):
    try:
        with open(path, 'w+', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    except TypeError as e:
        print(f"Error: The provided data is not serializable to JSON. {e}")
    
    except IOError as e:
        print(f"Error: An I/O error occurred while writing JSON to {path}. {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred while writing JSON to {path}: {e}")

class JSON:
    """
    ## EZ - JSON
    EZ - JSON provides tools for managing JSON files, simplifying the process of reading, saving and manipulating data stored in JSON format.
    """
    
    def __init__(self, filepath: str, default_value: any = None):
        self.filepath = filepath
        self.default_value = default_value
        
        self.data = loadJson(filepath)

    def save(self, path: str = None) -> None:
        """
        Save the current JSON data to a file.
    
        ### Parameters:
        - path (str): The path to the file where the JSON data will be saved. If not provided, the data will be saved to the file path provided during initialization.
        """
        writeJson(self.data, path if path else self.filepath)
    
    def overwrite(self, data: dict) -> None:
        """
        Replace the current JSON data with the provided data.

        ### Parameters:
        - data (dict): The new data to replace the current JSON data with.
        """
        self.data = data

    def read(self) -> dict:
        """
        This function retrieves the current JSON data stored in the file specified during initialization.

        ### Returns:
        - The function returns the current JSON data as a dictionary.
        """
        return self.data

    def _traverse_keys(self, key: str, create_missing: bool = True) -> tuple:
        keys = key.split('.')
        last_key = keys[-1]
        current_dict = self.data

        for k in keys[:-1]:
            if isinstance(current_dict, list) and k.isdigit():
                k = int(k)
                
                if k < len(current_dict):
                    current_dict = current_dict[k]
                
                else:
                    raise IndexError(f"Index {k} is out of range for the list.")
            
            elif isinstance(current_dict, dict):
                if create_missing and k not in current_dict:
                    current_dict[k] = {}
                current_dict = current_dict.get(k, {})
            
            else:
                raise KeyError(f"Key '{k}' does not exist or is not a dictionary.")

        return current_dict, last_key

    def __getitem__(self, key: str) -> Any:
        default = self.default_value

        keys = key.split('.')
        current_dict = self.data

        for k in keys:
            if k in current_dict:
                current_dict = current_dict[k]

            else:
                return default

        return current_dict

    def __setitem__(self, key: str, value: Any) -> None:
        current_dict, last_key = self._traverse_keys(key)
        
        current_dict[last_key] = value

    def __delitem__(self, key: str) -> None:
        current_dict, last_key = self._traverse_keys(key)
        
        if last_key in current_dict:
            del current_dict[last_key]

    def __str__(self) -> str:
        return json.dumps(self.data, indent = 4, ensure_ascii = False)

    def __contains__(self, key: str) -> bool:
        keys = key.split('.')
        current_dict = self.data

        for k in keys:
            if isinstance(current_dict, dict) and k in current_dict:
                current_dict = current_dict[k]
            
            else:
                return False

        return True
    
    def items(self) -> Iterator[Tuple[str, Any]]:
        """
        This function retrieves the key-value pairs of the current JSON data stored in the file specified during initialization.

        ### Returns:
        - The function returns an iterator that yields each key-value pair in the JSON data as a tuple.
        """
        return self.data.items()

# Example usage
if __name__ == '__main__':
    json_obj = JSON('NewJson.json')
    json_obj.data
    
    del json_obj['Chips1.Chips2']
    json_obj.save()
    print(json_obj)