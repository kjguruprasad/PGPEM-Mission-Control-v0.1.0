# 🎓 PGPEM Mission Control

> **Plan • Execute • Analyze • Improve**

An AI-powered Learning Operating System designed for working professionals preparing for Executive MBA entrance examinations such as **IIM Bangalore PGPEM**, CAT, GMAT, GRE and other professional certifications.

---

## Vision

Preparing for an Executive MBA while managing a demanding career is difficult.

Most professionals struggle because they:

- Don't know what to study next.
- Lose consistency.
- Don't revise systematically.
- Fail to analyze mock tests.
- Cannot measure real progress.

PGPEM Mission Control solves these problems by providing a structured preparation system inspired by modern engineering project management practices.

Instead of managing your preparation using scattered notebooks, spreadsheets and reminders, Mission Control provides a single platform to plan, execute, analyze and continuously improve your preparation.

---

# Why this project?

This repository started as a personal initiative to prepare for the Post Graduate Programme in Enterprise Management (PGPEM) offered by the Indian Institute of Management Bangalore.

While building a preparation plan, it became evident that existing study planners lacked several capabilities:

- Intelligent planning
- Analytics
- Revision scheduling
- Progress dashboards
- Mock analysis
- Interview preparation
- Automation

The goal of this project is to build an open-source Learning Operating System that any working professional can customize for their own learning journey.

---

# Objectives

The project aims to help users:

- Plan their entire preparation.
- Track every study session.
- Monitor progress.
- Analyse strengths and weaknesses.
- Improve consistency.
- Build disciplined learning habits.
- Prepare confidently for interviews.

---

# Key Features

## Planning

- SMART Goal Management
- 106-Day Study Planner
- Daily Planner
- Weekly Planner
- Monthly Planner
- Milestone Tracking

---

## Learning

- Quantitative Aptitude
- Data Interpretation
- Logical Reasoning
- Verbal Ability
- Reading Comprehension
- Vocabulary Builder

---

## Revision

- Formula Tracker
- Spaced Repetition
- Revision Calendar
- Mistake Log

---

## Mock Tests

- Mock Schedule
- Section-wise Scores
- Accuracy Analysis
- Time Analysis
- Improvement Tracker

---

## Analytics

- Executive Dashboard
- Study Hours
- Completion %
- Readiness Score
- Burndown Charts
- Heat Maps

---

## Interview Preparation

- STAR Stories
- Resume Tracker
- SOP Preparation
- Business News Tracker
- Current Affairs

---

## Future AI Features

- AI Coach
- Adaptive Scheduler
- Mock Analysis using LLMs
- Personalized Recommendations
- Daily Study Assistant
- Agentic Workflow

---

# Architecture

                +----------------------+
                |      Configuration   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Workbook Generator   |
                +----------+-----------+
                           |
         +-----------------+------------------+
         |                 |                  |
         v                 v                  v
   Dashboard          Planner            Analytics
         |                 |                  |
         +-----------------+------------------+
                           |
                           v
                   Excel Workbook

Future versions will replace the Excel workbook with a complete web platform.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python |
| Workbook | openpyxl |
| Data | Pandas |
| Charts | Matplotlib |
| Configuration | YAML |
| Future Backend | FastAPI |
| Future Frontend | React |
| Future Database | PostgreSQL |
| Future AI | Gemini + ADK |

---

# Repository Structure

```text
PGPEM-Mission-Control/
│
├── docs/
├── src/
├── tests/
├── config/
├── data/
├── output/
├── assets/
└── README.md
```

---

# Roadmap

## Version 0.1

Repository Foundation

## Version 0.2

Workbook Generator

## Version 0.3

Analytics Dashboard

## Version 0.4

Adaptive Scheduler

## Version 0.5

Interview Preparation

## Version 1.0

Mission Control MVP

## Version 2.0

AI Coach

## Version 3.0

Cloud Hosted Web Application

---

# Development Methodology

This project follows Scrum.

Sprint 0

Project Foundation

Sprint 1

Workbook Generator

Sprint 2

Analytics

Sprint 3

Revision Engine

Sprint 4

AI Coach

Sprint 5

Web Application

---

# Guiding Principles

- Consistency beats intensity.
- Measure everything.
- Automate repetitive work.
- Build systems instead of relying on motivation.
- Learn continuously.
- Improve through feedback.

---

# Future Vision

Mission Control is designed to evolve beyond PGPEM preparation.

The same platform can support:

- Executive MBA
- CAT
- GMAT
- GRE
- UPSC
- PMP
- AWS Certification
- Google Cloud Certification
- Microsoft Certification
- Technical Interview Preparation

The architecture is intentionally generic so that new learning paths can be added through configuration instead of code changes.

---

# Contributing

Contributions are welcome.

Future contribution guidelines will include:

- Coding Standards
- Pull Request Workflow
- Branching Strategy
- Documentation Standards
- Testing Requirements

---

# License

MIT License

---

# Author

Guruprasad K J

Senior Engineering Leader

AI Enthusiast

Continuous Learner

---

> "Success is not achieved by studying harder for one day. It is achieved by executing a well-designed system consistently for one hundred days."

