# Indonesia Guide Agent

A multi-agent AI tour guide for Indonesia, built with **Google Agent Development Kit (ADK)**. Ask about Indonesian tourism destinations, culture, or food and receive friendly, Wikipedia-backed answers delivered in the voice of a real-life tour guide.

## How It Works

The agent uses a sequential multi-agent pipeline:

```
User → tour_guide_greeter → indo_tour_workflow
                                 ├── agent_researcher  (Wikipedia lookup)
                                 └── agent_formatter   (Tour guide response)
```

1. **`tour_guide_greeter`** — Greets the user and saves their prompt to shared state via the `add_prompt_to_state` tool, then hands off to the workflow.
2. **`agent_researcher`** — Queries Wikipedia to gather facts about the requested Indonesian location, culture, or food.
3. **`agent_formatter`** — Takes the raw research data and rewrites it in an engaging, tour-guide style for the user.

## Prerequisites

- Python 3.10+
- A Google Cloud project with **Vertex AI** or **Gemini API** access
- Google Cloud credentials configured locally (`gcloud auth application-default login`)

## Installation

```bash
git clone https://github.com/ammarsufyan/IndonesiaGuideAgent.git
cd IndonesiaGuideAgent

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
PROJECT_ID=your-gcp-project-id
PROJECT_NUMBER=your-gcp-project-number
SA_NAME=your-service-account-name
SERVICE_ACCOUNT=your-service-account@your-project.iam.gserviceaccount.com
MODEL=gemini-2.5-flash
```

| Variable | Description |
|----------|-------------|
| `PROJECT_ID` | Google Cloud project ID |
| `PROJECT_NUMBER` | Google Cloud project number |
| `SA_NAME` | Service account name used for Cloud Run deployment |
| `SERVICE_ACCOUNT` | Full service account email (`name@project.iam.gserviceaccount.com`) |
| `MODEL` | Model identifier passed to Google ADK (e.g. `gemini-2.5-flash`) |

## Running the Agent

Use the Google ADK CLI to serve the agent locally:

```bash
adk web
```

Or run it via the ADK runner directly:

```bash
adk run IndonesiaGuideAgent
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `google-adk` | 1.14.0 | Agent framework (Agent, SequentialAgent, LangchainTool) |
| `langchain-community` | 0.3.27 | WikipediaQueryRun + WikipediaAPIWrapper |
| `wikipedia` | 1.4.0 | Wikipedia API backend for LangChain |

Additional implicit dependencies: `google-cloud-logging`, `python-dotenv`.

## License

MIT © 2026 Ammar Sufyan
