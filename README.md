# Architect: Autonomous Multi-Agent Engineering Engine

Architect is a high-performance system designed to automate the initial phase of the Software Development Life Cycle (SDLC). By leveraging a sequential multi-agent workflow and ultra-low-latency inference, it transforms high-level business objectives into formal technical specifications.

## System Architecture
The platform utilizes a three-tier agentic orchestration model:
1. **Principal Tech Consultant**: Performs heuristic technology stack selection based on scalability and performance requirements.
2. **Lead Systems Architect**: Synthesizes relational/non-relational database schemas and RESTful API specifications.
3. **Senior Security Engineer**: Conducts a formal risk assessment based on OWASP and NIST standards to identify vulnerabilities.

## Technical Stack
- **Orchestration**: CrewAI (Sequential Agentic Workflow)
- **Inference**: Llama-3.3-70B-Versatile via Groq Cloud (~250 tokens/sec)
- **Backend**: FastAPI (Asynchronous Microservice)
- **Frontend**: Streamlit (System Dashboard)
- **Data Validation**: Pydantic v2
  
<img width="1390" height="860" alt="Screenshot 2026-04-04 at 1 52 18 AM" src="https://github.com/user-attachments/assets/6975f34e-6121-4ba5-9ab0-e76e1d17653b" />

<img width="1394" height="860" alt="Screenshot 2026-04-04 at 1 51 36 AM" src="https://github.com/user-attachments/assets/1b31e55f-862b-4ca3-94bd-3b74bd777947" />

## Execution Process

### 1. Environment Setup
Clone the repository and initialize a virtual environment:
```bash
git clone https://github.com/dsarkar10/architect.git
cd architect
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### Execution Workflow
1.  **Stop all existing processes** in your terminals.
2.  **Paste the code** into the respective files.
3.  **Run Terminal 1:** `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
4.  **Run Terminal 2:** `streamlit run app.py --server.port 8501`
5.  **Test:** Enter a complex idea. You will now receive a dry, clinical, professional-grade technical document.




