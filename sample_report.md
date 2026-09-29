# Cyber Risk Executive Summary
_Generated 2026-09-28 | 8 risks | risk appetite threshold: residual score 10_

## 1. Headline numbers

- **Inherent annualised loss exposure:** $1,059,000
- **Residual annualised loss exposure:** $602,850
- **Value delivered by current controls:** 43% reduction
- **Residual rating mix:** Critical: 0, High: 1, Medium: 4, Low: 3

## 2. Top risks (by residual score)

| ID | Risk | Owner | Inherent | Residual | Rating | Residual ALE | Treatment |
|---|---|---|---|---|---|---|---|
| R-003 | Unpatched internet-facing VPN | IT Ops Manager | 15 | 12.0 | High | $168,000 | accept |
| R-002 | Phished admin credentials | IAM Lead | 16 | 9.6 | Medium | $144,000 | mitigate |
| R-001 | Ransomware on file servers | CISO | 20 | 9.0 | Medium | $121,500 | mitigate |
| R-007 | Insider data exfiltration | CISO | 10 | 6.5 | Medium | $39,000 | mitigate |
| R-005 | Third-party SaaS breach | Vendor Risk Mgr | 8 | 5.6 | Medium | $28,000 | transfer |

## 3. Risk appetite breaches requiring decision

- **R-003 Unpatched internet-facing VPN**: residual 12.0 exceeds appetite 10 while treatment is *accept*. Owner: IT Ops Manager. Escalate for formal acceptance or funded mitigation.

## 4. Exposure by NIST CSF 2.0 function

| Function | Risks | Residual ALE |
|---|---|---|
| Protect | 3 | $304,000 |
| Identify | 1 | $168,000 |
| Detect | 2 | $96,600 |
| Govern | 1 | $28,000 |
| Recover | 1 | $6,250 |

## 5. Exposure by CISSP domain

| Domain | Risks | Avg residual |
|---|---|---|
| Asset Security | 1 | 4.8 |
| Communication and Network Security | 1 | 6.5 |
| Identity and Access Management | 1 | 9.6 |
| Security Architecture and Engineering | 1 | 1.5 |
| Security Assessment and Testing | 1 | 12.0 |
| Security Operations | 1 | 9.0 |
| Security and Risk Management | 1 | 5.6 |
| Software Development Security | 1 | 5.0 |

## 6. Governance hygiene

- Overdue risk reviews: **2** (R-002, R-005)

## 7. Inherent risk heatmap

```
Impact
  5 |     .       R-007     R-003     R-001       .    
  4 |     .       R-005     R-004     R-002       .    
  3 |     .       R-006     R-008       .         .    
  2 |     .         .         .         .         .    
  1 |     .         .         .         .         .    
    +--------------------------------------------------
          1         2         3         4         5      Likelihood
```
