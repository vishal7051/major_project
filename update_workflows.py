import json
import os

# Files
job_scraper_file = "n8n_job_scraper_workflow.json"
market_insights_file = "n8n_market_insights_workflow.json"
job_workflow_file = "n8n_job_workflow.json"

# CHANGE 1 & 2
with open(job_scraper_file, "r", encoding="utf-8") as f:
    data1 = json.load(f)

# Change 1: Replace Fetch node
new_node = {
  "name": "Fetch Jobs from JSearch India",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://jsearch.p.rapidapi.com/search",
    "options": {},
    "queryParameters": {
      "parameters": [
        {
          "name": "query",
          "value": "={{ $json.currentRole }} jobs in India"
        },
        {
          "name": "page",
          "value": "1"
        },
        {
          "name": "num_pages",
          "value": "1"
        },
        {
          "name": "country",
          "value": "in"
        }
      ]
    },
    "headerParameters": {
      "parameters": [
        {
          "name": "X-RapidAPI-Key",
          "value": "6512cf9e15msha96f8649afe2102p18b106jsn4f23113f4d0f"
        },
        {
          "name": "X-RapidAPI-Host",
          "value": "jsearch.p.rapidapi.com"
        }
      ]
    },
    "responseFormat": "json"
  }
}

old_fetch_name = "Fetch Jobs (Adzuna)"
old_fetch_name_fallback = "Fetch Job Descriptions from Adzuna"

new_nodes = []
for node in data1.get("nodes", []):
    if node.get("name") in [old_fetch_name, old_fetch_name_fallback]:
        # keep id and position
        n = new_node.copy()
        n["id"] = node.get("id")
        n["position"] = node.get("position")
        n["typeVersion"] = node.get("typeVersion", 1)
        new_nodes.append(n)
    else:
        new_nodes.append(node)
data1["nodes"] = new_nodes

# Update connections for Change 1
if "connections" in data1:
    conn = data1["connections"]
    new_conn = {}
    for k, v in conn.items():
        if k == old_fetch_name or k == old_fetch_name_fallback:
            new_conn["Fetch Jobs from JSearch India"] = v
        else:
            new_conn[k] = v
            # also update inside the targets
            for port_type, targets in v.items():
                for target_list in targets:
                    for target in target_list:
                        if target.get("node") in [old_fetch_name, old_fetch_name_fallback]:
                            target["node"] = "Fetch Jobs from JSearch India"
    data1["connections"] = new_conn

# Change 2: Update code in Extract Skills node
code_change_2 = """const items = $input.all();
const results = [];

const skillsList = {
  "Software Engineer":         ["React", "Python", "TypeScript", "Node.js", "AWS", "Docker", "System Design"],
  "Web Developer":             ["React", "Next.js", "TypeScript", "Tailwind CSS", "Node.js", "MongoDB"],
  "Data Scientist":            ["Python", "Machine Learning", "SQL", "Pandas", "TensorFlow", "Tableau"],
  "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "MLOps", "Deep Learning", "AWS"],
  "UI/UX Designer":            ["Figma", "User Research", "Wireframing", "Prototyping", "Adobe XD"],
  "Business Analyst":          ["SQL", "Tableau", "Agile", "Jira", "Requirements Gathering", "Excel"],
  "Civil Engineer":            ["AutoCAD", "Revit", "Structural Analysis", "Project Management", "STAAD Pro"],
  "Mechanical Engineer":       ["SolidWorks", "AutoCAD", "MATLAB", "FEA", "Thermodynamics"],
  "Financial Analyst":         ["Excel", "Financial Modeling", "SQL", "Power BI", "Corporate Finance"]
};

for (const item of items) {
  const jobResults = item.json.data || [];

  const role = $('Loop Through Roles').first().json.currentRole
               || "Software Engineer";

  const skills = skillsList[role] || skillsList["Software Engineer"];
  const skillCounts = {};

  for (const skill of skills) {
    skillCounts[skill] = 0;
  }

  const totalJobs = jobResults.length || 1;

  for (const job of jobResults) {
    const text = (
      (job.job_title || "") + " " +
      (job.job_description || "") + " " +
      (job.job_highlights?.Qualifications?.join(" ") || "") + " " +
      (job.job_highlights?.Responsibilities?.join(" ") || "")
    ).toLowerCase();

    for (const skill of skills) {
      if (text.includes(skill.toLowerCase())) {
        skillCounts[skill]++;
      }
    }
  }

  const insights = skills.map(skill => ({
    skill: skill,
    frequency: Math.round((skillCounts[skill] / totalJobs) * 100)
  }));

  insights.sort((a, b) => b.frequency - a.frequency);

  results.push({
    json: {
      role: role,
      skills: skills,
      insights: insights
    }
  });
}

return results;"""

old_code_name = "Extract Skills & Frequency"
old_code_name_fallback = "Count Skill Frequency"

for node in data1.get("nodes", []):
    if node.get("name") in [old_code_name, old_code_name_fallback]:
        node["parameters"]["jsCode"] = code_change_2
        # Now I will rename it exactly as the prompt requested so the output has the right name.
        # Wait, the prompt says "Find the node with name 'Count Skill Frequency'". 
        # If they meant they will look at the new file, they might want it to still be named what they expect, or maybe I should rename it to "Count Skill Frequency". Let's rename it to "Count Skill Frequency" to match their expectations exactly.
        
        # update name
        node["name"] = "Count Skill Frequency"

# Wait, if we renamed it, we must update the connections too!
if "connections" in data1:
    conn = data1["connections"]
    new_conn = {}
    for k, v in conn.items():
        if k in [old_code_name, old_code_name_fallback]:
            new_conn["Count Skill Frequency"] = v
        else:
            new_conn[k] = v
            # also update inside the targets
            for port_type, targets in v.items():
                for target_list in targets:
                    for target in target_list:
                        if target.get("node") in [old_code_name, old_code_name_fallback]:
                            target["node"] = "Count Skill Frequency"
    data1["connections"] = new_conn

with open(market_insights_file, "w", encoding="utf-8") as f:
    json.dump(data1, f, indent=2)


# CHANGE 3
with open(job_workflow_file, "r", encoding="utf-8") as f:
    data2 = json.load(f)

code_change_3 = """const items = $input.all();
const results = [];

for (const item of items) {
  const role = item.json.search_parameters?.q || "Unknown Role";
  const jobResults = item.json.jobs_results || [];

  let count = 0;
  for (const job of jobResults) {
    if (count >= 2) break;

    let applyLink = "";
    const allOptions = job.apply_options || [];

    const naukri = allOptions.find(o =>
      o.link && o.link.includes("naukri.com")
    );
    if (naukri) applyLink = naukri.link;

    if (!applyLink) {
      const linkedin = allOptions.find(o =>
        o.link && o.link.includes("linkedin.com")
      );
      if (linkedin) applyLink = linkedin.link;
    }

    if (!applyLink) {
      const indeed = allOptions.find(o =>
        o.link && o.link.includes("indeed.com")
      );
      if (indeed) applyLink = indeed.link;
    }

    if (!applyLink && allOptions.length > 0) {
      applyLink = allOptions[0].link || "";
    }

    if (!applyLink && job.related_links?.length > 0) {
      applyLink = job.related_links[0].link || "";
    }

    if (!applyLink) {
      const q = encodeURIComponent(role);
      applyLink = "https://www.naukri.com/jobs-in-india?q=" + q;
    }

    const skills = [];
    const skillKeywords = [
      "Python", "React", "JavaScript", "TypeScript", "Node.js",
      "SQL", "AWS", "Docker", "Java", "Machine Learning",
      "Figma", "AutoCAD", "Excel", "Power BI", "Tableau",
      "Next.js", "MongoDB", "TensorFlow", "PyTorch", "Agile"
    ];

    if (job.description) {
      for (const skill of skillKeywords) {
        if (job.description.toLowerCase().includes(skill.toLowerCase())) {
          skills.push(skill);
        }
      }
    }

    results.push({
      role: role,
      job_title: job.title || "Job Opening",
      company: job.company_name || "Company",
      location: job.location || "India",
      skills: skills.slice(0, 5),
      apply_link: applyLink
    });

    count++;
  }
}

return [{ json: { jobs: results } }];"""

old_job_format_name = "Transform & Balance"
old_job_format_name_fallback = "Parse and Format Jobs"

for node in data2.get("nodes", []):
    if node.get("name") in [old_job_format_name, old_job_format_name_fallback]:
        node["parameters"]["jsCode"] = code_change_3
        # Rename to "Parse and Format Jobs"
        node["name"] = "Parse and Format Jobs"

if "connections" in data2:
    conn = data2["connections"]
    new_conn = {}
    for k, v in conn.items():
        if k in [old_job_format_name, old_job_format_name_fallback]:
            new_conn["Parse and Format Jobs"] = v
        else:
            new_conn[k] = v
            # also update inside the targets
            for port_type, targets in v.items():
                for target_list in targets:
                    for target in target_list:
                        if target.get("node") in [old_job_format_name, old_job_format_name_fallback]:
                            target["node"] = "Parse and Format Jobs"
    data2["connections"] = new_conn

with open(job_workflow_file, "w", encoding="utf-8") as f:
    json.dump(data2, f, indent=2)

print("Done")
