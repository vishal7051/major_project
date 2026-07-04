# Goal
The goal is to build an "AI-Driven Personalized Career Path Graph" application. This system will ingest user resumes, extract skills, compare them with real-time job market data (via n8n scraping), and use LangChain/LLMs to generate a personalized six-month learning plan visualized as an interactive graph or timeline.

## Proposed Architecture
To achieve this, we can design a modern, scalable architecture consisting of three main components:

1. **Frontend (Web Application)**  
   - **Tech Stack**: React.js / Next.js, styled with Vanilla CSS or Tailwind CSS, and Recharts or Vis.js for graph/timeline visualization.  
   - **Features**: User authentication, file upload (for resumes), interactive 6-month roadmap timeline, and skill gap visualization.  
   - **Aesthetics**: Premium, modern UI with smooth transitions and a dynamic interface.

2. **Backend Engine (API & AI Layer)**  
   - **Tech Stack**: Python (FastAPI), LangChain, and OpenAI (or other LLMs).  
   - **Features**: REST APIs to communicate with the frontend, resume parsing logic, interaction with LangChain to run skill-extraction prompts, and roadmap generation logic.  
   
3. **Data Collection Services**  
   - **Tech Stack**: n8n workflows.  
   - **Features**: Automated cron-jobs to scrape popular job portals (LinkedIn, Naukri) and build a dataset of in-demand skills per role.

## Proposed Steps

### Phase 1: Foundational Setup
- Set up a Next.js / Vite web app skeleton.
- Set up a FastAPI backend environment.
- Determine the structure of the data schema (e.g., how we store user skills, job descriptions, and roadmaps).

### Phase 2: n8n Workflow Configuration
- Design and run an n8n pipeline for scraping Naukri/LinkedIn.
- Filter the collected data to extract the most frequent skills related to target job roles.
- Expose this aggregated job market data to the backend.

### Phase 3: AI Resume Processing & NLP Integration
- Implement endpoints in FastAPI to accept Resume PDFs.
- Use LangChain to parse the resume, extract technical/soft skills, and determine current proficiency.
- Compare user skills against real-time market needs and prompt the LLM to output a month-by-month, structured 6-month learning graph.

### Phase 4: Frontend Development & Visualization
- Build a stunning user interface.
- Integrate interactive visual elements (skill radar charts, roadmap timelines, network graphs).
- Connect frontend pages to the FastAPI backend.

## Open Questions

> [!IMPORTANT]
> To ensure I set up the project exactly how you envision it, please provide feedback on the following:
> 1. **Framework Preferences:** Would you like to use **Next.js** for the frontend and **FastAPI** (Python) for the backend? This is a great combo for AI apps.
> 2. **AI Provider:** Do you have an API key for OpenAI, Anthropic, or Gemini that we will be using with LangChain?
> 3. **Priorities:** Do you want me to start by scaffolding the frontend UI entirely, or should we begin with backend logic / LangChain first?

## Verification Plan

### Automated Tests
- Running test queries through the API to ensure the LangChain parser outputs JSON structures perfectly fitting our 6-month visual schema.
- Ensuring the Python server handles PDF extraction without errors.

### Manual Verification
- Testing the frontend by uploading sample resumes and visualizing the output graph to ensure it looks modern and premium.
- Validating the scraped data from n8n.
