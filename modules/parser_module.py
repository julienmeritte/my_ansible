import yaml
import io
import json

def readHosts(path):
    json_data = {}
    with io.open(path , 'r' , encoding='utf-8') as outfile:
        data = yaml.safe_load(outfile)
        json_data.update(data)
    json_detail = json.dumps(json_data["xhosts"])
    json_detail = json.loads(json_detail)
    return json_detail
    

            

            
        

