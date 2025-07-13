from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import yaml
import json
from datetime import datetime, timezone

class ChatbotFunctions:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.prompt_path = Path("prompt.yaml")
        
    def get_prompt(self):
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as file:
                prompt_data = yaml.safe_load(file)
                return prompt_data.get('system_prompt', '')
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
    def load_rubric(self, rubric_path: Path):
        try:
            with open(rubric_path, 'r', encoding='utf-8') as file:
                content = file.read()
                content = content.replace('\ufeff', '')
                content = content.replace('\u2006', ' ')
                
                rubric_data = json.loads(content)
                return rubric_data
        except FileNotFoundError:
            raise FileNotFoundError(f"Rubric file not found: {rubric_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON rubric file: {e}")
    
    
    def load_transcript(self, transcript_file_path):
        try:
            with open(transcript_file_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read().strip()
                return transcript_text
        except FileNotFoundError:
            raise FileNotFoundError(f"Transcript file not found: {transcript_file_path}")
        except UnicodeDecodeError as e:
            raise ValueError(f"Error reading transcript file (encoding issue): {e}")
        
    def prepare_system_prompt(self, rubric_file_path):
        try:
            rubric = self.load_rubric(rubric_file_path)
            prompt_template = self.get_prompt()
            
            rubric_json = json.dumps(rubric, ensure_ascii=False, indent=2)
            system_prompt = prompt_template.replace("{rubric_json}", rubric_json)
            
            return system_prompt
            
        except Exception as e:
            raise RuntimeError(f"Error preparing system prompt: {e}")
    
    def grade_interview(self, rubric_file_path, transcript_file_path):
        try:
            system_prompt = self.prepare_system_prompt(rubric_file_path)
            transcript = self.load_transcript(transcript_file_path)
            llm_response = self.generation(system_prompt, transcript)
            
            try:
                analysis = json.loads(llm_response)
            except json.JSONDecodeError:
                raise ValueError("LLM response is not valid JSON")
            
            question_scores = [q_data["score"] for q_data in analysis["questions"].values()]
            overall_score = sum(question_scores) / len(question_scores) if question_scores else 0
            
            analysis["overall_score"] = round(overall_score, 1)
            analysis["timestamp"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            
            return analysis
            
        except Exception as e:
            raise RuntimeError(f"Error during interview grading: {e}")
    
    def save_analysis(self, analysis, output_file_path):
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                json.dump(analysis, file, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(f"Error saving analysis file: {e}")
    
    def generation(self, system_prompt, transcript):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            temperature=0,
        )
        answer = response.choices[0].message.content.strip()
        return answer