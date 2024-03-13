import requests
import time
import json
import random

base_url = "https://cs1.ucc.ie/yanlin/protein"

def test_param_search():
    total_time = 0
    num_requests = 100
    
    for _ in range(num_requests):
        params = {
            "rcScore": f"{random.randint(0, 50)},{random.randint(50, 100)}",
            "hydrophobicity": f"{random.uniform(-4.5, 0)},{random.uniform(0, 4.5)}",
            "instability": f"{random.randint(0, 50)},{random.randint(50, 100)}",
            "size": f"{random.randint(0, 1000)},",
            "isoelectricPoint": f"{random.randint(0, 7)},{random.randint(7, 15)}",
            "solventAccesibility": f"{random.randint(0, 50)},{random.randint(50, 100)}",
            "current": "1",
            "pageSize": "12"
        }
        
        start_time = time.time()
        response = requests.get(f"{base_url}/searchPdbByParam", params=params)
        end_time = time.time()
        
        if response.status_code == 200:
            total_time += end_time - start_time
        else:
            print(f"Parametric search failed with status code {response.status_code}")
    
    avg_time = total_time / num_requests
    print(f"Average parametric search time over {num_requests} requests: {avg_time:.2f} seconds")

def test_natural_language_search():
    queries = [
        "A protein that hydrophobicity is between 2 to 3",
        "Find proteins with high stability and low molecular weight",
        "Search for enzymes with catalytic activity in hydrolysis reactions"
    ]
    
    total_time = 0
    num_requests = 100
    
    for _ in range(num_requests):
        query = random.choice(queries)
        start_time = time.time()
        response = requests.get(f"{base_url}/searchPdbByNl", params={"text": query})
        end_time = time.time()
        
        if response.status_code == 200:
            total_time += end_time - start_time
        else:
            print(f"Natural language search for '{query}' failed with status code {response.status_code}")
    
    avg_time = total_time / num_requests
    print(f"Average natural language search time over {num_requests} requests: {avg_time:.2f} seconds")

def test_generate_new_sequence():
    data = {
        "seq": "GRRRRLVWTPSQSEALRACFERNPYPGIATRERLAQAIGIPEPRVQIWFQNERSRQLRQHRRESRPWPGRRGPPEGRRKRTAVTGSQTALLLRAFEKDRFPGIAAREELARETGLPESRIQIWFQNRRARHP",
        "freeze_mask": "000000000011111111110000000000000000000000000001111111111000000000000000000000000000111111111100000000000000000000000000000000000000",
        "targets": [
            {
                "name": "instability_index",
                "value": 6,
                "epsilon": 1000
            },
            {
                "name": "isoelectric_point",
                "value": 6,
                "epsilon": 1000
            },
            {
                "name": "gravy_score",
                "value": 6,
                "epsilon": 1000
            },
            {
                "name": "monoisotopic_mass",
                "value": 6,
                "epsilon": 1000
            }
        ],
        "dissimilarity": {
            "type": "point_to_point",
            "value": 2
        }
    }
    
    total_time = 0
    num_requests = 50
    
    for _ in range(num_requests):
        data["targets"][0]["value"] = random.randint(4, 8)
        data["targets"][1]["value"] = random.randint(4, 8)
        data["targets"][2]["value"] = random.randint(4, 8)
        data["targets"][3]["value"] = random.randint(4, 8)
        
        start_time = time.time()
        response = requests.post("https://cs1.ucc.ie/~sbm2/cgi-bin/Backend/v2/run.py/proteinsearch", json=data)
        
        if response.status_code == 200:
            result = response.json()
            uuid = result["request_id"]
            
            while True:
                response = requests.get(f"https://cs1.ucc.ie/~sbm2/cgi-bin/Backend/v2/run.py/proteinsearch?p={uuid}")
                result = response.json()
                if result["running"]:
                  time.sleep(1)
                  continue
                end_time = time.time()
                total_time += end_time - start_time
                break
        else:
            print(f"New sequence generation failed with status code {response.status_code}")
    
    avg_time = total_time / num_requests
    print(f"Average new sequence generation time over {num_requests} requests: {avg_time:.2f} seconds")

# Run the performance tests
test_param_search()
test_natural_language_search()
test_generate_new_sequence()
