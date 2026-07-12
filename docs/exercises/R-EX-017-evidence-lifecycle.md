# R-EX-017 — Client evidence lifecycle

**Domain 2 · Data handling**  
**Asset:** AST-030

## Task
Map Create → Store → Use → Share → Archive → Destroy for a DFIR case image. Note one control per stage.

## Answer key
Create: acquisition hash (CTL-COC) → Store: restricted share (CTL-EVIDENCE-ACCESS) → Use: ticketed analyst access + HITL (CTL-HITL) → Share: legal hold / engagement only → Archive: encrypted offline → Destroy: wipe + certificate. Never copy to AST-035.
