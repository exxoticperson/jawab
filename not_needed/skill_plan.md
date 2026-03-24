# Jawab Lead Intelligence Skill — Structure Plan

## Skill Name
`jawab-lead-intelligence`

## Skill Description (for frontmatter)
"End-to-end lead sourcing, enrichment, scoring, and outreach system for dental clinics in Gulf markets (UAE + Saudi). Includes ICP scoring, pain signal extraction, personalized outreach templates, and competitor intelligence for Jawab dental AI receptionist sales."

## Skill Purpose
This skill encapsulates the complete workflow for finding, qualifying, and reaching out to dental clinics across Dubai, Sharjah, and Abu Dhabi. It's designed for sales/business development agents executing the Jawab lead generation mission.

## Bundled Resources Structure

### 1. scripts/ (Executable code for repetitive tasks)

#### a) `lead_sourcer.py`
- **Purpose**: Bulk lead extraction from multiple sources
- **Inputs**: City name, search queries (Arabic + English)
- **Outputs**: CSV with clinic data
- **Tools used**: Google Maps API, Outscraper, Instagram scraping
- **Features**:
  - Query builder for Arabic + English searches
  - Phone number validation (+971 country code)
  - Instagram handle verification
  - Data deduplication

#### b) `pain_signal_extractor.py`
- **Purpose**: Scan Google reviews for pain signals
- **Inputs**: Clinic name, Google review URL
- **Outputs**: Pain signal classification, exact quotes
- **Keywords**: "couldn't reach", "no answer", "hard to book", "wait time", etc. (EN + AR)
- **Features**:
  - Bilingual keyword matching
  - Review quote extraction
  - Star rating capture
  - Signal confidence scoring

#### c) `icp_scorer.py`
- **Purpose**: Score clinics on 0-3 scale and tier them
- **Inputs**: Full clinic data (specialty, Instagram, website, pain signals, reviews)
- **Outputs**: CSV with ICP scores, tiers (A/B/C), sorted by score
- **Scoring logic**:
  - Specialty match: 1pt (cosmetic/implant/aesthetic)
  - Digital presence: 1pt (Instagram active + website)
  - Pain signal: 1pt (phone/booking complaint in reviews)
- **Tiering**:
  - Tier A (Top 30): Score 3 OR (Score 2 + 100+ reviews)
  - Tier B (Next 70): Score 2
  - Tier C (Remaining): Score 0-1

#### d) `outreach_generator.py`
- **Purpose**: Generate personalized outreach angles and message drafts
- **Inputs**: Tier A clinic data (top 30)
- **Outputs**: Personalized angles, WhatsApp (Arabic), Instagram DM (English), Email drafts
- **Features**:
  - Personalized angle generation from clinic-specific data
  - Gulf Arabic dialect messaging
  - Multi-channel templates (WhatsApp, Instagram, Email)
  - Objection handling library

#### e) `competitor_mapper.py`
- **Purpose**: Search and map competitor dental AI/chatbot solutions
- **Inputs**: Search queries for competitors
- **Outputs**: Competitor landscape CSV
- **Fields**: Name, website, target market, Arabic support, WhatsApp, voice, pricing, differentiator, weakness vs Jawab

#### f) `data_merger.py`
- **Purpose**: Consolidate data from Manus, Outscraper, manual research
- **Inputs**: Multiple CSV/JSON files
- **Outputs**: Single master Google Sheet with all tabs
- **Features**:
  - Deduplication by phone number
  - Field mapping and normalization
  - Automatic sheet creation

### 2. references/ (Documentation for context loading)

#### a) `icp_criteria.md`
- ICP definition for Gulf dental clinics
- Specialty prioritization (cosmetic > implant > general)
- Digital signal indicators
- Pain signal keywords (EN + AR)
- Disqualifiers (large chains, no online presence)

#### b) `outreach_templates.md`
- WhatsApp message templates (Gulf Arabic)
- Instagram DM templates (English)
- Email templates (professional English)
- Objection handling scripts
- Follow-up sequence (Day 0, 2, 5)
- Call close script (10 minutes)

#### c) `gulf_arabic_guide.md`
- Khaleeji vs MSA comparison
- Common Gulf expressions
- Transliterated Arabic (Arabizi) handling
- Tone guidelines (semi-formal → conversational)
- Greeting/closing phrases

#### d) `sourcing_sources.md`
- Google Maps / Outscraper setup
- Instagram research methodology
- Clinic directory sources (drfive.com, doctoruna.com, health.ae, whatclinic.com)
- LinkedIn clinic page identification
- Search query variations (EN + AR)

#### e) `competitor_landscape.md`
- Known competitors (Arini, Dentina.ai, etc.)
- Competitive positioning vs Jawab
- Market gaps and opportunities

#### f) `data_schema.md`
- Full data dictionary for all fields
- Validation rules
- Required vs optional fields
- Format specifications (phone, Instagram, URLs)

### 3. templates/ (Boilerplate and output assets)

#### a) `master_sheet_template.gsheet`
- Google Sheet template with all tabs pre-configured
- Tabs: All Clinics | Tier A | Tier B | Tier C | Competitors | Summary
- Formulas for auto-scoring and filtering
- Conditional formatting

#### b) `onboarding_document.md`
- Professional onboarding guide for clinics
- Bilingual (Arabic + English)
- Sections: What Jawab does, what we need, what to expect, guarantee, contact

#### c) `message_templates.txt`
- Ready-to-use message templates
- Placeholders for personalization
- Objection response library

#### d) `competitor_tracker.csv`
- Pre-filled with known competitors
- Columns for ongoing research

## SKILL.md Structure

### Frontmatter
- name: jawab-lead-intelligence
- description: [as above]

### Body Sections
1. **Overview** — What this skill does, when to use it
2. **Core Workflow** — 5-task sequence (sourcing → enrichment → scoring → outreach → competitors)
3. **Task 1: Mass Clinic Sourcing** — How to find 300-500 clinics
4. **Task 2: Deep Enrichment & Pain Signals** — How to extract pain signals from reviews
5. **Task 3: ICP Scoring & Ranking** — How to score and tier clinics
6. **Task 4: Personalized Outreach** — How to create angles and message drafts
7. **Task 5: Competitor Intelligence** — How to map competitors
8. **Output Format** — Google Sheet structure with all tabs
9. **Quality Rules** — Data validation, accuracy standards
10. **Tools & Scripts** — When to use each script
11. **Gulf Arabic Dialect** — Key phrases and tone guidelines
12. **Common Pitfalls** — What NOT to do

## Key Design Decisions

1. **Progressive Disclosure**: SKILL.md stays under 500 lines by moving detailed templates to references/
2. **Scripts vs Instructions**: Repetitive/deterministic tasks (scoring, merging) → scripts. Judgment calls (personalization, research) → SKILL.md guidance
3. **Bilingual Support**: All templates include Arabic + English versions
4. **Multi-source Integration**: Scripts handle data from Manus, Outscraper, manual research
5. **Output-Focused**: All scripts generate CSV/JSON that feed into master Google Sheet
6. **Reusability**: Scripts can run independently or in sequence

## Success Criteria for Skill

- ✅ Enables agent to find 300-500 clinics in 3-5 days
- ✅ Automates pain signal extraction and ICP scoring
- ✅ Generates personalized outreach for top 30 clinics
- ✅ Maps competitive landscape
- ✅ Produces clean, actionable Google Sheet output
- ✅ Includes Gulf Arabic dialect guidance
- ✅ Follows skill-creator best practices (concise, reusable, progressive disclosure)
