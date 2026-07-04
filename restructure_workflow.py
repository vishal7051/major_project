import json
import re

with open("n8n_market_insights_workflow.json", "r", encoding="utf-8") as f:
    old_data = json.load(f)

old_nodes = {n["name"]: n for n in old_data.get("nodes", [])}

nodes = []

# Node 1
n1 = old_nodes.get("Schedule Trigger (Daily)")
if n1:
    n1["position"] = [0, 200]
    nodes.append(n1)

# Node 2
n2 = {
  "parameters": {
    "values": {
      "string": [
        {
          "name": "roles",
          "value": "={{ [\"Software Engineer\", \"Web Developer\", \"UI/UX Designer\", \"Data Scientist\", \"Machine Learning Engineer\", \"Civil Engineer\", \"Mechanical Engineer\", \"Electrical Engineer\", \"Business Analyst\", \"Marketing Manager\", \"HR Manager\", \"Banking\", \"Financial Analyst\", \"Accountant\"] }}"
        }
      ]
    },
    "options": {}
  },
  "id": "set-all-roles-id",
  "name": "Set All Roles",
  "type": "n8n-nodes-base.set",
  "typeVersion": 1,
  "position": [200, 200]
}
nodes.append(n2)

# Node 3
n3 = {
  "parameters": {
    "batchSize": 1,
    "options": {}
  },
  "id": "loop-through-roles-id",
  "name": "Loop Through Roles",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 2,
  "position": [400, 200]
}
nodes.append(n3)

# Node 4
n4 = {
  "parameters": {
    "values": {
      "string": [
        {
          "name": "currentRole",
          "value": "={{ $json.roles }}"
        }
      ]
    },
    "options": {}
  },
  "id": "set-current-role-id",
  "name": "Set Current Role",
  "type": "n8n-nodes-base.set",
  "typeVersion": 1,
  "position": [600, 200]
}
nodes.append(n4)

# Node 5
n5 = old_nodes.get("Fetch Jobs from JSearch India")
if n5:
    for param in n5["parameters"]["queryParameters"]["parameters"]:
        if param["name"] == "query":
            param["value"] = "={{ $json.currentRole }} jobs in India"
    n5["position"] = [800, 200]
    nodes.append(n5)

# Node 6 (if exists)
has_node_6 = False
n6 = old_nodes.get("Split Out")
if n6:
    has_node_6 = True
    n6["position"] = [1000, 200]
    nodes.append(n6)

# Node 7
n7 = old_nodes.get("Count Skill Frequency")
if n7:
    n7["position"] = [1200 if has_node_6 else 1000, 200]
    code = n7["parameters"]["jsCode"]
    code = code.replace(
        "const role = \"Software Engineer\";",
        "const role = $('Set Current Role').first().json.currentRole\n               || \"Software Engineer\";"
    )
    insert_str = """  "Financial Analyst":         ["Excel", "Financial Modeling", "SQL", "Power BI", "Corporate Finance"],
  "Electrical Engineer": ["Circuit Design", "PLC", "MATLAB", "Power Systems", "AutoCAD Electrical"],
  "Marketing Manager":   ["SEO", "Google Analytics", "Content Strategy", "CRM", "Social Media"],
  "HR Manager":          ["Talent Acquisition", "Employee Relations", "HRIS", "Labor Laws", "Performance Management"],
  "Banking":             ["Risk Management", "Financial Modeling", "Excel", "Regulatory Compliance", "Credit Analysis"],
  "Accountant":          ["QuickBooks", "Excel", "GAAP", "Tax Preparation", "Financial Reporting"]"""
    
    code = re.sub(
        r'  "Financial Analyst":.*Corporate Finance"\]',
        insert_str,
        code
    )
    n7["parameters"]["jsCode"] = code
    nodes.append(n7)

# Node 8
n8 = old_nodes.get("Push to FastAPI Backend")
if n8:
    n8["position"] = [1400 if has_node_6 else 1200, 200]
    n8["parameters"]["url"] = "http://localhost:8000/api/webhooks/market-trends"
    nodes.append(n8)


connections = {
    "Schedule Trigger (Daily)": {
        "main": [ [ {"node": "Set All Roles", "type": "main", "index": 0} ] ]
    },
    "Set All Roles": {
        "main": [ [ {"node": "Loop Through Roles", "type": "main", "index": 0} ] ]
    },
    "Loop Through Roles": {
        "main": [ [ {"node": "Set Current Role", "type": "main", "index": 0} ] ]
    },
    "Set Current Role": {
        "main": [ [ {"node": "Fetch Jobs from JSearch India", "type": "main", "index": 0} ] ]
    },
    "Fetch Jobs from JSearch India": {
        "main": [ [ {"node": "Split Out" if has_node_6 else "Count Skill Frequency", "type": "main", "index": 0} ] ]
    }
}

if has_node_6:
    connections["Split Out"] = {
        "main": [ [ {"node": "Count Skill Frequency", "type": "main", "index": 0} ] ]
    }

connections["Count Skill Frequency"] = {
    "main": [ [ {"node": "Push to FastAPI Backend", "type": "main", "index": 0} ] ]
}

connections["Push to FastAPI Backend"] = {
    "main": [ [ {"node": "Loop Through Roles", "type": "main", "index": 0} ] ]
}

old_data["nodes"] = nodes
old_data["connections"] = connections

with open("n8n_market_insights_workflow.json", "w", encoding="utf-8") as f:
    json.dump(old_data, f, indent=2)

print("Workflow restructured successfully.")
