# NetSage-AI Demo Script

This script walks through demonstrating the core value proposition: AI-assisted network troubleshooting with a mandatory human-in-the-loop and safe-fail defaults.

## Phase 1: The Dataset
1. Open `data/cases.csv` to show the ground truth labels.
2. Run `python data/validate_cases.py` to demonstrate integrity checking.
   *Talking point:* "We enforce strict schema and minimum row counts before any AI process runs."

## Phase 2: The Rules
1. Show `checker/rule_checker.py`.
2. Run `python checker/rule_checker.py --case-id CASE001`.
   *Talking point:* "Before the LLM even sees the output, deterministic scripts check for obvious errors like missing gateways. This ensures we don't rely on AI for basic fact-checking."

## Phase 3: The AI Diagnosis
1. Show `prompts/diagnose_prompt.md` to highlight the JSON enforcement and confidence bounds.
2. Run `python ai/diagnose.py --limit 3` (or `--dry-run`).
   *Talking point:* "The model analyzes the CLI outputs and correlates them with the symptoms, outputting strict JSON and a confidence score."

## Phase 4: Human-in-the-Loop
1. Run `python review/review_cli.py`.
2. Accept a case, then deliberately reject a case, providing a comment.
   *Talking point:* "No diagnosis is accepted automatically. The human operator must review the evidence."

## Phase 5: Responsible AI Audit
1. Run `python review/generate_rai_log.py`.
2. Open `review/responsible_ai_log.md`.
3. Run `streamlit run dashboard/dashboard.py` and show the UI.
   *Talking point:* "Every rejection is audited so we can improve our prompts or catch model drift."
