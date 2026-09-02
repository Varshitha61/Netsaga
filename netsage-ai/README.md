# NetSage-AI

**AI-Assisted Network Troubleshooting Helper for Cisco Packet Tracer Labs — with Mandatory Human Review**

---

## Overview

NetSage-AI combines a large language model (Claude) with deterministic rule-checking and a mandatory human-in-the-loop review step to diagnose common network faults found in Cisco Packet Tracer labs. The system is deliberately designed so that **no AI diagnosis is ever accepted without human sign-off**.

---

## Project Structure

```
netsage-ai/
├── data/
│   ├── cases.csv            # 30+ labelled troubleshooting cases
│   └── validate_cases.py    # Dataset integrity checker
├── prompts/
│   ├── diagnose_prompt.md   # System prompt (JSON-enforced output)
│   └── few_shot_examples.md # Worked examples for the model
├── checker/
│   ├── rule_checker.py      # Deterministic rule-based validator
│   └── tests/
│       └── test_rule_checker.py
├── ai/
│   ├── diagnose.py          # Anthropic API client + CLI
│   └── schema.py            # Pydantic response model
├── review/
│   ├── review_cli.py        # Interactive human review tool
│   ├── review_log.csv       # Append-only review audit log
│   ├── responsible_ai_log.md
│   └── generate_rai_log.py
├── dashboard/
│   └── dashboard.py         # Streamlit dashboard
├── demo/
│   └── demo_script.md
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Validate the dataset
```bash
python data/validate_cases.py
```

### 4. Run AI diagnosis (dry run)
```bash
python ai/diagnose.py --dry-run --limit 3
```

### 5. Run AI diagnosis (real, first 5 cases)
```bash
python ai/diagnose.py --limit 5
```

### 6. Run the rule checker on a case
```bash
python checker/rule_checker.py --case-id CASE001
```

### 7. Run tests
```bash
pytest checker/tests/ -v
```

### 8. Human review session
```bash
python review/review_cli.py
```

### 9. Generate responsible AI log
```bash
python review/generate_rai_log.py
```

### 10. Launch dashboard
```bash
streamlit run dashboard/dashboard.py
```

---

## Responsible AI Design

| Principle | Implementation |
|-----------|---------------|
| **Human in the loop** | Every AI diagnosis goes through `review_cli.py` before being counted |
| **Transparency** | All AI evidence and confidence scores are shown to the reviewer |
| **Auditability** | `review_log.csv` is append-only; `responsible_ai_log.md` documents failures |
| **Fail-safe defaults** | Rule checker runs independently of AI; parsing failures are logged, not silent |
| **Bounded claims** | System prompt instructs model to lower confidence when evidence is insufficient |

---

## Fault Categories Covered

- VLAN Misconfiguration
- Default Gateway Issues
- DHCP Failure
- DNS Failure
- Routing Problems
- ACL Blocking
- NAT Misconfiguration
- Wireless / SSID Security Issues

---

## License

MIT
