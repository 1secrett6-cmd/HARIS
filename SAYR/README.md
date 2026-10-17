# SAYR · سَيْر

**The AI Traffic Command Brain for Amman — See. Predict. Act.**
**العقل المروري الذكي لعمّان — نرى. نتنبّأ. نتصرّف.**

Team **NEXORA** · Jordan Students Pitch Competition (GEW Jordan)

SAYR is an AI decision-and-action layer for traffic control rooms. It forecasts congestion and how it spreads across the network, tests every decision in a digital twin before acting, opens green corridors for emergency vehicles, and alerts control-room teams with an Arabic-speaking copilot.

- 📄 Full proposal (Arabic): [`docs/PROPOSAL_AR.md`](docs/PROPOSAL_AR.md)
- 📝 Submission-ready Word file: [`proposal/SAYR_Proposal.docx`](proposal/SAYR_Proposal.docx) (rebuild with `python scripts/build_proposal_docx.py`)
- 🏷️ Naming rationale: [`docs/NAMING.md`](docs/NAMING.md)

## Architecture

| Layer | Package | Purpose |
|---|---|---|
| 1. SEE | `src/sayr/perception` | Vision on authorized camera feeds, data fusion, calendar/weather features |
| 2. PREDICT | `src/sayr/forecasting` | Spatio-temporal forecasting, congestion contagion, incident detection |
| 3. TEST | `src/sayr/twin` | SUMO digital twin built from OpenStreetMap, scenario runner |
| 4. DECIDE | `src/sayr/decision` | Network-level optimization, MARL, safety shield |
| 5. ACT / COMMAND | `src/sayr/command` | Alerts, green corridor, Arabic operator copilot, autonomy levels |
| Future | `src/sayr/field_units` | Drone and robotic field-unit interfaces (L4 vision) |

```
SAYR/
├── docs/            proposal, naming, research notes
├── proposal/        generated .docx for submission
├── scripts/         tooling (proposal builder, data prep)
├── src/sayr/        the platform, one package per layer
├── dashboard/       control-room UI (Streamlit)
├── sim/networks/    SUMO networks (.net.xml, routes)
├── data/            raw/ and processed/ (git-ignored contents)
└── tests/
```

## Getting started

```bash
cd SAYR
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

SUMO is installed separately: https://eclipse.dev/sumo/

## MVP milestones (12 weeks)

- [ ] W1–2: Pick the Amman study area, export OSM, build the SUMO network
- [ ] W3–4: Baseline + first forecasting model (MAE/RMSE vs. naive baseline)
- [ ] W5–6: Decision engine + scenario comparison in the twin
- [ ] W7–8: Emergency green corridor + severity-ranked alerts
- [ ] W9–10: Control-room dashboard + Arabic copilot
- [ ] W11–12: Repeated experiments, documented results, live demo
