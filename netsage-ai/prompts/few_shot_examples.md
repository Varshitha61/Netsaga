# Few-Shot Examples

## Example 1: Missing Default Gateway on End Device

**Input:**
- Symptom: PC1 cannot ping Server1 on another subnet.
- Topology Note: PC1 is in VLAN 10 (192.168.10.0/24), Server1 is in VLAN 20 (192.168.20.0/24).
- Command Outputs:
  ```
  PC1> ipconfig
  FastEthernet0 Connection:(default port)
     Connection-specific DNS Suffix..: 
     Link-local IPv6 Address.........: FE80::201:97FF:FE75:3286
     IPv4 Address....................: 192.168.10.10
     Subnet Mask.....................: 255.255.255.0
     Default Gateway.................: 0.0.0.0
  ```

**Expected JSON Output:**
```json
{
  "diagnosis": "PC1 is missing a default gateway configuration, preventing it from reaching other subnets.",
  "fault_category": "Default Gateway Issues",
  "evidence": [
    "ipconfig output on PC1 shows Default Gateway as 0.0.0.0"
  ],
  "confidence": 0.95,
  "recommended_fix": "Configure the default gateway on PC1 (e.g., 192.168.10.1) depending on the router interface IP."
}
```

## Example 2: VLAN Mismatch on Access Port

**Input:**
- Symptom: PC2 cannot communicate with other devices in VLAN 20.
- Topology Note: PC2 is connected to Switch1 FastEthernet0/2. Switch1 should place PC2 in VLAN 20.
- Command Outputs:
  ```
  Switch1# show vlan brief
  VLAN Name                             Status    Ports
  ---- -------------------------------- --------- -------------------------------
  1    default                          active    Fa0/1, Fa0/2, Fa0/3
  20   Engineering                      active    Fa0/10
  ```

**Expected JSON Output:**
```json
{
  "diagnosis": "Switch1 port Fa0/2 is configured in the default VLAN 1 instead of VLAN 20.",
  "fault_category": "VLAN Misconfiguration",
  "evidence": [
    "show vlan brief output shows Fa0/2 is in VLAN 1, not VLAN 20."
  ],
  "confidence": 0.90,
  "recommended_fix": "conf t\ninterface fa0/2\nswitchport access vlan 20"
}
```
