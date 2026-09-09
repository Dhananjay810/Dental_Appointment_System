# Dental Appointment Management System

A conversational AI system for managing dental appointments, powered by **LangGraph and OpenRouter (Qwen)**. This project demonstrates an AI-agent workflow where specialized tools work together to handle appointment-related tasks through natural language interactions.

---

## Overview

This system provides a chat-based interface for patients and clinic staff to:

* **Check available appointment slots** and doctor information
* **Book new appointments** with preferred doctors
* **Cancel existing appointments**
* **Reschedule appointments** to different time slots

The system uses a conversational agent that can intelligently understand user intent and invoke the appropriate tools for appointment management, making it a strong educational example of **LangGraph + LangChain + Tool Calling** workflows.

---

## Architecture

### Agent Workflow

The system follows a tool-based conversational workflow:

```text
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
                           │
                           ▼
                 ┌─────────────────┐
                 │  LangGraph Agent│
                 │ (ReAct Workflow)│
                 └────────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 ┌─────────────┐  ┌──────────────┐  ┌───────────────┐
 │ CSV Reader  │  │ CSV Writer   │  │ Slot Validator│
 │    Tools    │  │    Tools     │  │     Tools     │
 └─────────────┘  └──────────────┘  └───────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ doctor_         │
                 │ availability.csv│
                 └─────────────────┘
```

---

## Tool Responsibilities

### Reader Tools

* Get available appointment slots
* List doctors by specialization
* Check patient appointments
* Verify slot availability

### Writer Tools

* Book appointments
* Cancel appointments
* Reschedule appointments

### Validation Layer

* Ensures slots exist
* Prevents double booking
* Validates date formats
* Maintains data consistency

---

## Technology Stack

* **LangGraph** – Workflow orchestration and state management
* **LangChain** – LLM integration and tool framework
* **OpenRouter** – OpenAI-compatible API gateway
* **Qwen 2.5** – Conversational language model
* **Pandas** – CSV data management
* **Pydantic** – Structured validation and schemas
* **Python 3.10+**

---

## Project Structure

```text
dental_agent_project/
├── main.py                          # Interactive CLI entry point
├── doctor_availability.csv          # Appointment data store
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── dental_agent/
│   ├── agent.py                     # Main LangGraph agent
│   ├── config/
│   │   └── settings.py              # Configuration settings
│   ├── tools/
│   │   ├── csv_reader.py            # Read/query operations
│   │   └── csv_writer.py            # Write/update operations
│   ├── utils.py                     # Helper utilities
│   └── workflows/
│       └── graph.py                 # LangGraph workflow definition
```

---

## Installation

### Prerequisites

* Python **3.10 or higher**
* An **OpenRouter API key**

### Setup Steps

#### 1. Clone the repository

```bash
git clone <repository-url>
cd dental_agent_project
```

#### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a **`.env`** file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
MODEL_NAME=qwen/qwen-2.5-7b-instruct
TEMPERATURE=0
```

Get your API key from:

**https://openrouter.ai/keys**

---

## Running the Application

Start the interactive system:

```bash
python main.py
```

### Startup Banner

```text
╔══════════════════════════════════════════════════════════╗
║         Dental Appointment Management System             ║
║      Powered by LangGraph + OpenRouter + Qwen           ║
╚══════════════════════════════════════════════════════════╝
```

---

## Example Interactions

### Check Available Slots

```text
You: Show available slots for an orthodontist

Agent: Here are the available orthodontist appointments:
1. 5/10/2026 9:00 - Dr. Emily Johnson
2. 5/10/2026 10:00 - Dr. Emily Johnson
3. 5/12/2026 14:00 - Dr. Emily Johnson
```

### Book an Appointment

```text
You: Book patient 1000082 with Emily Johnson on 5/10/2026 9:00

Agent: Let me check that slot first...
The slot is available!

I've booked the appointment:
- Patient ID: 1000082
- Doctor: Emily Johnson
- Date/Time: 5/10/2026 9:00
- Specialization: orthodontist
```

### Check Patient Appointments

```text
You: What appointments does patient 1000048 have?

Agent: Patient 1000048 has the following appointments:
1. 5/8/2026 9:00 - Dr. John Doe (general_dentist)
```

### Cancel an Appointment

```text
You: Cancel appointment for patient 1000082 at 5/10/2026 9:00

Agent: I've cancelled the appointment for patient 1000082 on 5/10/2026 at 9:00.
```

### Reschedule an Appointment

```text
You: Reschedule patient 1000082 from 5/10/2026 9:00 to 5/12/2026 10:00

Agent: Let me verify the new slot is available...
It's available!

I've rescheduled the appointment:
- Patient ID: 1000082
- New Date/Time: 5/12/2026 10:00
- Doctor: Emily Johnson
```

---

## Available Specializations

The system supports the following dental specializations:

* `general_dentist`
* `oral_surgeon`
* `orthodontist`
* `cosmetic_dentist`
* `prosthodontist`
* `pediatric_dentist`
* `emergency_dentist`

---

## Data Model

Appointments are stored in **`doctor_availability.csv`**.

| Field               | Description                                 |
| ------------------- | ------------------------------------------- |
| `date_slot`         | Appointment date and time (`M/D/YYYY H:MM`) |
| `specialization`    | Type of dental specialist                   |
| `doctor_name`       | Dentist name                                |
| `is_available`      | Whether the slot is available               |
| `patient_to_attend` | Patient ID if booked                        |

### Example

| date_slot       | specialization | doctor_name   | is_available | patient_to_attend |
| --------------- | -------------- | ------------- | ------------ | ----------------- |
| 5/10/2026 9:00  | orthodontist   | Emily Johnson | False        | 1000082           |
| 5/10/2026 10:00 | orthodontist   | Emily Johnson | True         |                   |

---

## Conversation Flow

The following diagram shows how a booking request is processed:

```text
User Request
      │
      ▼
┌──────────────────────┐
│ "Book an appointment"│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Extract booking info │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Check slot available │
└──────┬─────────┬─────┘
       │ Yes     │ No
       ▼         ▼
┌─────────────┐  ┌──────────────────┐
│ Create      │  │ Suggest alternate│
│ appointment │  │ available slots  │
└──────┬──────┘  └──────────────────┘
       │
       ▼
┌──────────────────────┐
│ Confirm booking      │
└──────────────────────┘
```

---

## For Students: What This Project Demonstrates

This project is useful for learning several important **AI engineering concepts**:

### 1. Tool Calling

The LLM can invoke Python functions as tools instead of generating text-only responses.

### 2. State Management

LangGraph maintains conversation history and tool outputs across multiple turns.

### 3. Structured Validation

Pydantic and utility functions ensure that:

* dates follow the correct format
* required fields are present
* invalid operations are prevented

### 4. Separation of Concerns

* **Agent layer** → conversation and reasoning
* **Tool layer** → business logic
* **Data layer** → CSV persistence

### 5. ReAct Pattern

The agent follows a **Reason → Act → Observe** cycle:

```text
User asks question
        │
        ▼
Agent reasons about intent
        │
        ▼
Agent selects tool
        │
        ▼
Tool executes
        │
        ▼
Agent observes result
        │
        ▼
Agent responds to user
```

---

## Configuration

Environment variables can be customized in `.env`.

| Variable             | Description         | Default                     |
| -------------------- | ------------------- | --------------------------- |
| `OPENROUTER_API_KEY` | OpenRouter API key  | **Required**                |
| `MODEL_NAME`         | Qwen model to use   | `qwen/qwen-2.5-7b-instruct` |
| `TEMPERATURE`        | Response randomness | `0`                         |

For deterministic appointment handling, keep **`TEMPERATURE=0`**.

---

## Future Improvements

Possible enhancements for this project:

* Replace CSV with **SQLite or PostgreSQL**
* Add a **FastAPI** REST backend
* Create a **React or Streamlit UI**
* Add **doctor authentication**
* Send **email/SMS appointment reminders**
* Integrate **calendar synchronization**
* Add **multi-user session support**

---

## Resume-Friendly Description

**Dental Appointment Management System**

Developed an AI-powered dental appointment scheduling assistant using **LangGraph, LangChain, OpenRouter, and Qwen**. Implemented conversational workflows for checking doctor availability, booking appointments, cancellations, and rescheduling with structured tool calling, slot validation, and persistent CSV-based appointment management.

---
