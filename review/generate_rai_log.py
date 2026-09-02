import os
import pandas as pd
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "review_log.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "responsible_ai_log.md")

def generate_report():
    if not os.path.exists(LOG_PATH):
        print("No review_log.csv found.")
        return
        
    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("Review log is empty.")
        return
        
    total = len(df)
    accepted = len(df[df["human_decision"] == "Accepted"])
    rejected = len(df[df["human_decision"] == "Rejected"])
    
    acceptance_rate = (accepted / total) * 100 if total > 0 else 0
    
    report = f"""# Responsible AI Audit Log

**Generated On:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary Metrics
- **Total Cases Reviewed:** {total}
- **Accepted by Human:** {accepted}
- **Rejected by Human:** {rejected}
- **Acceptance Rate:** {acceptance_rate:.2f}%

## Rejected Cases Analysis

"""
    
    rejections = df[df["human_decision"] == "Rejected"]
    if rejections.empty:
        report += "*No cases have been rejected yet.*"
    else:
        for idx, row in rejections.iterrows():
            report += f"### Case: {row['case_id']}\n"
            report += f"- **AI Confidence:** {row['ai_confidence']}\n"
            report += f"- **AI Diagnosis:** {row['ai_diagnosis']}\n"
            report += f"- **Human Comment:** {row['comments']}\n\n"
            
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Responsible AI log generated at {OUT_PATH}")

if __name__ == "__main__":
    generate_report()
