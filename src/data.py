import json

def read_data(file):
    f = open(file)
    data = json.load(f)
    return data

def write_cars(cars, file):
    data = read_data(file)
    dict = {
    "cars": cars,
    "avg": data['avg'],
    }
 
    # Serializing json
    json_object = json.dumps(dict, indent=2)
    
    # Writing to json
    with open(file, "w") as outfile:
        outfile.write(json_object)

def write_data(cars, avg):
    dict = {
    "cars": cars,
    "avg": avg,
    }
 
    # Serializing json
    json_object = json.dumps(dict, indent=2)
    
    # Writing to sample.json
    with open("data.json", "w") as outfile:
        outfile.write(json_object)
