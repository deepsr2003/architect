import os
os.environ["OTEL_SDK_DISABLED"] = "true"

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

app = FastAPI(title="Architect Systems Engine")

ENGINE_LLM = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

@app.get("/")
def health_check():
    return {"status": "active", "service": "Architect Backend", "version": "1.0.0"}

@app.get("/build")
async def build_architecture(project_idea: str):
    if not project_idea:
        raise HTTPException(status_code=400, detail="Missing required parameter: project_idea")

    try:
        researcher = Agent(
            role="Principal Technology Consultant",
            goal=f"Produce a rigorous, justifiable technology stack recommendation for: {project_idea}",
            backstory="""You are a principal-level infrastructure consultant with 15+ years of experience
architecting production systems at companies like Google, Stripe, and Netflix. You have deep expertise in:
- Trade-off analysis between monolith, microservices, and serverless architectures
- Database selection (relational, document, columnar, graph, time-series)
- Cloud provider optimization (AWS, GCP, Azure) including cost modeling
- Language and framework selection based on team productivity, ecosystem maturity, and performance requirements
- Integration patterns, message queues, and event-driven architectures

You never recommend a technology without justifying it with clear reasoning about scalability,
maintainability, cost, and operational complexity.""",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        architect = Agent(
            role="Lead Systems Architect",
            goal="Translate the approved technology stack into a detailed, implementation-ready system design",
            backstory="""You are a staff-level systems architect who has designed platforms handling
millions of requests per second at companies like Uber and MongoDB. Your expertise includes:
- Relational and NoSQL schema design with normalization, indexing strategies, and migration planning
- RESTful and GraphQL API design following RFC 7231 and best practices for versioning, pagination, HATEOAS
- Data flow modeling, CQRS, event sourcing, and eventual consistency patterns
- Horizontal scaling, caching layers (CDN, Redis, Memcached), and database read replicas
- Deployment architecture including containerization, orchestration, and CI/CD pipelines

You produce specifications precise enough for a team of engineers to implement directly.""",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        auditor = Agent(
            role="Senior Security Engineer",
            goal="Conduct a thorough threat model and security audit of the proposed architecture",
            backstory="""You are a seasoned security engineer with experience at CrowdStrike and as a
bounty program reviewer for OWASP. Your areas of depth include:
- Threat modeling using STRIDE and PASTA methodologies
- OWASP Top 10 (2021) vulnerability analysis and mitigation
- NIST SP 800-53 and SOC 2 compliance requirements
- Authentication/authorization patterns (OAuth 2.1, SAML, JWT best practices, RBAC/ABAC)
- Data privacy regulations (GDPR, CCPA, HIPAA) and encryption standards (AES-256, TLS 1.3)
- Supply chain security, dependency scanning, and secrets management

You are thorough to the point of paranoia — you never say "secure enough".""",
            llm=ENGINE_LLM,
            verbose=True,
            allow_delegation=False
        )

        t1 = Task(
            description=f"""Analyze the following project and produce a technology stack recommendation:

Project: {project_idea}

Your report must include these sections:

1. EXECUTIVE SUMMARY
   - 2-3 sentence overview of the recommended stack

2. ARCHITECTURE STYLE
   - Monolith vs microservices vs serverless — with rationale
   - System diagram: Use ONLY plain text with arrows (->) and indentation. NEVER use box-drawing characters (+, -, |, ┌, ┐, etc.). Example:

     Client -> CDN -> Load Balancer -> API Gateway
                                        -> Service A -> PostgreSQL
                                        -> Service B -> PostgreSQL
                                        -> Cache (Redis)

3. LANGUAGE & FRAMEWORK
   - Primary language with version
   - Framework(s) with specific version recommendations
   - Justification based on ecosystem maturity, performance, and team productivity

4. DATABASE
   - Primary database(s) with specific engine and version
   - Caching layer recommendation
   - Justification for relational vs NoSQL vs hybrid approach
   - Estimated data model complexity

5. INFRASTRUCTURE & DEPLOYMENT
   - Cloud provider and specific services
   - Containerization and orchestration approach
   - CI/CD pipeline recommendation

6. COST & SCALABILITY CONSIDERATIONS
   - Estimated operational complexity
   - Scaling strategy (horizontal vs vertical)
   - Cost optimization trade-offs""",
            expected_output="A structured technical selection report with exactly the sections listed above. Use markdown headings, tables for comparisons, and ASCII diagrams where helpful. Professional tone, no emojis.",
            agent=researcher
        )

        t2 = Task(
            description="""Based on the technology stack selected by the Principal Technology Consultant, produce a detailed system design specification.

Your report must include these sections:

1. DATABASE SCHEMA
   - Complete entity list with attributes, types, and constraints
   - Primary keys, foreign keys, indexes, and unique constraints
   - Migration strategy (schema evolution approach)
   - At least 5 core entities with full column definitions in markdown tables

2. REST API SPECIFICATION
   - All endpoints grouped by resource, with HTTP methods, paths, request/response shapes
   - Authentication and authorization model (which endpoints require which roles)
   - Pagination, filtering, sorting, and error response conventions
   - Rate limiting strategy
   - At least 8 endpoints covering CRUD + business logic operations

3. DATA FLOW
   - How data moves through the system for the 3 most critical user journeys
   - Async vs sync communication patterns
   - Event/message schema if using queues

4. DEPLOYMENT ARCHITECTURE
   - Simple service topology diagram using only plain text, arrows (->), and indentation. No box-drawing characters. Example:

     Client -> Load Balancer -> API Gateway -> Auth Service
                                                 -> Patient Service -> PostgreSQL
                                                 -> Doctor Service -> PostgreSQL
                                                  -> Cache (Redis)
   - Load balancing and auto-scaling configuration
   - Disaster recovery and backup strategy""",
            expected_output="A comprehensive technical specification with markdown tables, ASCII architecture diagrams, and precise endpoint definitions. Every section must be present. No emojis.",
            agent=architect
        )

        t3 = Task(
            description="""Review the full system design produced by the Lead Systems Architect and deliver a security audit.

Your report must include these sections:

1. THREAT MODEL
   - STRIDE analysis: at least one finding per category (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege)
   - Simple attack surface diagram using only plain text, arrows (->), and indentation. No box-drawing characters. Example:

     Attacker -> Public Endpoints -> API Gateway
                                      -> Auth (JWT validation)
                                      -> Rate Limiter
                                      -> Internal Services
     Attacker -> Client-side (XSS, CSRF)
     Insider -> Admin Panel -> Audit Logs

2. VULNERABILITY ASSESSMENT
   - OWASP Top 10 mapping: identify which of the top 10 risks apply and how
   - At least 5 specific vulnerabilities with:
     * Vulnerability name and CWE reference
     * Affected component
     * Likelihood (Low/Med/High) and Impact (Low/Med/High)
     * Detailed mitigation strategy with code/config examples

3. AUTHENTICATION & AUTHORIZATION
   - Review of the proposed auth model
   - JWT token handling best practices (expiry, rotation, storage)
   - Session management recommendations

4. DATA PROTECTION
   - Encryption in transit (TLS version, cipher suites)
   - Encryption at rest (algorithm, key management)
   - PII handling and compliance considerations

5. OPERATIONAL SECURITY
   - Secrets management recommendation
   - Logging and monitoring for security events
   - Incident response recommendations""",
            expected_output="A formal security audit report with all sections above, including a risk matrix table and actionable remediation steps. No emojis.",
            agent=auditor
        )

        crew = Crew(
            agents=[researcher, architect, auditor],
            tasks=[t1, t2, t3],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        agents_output = [
            {
                "role": task_out.agent,
                "output": task_out.raw
            }
            for task_out in result.tasks_output
        ]

        return {
            "status": "success",
            "project_context": project_idea,
            "agents_output": agents_output,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")
