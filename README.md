# 🚀 MULTI AI AGENT PLATFORM

A full-stack **Multi-AI Agent application** built with **LangChain, Groq, Tavily, FastAPI, Streamlit**, and deployed using a complete **CI/CD pipeline with Docker, Jenkins, SonarQube, and AWS (ECR + ECS Fargate)**.

---

## 📌 Project Overview

This project demonstrates how multiple AI agents can collaborate to solve user queries efficiently. Each agent has a clearly defined responsibility (research, analysis, and reasoning), and they communicate through an orchestrated workflow to produce high-quality, context-aware responses.

Beyond AI orchestration, the project also showcases real-world DevOps practices for deploying AI applications at scale. The system is containerized with Docker, continuously integrated and tested using Jenkins and SonarQube, and deployed to AWS using ECR and ECS Fargate. This ensures the application is scalable, modular, cloud-native, and production-ready, reflecting industry-standard MLOps and DevOps workflows for modern AI systems.

---

## 🧠 System Architecture

![System Architecture](images/architecture.png)


### Agent Responsibilities

| Agent | Description |
|-----|------------|
| Research Agent | Uses Tavily API to retrieve real-time information e.g Live info, trending topics |
| Reasoning Agent | Generates final responses using Groq LLM e.g Recommendations, final answer|

Agents are dynamically created and orchestrated using LangChain-based logic.


**LangChain** is a framework for building applications powered by LLMs. It provides tools to manage prompts, models, memory, agents, and external tools in a structured way.

In this project, LangChain is used to:

- Connect and manage different AI models (e.g. Groq-hosted LLMs)

- Build an AI agent that can reason, follow instructions, and optionally use tools like web search (Tavily)

- Orchestrate how user input, system prompts, and tool outputs are combined to generate intelligent responses

- It enables the multi-agent, tool-aware, and production-ready AI behavior demonstrated in this application

---

##  Tech Stack

### Backend
- **FastAPI** - Manages requests and agent orchestration
- **LangChain**
- **Groq API** - Fast and cost-efficient reasoning for agents
- **Tavily Search API** - Fast and cost-efficient reasoning for agents

### Frontend
- **Streamlit**

### DevOps & Cloud Infrastructure
- **Docker**
- **Jenkins**
- **SonarQube**
- **AWS ECR**
- **AWS ECS Fargate**

---


## Project Structure

- `app/frontend/ui.py` — Frontend application (Streamlit)
- `app/backend/api.py` — FastAPI to receive requests
- `app/core/ai_agent.py` — Reasearch and Reasoning agent code
- `app/main.py` — Main code which runs Frontend and Backend with the aid of threads
- `app/common/custom_exception.py` -  Returning detailed error
- `app/common/logger.py` - Logging actions
- `app/config/settings.py` - Loading our Groq and Tavily keys as well as our allowed models
- `custom_jenkins/Dockerfile` - Jenkins container Dockerfile

---

## Getting Started


 **Local Development:**
   - Clone this repository.
   - Make sure to the `requirements.txt` file and install necessary libraries in order to run the app locally.
   - Enter the command `python -m app.main` and wait for webpage to load

---

## 🔄 Application Flow

1. User submits query from Streamlit UI
2. FastAPI backend receives request
3. Multi-agent system processes request
4. Agents collaborate and generate response
5. Result returned to UI

![Flow](images/application.png)

![Flow](images/application1.png)

---

##  CI/CD Pipeline

The CI/CD pipeline is fully automated using Jenkins:

1. Code checkout from GitHub
2. Static code analysis with SonarQube

    ![Sonartest](images/sonar.png)

3. Docker image build
4. Image pushed to AWS Elastic Container Registry
5. Deployed to AWS ECS (Fargate)

Every push to main triggers a pipeline → builds → scans → deploys automatically.

     Stage             | Tool Used                               
     ----------------- | --------------------------------------- 
     Build, Test, Lint | Jenkins                                 
     Code Quality      | SonarQube                               
     Containerization  | Docker                                  
     Image Registry    | AWS ECR                                 
     Deployment        | AWS ECS Fargate (serverless containers) 


---

## 🚧 Challenges Faced & Solutions

### 1. LangChain Import & Version Conflicts
**Problem:** Multiple breaking changes (`langchain.schema`, `HumanMessage`, agent APIs). Most fuction calls were obsolute and had been migrated from LangGraph to LangChain 

**Solution:** Did a lot of documentation reading and research to find the right information. Migrated to `langchain-core`, updated imports, and refactored agent creation logic to match the latest LangChain API signature.

---

### 2. Jenkins & Sonarqube Server
**Problem:** Initial allocated EC2 instance to run Jenkins and Sonarqube server didn't have enough capacity to run efficiently

**Solution:** Ensured I upgraded the EC2 size on AWS to t3.large

---


### 3. AWS CLI Not Found in Jenkins
**Problem:** **AWS CLI unavailable during pipeline execution** 

My Jenkins server was ran from a docker image inside the EC2, because of this I had to install the AWS CLI inside the Jenkins docker container. 

However when running the CI/CD Pipeline, the pipeline couldn't find the AWS CLI. This was due to the fact that I restarted the container earlier. As a result of this, the installed AWS CLI wasn't presisted in the changes

**Solution:** Installed AWS CLI inside the Jenkins Docker image. From the custom_jenkins docker file, you can see that I added and extra line of code which installs the AWS CLI inside the Jenkins container whenever the image is built

---
---

## ☁️ Deployment

- Jenkins runs inside Docker on AWS EC2
- Sonarqube runs as well inside Docker on AWS EC2
- Docker images pushed to AWS ECR
- Application deployed using **AWS ECS Fargate**

---

## 🎯 Key Takeaways

- Real-world AI agent orchestration  
- Full CI/CD automation  
- Demonstrates LLM orchestration in a multi-agent ecosystem
- Combines DevOps + Cloud + AI engineering
- Real troubleshooting experience and Production-grade architecture  

---

## Future Improvements

- Add role-based agent selection
- Ecpanding logger file code to report logs to AWS cloud monitoring
- Implement Infrastructure as Code to fast track deployment
- Optimizing Application by implemeting Cloud Architecture best practices such as Disaster Recovery, Security architecture, load balancing.

---

##  Author

**Tobi Segun Oluwategbe**  
AI / MLOps / DevOps Engineer  
