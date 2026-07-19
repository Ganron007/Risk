# GRC sinks overview (CISO Assistant + VerifyWise)

CADRE-Risk keeps **Markdown as source of truth**. Two Docker UIs are available as sinks:

```text
 samples / board memo / risk-register-baseline.md
                    │
                    ▼
            CADRE-Risk engine
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   CISO Assistant         VerifyWise
   (classic GRC)          (AI governance)
   :8080 HTTP             :18080
```

| Tool | Best for Cadre Corp… | CISSP angle |
|------|----------------------|-------------|
| **CISO Assistant** | Asset/risk register, SOC 2 / ISO 27001 / NIST CSF — [REST seed](ciso-notes.md) | Domains 1, 2, 6, 7 |
| **VerifyWise** | DarkAI / RevAI / Praxis as AI systems under EU AI Act / ISO 42001 — [practice + REST](verifywise-notes.md) | Domains 1, 3, 8 + AI governance |

Bring-up: [`docker/README.md`](../docker/README.md).

---

*2026-07-13 — Eramba removed*
