# Interview Grader CLI

A simple CLI tool that uses AI to grade interview transcripts against a predefined rubric.

## Usage

```bash
python grade_interview.py -r rubric.json -t transcript.txt -o analysis.json
```

**Arguments:**
- `-r, --rubric`: Path to the rubric JSON file
- `-t, --transcript`: Path to the interview transcript text file  
- `-o, --output`: Path where the analysis JSON will be written

## Setup

1. Install dependencies: `openai`, `python-dotenv`, `pyyaml`
2. Set your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Example

```bash
python grade_interview.py -r rubric.json -t transcripts/transcript1.txt -o results.json
```

The tool will analyze the transcript against the rubric questions and output a JSON file with scores and feedback for each question.