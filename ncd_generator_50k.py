import argparse
import json
import re
from collections import Counter
from typing import Dict, List, Tuple
import random


# ============================================================================
# 15 NEW NCD CATEGORIES (ASI SPECIFIED)
# ============================================================================
NCD_CATEGORIES = [
    "Diabetes Mellitus",
    "Hypertension",
    "Coronary Artery Disease",
    "Obesity",
    "Asthma",
    "Chronic Obstructive Pulmonary Disease",
    "Alzheimer's Disease",
    "Chronic Kidney Disease",
    "Osteoporosis",
    "Stroke",
    "Rheumatoid Arthritis",
    "Parkinson's Disease",
    "Colorectal Cancer",
    "Non-Alcoholic Fatty Liver Disease",
    "Depressive Disorders",
]

# ============================================================================
# CATEGORY KEYWORDS FOR DETECTION
# ============================================================================
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Diabetes Mellitus": [
        "diabetes", "blood sugar", "glucose", "insulin", "a1c", "glycemic",
        "hypoglycemia", "hyperglycemia", "diabetic", "hba1c", "glucose meter"
    ],
    "Hypertension": [
        "hypertension", "blood pressure", "systolic", "diastolic", "hbp",
        "high bp", "antihypertensive", "ace inhibitor", "beta blocker"
    ],
    "Coronary Artery Disease": [
        "coronary", "artery", "heart disease", "angina", "stent", "cardiac",
        "cardiovascular", "myocardial", "chest pain", "coronary artery"
    ],
    "Obesity": [
        "obesity", "overweight", "weight gain", "bmi", "calorie", "portion",
        "lose weight", "weight loss", "body mass index", "bariatric"
    ],
    "Asthma": [
        "asthma", "bronchial", "wheezing", "inhaler", "asthmatic", "albuterol",
        "bronchospasm", "airway", "breathing difficulty", "respiratory"
    ],
    "Chronic Obstructive Pulmonary Disease": [
        "copd", "chronic obstructive", "emphysema", "chronic bronchitis",
        "pulmonary", "lung disease", "bronchodilator", "smoking related"
    ],
    "Alzheimer's Disease": [
        "alzheimer", "dementia", "memory loss", "cognitive", "neurodegeneration",
        "brain", "neurodegenerative", "amyloid", "memory"
    ],
    "Chronic Kidney Disease": [
        "kidney", "renal", "nephropathy", "kidney disease", "glomerular",
        "creatinine", "gfr", "dialysis", "kidney function", "renal failure"
    ],
    "Osteoporosis": [
        "osteoporosis", "bone density", "fracture risk", "bone loss", "skeletal",
        "calcium", "vitamin d", "bone health", "osteoporotic"
    ],
    "Stroke": [
        "stroke", "cerebrovascular", "tia", "transient ischemic", "brain attack",
        "ischemic", "hemorrhagic", "thrombotic", "paralysis", "aphasia"
    ],
    "Rheumatoid Arthritis": [
        "rheumatoid arthritis", "ra", "joint inflammation", "autoimmune",
        "arthritis", "rheumatic", "joint pain", "immune system", "inflammatory"
    ],
    "Parkinson's Disease": [
        "parkinson", "tremor", "parkinsonism", "dopamine", "motor control",
        "bradykinesia", "rigidity", "levodopa", "neurological"
    ],
    "Colorectal Cancer": [
        "colorectal", "colon cancer", "rectal cancer", "cancer", "tumor",
        "chemotherapy", "radiation", "metastatic", "bowel cancer", "malignancy"
    ],
    "Non-Alcoholic Fatty Liver Disease": [
        "fatty liver", "nafld", "hepatic steatosis", "liver disease", "cirrhosis",
        "liver dysfunction", "hepatic", "fibrosis", "liver damage"
    ],
    "Depressive Disorders": [
        "depression", "depressive", "mood disorder", "antidepressant", "mental health",
        "sadness", "anxiety disorder", "ssri", "psychotherapy", "bipolar"
    ],
}

# ============================================================================
# DIVERSITY MATRIX - FULL EXTENDED VERSION
# ============================================================================

CONDITIONS = [
    "Type 1 Diabetes", "Type 2 Diabetes", "Gestational Diabetes",
    "Pre-diabetes", "Obesity", "Metabolic Syndrome",
    "Hypertension", "Heart Failure", "Coronary Artery Disease",
    "Atrial Fibrillation", "Post-Stroke Recovery", "Peripheral Artery Disease",
    "High Cholesterol", "Angina",
    "COPD", "Asthma", "Interstitial Lung Disease", "Sleep Apnea",
    "Bronchiectasis", "Post-COVID Lung Issues",
    "Chronic Kidney Disease Stage 1", "Chronic Kidney Disease Stage 5", "Diabetic Nephropathy",
    "Chronic UTI", "Polycystic Kidney Disease",
    "Osteoarthritis", "Rheumatoid Arthritis", "Gout", "Osteoporosis",
    "Lupus", "Fibromyalgia",
    "Migraine", "Epilepsy", "Parkinson's Disease", "Multiple Sclerosis",
    "Dementia", "Neuropathy",
    "Thyroid Disease", "Fatty Liver Disease", "Anemia", "Cancer Survivorship",
    "HIV/AIDS Management", "Hepatitis C"
]

PERSONAS = [
    "a teenager (13-19) managing illness independently",
    "a young adult (20-30) newly diagnosed",
    "a parent (30-50) of young children",
    "a middle-aged professional (40-60) with multiple comorbidities",
    "an elderly person (65+) managing complex medications",
    "a very elderly person (80+) with limited mobility",
    "a high-stress executive", "a night-shift nurse", "a construction worker",
    "a teacher in a classroom environment", "a healthcare worker",
    "an athlete/sports professional", "a musician on tour",
    "a chef/restaurant worker", "a farmer with seasonal stress",
    "a freelancer with irregular income", "a truck driver",
    "a factory worker with shift changes",
    "someone living alone in a rural area", "someone in a shared apartment",
    "someone homeless or housing-insecure", "someone in a care home",
    "someone living with extended family", "someone in a dorm",
    "someone with a caregiver/family support",
    "a fitness enthusiast/gym-goer", "a sedentary office worker",
    "a vegan/vegetarian", "someone with food allergies",
    "a frequent international traveler", "someone unable to afford medications",
    "someone with limited internet access", "a tech-savvy digital nomad",
    "a person with limited education/health literacy",
    "someone dealing with substance use history",
    "a pregnant woman with chronic illness", "a new mother",
    "a caregiver for another chronic patient", "someone recently bereaved",
    "someone recovering from surgery", "someone with mental health comorbidity",
    "an immigrant with language barriers", "someone in financial stress",
    "a person recently retired", "someone with a new diagnosis",
    "a student balancing studies and health", "a single parent",
    "someone with a supportive partner", "a competitive athlete",
]

TOPICS = [
    "carbohydrate counting for diabetes", "DASH diet implementation",
    "Mediterranean diet benefits", "salt reduction strategies",
    "meal prep and batch cooking", "reading food labels",
    "managing cravings and emotional eating", "intermittent fasting safety",
    "ketogenic diet risks/benefits", "vegetarian/vegan protein sources",
    "managing hunger while losing weight", "restaurant meal choices",
    "grocery shopping on a budget", "hydration and fluid management",
    "caffeine and stimulant intake", "alcohol interactions with medications",
    "managing portion sizes at home", "food safety with weakened immunity",
    "starting an exercise program from zero", "safe exercise intensity zones",
    "resistance training with limited mobility", "aquatic therapy",
    "yoga and flexibility for stiffness", "high-altitude exercise risks",
    "exercise in extreme weather", "preventing exercise-related injuries",
    "recovery and rest days", "staying active during flare-ups",
    "home exercises without equipment", "group fitness classes",
    "walking programs", "fall prevention and balance",
    "understanding drug interactions", "managing medication side effects",
    "remembering to take multiple medications", "using pill organizers/reminders",
    "buying generic vs. brand medications", "medication costs and insurance",
    "stopping medications safely", "adjusting doses during illness",
    "medication storage and expiration", "medication during pregnancy",
    "interactions with supplements/herbs", "timing of medication doses",
    "anxiety related to health condition", "depression from chronic illness",
    "health anxiety and excessive checking", "sleep problems and insomnia",
    "stress management techniques", "mindfulness and meditation",
    "counseling and therapy options", "managing social isolation",
    "coping with disease progression", "sexual health and intimacy",
    "grief and acceptance", "building resilience",
    "interpreting home glucose/BP/weight readings", "when to seek emergency care",
    "red flags specific to my condition", "tracking symptoms in a diary",
    "using wearable devices and apps", "recognizing early warning signs",
    "managing pain at home", "managing fatigue", "managing swelling/edema",
    "controlling cough and breathing issues", "managing nausea/vomiting",
    "managing illness while traveling", "adjusting routine for work",
    "explaining my condition to family", "managing relationships with illness",
    "parenting while chronically ill", "school/university attendance",
    "dating and disclosure of illness", "driving safely with my condition",
    "workplace accommodations and rights", "financial planning with illness",
    "insurance and healthcare navigation", "accessing care in remote areas",
    "managing during cold/flu season", "adjusting care in extreme heat",
    "managing in high humidity or air pollution", "altitude and travel",
    "seasonal mood changes", "managing during natural disasters",
    "vaccine safety with my condition", "managing during pandemics"
]

SETTINGS = [
    "early morning routine", "nighttime/bedtime management",
    "shift work and irregular hours", "weekend vs. weekday routine",
    "seasonal changes", "holiday season management",
    "at home alone", "in a hospital/clinic", "at work",
    "while traveling internationally", "in a rural/remote area",
    "in a refugee camp or temporary shelter", "on vacation",
    "at a social gathering/party", "at a restaurant/cafe",
    "at the gym or fitness facility", "outdoors in nature",
    "with family present", "with romantic partner", "with friends",
    "at work with colleagues", "in public/with strangers",
    "while caregiving for someone else",
    "during symptom flare-up", "during extreme stress", "during grief",
    "during financial hardship", "during relationship conflict",
    "when accessing healthcare is difficult", "when medication is unavailable",
    "at a funeral or sad event", "at a celebration or happy event",
    "during a health crisis", "after receiving bad news", "after good news"
]

COMORBIDITIES = [
    "no other conditions",
    "plus depression", "plus anxiety", "plus both depression and anxiety",
    "plus chronic pain", "plus sleep disorder",
    "plus another NCD", "plus multiple NCDs",
    "plus active infection/illness", "plus recent surgery",
    "plus substance use disorder history", "plus eating disorder history",
    "plus cognitive impairment", "plus mobility limitations",
    "plus hearing loss", "plus vision loss", "plus both hearing and vision loss"
]

RESOURCE_LEVEL = [
    "high income - unlimited resources",
    "middle income - some financial constraints",
    "low income - significant financial limitations",
    "homeless or unstable housing",
    "refugee or displaced person"
]

TECH_ACCESS = [
    "smartphone and internet access",
    "basic phone, limited internet",
    "no smartphone, limited tech",
    "no reliable internet access",
    "access to library/community tech"
]

HEALTH_LITERACY = [
    "high - understands medical terms",
    "medium - some medical knowledge",
    "low - needs simple explanations",
    "very low - needs visual/oral explanations",
    "language barrier - non-native speaker"
]

MOTIVATION = [
    "highly motivated - wants perfect compliance",
    "moderately motivated - trying to do best",
    "low motivation - struggling with adherence",
    "newly diagnosed - still in denial phase",
    "overwhelmed - confused about priorities"
]

CULTURAL_CONTEXT = [
    "English-speaking, Western culture",
    "Turkish culture and values",
    "Arabic/Islamic culture",
    "Asian (South/East/Southeast Asian) culture",
    "African culture and context",
    "Latin American culture",
    "Indigenous/Traditional medicine beliefs",
    "Immigrant with culture transition challenges"
]

# ============================================================================
# DETAILS BY CATEGORY (EXPANDED)
# ============================================================================

DETAILS_BY_CATEGORY = {
    "Diabetes Mellitus": [
        "meal timing", "glucose monitoring", "hypoglycemia prevention",
        "medication timing", "foot care", "blood sugar targets", "carb counting"
    ],
    "Hypertension": [
        "home blood pressure monitoring", "sodium reduction", "medication timing",
        "caffeine limits", "sleep quality", "stress management", "regular checkups"
    ],
    "Coronary Artery Disease": [
        "chest pain management", "safe exercise", "medication adherence",
        "heart medication timing", "stress reduction", "cardiac rehabilitation"
    ],
    "Obesity": [
        "portion control", "meal planning", "craving management",
        "sustainable exercise", "behavior change tracking", "water intake"
    ],
    "Asthma": [
        "inhaler technique", "trigger avoidance", "peak flow monitoring",
        "exercise safety", "allergy management", "medication adherence"
    ],
    "Chronic Obstructive Pulmonary Disease": [
        "breathing techniques", "oxygen therapy", "medication adherence",
        "airway clearance", "exercise tolerance", "infection prevention"
    ],
    "Alzheimer's Disease": [
        "memory support strategies", "safety precautions", "medication adherence",
        "cognitive activities", "caregiver support", "routine establishment"
    ],
    "Chronic Kidney Disease": [
        "fluid intake management", "sodium restriction", "protein intake",
        "phosphorus management", "medication timing", "lab monitoring"
    ],
    "Osteoporosis": [
        "calcium intake", "vitamin D levels", "fall prevention", "bone density",
        "exercise safety", "medication adherence"
    ],
    "Stroke": [
        "speech recovery", "muscle rehabilitation", "medication adherence",
        "blood clot prevention", "secondary stroke prevention", "therapy sessions"
    ],
    "Rheumatoid Arthritis": [
        "joint protection", "inflammation management", "exercise for mobility",
        "medication adherence", "pain management", "fatigue management"
    ],
    "Parkinson's Disease": [
        "tremor management", "movement optimization", "medication timing",
        "balance and fall prevention", "speech exercises", "cognitive activities"
    ],
    "Colorectal Cancer": [
        "treatment side effect management", "nutrition support", "pain management",
        "follow-up surveillance", "chemotherapy tolerance", "psychosocial support"
    ],
    "Non-Alcoholic Fatty Liver Disease": [
        "weight management", "alcohol avoidance", "nutrition planning",
        "exercise routine", "liver enzyme monitoring", "disease progression prevention"
    ],
    "Depressive Disorders": [
        "medication adherence", "therapy engagement", "mood tracking",
        "sleep hygiene", "social connection", "physical activity", "crisis planning"
    ],
}

# ============================================================================
# QUESTION TEMPLATES FOR DIVERSITY
# ============================================================================

QUESTION_TEMPLATES = [
    "As {persona}, I have {condition}. {topic_phrase}. What should I do?",
    "I'm {persona} and I'm struggling with {topic}. How can I manage this {setting}?",
    "With {comorbidity}, how should I handle {topic} when I'm {persona}?",
    "{persona} here, with {condition}. Can you explain {topic} in simple terms?",
    "I'm {persona}, and {topic} is difficult {setting}. What's a practical approach?",
    "As {persona}, I'm worried about {topic} because of my {condition}. What can help?",
    "With my {condition} and {comorbidity}, how do I manage {topic} while {setting}?",
    "I'm {persona} with {resource} and limited {tech}. How do I address {topic}?",
    "{persona} managing {condition}. My health literacy is {literacy}. {topic_phrase}?",
    "My motivation is {motivation} for managing {topic}. I'm {persona} with {condition}. Suggestions?",
]

RESPONSE_TEMPLATES = [
    "For your situation as {persona}, the key is {detail}. Here's a practical approach: {approach}.",
    "Managing {topic} with {condition} requires {detail}. Start by {action}, then {action2}.",
    "Given your {resource} and {tech} access, focus on {detail} first. You can {approach}.",
    "With {literacy}, I'll keep this simple: {approach}. The most important part is {detail}.",
    "Your {motivation} is good. To address {topic}, prioritize {detail} and {action}.",
    "Considering {comorbidity}, be especially attentive to {detail}. Your best approach: {approach}.",
    "In your {setting}, the safest strategy for {topic} is {approach}. Remember: {important_point}.",
    "For {persona} managing {condition}, {topic} works best when you {action}. Focus on {detail}.",
]

APPROACHES = [
    "track daily patterns for one week",
    "start with one small change",
    "use a reminder system or app",
    "work with a healthcare provider",
    "join a support group",
    "practice gradual adjustment",
    "seek professional guidance",
    "involve your family",
    "break it into smaller steps",
    "monitor for changes"
]

IMPORTANT_POINTS = [
    "consistency matters more than perfection",
    "don't hesitate to ask for help",
    "your mental health is equally important",
    "small changes accumulate over time",
    "listen to your body's signals",
    "reach out if symptoms worsen",
    "celebrate small victories",
    "adapt your plan as needed",
    "regular check-ins with your doctor are essential",
    "you're not alone in this journey"
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip().lower())

def detect_category(text: str, fallback_index: int) -> str:
    text_lower = text.lower()
    best_category = ""
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > best_score:
            best_score = score
            best_category = category

    if best_category:
        return best_category
    return NCD_CATEGORIES[fallback_index % len(NCD_CATEGORIES)]

def ensure_question_mark(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text.endswith("?"):
        return text
    return f"{text}?"

# ============================================================================
# PRIMARY FUNCTION
# ============================================================================

def generate_diverse_question_pair(
    source_index: int, variant_index: int
) -> Tuple[str, str, str]:
    """Generate a diverse QA pair using the diversity matrix."""
    
    condition = CONDITIONS[source_index % len(CONDITIONS)]
    persona = PERSONAS[(source_index + variant_index) % len(PERSONAS)]
    topic = TOPICS[(source_index * 2 + variant_index) % len(TOPICS)]
    setting = SETTINGS[(source_index * 3 + variant_index * 2) % len(SETTINGS)]
    comorbidity = COMORBIDITIES[(source_index + variant_index * 3) % len(COMORBIDITIES)]
    resource = RESOURCE_LEVEL[(source_index * 5 + variant_index) % len(RESOURCE_LEVEL)]
    tech = TECH_ACCESS[(source_index * 7 + variant_index * 2) % len(TECH_ACCESS)]
    literacy = HEALTH_LITERACY[(source_index + variant_index * 5) % len(HEALTH_LITERACY)]
    motivation = MOTIVATION[(source_index * 11 + variant_index) % len(MOTIVATION)]
    culture = CULTURAL_CONTEXT[(source_index * 13 + variant_index * 3) % len(CULTURAL_CONTEXT)]
    
    category = detect_category(f"{condition} {topic}", source_index % len(NCD_CATEGORIES))
    
    # Select a question template
    q_template = QUESTION_TEMPLATES[variant_index % len(QUESTION_TEMPLATES)]
    topic_phrase = f"I need help with {topic}"
    
    patient_query = ensure_question_mark(
        q_template.format(
            persona=persona,
            condition=condition,
            topic_phrase=topic_phrase,
            topic=topic,
            setting=setting,
            comorbidity=comorbidity,
            resource=resource,
            tech=tech,
            literacy=literacy,
            motivation=motivation
        )
    )
    
    # Generate response
    detail_opts = DETAILS_BY_CATEGORY.get(category, DETAILS_BY_CATEGORY["Diabetes Mellitus"])
    detail = detail_opts[(source_index + variant_index * 7) % len(detail_opts)]
    approach = APPROACHES[(source_index * 17 + variant_index) % len(APPROACHES)]
    action = approach
    action2 = APPROACHES[(source_index * 19 + variant_index * 2) % len(APPROACHES)]
    important = IMPORTANT_POINTS[(source_index * 23 + variant_index * 3) % len(IMPORTANT_POINTS)]
    
    r_template = RESPONSE_TEMPLATES[variant_index % len(RESPONSE_TEMPLATES)]
    doctor_response = r_template.format(
        persona=persona,
        detail=detail,
        approach=approach,
        action=action,
        action2=action2,
        topic=topic,
        condition=condition,
        resource=resource,
        tech=tech,
        literacy=literacy,
        motivation=motivation,
        comorbidity=comorbidity,
        setting=setting,
        important_point=important
    )
    
    return ensure_question_mark(patient_query), doctor_response, category

# ============================================================================
# MAIN GENERATION LOGIC
# ============================================================================

def generate_50k_dataset(output_file: str, target_count: int = 50000) -> List[Dict]:
    """Generate 50,000 unique diverse questions."""
    
    generated: List[Dict] = []
    seen_queries = set()
    
    base_sources = len(CONDITIONS)
    variants_per_source = target_count // base_sources
    extra = target_count % base_sources
    
    print(f"Generating {target_count} unique questions from {base_sources} base conditions...")
    print(f"Variants per source: {variants_per_source} + {extra} extra\n")
    
    record_id = 1
    for source_idx in range(base_sources):
        variant_count = variants_per_source + (1 if source_idx < extra else 0)
        
        for variant_idx in range(1, variant_count + 1):
            try:
                query, response, category = generate_diverse_question_pair(source_idx, variant_idx)
                
                normalized_q = normalize_text(query)
                if normalized_q in seen_queries:
                    continue
                
                seen_queries.add(normalized_q)
                
                generated.append({
                    "patient_query": query,
                    "doctor_response": response,
                    "category": category
                })
                
                record_id += 1
                
                if record_id % 5000 == 0:
                    print(f"Generated {record_id} unique questions...")
                
                if len(generated) >= target_count:
                    break
            except Exception as e:
                print(f"Error generating variant {variant_idx}: {e}")
                continue
        
        if len(generated) >= target_count:
            break
    
    generated = generated[:target_count]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated, f, ensure_ascii=False, indent=2)
    
    return generated

# ============================================================================
# SUMMARY AND VALIDATION
# ============================================================================

def print_summary(records: List[Dict]) -> None:
    print("\n" + "="*70)
    print("DATASET GENERATION SUMMARY")
    print("="*70)
    print(f"\nTotal records generated: {len(records)}")
    
    category_counts = Counter(r["category"] for r in records)
    print("\nCategory Distribution:")
    for category in sorted(NCD_CATEGORIES):
        count = category_counts.get(category, 0)
        percent = (count / len(records)) * 100 if records else 0
        print(f"  {category:.<50} {count:>6} ({percent:>5.2f}%)")
    
    seen = set()
    duplicates = 0
    for r in records:
        normalized = normalize_text(r["patient_query"])
        if normalized in seen:
            duplicates += 1
        seen.add(normalized)
    
    print(f"\nUniqueness Check:")
    print(f"  Total queries: {len(records)}")
    print(f"  Unique queries: {len(seen)}")
    print(f"  Duplicates detected: {duplicates}")
    if duplicates == 0:
        print("    All queries are unique!")
    
    print(f"\nFile Statistics:")
    print(f"  Approx. size: {len(json.dumps(records, ensure_ascii=False)) / (1024*1024):.2f} MB")
    print(f"  Date: March 13, 2026")
    print("="*70 + "\n")

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate 50K diverse NCD questions")
    parser.add_argument("--output", default="new_data_50000.json", help="Output JSON file")
    parser.add_argument("--target", type=int, default=50000, help="Target question count")
    args = parser.parse_args()
    
    print("\n🚀 Starting 50K NCD Question Generation...")
    print(f"   Categories: {len(NCD_CATEGORIES)}")
    print(f"   Base conditions: {len(CONDITIONS)}")
    print(f"   Personas: {len(PERSONAS)}")
    print(f"   Topics: {len(TOPICS)}")
    print(f"   Settings: {len(SETTINGS)}")
    print(f"   Target output: {args.output}\n")
    
    records = generate_50k_dataset(args.output, args.target)
    print_summary(records)
    print(f"  Dataset saved to: {args.output}")

if __name__ == "__main__":
    main()
