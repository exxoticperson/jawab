---
name: jawab-lead-intelligence
description: "End-to-end lead sourcing, enrichment, scoring, and outreach system for dental clinics in Gulf markets (UAE + Saudi). Includes ICP scoring, pain signal extraction, personalized outreach templates, and competitor intelligence for Jawab dental AI receptionist sales."
---

# Jawab Lead Intelligence Skill

This skill encapsulates the complete workflow for finding, qualifying, and reaching out to dental clinics across Dubai, Sharjah, and Abu Dhabi for Jawab — a bilingual Arabic-English AI front-desk system.

## Overview

Use this skill when executing a lead sourcing and market intelligence mission for Jawab. The workflow is divided into 5 tasks: Mass Sourcing, Pain Signal Extraction, ICP Scoring, Personalized Outreach, and Competitor Intelligence.

## Core Workflow

### Task 1: Mass Clinic Sourcing (Target: 300–500 clinics)
Search for private dental clinics in priority order: Dubai (1) → Sharjah (2) → Abu Dhabi (3).
- **Queries:** "dental clinic [city]", "cosmetic dentist [city]", "implant dentist [city]" (in both English and Arabic).
- **Sources:** Google Maps (primary), Outscraper, Instagram, clinic directories.
- **Data to collect:** See `references/data_schema.md` for required fields.

### Task 2: Deep Enrichment & Pain Signal Extraction
Scan Google reviews for every sourced clinic to find pain signals related to phone/booking issues.
- **Keywords:** "couldn't reach", "no answer", "ما حد رد", "صعب الحجز", etc.
- **Action:** Use `scripts/pain_signal_extractor.py` to automate this process on your CSV data.

### Task 3: ICP Scoring & Ranking
Score each clinic on a 0–3 scale based on specialty, digital presence, and pain signals.
- **Action:** Run `scripts/icp_scorer.py` on your enriched CSV.
- **Tiers:**
  - **Tier A (Top 30):** Score 3, or Score 2 with 100+ reviews (High-personalization).
  - **Tier B (Next 70):** Score 2 (Standard outreach).
  - **Tier C:** Score 0-1 (Backup pipeline).
- **Details:** See `references/icp_criteria.md`.

### Task 4: Personalized Outreach Angles (Top 30 Only)
For Tier A clinics, create specific observations for opening lines and draft multi-channel messages.
- **Action:** Run `scripts/outreach_generator.py` on your Tier A CSV.
- **Templates:** See `references/outreach_templates.md` for WhatsApp (Gulf Arabic), Instagram, and Email templates.
- **Dialect:** Always use Gulf Arabic (Khaleeji), never MSA. See `references/gulf_arabic_guide.md`.

### Task 5: Competitor Intelligence
Map the competitive landscape of dental AI receptionists in the Gulf.
- **Queries:** "dental AI receptionist UAE", "Arini dental", "Dentina.ai".
- **Details:** See `references/competitor_landscape.md`.

## Output Format
Deliver all findings in a single Google Sheet or structured CSV files with these tabs:
1. All Clinics (Full list with Task 1 + 2 data)
2. Tier A (Filtered, enriched, with outreach drafts)
3. Tier B (Filtered with scores)
4. Tier C (Backup)
5. Competitors (Task 5 data)
6. Summary (Key stats)

## Quality Rules
- Every phone number must include the +971 country code.
- Instagram handles must be verified.
- Pain signal quotes must be real, copied directly from reviews.
- Personalized angles must reference something specific and verifiable.
- Do not invent data. Mark missing fields as "Not found."

## Using Bundled Resources

**Scripts (`scripts/`):**
- `python3 /home/ubuntu/skills/jawab-lead-intelligence/scripts/pain_signal_extractor.py input.csv output.csv`: Extracts pain signals from review text.
- `python3 /home/ubuntu/skills/jawab-lead-intelligence/scripts/icp_scorer.py input.csv output.csv`: Calculates scores and assigns tiers.
- `python3 /home/ubuntu/skills/jawab-lead-intelligence/scripts/outreach_generator.py input.csv output.csv`: Drafts personalized messages for Tier A.

**References (`references/`):**
- Load `icp_criteria.md` when evaluating leads.
- Load `outreach_templates.md` when handling objections or writing manual follow-ups.
- Load `gulf_arabic_guide.md` when analyzing patient replies or adjusting tone.
- Load `data_schema.md` to ensure all required fields are present.
- Load `competitor_landscape.md` when performing market research.
