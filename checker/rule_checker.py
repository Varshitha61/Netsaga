import os
import sys
import argparse
import pandas as pd

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cases.csv")

def check_ip_gateway_mismatch(command_output: str) -> bool:
    """
    Very basic heuristic to check if ipconfig shows an IP but gateway is 0.0.0.0
    In reality, this would use a proper CLI parser (like TextFSM/ntc-templates).
    """
    if "IPv4 Address" in command_output and "Default Gateway" in command_output:
        if "0.0.0.0" in command_output:
            return True
    return False

def check_vlan_missing(command_output: str) -> bool:
    """
    Heuristic to check if a specific VLAN might be missing from switchport access.
    """
    if "switchport access vlan" in command_output.lower() or "vlan brief" in command_output.lower():
        # A true implementation would parse out the active VLANs and compare with required.
        pass
    return False

def run_checks(case_id: str) -> dict:
    df = pd.read_csv(CSV_PATH)
    case = df[df["case_id"] == case_id]
    
    if case.empty:
        print(f"Case {case_id} not found.")
        sys.exit(1)
        
    outputs = case.iloc[0]["show_command_outputs"]
    
    results = {
        "case_id": case_id,
        "ip_gateway_mismatch": check_ip_gateway_mismatch(outputs),
        "vlan_missing": check_vlan_missing(outputs),
        # ... other deterministic checks
    }
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Run deterministic rule checks on a case.")
    parser.add_argument("--case-id", required=True, help="The Case ID to check (e.g., CASE001)")
    args = parser.parse_args()
    
    results = run_checks(args.case_id)
    print(f"Rule Checker Results for {args.case_id}:")
    for k, v in results.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
