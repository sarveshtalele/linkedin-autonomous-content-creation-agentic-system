# LinkedIn Autonomous Content Creation Agentic System
An autonomous multi-agent system that ingests information from multiple sources and generates high-quality LinkedIn posts using AI agents, retrieval augmented generation (RAG), and workflow orchestration.

## Demo

Watch the system generate LinkedIn posts autonomously using a multi-agent workflow.

<p align="center">
  <a href="https://youtu.be/cI2e5bfqMUA">
    <img src="https://img.youtube.com/vi/cI2e5bfqMUA/maxresdefault.jpg" width="900">
  </a>
</p>


This project demonstrates how to build a production-grade AI content generation pipeline using modular agents and stateful orchestration.

 ## System Architecture

![System Architecture](architecture_diagram.png)

## Overview

Maintaining a strong LinkedIn presence requires consistent, insightful content. This project automates the end-to-end process of content creation by combining multiple AI agents into a structured pipeline.

### LangGraph Execution Flow

![LangGraph Flow](https://github.com/sarveshtalele/linkedin-autonomous-content-creation-agentic-system/blob/main/langraph_flow.png)


The system:

• Ingests content from multiple sources  
• Extracts trends and insights  
• Retrieves relevant context using RAG  
• Generates LinkedIn posts  
• Reviews and improves content automatically  

Instead of a single prompt-based system, the architecture uses specialized agents coordinated through a workflow graph.

 

## Key Features

Multi-Agent Architecture  
Separate agents handle cleaning, keyword extraction, writing, and review.

Retrieval Augmented Generation (RAG)  
Relevant context is retrieved from indexed documents before generation.

Content Quality Review Loop  
Generated posts are scored and automatically improved.

Multi-Source Ingestion  
Supports PDFs, images, web pages, and plain text.

Modular Architecture  
Each component is independently extensible.

Local LLM Support  
Compatible with Ollama models.

 

## Architecture

The system follows a structured multi-agent pipeline:

```
Ingestion → Cleaning Agent → Keyword Agent → RAG Retrieval
→ Writer Agent → Reviewer Agent → Rewrite Agent → Output
```

Each agent operates on a shared state object managed by the workflow orchestrator.

# Pipeline Execution Flow

![Pipeline Flow](pipeline_flow.png)

---
 
# Repository Structure

```
src
│
├── agents
│   ├── cleaning_agent.py
│   ├── keyword_agent.py
│   ├── linkedin_writer_agent.py
│   ├── reviewer_agent.py
│   └── rewrite_agent.py
│
├── ingestion
│   ├── pdf_loader.py
│   ├── web_loader.py
│   ├── image_loader.py
│   ├── text_loader.py
│   └── pipeline.py
│
├── keywords
│   └── trend_extractor.py
│
├── rag
│   ├── chunker.py
│   ├── vector_store.py
│   └── hybrid_retriever.py
│
├── memory
│   └── graph_memory.py
│
├── pipeline
│   ├── workflow.py
│   ├── runner.py
│   └── state.py
│
├── storage
│   ├── json_store.py
│   └── yaml_store.py
│
└── ui
    └── app.py
```

 

#3 Setup Guide

### 1 Clone the Repository

```
git clone https://github.com/sarveshtalele/linkedIn-autonomous-content-agent.git
cd linkedIn-autonomous-content-agent
```

 

### 2 Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

 

### 3 Install Dependencies

```
pip install -r requirements.txt
```

 

### 4 Install and Run Ollama

Install Ollama

https://ollama.com

Pull a model

```
ollama pull phi3
```

or

```
ollama pull llama3
```

 

## 5 Run the Application

```
python src/ui/app.py
```

or run pipeline directly

```
python -m src.pipeline.runner
```

 

## Example Workflow

Input

```
Topic: AI Agents Transforming Product Engineering
Sources:
- Blog articles
- Research papers
- News content
```

Output

```
LinkedIn Post
Score: 92
Keywords: AI Agents, Autonomous Systems, Developer Productivity
```

 

## Technologies Used

- Python  
- LangChain  
- LangGraph  
- Ollama  
- Vector Databases  
- Hybrid Retrieval  
- Multi-Agent Architecture  
 

## Future Improvements

- Observability and tracing for agents  
- Automated evaluation benchmarks  
- Human-in-the-loop review  
- Content scheduling integration  
- Deployment as API service  

