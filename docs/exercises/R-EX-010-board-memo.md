# R-EX-010 — Board risk memo

**CISSP skill:** Executive communication  
**Inputs:** `python -m src.board_report`, baseline register

## Task

1. Generate a memo from samples.
2. Rewrite the top three findings in **business language** (no jargon dump).
3. State one clear ask of the board for each.

## Answer key

1. Run from repo root after deps installed — see [`../examples/board-memo-sample.md`](../examples/board-memo-sample.md).
2. Examples:
   - DCSync alert → “Attacker-level access to our identity systems is plausible; client monitoring credibility at risk.”
   - Prompt injection → “AI lab leaked a secret; confirm isolation from client evidence.”
   - VR schtask → “Post-exploitation persistence on a member server — close the attack path and verify detections.”
3. Asks: fund identity detection coverage; affirm lab isolation policy; accept residual only with dated review.

**Pass criteria:** A non-technical CEO could act on your memo without reading Elastic JSON.
