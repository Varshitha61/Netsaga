import os
import json
import csv
from datetime import datetime

AI_RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai", "ai_results.json")
REVIEW_LOG_PATH = os.path.join(os.path.dirname(__file__), "review_log.csv")

def load_ai_results():
    if not os.path.exists(AI_RESULTS_PATH):
        print(f"No AI results found at {AI_RESULTS_PATH}. Run ai/diagnose.py first.")
        return []
    with open(AI_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def append_to_log(case_id, ai_diagnosis, ai_confidence, human_decision, comments):
    file_exists = os.path.isfile(REVIEW_LOG_PATH)
    with open(REVIEW_LOG_PATH, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "case_id", "ai_diagnosis", "ai_confidence", "human_decision", "comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "ai_diagnosis": ai_diagnosis,
            "ai_confidence": ai_confidence,
            "human_decision": human_decision,
            "comments": comments
        })

def main():
    print("=========================================")
    print(" NetSage-AI Mandatory Human Review Tool")
    print("=========================================\n")
    
    results = load_ai_results()
    if not results:
        return
        
    for res in results:
        print(f"\n--- Reviewing Case: {res.get('case_id')} ---")
        print(f"Diagnosis: {res.get('diagnosis')}")
        print(f"Category:  {res.get('fault_category')}")
        print(f"Evidence:  {res.get('evidence')}")
        print(f"Confidence: {res.get('confidence')}")
        print(f"Fix:       {res.get('recommended_fix')}")
        print("-" * 40)
        
        while True:
            decision = input("Accept (a), Reject (r), or Skip (s)? ").strip().lower()
            if decision in ['a', 'r', 's']:
                break
            print("Invalid input. Please enter 'a', 'r', or 's'.")
            
        if decision == 's':
            print("Skipped.")
            continue
            
        comments = ""
        if decision == 'r':
            comments = input("Reason for rejection: ").strip()
            
        status = "Accepted" if decision == 'a' else "Rejected"
        append_to_log(res.get('case_id'), res.get('diagnosis'), res.get('confidence'), status, comments)
        print(f"Log appended: {status}")
        
    print("\nReview session complete. All decisions logged to review_log.csv.")

if __name__ == "__main__":
    main()
