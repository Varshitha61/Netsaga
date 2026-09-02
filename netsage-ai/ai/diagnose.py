import os
import sys
import argparse
import json
import pandas as pd
from anthropic import Anthropic
from pydantic import ValidationError
from dotenv import load_dotenv

# Ensure we can import from other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.schema import DiagnosisResult

load_dotenv()

# Constants
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cases.csv")
PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "diagnose_prompt.md")
FEW_SHOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "few_shot_examples.md")

def load_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def construct_prompt(case_row: pd.Series) -> str:
    system_prompt = load_file(PROMPT_PATH)
    few_shot = load_file(FEW_SHOT_PATH)
    
    user_input = f"""
Please diagnose the following case:

Symptom: {case_row['symptom']}
Topology Note: {case_row['topology_note']}
Command Outputs:
{case_row['show_command_outputs']}
"""
    
    return f"{system_prompt}\n\n{few_shot}\n\n{user_input}"

def call_anthropic_api(prompt: str, dry_run: bool = False) -> str:
    if dry_run:
        print("\n--- DRY RUN PROMPT ---")
        print(prompt)
        print("----------------------\n")
        # Return a mock JSON response matching schema
        return json.dumps({
            "diagnosis": "Mock diagnosis for dry run.",
            "fault_category": "Unknown",
            "evidence": ["Mock evidence."],
            "confidence": 0.5,
            "recommended_fix": "Mock fix."
        })

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # In a real implementation, we'd use the message API
    # Since Claude 3, we use the messages endpoint
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Cost effective and fast
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def process_cases(limit: int = 5, dry_run: bool = False):
    df = pd.read_csv(CSV_PATH)
    df = df.head(limit)
    
    results = []
    
    for idx, row in df.iterrows():
        print(f"\nProcessing Case ID: {row['case_id']}...")
        prompt = construct_prompt(row)
        raw_response = call_anthropic_api(prompt, dry_run)
        
        try:
            # Attempt to parse JSON from the raw response
            # Sometimes Claude wraps JSON in markdown blocks
            if "```json" in raw_response:
                json_str = raw_response.split("```json")[1].split("```")[0].strip()
            else:
                json_str = raw_response.strip()
                
            parsed = json.loads(json_str)
            # Validate with Pydantic
            validated = DiagnosisResult(**parsed)
            
            print(f"Success - Diagnosis: {validated.diagnosis}")
            
            result_dict = validated.model_dump()
            result_dict['case_id'] = row['case_id']
            results.append(result_dict)
            
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Failed to parse response for {row['case_id']}: {e}")
            if dry_run:
                print(f"Raw Response: {raw_response}")
                
    # Save results for review
    if results:
        out_path = os.path.join(os.path.dirname(__file__), "ai_results.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved {len(results)} results to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Run AI Diagnosis on test cases.")
    parser.add_argument("--limit", type=int, default=5, help="Number of cases to process.")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without calling API.")
    args = parser.parse_args()
    
    process_cases(limit=args.limit, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
