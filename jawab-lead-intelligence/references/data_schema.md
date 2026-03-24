# Jawab Lead Intelligence Data Schema

This document defines the required data fields and formats for the final output spreadsheet.

## Required Fields

Every clinic record must contain the following fields. If a field cannot be found, mark it exactly as "Not found."

| Field | Description & Format Rules |
|-------|----------------------------|
| **Clinic Name** | Full name as it appears on Google Maps. |
| **City** | Must be one of: Dubai, Sharjah, Abu Dhabi. |
| **Area/District** | Specific neighborhood (e.g., JLT, Marina, Deira, Mirdif). |
| **Phone Number** | Primary phone. **MUST include country code (+971...)**. |
| **WhatsApp Number** | If visible on website or Instagram bio. Often same as phone or separate. Mark "Not visible" if not found. |
| **Website** | Full URL including https://. |
| **Instagram Handle** | Format: `@handle`. Must be verified as the correct clinic (not a random match). |
| **Google Rating** | Numeric (e.g., 4.6). |
| **Google Review Count** | Integer (e.g., 342). |
| **Specialty** | Categorize as: Cosmetic, Implant, General, Orthodontic, Pediatric, or Multi-specialty. |
| **Owner/Lead Dentist Name** | If visible on website, Google listing, or LinkedIn. |
| **Chain or Independent** | Categorize as: Chain or Independent. |
| **Email** | If visible on website or Google listing. |
| **Instagram Follower Count** | Integer (if easily visible). |
| **Last Instagram Post Date** | Date format (YYYY-MM-DD) to gauge activity. |

## Enrichment Fields (Task 2)

| Field | Description & Format Rules |
|-------|----------------------------|
| **Pain Signal Found** | Yes / No. |
| **Pain Signal Type** | Categorize as: phone, booking, response, or front desk. |
| **Exact Review Quote** | Copy the specific sentence in its original language. Do not paraphrase. |
| **Review Star Rating** | Star rating of the individual review (1-5). |

## Scoring Fields (Task 3)

| Field | Description & Format Rules |
|-------|----------------------------|
| **ICP Score** | Integer from 0 to 3 based on scoring criteria. |
| **Tier** | A, B, or C. |
| **Primary Outreach Channel** | Preferred method based on available data (WhatsApp > Instagram DM > Email). |
| **Secondary Channel** | Fallback contact method. |

## Personalization Fields (Task 4 - Tier A Only)

| Field | Description & Format Rules |
|-------|----------------------------|
| **Personalized Angle** | One specific observation to be used in the opening line. Must reference something real and verifiable. |
| **WhatsApp Draft (AR)** | Full drafted message in Gulf Arabic. |
| **Instagram Draft (EN)** | Full drafted message in English. |
| **Email Draft (EN)** | Full drafted email with subject line. |

## Competitor Fields (Task 5)

| Field | Description & Format Rules |
|-------|----------------------------|
| **Name** | Company/product name. |
| **Website** | Full URL. |
| **Target Market** | Which countries/regions they target. |
| **Arabic Support** | Yes / No / Partial. |
| **WhatsApp Support** | Yes / No. |
| **Voice Support** | Yes / No. |
| **Pricing** | Include if publicly available. |
| **Key Differentiator** | What is their main pitch? |
| **Gulf Presence** | Do they have Gulf-specific clients or content? |
| **Weakness vs Jawab** | What does Jawab do better? |
