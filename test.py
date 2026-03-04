import requests

try:
    
    data = [{"name":"How to learn Python", "views": 1000, "likes": 100},
            {"name":"How to learn JavaScript", "views": 2000, "likes": 200},
            {"name":"How to learn Java", "views": 3000, "likes": 300}]
    
    base_url = "http://127.0.0.1:5000/"
    
    for i in range(len(data)):
        response = requests.put(base_url+"/video/"+str(i+1), json=data[i])
        print(response.json())
        print(response.status_code)
        print(response.text)
    
    input("Press Enter to continue...")
    
    response0 = requests.delete(base_url+"/video/0")
    print(response0.status_code)
    print(response0)   
    
    input("Press Enter to continue...")
    
    response1 = requests.get(base_url+"/video/2")
    print(response1.json())
    print(response1.status_code)
    
    
    
except Exception as e:
    print(f"An error occurred: {e}")

