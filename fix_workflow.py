import json

with open('n8n_market_insights_workflow.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if node.get('name') == 'Count Skill Frequency':
        old_str = "const role = $('Loop Through Roles').first().json.currentRole\n               || \"Software Engineer\";"
        new_str = 'const role = "Software Engineer";'
        node['parameters']['jsCode'] = node['parameters']['jsCode'].replace(old_str, new_str)
    
    if node.get('name') == 'Fetch Jobs from JSearch India':
        for param in node['parameters']['queryParameters']['parameters']:
            if param['name'] == 'query' and param['value'] == '={{ $json.currentRole }} jobs in India':
                param['value'] = 'software engineer jobs in India'

with open('n8n_market_insights_workflow.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
