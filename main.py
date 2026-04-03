import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load Configuration
load_dotenv()

app = FastAPI(title="Architect Systems Engine")

# Centralized LLM Configuration (Groq Llama-3.3-70B)
ENGINE_LLM = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2 # Lower temperature for deterministic technical output
)

@app.get("/")
def health_check():
    return {"status": "active", "service": "Architect Backend", "version": "1.0.0"}

@app.get("/build")
async def build_architecture(project_idea: str):
    if not project_idea:
        raise HTTPException(status_code=400, detail="Missing required parameter: project_idea")

    try:
        # Agent 1: Principal Technology Consultant
        researcher = Agent(
            role="Principal Technology Consultant",
            goal=f"Determine the optimal technology stack for: {project_idea}",
            backstory="Experienced in enterprise-scale infrastructure. Specializes in selecting high-performance, cost-effective, and scalable cloud-native technologies.",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        # Agent 2: Lead Systems Architect
        architect = Agent(
            role="Lead Systems Architect",
            goal="Synthesize a formal Database Schema and RESTful API Specification.",
            backstory="Senior expert in relational and non-relational data modeling. Focuses on normalized structures, API consistency, and system interoperability.",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        # Agent 3: Senior Security Engineer
        auditor = Agent(
            role="Senior Security Engineer",
            goal="Perform a comprehensive security audit and vulnerability assessment of the proposed architecture.",
            backstory="Specializes in OWASP Top 10, NIST standards, and data privacy regulations. Identifies critical failure points in system design.",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        # Task Definitions with strict formatting constraints
        t1 = Task(
            description=f"Evaluate technical requirements for: {project_idea}. Select Language, Framework, and Database.",
            expected_output="A formal technical selection report. No emojis. Professional prose only.",
            agent=researcher
        )

        t2 = Task(
            description="Generate a comprehensive Database Schema and REST API Contract based on the tech stack.",
            expected_output="Detailed Technical Specification including Markdown tables for Schema and Endpoints. No emojis.",
            agent=architect
        )

        t3 = Task(
            description="Identify 3-5 security risks in the proposed design and provide technical mitigation strategies.",
            expected_output="A formal Security Audit Report. Focus on authentication, data integrity, and injection prevention. No emojis.",
            agent=auditor
        )

        # Orchestration Engine
        crew = Crew(
            agents=[researcher, architect, auditor],
            tasks=[t1, t2, t3],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        return {
            "status": "success",
            "project_context": project_idea,
            "blueprint": str(result)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")