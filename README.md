# NCD Paper IEEE Consumer Electronics Magazine

## Overview
This repository contains code and data resources for generating and analyzing question-answer pairs related to Non-Communicable Diseases (NCDs). The project supports research in automated question generation, categorization, and response synthesis for a wide range of NCDs, with a focus on diversity, real-world scenarios, and clinical relevance.

## Contents
- **ncd_generator_500k.py**: Python script for generating a large-scale (500,000+) dataset of NCD-related Q&A pairs. It uses an expanded set of 50+ NCD categories, detailed keyword mappings, and a diversity matrix for personas and topics.
- **ncd_generator_50k.py**: Python script for generating a smaller (50,000+) dataset, focusing on 15 core NCD categories and their associated keywords.
- **question_bank/**: Directory containing JSON files with Q&A data:
  - `new_data_50k.json`: Newer, diverse Q&A pairs with detailed persona and topic coverage.
  - `seed_data_10k.json`: Seed dataset with foundational Q&A pairs for initial model training or benchmarking.
  - `synthesized_200k.json`: Large synthesized dataset (not viewable in VS Code due to size) for large-scale experiments.

## Key Features
- **Comprehensive NCD Coverage**: From diabetes and hypertension to rare and complex conditions, the scripts support a wide range of NCDs.
- **Persona & Topic Diversity**: Q&A pairs are generated for various patient personas (age, occupation, social context) and real-world topics (diet, medication, mental health, etc.).
- **Keyword-Based Categorization**: Each NCD category is mapped to a set of keywords for accurate detection and classification.
- **Scalable Data Generation**: Scripts can generate datasets of varying sizes for different research needs.

## Usage
1. **Requirements**: Python 3.7+
2. **Run Data Generation**:
   - For 50k dataset: `python ncd_generator_50k.py`
   - For 500k dataset: `python ncd_generator_200k.py`
3. **Data Files**: Generated Q&A pairs are saved in the `question_bank/` directory as JSON files.

## Example Q&A Format
Each entry in the JSON files follows this structure:
```json
{
  "patient_query": "I'm a young adult (20-30) newly diagnosed and I'm struggling with DASH diet implementation. How can I manage this shift work and irregular hours?",
  "doctor_response": "Managing DASH diet implementation with Type 1 Diabetes requires meal timing. Start by start with one small change, then use a reminder system or app.",
  "category": "Diabetes Mellitus"
}
```

## Research Applications
- Training and evaluating NLP models for medical Q&A
- Studying diversity and bias in clinical question answering
- Benchmarking NCD-related information retrieval systems

## Notes
- The `synthesized_200k.json` file is very large and may not be viewable in some editors.
- All data is synthetic and intended for research purposes only.

## Citation
If you use this resource in your research, please cite our paper:

*Authors: Muhammad Jamil*
*Title: Collaborative Intelligence for Non-Communicable Disease Self-Care Using Digital Twin and Metaverse in Consumer Health IoT Ecosystem*
*Conference/Journal: IEEE Consumer Electronics Magazine*

---
For questions or collaboration, contact: [Your Email Here]
