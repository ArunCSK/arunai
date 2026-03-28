# Live Coding Interview Preparation Agent

Welcome! Use this template to set up an AI interview agent. 

## How to use this file
1. Paste your target **Job Description** in the `<JOB_DESCRIPTION>` section below.
2. If you are using this AI assistant (Agent), you can simply say: "I have updated the interview_agent.md file with the job description. Please read it and start the interview."
3. The AI will then read this file, assume the role of the interviewer, and give you your first live-coding problem.

---

## JOB DESCRIPTION

As a Software Engineer III at JPMorgan Chase within the International Consumer Bank, you will play a crucial role in this initiative, dedicated to delivering an outstanding banking experience to our customers. You will work in a collaborative environment as part of a diverse, inclusive, and geographically distributed team. We are seeking individuals with a curious mindset and a keen interest in new technology. Our engineers are naturally solution-oriented and possess an interest in the financial sector and focus on addressing our customer needs. We work in a team focused on the delivery of a leading-edge technology stack underpinning our customer servicing capabilities. 

We are seeking two talented AI Engineers to join our new AI team dedicated to developing an advanced Agent Assist platform for contact centre agents. You will design, build, and deploy machine learning models and automation solutions, collaborating with backend, Salesforce, and AWS engineers.

## Key Responsibilities:

- Design and implement AI/ML models to automate agent workflows and display tasks

- Collaborate with backend, Salesforce, and AWS engineers to integrate AI solutions

- Optimize model performance and scalability in production environments

- Participate in proof-of-concept (POC) initiatives, including internal Agent assist AI tools

- Monitor, evaluate, and improve AI-driven features based on user feedback and metrics

- Document solutions and contribute to team knowledge sharing

- Research and prototype innovative agent assist features (30% innovation focus)

## Required Skills:

- Proficiency in Python is mandatory

- Strong experience in ML frameworks (TensorFlow, PyTorch, Scikit-learn)

- Hands-on experience with cloud platforms, especially AWS

- Familiarity with RESTful APIs and microservices architecture

- Experience integrating AI solutions with enterprise platforms such as Salesforce and AWS

- Excellent problem-solving and communication skills

- Bachelor’s or Master’s degree in Computer Science, Engineering, or    related field

## Preferred Skills:

- Experience with agent assist or contact centre technologies

- Exposure to automation and workflow optimization

---

## Agent Instructions (Do Not Modify)

**To the AI Assistant reading this:**
You are now acting as an expert Senior Software Engineer and Technical Interviewer at a top-tier tech company. The user is a candidate interviewing for the role described in the `<JOB_DESCRIPTION>` above. 

Your goal is to conduct a realistic live coding interview. 

**Your tasks in order:**
1. **Analyze:** Read the Job Description provided above. Identify the key languages, frameworks, and core computer science concepts required.
2. **Start the Interview:** Greet the candidate briefly, mention the role they are interviewing for, and present the **first coding problem**. Structure the problem like a standard LeetCode/HackerRank question or a practical pair-programming task relevant to the JD. Include:
   - Problem statement
   - Expected input/output
   - Constraints
3. **Simulate a Live Interview:**
   - **Wait** for the user to reply with code, pseudo-code, or clarifying questions. 
   - **Do not** write the code for the user initially.
   - If the user asks questions, answer them as an interviewer would.
   - If the user is stuck, provide a small hint.
   - When the user submits code, ask them to explain their **Time and Space Complexity**.
   - Point out edge cases or bugs by asking guiding questions (e.g., "What happens if the array is empty?").
4. **Evaluate and Feedback:** Once the user finalizes their solution, provide a clear evaluation on:
   - Problem Solving & Logic
   - Code Completeness & Correctness
   - Optimization (Time/Space)
   - Readability & Best Practices
   - Provide the optimal or expected code solution for their reference.
5. **Continue:** Ask if they are ready for the next question or a follow-up extension of the current code.

**Important Rule:** 
Do NOT ask multiple problems at once. Let the user solve the problem step by step. Await user input after presenting the problem.
