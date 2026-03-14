import argparse
import json
import re
from collections import Counter
from typing import Dict, List, Tuple
import random


# ============================================================================
# 50 COMPREHENSIVE NCD CATEGORIES (MASSIVELY EXPANDED)
# ============================================================================
NCD_CATEGORIES = [
    # Endocrine & Metabolic
    "Type 1 Diabetes Mellitus",
    "Type 2 Diabetes Mellitus",
    "Gestational Diabetes",
    "Metabolic Syndrome",
    "Thyroid Disorders",
    "Hyperlipidemia",
    
    # Cardiovascular
    "Hypertension",
    "Coronary Artery Disease",
    "Heart Failure",
    "Atrial Fibrillation",
    "Peripheral Arterial Disease",
    "Stroke",
    "Transient Ischemic Attack",
    "Aortic Aneurysm",
    "Venous Thromboembolism",
    "Myocarditis",
    "Pericarditis",
    "Cardiomyopathy",
    
    # Respiratory
    "Asthma",
    "Chronic Obstructive Pulmonary Disease",
    "Interstitial Lung Disease",
    "Pulmonary Hypertension",
    "Cystic Fibrosis",
    "Sleep Apnea",
    "Bronchiectasis",
    "Idiopathic Pulmonary Fibrosis",
    
    # Renal & Urologic
    "Chronic Kidney Disease",
    "End-Stage Renal Disease",
    "Diabetic Nephropathy",
    "Glomerulonephritis",
    "Polycystic Kidney Disease",
    "Chronic Urinary Tract Infections",
    
    # Musculoskeletal & Rheumatologic
    "Osteoarthritis",
    "Rheumatoid Arthritis",
    "Systemic Lupus Erythematosus",
    "Gout",
    "Osteoporosis",
    "Ankylosing Spondylitis",
    "Fibromyalgia",
    
    # Neurologic
    "Parkinson's Disease",
    "Alzheimer's Disease",
    "Multiple Sclerosis",
    "Epilepsy",
    "Migraine Disorder",
    "Peripheral Neuropathy",
    
    # Hepatic & Gastrointestinal
    "Non-Alcoholic Fatty Liver Disease",
    "Hepatitis C",
    "Cirrhosis",
    "Inflammatory Bowel Disease",
    "Celiac Disease",
    "Gastroesophageal Reflux Disease",
    
    # Hematologic & Oncologic
    "Colorectal Cancer",
    "Lung Cancer",
    "Breast Cancer",
    "Prostate Cancer",
    "Anemia",
    
    # Infectious
    "HIV/AIDS",
    "Tuberculosis",
    
    # Mental Health & Behavioral
    "Depressive Disorder",
    "Anxiety Disorder",
    "Bipolar Disorder",
    "Chronic Pain Syndrome",
    "Substance Use Disorder",
    
    # Endocrine
    "Cushing's Syndrome",
    "Addison's Disease",
]

# ============================================================================
# EXPANDED CATEGORY KEYWORDS (MASSIVELY ENHANCED)
# ============================================================================
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Type 1 Diabetes Mellitus": [
        "type 1 diabetes", "t1dm", "juvenile diabetes", "insulin dependent",
        "autoimmune diabetes", "beta cells", "pancreatic failure", "ketone bodies",
        "diabetic ketoacidosis", "dka", "insulin pump", "continuous glucose monitor",
        "cgm", "carbohydrate counting", "basal bolus", "insulin pen", "insulin vial"
    ],
    "Type 2 Diabetes Mellitus": [
        "type 2 diabetes", "t2dm", "adult onset diabetes", "non-insulin dependent",
        "insulin resistance", "metformin", "sulfonylurea", "glipitin", "glp-1",
        "sglt2 inhibitor", "diabetes reversal", "remission", "prediabetes",
        "impaired fasting glucose", "impaired glucose tolerance"
    ],
    "Gestational Diabetes": [
        "gestational diabetes", "gdm", "pregnancy diabetes", "glucose tolerance test",
        "gtt", "oral glucose tolerance test", "ogtt", "pregnant with diabetes",
        "postpartum glucose", "fetal macrosomia", "preeclampsia risk", "neonatal hypoglycemia"
    ],
    "Metabolic Syndrome": [
        "metabolic syndrome", "insulin resistance syndrome", "syndrome x",
        "central obesity", "visceral fat", "triglycerides", "hdl cholesterol",
        "fasting glucose", "blood pressure elevation", "metabolic triad"
    ],
    "Thyroid Disorders": [
        "thyroid", "hypothyroidism", "hyperthyroidism", "graves disease",
        "hashimoto thyroiditis", "tsh", "t3", "t4", "thyroid hormone",
        "levothyroxine", "propylthiouracil", "methimazole", "thyroid nodule",
        "thyroid cancer", "goiter", "thyroiditis", "thyroid stimulating hormone"
    ],
    "Hyperlipidemia": [
        "hyperlipidemia", "dyslipidemia", "high cholesterol", "ldl cholesterol",
        "hdl cholesterol", "triglyceride", "familial hypercholesterolemia",
        "statin", "lipid profile", "cholesterol medication", "atorvastatin",
        "rosuvastatin", "pravastatin", "ezetimibe", "pcsk9 inhibitor"
    ],
    "Hypertension": [
        "hypertension", "high blood pressure", "hbp", "systolic pressure",
        "diastolic pressure", "blood pressure control", "ace inhibitor",
        "angiotensin receptor blocker", "arb", "beta blocker", "calcium channel blocker",
        "diuretic", "thiazide", "home blood pressure monitoring", "blood pressure cuff",
        "ambulatory blood pressure monitoring", "resistant hypertension", "white coat hypertension"
    ],
    "Coronary Artery Disease": [
        "coronary artery disease", "cad", "heart disease", "ischemic heart disease",
        "angina pectoris", "stable angina", "unstable angina", "myocardial infarction",
        "heart attack", "stent", "coronary angiography", "cardiac catheterization",
        "troponin", "ecg changes", "chest pain", "cardiac biomarkers", "aspirin",
        "clopidogrel", "statins", "beta blockers", "nitrates", "ischemia"
    ],
    "Heart Failure": [
        "heart failure", "chf", "congestive heart failure", "systolic heart failure",
        "diastolic heart failure", "hfpef", "hfref", "ejection fraction", "lvef",
        "ace inhibitors", "arb", "beta blockers", "diuretics", "digoxin",
        "aldosterone antagonist", "sacubitril", "valsartan", "heart failure classification",
        "new york heart association", "nyha", "dyspnea", "orthopnea", "paroxysmal nocturnal dyspnea",
        "pnd", "peripheral edema", "pulmonary edema", "cardiomegaly"
    ],
    "Atrial Fibrillation": [
        "atrial fibrillation", "afib", "af", "arrhythmia", "irregular heartbeat",
        "palpitations", "rapid heart rate", "tachycardia", "stroke risk",
        "anticoagulation", "warfarin", "dabigatran", "rivaroxaban", "apixaban",
        "edoxaban", "direct oral anticoagulant", "doac", "rate control",
        "rhythm control", "rate control strategy", "cardioversion", "ablation"
    ],
    "Peripheral Arterial Disease": [
        "peripheral arterial disease", "pad", "peripheral vascular disease",
        "pvd", "intermittent claudication", "critical limb ischemia", "rest pain",
        "lower extremity ischemia", "ankle brachial index", "abi", "duplex ultrasound",
        "ct angiography", "angiography", "revascularization", "amputation risk"
    ],
    "Stroke": [
        "stroke", "cerebrovascular accident", "cva", "brain attack",
        "ischemic stroke", "hemorrhagic stroke", "transient ischemic attack",
        "tia", "mini stroke", "thrombolysis", "tpa", "alteplase",
        "thrombectomy", "clot retrieval", "aphasia", "dysarthria",
        "hemiplegia", "hemiparesis", "speech therapy", "physical therapy"
    ],
    "Transient Ischemic Attack": [
        "transient ischemic attack", "tia", "mini stroke", "amaurosis fugax",
        "monocular vision loss", "tia symptoms", "tia risk factors",
        "carotid stenosis", "vertebrobasilar insufficiency", "secondary stroke prevention"
    ],
    "Aortic Aneurysm": [
        "aortic aneurysm", "abdominal aortic aneurysm", "aaa", "thoracic aortic aneurysm",
        "taa", "aortic dissection", "aneurysm rupture", "aortic screening",
        "aortic diameter", "ct angiography", "endovascular repair", "evar",
        "open surgical repair", "aortic replacement", "abdominal pain"
    ],
    "Venous Thromboembolism": [
        "venous thromboembolism", "vte", "deep vein thrombosis", "dvt",
        "pulmonary embolism", "pe", "blood clot", "anticoagulation",
        "warfarin", "heparin", "low molecular weight heparin", "lmwh",
        "unfractionated heparin", "fondaparinux", "doac", "ischemic event"
    ],
    "Myocarditis": [
        "myocarditis", "inflammation of heart muscle", "viral myocarditis",
        "autoimmune myocarditis", "chest pain", "troponin elevation",
        "echocardiography", "cardiac mri", "heart failure symptoms",
        "arrhythmias", "fulminant myocarditis", "recovery"
    ],
    "Pericarditis": [
        "pericarditis", "pericardial inflammation", "pericardial effusion",
        "tamponade", "constrictive pericarditis", "pleuritic chest pain",
        "pericardial friction rub", "echocardiography findings",
        "pericardiocentesis", "anti-inflammatory therapy"
    ],
    "Cardiomyopathy": [
        "cardiomyopathy", "dilated cardiomyopathy", "dcm", "hypertrophic cardiomyopathy",
        "hcm", "restrictive cardiomyopathy", "takotsubo cardiomyopathy",
        "stress cardiomyopathy", "peripartum cardiomyopathy", "ejection fraction",
        "systolic dysfunction", "diastolic dysfunction", "sudden cardiac death"
    ],
    "Asthma": [
        "asthma", "bronchial asthma", "reactive airway disease", "wheezing",
        "shortness of breath", "dyspnea", "asthma attack", "asthma exacerbation",
        "inhaler technique", "albuterol", "salbutamol", "inhaled corticosteroids",
        "laba", "ltra", "omalizumab", "biologic therapy", "peak flow",
        "peak expiratory flow", "pef", "spirometry", "fev1", "trigger avoidance"
    ],
    "Chronic Obstructive Pulmonary Disease": [
        "copd", "chronic obstructive pulmonary disease", "emphysema",
        "chronic bronchitis", "smoking related lung disease", "airflow obstruction",
        "fev1", "spirometry", "bronchodilator", "albuterol", "tiotropium",
        "ipratropium", "combination inhalers", "roflumilast", "theophylline",
        "oxygen therapy", "pulmonary rehabilitation", "smoking cessation"
    ],
    "Interstitial Lung Disease": [
        "interstitial lung disease", "ild", "pulmonary fibrosis",
        "idiopathic pulmonary fibrosis", "ipf", "sarcoidosis",
        "hypersensitivity pneumonitis", "occupational lung disease",
        "asbestosis", "silicosis", "high resolution ct", "hrct",
        "honeycombing", "ground glass opacities", "pirfenidone", "nintedanib"
    ],
    "Pulmonary Hypertension": [
        "pulmonary hypertension", "ph", "pulmonary artery pressure",
        "right ventricular dysfunction", "right heart failure",
        "idiopathic pulmonary arterial hypertension", "ipah",
        "connective tissue disease associated ph", "chronic thromboembolic ph",
        "phosphodiesterase inhibitor", "endothelin receptor antagonist",
        "prostacyclin analogue", "treprostinil", "epoprostenol"
    ],
    "Cystic Fibrosis": [
        "cystic fibrosis", "cf", "cftr gene mutation",
        "pancreatic insufficiency", "cf related diabetes", "cfrd",
        "meconium ileus", "pancreatic enzyme replacement",
        "vest", "airway clearance devices", "hypertonic saline",
        "dornase alfa", "ivacaftor", "lumacaftor", "tezacaftor",
        "elexacaftor", "lung transplant candidacy"
    ],
    "Sleep Apnea": [
        "sleep apnea", "obstructive sleep apnea", "osa", "central sleep apnea",
        "csa", "sleep disordered breathing", "apnea hypopnea index", "ahi",
        "continuous positive airway pressure", "cpap", "bipap",
        "auto-titrating cpap", "autpap", "sleep study", "polysomnography",
        "daytime somnolence", "apneic episodes", "oxygen desaturation"
    ],
    "Bronchiectasis": [
        "bronchiectasis", "chronic lung infection", "bronchial dilation",
        "pseudomonas aeruginosa", "chronic sputum production",
        "hemoptysis", "recurrent pneumonia", "airway clearance",
        "oscillatory positive expiratory pressure", "opep", "high resolution ct",
        "bronchial artery embolization", "lung transplant"
    ],
    "Idiopathic Pulmonary Fibrosis": [
        "idiopathic pulmonary fibrosis", "ipf", "progressive fibrosis",
        "usual interstitial pneumonia", "uip pattern", "honeycombing",
        "traction bronchiectasis", "forced vital capacity", "fvc",
        "dlco", "pirfenidone", "nintedanib", "lung transplant", "prognosis"
    ],
    "Chronic Kidney Disease": [
        "chronic kidney disease", "ckd", "renal disease", "kidney disease",
        "glomerular filtration rate", "gfr", "estimated gfr", "egfr",
        "serum creatinine", "blood urea nitrogen", "bun", "proteinuria",
        "albuminuria", "ckd stages", "kidney function decline",
        "angiotensin converting enzyme inhibitor", "ace inhibitor",
        "angiotensin receptor blocker", "arb", "renin-angiotensin system blockade"
    ],
    "End-Stage Renal Disease": [
        "end stage renal disease", "esrd", "stage 5 ckd", "kidney failure",
        "dialysis", "hemodialysis", "peritoneal dialysis", "pdialysis",
        "arteriovenous fistula", "vascular access", "transplant", "immunosuppression",
        "kidney transplant rejection", "transplant survival", "graft function"
    ],
    "Diabetic Nephropathy": [
        "diabetic nephropathy", "diabetes related kidney disease",
        "diabetic kidney disease", "dkd", "albuminuria", "proteinuria",
        "microalbuminuria", "macroalbuminuria", "glomerular basement membrane",
        "nodular glomerulosclerosis", "kimmelstiel wilson lesion",
        "podocyte dysfunction", "glomerular filtration barrier"
    ],
    "Glomerulonephritis": [
        "glomerulonephritis", "igA nephropathy", "post infectious",
        "membranoproliferative", "mpgn", "focal segmental glomerulosclerosis",
        "fsgs", "membranous nephropathy", "minimal change disease",
        "mcd", "lupus nephritis", "kidney biopsy", "immunosuppressive therapy"
    ],
    "Polycystic Kidney Disease": [
        "polycystic kidney disease", "pkd", "autosomal dominant pkd",
        "adpkd", "autosomal recessive pkd", "arpkd", "multiple kidney cysts",
        "cyst rupture", "hematuria", "flank pain", "hypertension",
        "rapid decline in gfr", "tolvaptan", "kidney replacement therapy"
    ],
    "Chronic Urinary Tract Infections": [
        "chronic urinary tract infection", "uti", "recurrent uti",
        "bacteriuria", "urinary bacteria", "urine culture",
        "dysuria", "urinary frequency", "urinary urgency", "catheter associated uti",
        "cauti", "prophylactic antibiotics", "antibiotic resistance",
        "nitrofurantoin", "trimethoprim sulfamethoxazole"
    ],
    "Osteoarthritis": [
        "osteoarthritis", "oa", "degenerative joint disease",
        "joint degeneration", "cartilage loss", "bone spur", "osteophyte",
        "joint stiffness", "joint pain", "crepitus", "joint swelling",
        "nonsteroidal anti-inflammatory drug", "nsaid", "acetaminophen",
        "intra-articular injection", "hyaluronic acid", "corticosteroid injection"
    ],
    "Rheumatoid Arthritis": [
        "rheumatoid arthritis", "ra", "inflammatory arthritis",
        "rheumatoid factor", "anti-cyclic citrullinated peptide", "anti-ccp",
        "inflammatory cytokines", "disease modifying antirheumatic drug", "dmard",
        "methotrexate", "tumor necrosis factor", "tnf", "tnf inhibitor",
        "abatacept", "rituximab", "joint erosion", "joint destruction"
    ],
    "Systemic Lupus Erythematosus": [
        "systemic lupus erythematosus", "sle", "lupus", "butterfly rash",
        "malar rash", "discoid rash", "photosensitivity", "oral ulcer",
        "anti-nuclear antibody", "ana", "anti-dsdna antibody",
        "anti-smith antibody", "lupus nephritis", "hydroxychloroquine",
        "azathioprine", "cyclophosphamide", "mycophenolate mofetil"
    ],
    "Gout": [
        "gout", "gouty arthritis", "acute gout attack", "uric acid",
        "hyperuricemia", "urate deposition", "monosodium urate crystal",
        "crystal induced arthritis", "tophus", "gout flare", "acute flare",
        "allopurinol", "febuxostat", "uricosuric agents", "probenecid",
        "colchicine", "nsaid", "indomethacin"
    ],
    "Osteoporosis": [
        "osteoporosis", "bone loss", "low bone density", "t-score",
        "z-score", "dual-energy x-ray absorptiometry", "dexa", "bone mineral density",
        "bmd", "fracture risk", "osteoporotic fracture", "vertebral fracture",
        "hip fracture", "wrist fracture", "bisphosphonate", "alendronate",
        "risedronate", "zoledronic acid", "denosumab", "teriparatide"
    ],
    "Ankylosing Spondylitis": [
        "ankylosing spondylitis", "as", "axial spondyloarthritis",
        "human leukocyte antigen b27", "hla b27", "axial arthritis",
        "sacroiliitis", "spinal fusion", "bamboo spine", "inflammatory back pain",
        "morning stiffness", "enthesitis", "tnf inhibitor", "il-17 inhibitor"
    ],
    "Fibromyalgia": [
        "fibromyalgia", "fm", "widespread pain", "tender points",
        "myofascial pain", "chronic pain syndrome", "central sensitization",
        "fatigue", "sleep disturbance", "cognitive dysfunction", "brain fog",
        "pregabalin", "duloxetine", "milnacipran", "low dose naltrexone",
        "cognitive behavioral therapy", "graded exercise therapy"
    ],
    "Parkinson's Disease": [
        "parkinson disease", "parkinson's", "parkinsonian", "tremor",
        "resting tremor", "bradykinesia", "rigidity", "postural instability",
        "levodopa", "carbidopa", "dopamine agonist", "monoamine oxidase inhibitor",
        "maoi", "deep brain stimulation", "dbs", "motor fluctuations",
        "dyskinesia", "on-off phenomena", "neurodegenerative"
    ],
    "Alzheimer's Disease": [
        "alzheimer disease", "alzheimer's", "dementia", "neurodegenerative dementia",
        "cognitive decline", "memory loss", "amnestic dementia", "amyloid beta",
        "tau pathology", "neuritic plaques", "neurofibrillary tangles",
        "aducanumab", "donepezil", "rivastigmine", "galantamine",
        "memantine", "behavioral symptoms", "caregiver burden"
    ],
    "Multiple Sclerosis": [
        "multiple sclerosis", "ms", "relapsing remitting", "rrms",
        "secondary progressive", "spms", "primary progressive", "ppms",
        "progressive relapsing", "prms", "demyelinating disease",
        "white matter lesion", "optic neuritis", "transverse myelitis",
        "disease modifying therapy", "dmt", "interferon beta",
        "glatiramer acetate", "natalizumab", "fingolimod"
    ],
    "Epilepsy": [
        "epilepsy", "seizure disorder", "seizure", "convulsion",
        "generalized seizure", "focal seizure", "tonic clonic", "absence seizure",
        "status epilepticus", "seizure threshold", "antiepileptic drug", "aed",
        "valproate", "levetiracetam", "lamotrigine", "phenytoin",
        "carbamazepine", "seizure trigger", "seizure management"
    ],
    "Migraine Disorder": [
        "migraine", "migraine disorder", "migraine with aura", "migraine without aura",
        "chronic migraine", "episodic migraine", "hemiplegic migraine",
        "migraine with brainstem aura", "status migrainosus",
        "tension headache", "triptan", "sumatriptan", "ergotamine",
        "prophylactic therapy", "propranolol", "topiramate", "botulinum toxin"
    ],
    "Peripheral Neuropathy": [
        "peripheral neuropathy", "diabetic neuropathy", "sensory neuropathy",
        "motor neuropathy", "sensorimotor neuropathy", "distal symmetrical",
        "paresthesia", "numbness", "tingling", "nerve conduction study",
        "electromyography", "emg", "nerve biopsy", "small fiber neuropathy",
        "gabapentin", "pregabalin", "duloxetine", "alpha lipoic acid"
    ],
    "Non-Alcoholic Fatty Liver Disease": [
        "non-alcoholic fatty liver disease", "nafld", "fatty liver", "liver steatosis",
        "hepatic steatosis", "simple steatosis", "non-alcoholic steatohepatitis",
        "nash", "liver fibrosis", "liver cirrhosis", "hepatocellular carcinoma",
        "hcc", "transient elastography", "fibroscan", "liver biopsy",
        "pioglitazone", "vitamin e", "weight loss"
    ],
    "Hepatitis C": [
        "hepatitis c", "hcv", "hepatitis c virus", "viral hepatitis",
        "chronic hepatitis c", "acute hepatitis c", "cirrhosis",
        "hepatocellular carcinoma", "hcc", "hepatitis c antibody",
        "hcv rna", "direct-acting antiviral", "daa", "sofosbuvir",
        "ledipasvir", "harvoni", "cure rate", "sustained virologic response", "svr"
    ],
    "Cirrhosis": [
        "cirrhosis", "hepatic cirrhosis", "end-stage liver disease",
        "esld", "decompensated cirrhosis", "compensated cirrhosis",
        "portal hypertension", "ascites", "variceal bleeding",
        "hepatic encephalopathy", "hepatorenal syndrome",
        "liver transplant", "model for end-stage liver disease", "meld score"
    ],
    "Inflammatory Bowel Disease": [
        "inflammatory bowel disease", "ibd", "crohn disease", "ulcerative colitis",
        "uc", "colitis", "enteritis", "mucosal inflammation",
        "diarrhea", "abdominal pain", "blood in stool", "weight loss",
        "corticosteroid", "immunosuppressant", "tnf inhibitor",
        "aminosalicylate", "5-asa", "intestinal resection"
    ],
    "Celiac Disease": [
        "celiac disease", "celiac sprue", "gluten sensitive enteropathy",
        "gse", "tissue transglutaminase", "ttg", "tissue transglutaminase antibody",
        "ttg-iga", "endomysial antibody", "ema", "intestinal villous atrophy",
        "malabsorption", "gluten free diet", "dermatitis herpetiformis",
        "primary biliary cholangitis", "pbc"
    ],
    "Gastroesophageal Reflux Disease": [
        "gastroesophageal reflux disease", "gerd", "acid reflux", "heartburn",
        "regurgitation", "erosive esophagitis", "barrett esophagus",
        "esophageal adenocarcinoma", "proton pump inhibitor", "ppi",
        "omeprazole", "lansoprazole", "pantoprazole", "h2 receptor antagonist",
        "h2 blocker", "ranitidine", "antacid", "lifestyle modification"
    ],
    "Colorectal Cancer": [
        "colorectal cancer", "colon cancer", "rectal cancer", "bowel cancer",
        "crc", "adenocarcinoma", "tumor stage", "tnm staging",
        "metastatic disease", "chemotherapy", "5-fluorouracil", "5-fu",
        "oxaliplatin", "irinotecan", "bevacizumab", "cetuximab",
        "microsatellite instability", "msi", "mismatch repair", "mmr"
    ],
    "Lung Cancer": [
        "lung cancer", "non-small cell lung cancer", "nsclc",
        "small cell lung cancer", "sclc", "adenocarcinoma", "squamous cell",
        "large cell carcinoma", "tobacco smoking", "secondhand smoke",
        "radon exposure", "chemotherapy", "targeted therapy",
        "epidermal growth factor receptor", "egfr", "anaplastic lymphoma kinase", "alk"
    ],
    "Breast Cancer": [
        "breast cancer", "invasive ductal carcinoma", "idc",
        "invasive lobular carcinoma", "ilc", "ductal carcinoma in situ", "dcis",
        "lobular carcinoma in situ", "lcis", "estrogen receptor", "er",
        "progesterone receptor", "pr", "human epidermal growth factor receptor 2", "her2",
        "hormone therapy", "tamoxifen", "aromatase inhibitor", "trastuzumab"
    ],
    "Prostate Cancer": [
        "prostate cancer", "adenocarcinoma of prostate", "gleason score",
        "prostate specific antigen", "psa", "digital rectal exam", "dre",
        "metastatic prostate cancer", "bone metastasis", "hormone therapy",
        "androgen deprivation therapy", "adt", "gonadotropin releasing hormone", "gnrh",
        "chemotherapy", "immunotherapy", "external beam radiation"
    ],
    "Anemia": [
        "anemia", "iron deficiency anemia", "ida", "hemoglobin",
        "hematocrit", "red blood cell", "rbc", "microcytic anemia",
        "macrocytic anemia", "normocytic anemia", "hemolytic anemia",
        "aplastic anemia", "pernicious anemia", "vitamin b12 deficiency",
        "folate deficiency", "erythropoietin", "epo", "iron supplementation"
    ],
    "HIV/AIDS": [
        "hiv", "aids", "human immunodeficiency virus",
        "acquired immunodeficiency syndrome", "cd4 count", "viral load",
        "hiv rna", "antiretroviral therapy", "art",
        "nucleoside reverse transcriptase inhibitor", "nrti",
        "non-nucleoside reverse transcriptase inhibitor", "nnrti",
        "protease inhibitor", "pi", "integrase inhibitor",
        "opportunistic infection", "ooi", "pneumocystis pneumonia", "pcp"
    ],
    "Tuberculosis": [
        "tuberculosis", "tb", "mycobacterium tuberculosis",
        "pulmonary tuberculosis", "extrapulmonary tuberculosis",
        "latent tuberculosis infection", "ltbi", "active tuberculosis",
        "tb meningitis", "tb lymphadenitis", "isoniazid", "rifampicin",
        "rifampin", "pyrazinamide", "ethambutol", "multidrug resistant",
        "mdr-tb", "extensively drug resistant", "xdr-tb"
    ],
    "Depressive Disorder": [
        "major depressive disorder", "mdd", "depression", "depressive episode",
        "persistent depressive disorder", "dysthymia", "seasonal affective disorder",
        "sad", "bipolar disorder", "major depression", "clinical depression",
        "antidepressant", "selective serotonin reuptake inhibitor", "ssri",
        "serotonin norepinephrine reuptake inhibitor", "snri", "tricyclic antidepressant",
        "cognitive behavioral therapy", "cbt", "electroconvulsive therapy", "ect"
    ],
    "Anxiety Disorder": [
        "anxiety disorder", "generalized anxiety disorder", "gad",
        "social anxiety disorder", "panic disorder", "panic attack",
        "agoraphobia", "specific phobia", "separation anxiety",
        "anxiolytic", "benzodiazepine", "buspirone", "hydroxyzine",
        "selective serotonin reuptake inhibitor", "ssri", "exposure therapy",
        "cognitive behavioral therapy", "cbt", "relaxation technique"
    ],
    "Bipolar Disorder": [
        "bipolar disorder", "bipolar i disorder", "bipolar ii disorder",
        "cyclothymia", "manic episode", "hypomanic episode",
        "depressive episode", "mixed episode", "mood stabilizer",
        "lithium", "valproate", "carbamazepine", "lamotrigine",
        "antipsychotic", "atypical antipsychotic", "quetiapine",
        "olanzapine", "mood disorder", "mood cycling"
    ],
    "Chronic Pain Syndrome": [
        "chronic pain syndrome", "chronic pain", "central sensitization",
        "widespread pain", "pain amplification", "nociceptive pain",
        "neuropathic pain", "nociplastic pain", "pain catastrophizing",
        "pain medication", "opioid", "analgesic", "nonsteroidal anti-inflammatory drug",
        "nsaid", "pain rehabilitation", "interdisciplinary pain management"
    ],
    "Substance Use Disorder": [
        "substance use disorder", "sud", "alcohol use disorder",
        "aud", "drug addiction", "opioid use disorder", "oud",
        "cannabis use disorder", "cocaine addiction", "methamphetamine addiction",
        "medication assisted treatment", "mat", "methadone", "buprenorphine",
        "naltrexone", "withdrawal syndrome", "detoxification", "rehabilitation"
    ],
    "Cushing's Syndrome": [
        "cushing syndrome", "hypercortisolism", "excessive cortisol",
        "adrenocorticotropic hormone", "acth", "pituitary adenoma",
        "adrenal tumor", "adrenal adenoma", "adrenal carcinoma",
        "ectopic acth", "24-hour urine cortisol", "dexamethasone suppression test",
        "dst", "cortisol level", "central obesity", "buffalo hump",
        "purple striae", "easy bruising"
    ],
    "Addison's Disease": [
        "addison disease", "primary adrenal insufficiency",
        "adrenal insufficiency", "hypoadrenalism", "low cortisol",
        "autoimmune adrenalitis", "hyperpigmentation", "adrenal crisis",
        "adrenal shock", "corticosteroid replacement", "glucocorticoid",
        "mineralocorticoid", "fludrocortisone", "fatigue", "weight loss",
        "hypotension", "hyponatremia", "hyperkalemia"
    ],
}

# ============================================================================
# MASSIVELY EXPANDED DIVERSITY MATRIX
# ============================================================================

CONDITIONS = [
    # Metabolic
    "Type 1 Diabetes", "Type 2 Diabetes", "Gestational Diabetes",
    "Pre-diabetes", "Metabolic Syndrome", "Thyroid Disorder",
    "Hypercholesterolemia",
    
    # Cardiovascular
    "Hypertension", "Heart Failure", "Coronary Artery Disease",
    "Atrial Fibrillation", "Post-Stroke Recovery", "Peripheral Artery Disease",
    "Angina", "Aortic Aneurysm", "Deep Vein Thrombosis",
    "Pulmonary Embolism", "Cardiomyopathy",
    
    # Respiratory
    "COPD", "Asthma", "Interstitial Lung Disease", "Sleep Apnea",
    "Bronchiectasis", "Post-COVID Lung Issues", "Pulmonary Hypertension",
    "Cystic Fibrosis",
    
    # Renal
    "CKD Stage 1", "CKD Stage 5", "Diabetic Nephropathy",
    "Chronic UTI", "Polycystic Kidney Disease", "Glomerulonephritis",
    
    # Musculoskeletal
    "Osteoarthritis", "Rheumatoid Arthritis", "Gout", "Osteoporosis",
    "Lupus", "Fibromyalgia", "Ankylosing Spondylitis",
    
    # Neurologic
    "Migraine", "Epilepsy", "Parkinson's Disease", "Multiple Sclerosis",
    "Dementia", "Peripheral Neuropathy", "Stroke Recovery",
    
    # GI/Hepatic
    "NAFLD", "Hepatitis C", "Cirrhosis", "IBD", "Celiac Disease", "GERD",
    
    # Oncologic
    "Colorectal Cancer", "Lung Cancer", "Breast Cancer",
    "Prostate Cancer", "Cancer Survivorship",
    
    # Hematologic
    "Anemia", "Sickle Cell",
    
    # Infectious
    "HIV Management", "Tuberculosis",
    
    # Mental Health
    "Depression", "Anxiety Disorder", "Bipolar Disorder",
    
    # Other
    "Chronic Pain", "Substance Use Disorder", "Cushing's Syndrome", "Addison's Disease"
]

PERSONAS = [
    # Age-based
    "a teenager (13-19) managing illness independently",
    "a young adult (20-30) newly diagnosed",
    "a parent (30-50) of young children",
    "a middle-aged professional (40-60) with multiple comorbidities",
    "an elderly person (65+) managing complex medications",
    "a very elderly person (80+) with limited mobility",
    "a centenarian (100+) managing multiple chronic conditions",
    
    # Occupation
    "a high-stress executive", "a night-shift nurse", "a construction worker",
    "a teacher in a classroom", "a healthcare worker",
    "an athlete/sports professional", "a musician on tour",
    "a chef/restaurant worker", "a farmer with seasonal stress",
    "a freelancer with irregular income", "a truck driver",
    "a factory worker with shift changes", "a surgeon with demanding schedule",
    "a pilot with regulatory restrictions", "a police officer",
    "a fitness trainer", "a software developer", "an artist",
    
    # Living situation
    "someone living alone in a rural area", "someone in a shared apartment",
    "someone homeless or housing-insecure", "someone in a care home",
    "someone living with extended family", "someone in a dorm",
    "someone with a caregiver/family support", "someone in transitional housing",
    "someone in a shelter", "someone with unstable housing",
    
    # Lifestyle
    "a fitness enthusiast/gym-goer", "a sedentary office worker",
    "a vegan/vegetarian with allergies", "someone with food allergies",
    "a frequent international traveler", "someone unable to afford medications",
    "someone with limited internet access", "a tech-savvy digital nomad",
    "a person with limited education/health literacy", "someone dealing with substance use history",
    "a recovering addict in treatment", "someone newly sober",
    
    # Family status
    "a pregnant woman with chronic illness", "a new mother with postpartum complications",
    "a caregiver for another chronic patient", "someone recently bereaved",
    "someone recovering from surgery", "someone with mental health comorbidity",
    "an immigrant with language barriers", "someone in financial stress",
    "a person recently retired", "someone with a new diagnosis",
    "a student balancing studies and health", "a single parent",
    "someone with a supportive partner", "a competitive athlete",
    "a parent of a child with chronic illness", "someone in an unhappy relationship",
    "someone with excellent family support", "a caregiver experiencing burnout",
]

TOPICS = [
    # Nutrition
    "carbohydrate counting for diabetes", "DASH diet implementation",
    "Mediterranean diet benefits", "salt reduction strategies",
    "meal prep and batch cooking", "reading food labels",
    "managing cravings and emotional eating", "intermittent fasting safety",
    "ketogenic diet risks/benefits", "vegetarian/vegan protein sources",
    "managing hunger while losing weight", "restaurant meal choices",
    "grocery shopping on a budget", "hydration and fluid management",
    "caffeine and stimulant intake", "alcohol interactions with medications",
    "managing portion sizes at home", "food safety with weakened immunity",
    "high fiber diet for digestive health", "low sodium cooking",
    "managing weight during medication use", "nutritional supplements",
    
    # Exercise & Activity
    "starting an exercise program from zero", "safe exercise intensity zones",
    "resistance training with limited mobility", "aquatic therapy",
    "yoga and flexibility for stiffness", "high-altitude exercise risks",
    "exercise in extreme weather", "preventing exercise-related injuries",
    "recovery and rest days", "staying active during flare-ups",
    "home exercises without equipment", "group fitness classes",
    "walking programs", "fall prevention and balance",
    "stretching routines for pain relief", "building core strength safely",
    
    # Medication Management
    "understanding drug interactions", "managing medication side effects",
    "remembering to take multiple medications", "using pill organizers/reminders",
    "buying generic vs. brand medications", "medication costs and insurance",
    "stopping medications safely", "adjusting doses during illness",
    "medication storage and expiration", "medication during pregnancy",
    "interactions with supplements/herbs", "timing of medication doses",
    "medication adherence challenges", "managing polypharmacy",
    
    # Mental Health & Coping
    "anxiety related to health condition", "depression from chronic illness",
    "health anxiety and excessive checking", "sleep problems and insomnia",
    "stress management techniques", "mindfulness and meditation",
    "counseling and therapy options", "managing social isolation",
    "coping with disease progression", "sexual health and intimacy",
    "grief and acceptance", "building resilience",
    "managing catastrophic thinking", "dealing with setbacks",
    
    # Monitoring & Self-Management
    "interpreting home glucose/BP/weight readings", "when to seek emergency care",
    "red flags specific to my condition", "tracking symptoms in a diary",
    "using wearable devices and apps", "recognizing early warning signs",
    "managing pain at home", "managing fatigue", "managing swelling/edema",
    "controlling cough and breathing issues", "managing nausea/vomiting",
    "home remedies and evidence-based care", "self-monitoring techniques",
    
    # Travel & Lifestyle
    "managing illness while traveling", "adjusting routine for work",
    "explaining my condition to family", "managing relationships with illness",
    "parenting while chronically ill", "school/university attendance",
    "dating and disclosure of illness", "driving safely with my condition",
    "workplace accommodations and rights", "financial planning with illness",
    "insurance and healthcare navigation", "accessing care in remote areas",
    
    # Seasonal & Environmental
    "managing during cold/flu season", "adjusting care in extreme heat",
    "managing in high humidity or air pollution", "altitude and travel",
    "seasonal mood changes", "managing during natural disasters",
    "vaccine safety with my condition", "managing during pandemics",
    "sun protection with my condition", "managing in cold weather",
    
    # Specific Clinical Topics
    "understanding my test results", "preparing for medical procedures",
    "managing before and after surgery", "post-hospitalization recovery",
    "managing chronic pain flare-ups", "recognizing infection signs",
    "managing low energy days", "optimizing sleep quality",
]

SETTINGS = [
    # Time-based
    "early morning routine", "nighttime/bedtime management",
    "shift work and irregular hours", "weekend vs. weekday routine",
    "seasonal changes", "holiday season management",
    "morning rush before work", "evening wind-down",
    
    # Location-based
    "at home alone", "in a hospital/clinic", "at work",
    "while traveling internationally", "in a rural/remote area",
    "in a refugee camp or temporary shelter", "on vacation",
    "at a social gathering/party", "at a restaurant/cafe",
    "at the gym or fitness facility", "outdoors in nature",
    "at a family gathering", "on public transportation",
    "in a car", "at the beach", "in the mountains",
    
    # Social contexts
    "with family present", "with romantic partner", "with friends",
    "at work with colleagues", "in public/with strangers",
    "while caregiving for someone else", "at a wedding",
    "at a funeral", "with healthcare provider", "alone",
    
    # Health crisis contexts
    "during symptom flare-up", "during extreme stress", "during grief",
    "during financial hardship", "during relationship conflict",
    "when accessing healthcare is difficult", "when medication is unavailable",
    "during a health crisis", "after receiving bad news",
    "after good news", "during medication shortage",
    "during insurance coverage gaps", "during pandemic",
]

COMORBIDITIES = [
    "no other conditions",
    "plus depression", "plus anxiety", "plus both depression and anxiety",
    "plus chronic pain", "plus sleep disorder",
    "plus another NCD", "plus multiple NCDs",
    "plus active infection/illness", "plus recent surgery",
    "plus substance use disorder history", "plus eating disorder history",
    "plus cognitive impairment", "plus mobility limitations",
    "plus hearing loss", "plus vision loss", "plus both hearing and vision loss",
    "plus arthritis", "plus asthma", "plus cancer history",
    "plus previous stroke", "plus heart disease",
]

RESOURCE_LEVEL = [
    "high income - unlimited resources",
    "upper middle income - good resources",
    "middle income - some financial constraints",
    "lower middle income - significant constraints",
    "low income - significant financial limitations",
    "very low income - severe limitations",
    "homeless or unstable housing",
    "refugee or displaced person",
    "income variable - freelancer/gig worker",
]

TECH_ACCESS = [
    "smartphone and internet access",
    "multiple devices and high-speed internet",
    "basic phone and limited internet",
    "smartphone only, spotty internet",
    "no smartphone, limited tech",
    "no reliable internet access",
    "access to library/community tech",
    "shared device access",
    "landline only",
]

HEALTH_LITERACY = [
    "high - understands medical terms",
    "high with medical background",
    "medium - some medical knowledge",
    "medium - learning gradually",
    "low - needs simple explanations",
    "very low - needs visual/oral explanations",
    "language barrier - non-native speaker",
    "cognitive limitation affecting understanding",
]

MOTIVATION = [
    "highly motivated - wants perfect compliance",
    "very motivated - trying hard",
    "moderately motivated - trying to do best",
    "inconsistently motivated - on and off",
    "low motivation - struggling with adherence",
    "no motivation - feeling hopeless",
    "newly diagnosed - still in denial phase",
    "overwhelmed - confused about priorities",
    "burned out from disease management",
]

CULTURAL_CONTEXT = [
    "English-speaking, Western culture",
    "Turkish culture and values",
    "Arabic/Islamic culture",
    "South Asian culture",
    "East Asian culture",
    "Southeast Asian culture",
    "African culture and context",
    "Latin American culture",
    "Caribbean culture",
    "Indigenous/Traditional medicine beliefs",
    "Immigrant with culture transition challenges",
    "Multi-cultural household",
    "Traditional medicine preference",
    "Western medicine skeptical background",
]

# ============================================================================
# EXPANDED DETAILS BY CATEGORY
# ============================================================================

DETAILS_BY_CATEGORY = {
    "Type 1 Diabetes Mellitus": [
        "insulin dosing", "carbohydrate counting", "glucose monitoring",
        "hypoglycemia prevention", "ketone body management", "pump therapy",
        "continuous glucose monitoring", "insulin pen technique"
    ],
    "Type 2 Diabetes Mellitus": [
        "medication selection", "metformin dosing", "blood sugar targets",
        "weight loss strategies", "exercise benefits", "remission potential",
        "medication interactions", "lifestyle modification"
    ],
    "Gestational Diabetes": [
        "glucose monitoring during pregnancy", "dietary management",
        "fetal monitoring", "delivery planning", "postpartum glucose testing",
        "breastfeeding considerations", "lifestyle modifications"
    ],
    "Metabolic Syndrome": [
        "waist circumference reduction", "triglyceride management",
        "hdl increase", "blood pressure control", "glucose management",
        "metabolic rate optimization"
    ],
    "Thyroid Disorders": [
        "hormone replacement", "tsh monitoring", "medication timing",
        "symptom management", "dietary iodine", "medication interactions",
        "radioactive iodine therapy"
    ],
    "Hyperlipidemia": [
        "statin therapy", "ldl targets", "triglyceride reduction",
        "hdl improvement", "dietary modifications", "medication adherence",
        "side effect management"
    ],
    "Hypertension": [
        "home monitoring", "sodium restriction", "medication timing",
        "lifestyle changes", "stress reduction", "regular check-ups",
        "medication combinations"
    ],
    "Coronary Artery Disease": [
        "chest pain management", "exercise guidelines", "medication adherence",
        "stress reduction", "risk factor modification", "cardiac rehabilitation",
        "medication timing"
    ],
    "Heart Failure": [
        "fluid restriction", "salt reduction", "medication adherence",
        "exercise tolerance", "weight monitoring", "daily tracking",
        "symptom recognition"
    ],
    "Atrial Fibrillation": [
        "heart rate control", "rhythm management", "anticoagulation",
        "medication adherence", "trigger avoidance", "emergency planning",
        "stroke risk management"
    ],
    "Peripheral Arterial Disease": [
        "walking program", "leg pain management", "wound care",
        "smoking cessation", "medication adherence", "foot monitoring",
        "revascularization options"
    ],
    "Stroke": [
        "speech therapy", "physical rehabilitation", "medication adherence",
        "blood clot prevention", "recovery milestones", "fall prevention",
        "cognitive rehabilitation"
    ],
    "Transient Ischemic Attack": [
        "prevention strategies", "medication adherence", "risk factor management",
        "carotid monitoring", "lifestyle modifications", "emergency recognition"
    ],
    "Aortic Aneurysm": [
        "monitoring schedule", "size tracking", "activity restrictions",
        "symptom recognition", "emergency planning", "surgery decision",
        "post-operative recovery"
    ],
    "Venous Thromboembolism": [
        "anticoagulation management", "bleeding risk", "medication adherence",
        "compression therapy", "mobility improvement", "clot prevention",
        "monitoring duration"
    ],
    "Myocarditis": [
        "activity restriction", "cardiac monitoring", "medication use",
        "symptom recognition", "recovery timeline", "return to activity",
        "follow-up imaging"
    ],
    "Pericarditis": [
        "pain management", "inflammation control", "fluid monitoring",
        "activity restriction", "recurrence prevention", "medication timing",
        "follow-up assessment"
    ],
    "Cardiomyopathy": [
        "ejection fraction monitoring", "medication management",
        "activity limitations", "device consideration", "transplant options",
        "heart rate control", "fluid management"
    ],
    "Asthma": [
        "inhaler technique", "trigger identification", "peak flow monitoring",
        "medication adherence", "action plan", "exercise safety",
        "emergency management"
    ],
    "Chronic Obstructive Pulmonary Disease": [
        "breathing techniques", "oxygen therapy", "medication adherence",
        "exercise tolerance", "infection prevention", "pulmonary rehabilitation",
        "exacerbation management"
    ],
    "Interstitial Lung Disease": [
        "breathing exercise", "oxygen use", "medication timing",
        "disease progression", "activity tolerance", "symptom tracking",
        "transplant consideration"
    ],
    "Pulmonary Hypertension": [
        "exercise tolerance", "oxygen saturation", "medication management",
        "activity pacing", "right heart assessment", "medication side effects",
        "disease progression"
    ],
    "Cystic Fibrosis": [
        "airway clearance", "enzyme replacement", "nutrition management",
        "diabetes monitoring", "infection prevention", "lung function",
        "gene therapy options"
    ],
    "Sleep Apnea": [
        "cpap use", "mask fitting", "equipment cleaning",
        "sleep environment", "positional therapy", "weight management",
        "symptom improvement"
    ],
    "Bronchiectasis": [
        "airway clearance techniques", "infection management",
        "sputum production", "exercise tolerance", "medication adherence",
        "hemoptysis management", "transplant consideration"
    ],
    "Idiopathic Pulmonary Fibrosis": [
        "disease progression", "lung function monitoring", "oxygen needs",
        "medication timing", "activity tolerance", "palliative care",
        "transplant timeline"
    ],
    "Chronic Kidney Disease": [
        "gfr monitoring", "blood pressure control", "protein intake",
        "sodium restriction", "potassium management", "medication adherence",
        "progression prevention"
    ],
    "End-Stage Renal Disease": [
        "dialysis schedule", "access care", "medication management",
        "fluid restriction", "nutrition planning", "transplant preparation",
        "quality of life"
    ],
    "Diabetic Nephropathy": [
        "glucose control", "blood pressure targets", "protein restriction",
        "medication adherence", "gfr monitoring", "proteinuria reduction",
        "progression slowing"
    ],
    "Glomerulonephritis": [
        "immunosuppressive therapy", "blood pressure control",
        "protein monitoring", "kidney function", "medication side effects",
        "disease remission", "relapse prevention"
    ],
    "Polycystic Kidney Disease": [
        "blood pressure control", "pain management", "progression monitoring",
        "cyst monitoring", "infection recognition", "transplant timeline",
        "genetic counseling"
    ],
    "Chronic Urinary Tract Infections": [
        "prophylactic therapy", "hydration management", "urine cultures",
        "antibiotic resistance", "symptom monitoring", "prevention strategies",
        "treatment protocols"
    ],
    "Osteoarthritis": [
        "pain management", "joint protection", "weight management",
        "exercise programs", "medication use", "joint replacement",
        "mobility optimization"
    ],
    "Rheumatoid Arthritis": [
        "inflammation control", "medication adherence", "joint protection",
        "exercise routine", "fatigue management", "remission targets",
        "disease monitoring"
    ],
    "Systemic Lupus Erythematosus": [
        "flare prevention", "medication management", "sun protection",
        "organ involvement", "antibody monitoring", "disease activity",
        "treatment adjustment"
    ],
    "Gout": [
        "uric acid lowering", "flare prevention", "medication adherence",
        "dietary purine", "medication interactions", "acute attack management",
        "prophylaxis initiation"
    ],
    "Osteoporosis": [
        "bone density monitoring", "calcium intake", "vitamin d levels",
        "fall prevention", "exercise safety", "medication adherence",
        "fracture prevention"
    ],
    "Ankylosing Spondylitis": [
        "inflammation control", "posture maintenance", "exercise benefits",
        "medication adherence", "spinal flexibility", "disease monitoring",
        "functional improvement"
    ],
    "Fibromyalgia": [
        "pain management", "sleep improvement", "exercise pacing",
        "stress reduction", "medication use", "symptom tracking",
        "quality of life"
    ],
    "Parkinson's Disease": [
        "medication timing", "motor symptom control", "fall prevention",
        "speech exercises", "cognitive support", "medication adjustments",
        "disease progression"
    ],
    "Alzheimer's Disease": [
        "cognitive support", "medication use", "safety precautions",
        "caregiver support", "behavior management", "routine establishment",
        "advanced planning"
    ],
    "Multiple Sclerosis": [
        "disease modifying therapy", "symptom management", "relapse prevention",
        "medication adherence", "disability progression", "fatigue management",
        "cognitive symptoms"
    ],
    "Epilepsy": [
        "seizure prevention", "medication adherence", "seizure triggers",
        "medication levels", "trigger avoidance", "emergency planning",
        "seizure documentation"
    ],
    "Migraine Disorder": [
        "trigger identification", "medication timing", "migraine prevention",
        "acute management", "lifestyle factors", "medication efficacy",
        "preventive therapy"
    ],
    "Peripheral Neuropathy": [
        "pain management", "foot care", "balance exercises",
        "medication use", "symptom monitoring", "preventive care",
        "quality of life"
    ],
    "Non-Alcoholic Fatty Liver Disease": [
        "weight reduction", "alcohol avoidance", "nutrient management",
        "fibrosis monitoring", "exercise routine", "disease progression",
        "hepatocellular carcinoma screening"
    ],
    "Hepatitis C": [
        "treatment completion", "viral load monitoring", "cure confirmation",
        "liver function", "cirrhosis assessment", "medication adherence",
        "cure rate assessment"
    ],
    "Cirrhosis": [
        "portal hypertension management", "ascites control", "variceal bleeding prevention",
        "encephalopathy management", "transplant consideration", "medication adherence",
        "quality of life"
    ],
    "Inflammatory Bowel Disease": [
        "flare prevention", "medication adherence", "nutrition optimization",
        "inflammation control", "symptom tracking", "remission maintenance",
        "surgery consideration"
    ],
    "Celiac Disease": [
        "gluten avoidance", "nutrition optimization", "healing progression",
        "antibody monitoring", "nutrient supplementation", "diet adherence",
        "symptom improvement"
    ],
    "Gastroesophageal Reflux Disease": [
        "symptom triggers", "medication timing", "lifestyle modifications",
        "acid reduction", "medication adherence", "erosion prevention",
        "symptom management"
    ],
    "Colorectal Cancer": [
        "treatment tolerance", "symptom management", "surveillance schedule",
        "nutritional support", "medication side effects", "psychological support",
        "recurrence prevention"
    ],
    "Lung Cancer": [
        "treatment type", "side effect management", "symptom control",
        "follow-up imaging", "respiratory support", "nutritional status",
        "quality of life"
    ],
    "Breast Cancer": [
        "hormone therapy", "chemotherapy effects", "radiation side effects",
        "surveillance schedule", "reconstruction options", "psychological support",
        "recurrence prevention"
    ],
    "Prostate Cancer": [
        "hormone therapy", "psa monitoring", "radiation effects",
        "surgery recovery", "sexual function", "surveillance schedule",
        "quality of life"
    ],
    "Anemia": [
        "iron supplementation", "b12 replacement", "folate intake",
        "symptom improvement", "lab monitoring", "dietary management",
        "underlying cause"
    ],
    "HIV/AIDS": [
        "antiretroviral adherence", "viral load suppression", "cd4 monitoring",
        "opportunistic infection prevention", "medication interactions",
        "treatment initiation", "undetectable viral load"
    ],
    "Tuberculosis": [
        "medication adherence", "treatment completion", "drug interactions",
        "side effect management", "infection control", "treatment duration",
        "cure confirmation"
    ],
    "Depressive Disorder": [
        "medication adherence", "therapy engagement", "mood tracking",
        "activity scheduling", "social engagement", "sleep hygiene",
        "crisis management"
    ],
    "Anxiety Disorder": [
        "anxiety reduction", "breathing techniques", "exposure therapy",
        "medication management", "lifestyle modifications", "stress management",
        "symptom control"
    ],
    "Bipolar Disorder": [
        "mood stabilization", "medication adherence", "mood tracking",
        "episode prevention", "sleep maintenance", "stress management",
        "relapse prevention"
    ],
    "Chronic Pain Syndrome": [
        "pain management", "pain pacing", "psychological coping",
        "medication use", "physical therapy", "functional improvement",
        "quality of life"
    ],
    "Substance Use Disorder": [
        "medication assisted treatment", "abstinence support", "relapse prevention",
        "treatment engagement", "mental health", "social support",
        "recovery maintenance"
    ],
    "Cushing's Syndrome": [
        "cortisol reduction", "medication management", "symptom improvement",
        "comorbidity management", "treatment completion", "hypercortisolism control",
        "quality of life"
    ],
    "Addison's Disease": [
        "hormone replacement", "medication adherence", "stress dosing",
        "salt intake", "medication timing", "crisis prevention",
        "quality of life"
    ],
}

# ============================================================================
# EXPANDED QUESTION AND RESPONSE TEMPLATES
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
    "Given my {cultural_context}, how do I manage {topic} with {condition}?",
    "I'm {persona}, newly {comorbidity}, dealing with {topic}. Help?",
]

RESPONSE_TEMPLATES = [
    "For your situation as {persona}, the key is {detail}. Here's a practical approach: {approach}.",
    "Managing {topic} with {condition} requires {detail}. Start by {action}, then {action2}.",
    "Given your {resource} and {tech} access, focus on {detail} first. You can {approach}.",
    "With {literacy}, I'll keep this simple: {approach}. The most important part is {detail}.",
    "Your {motivation} is important. To address {topic}, prioritize {detail} and {action}.",
    "Considering {comorbidity}, be especially attentive to {detail}. Your best approach: {approach}.",
    "In your {setting}, the safest strategy for {topic} is {approach}. Remember: {important_point}.",
    "For {persona} managing {condition}, {topic} works best when you {action}. Focus on {detail}.",
    "In {cultural_context}, this approach respects your values: {approach}. Key point: {important_point}.",
    "{persona}, with your {motivation}, break {topic} into: first {action}, then {action2}.",
]

APPROACHES = [
    "track daily patterns for one week", "start with one small change",
    "use a reminder system or app", "work with a healthcare provider",
    "join a support group", "practice gradual adjustment",
    "seek professional guidance", "involve your family",
    "break it into smaller steps", "monitor for changes",
    "create a simple checklist", "use written reminders",
    "discuss with your doctor first", "try a time-limited experiment",
    "document your progress", "celebrate small wins",
    "adjust based on feedback", "seek peer support",
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
    "you're not alone in this journey",
    "progress isn't always linear",
    "self-compassion is important",
    "ask for accommodations when needed",
    "your experience is valid",
    "recovery takes time",
    "support from others matters",
    "managing expectations helps",
    "flexibility is key",
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
# PRIMARY GENERATION FUNCTION
# ============================================================================

def generate_diverse_question_pair(
    source_index: int, variant_index: int
) -> Tuple[str, str, str]:
    """Generate a diverse QA pair using the massive diversity matrix."""
    
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
    
    try:
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
                motivation=motivation,
                cultural_context=culture
            )
        )
    except KeyError:
        patient_query = f"As {persona}, I have {condition}. Can you help with {topic}?"
    
    # Generate response
    detail_opts = DETAILS_BY_CATEGORY.get(category, DETAILS_BY_CATEGORY.get("Type 1 Diabetes Mellitus", ["general management"]))
    detail = detail_opts[(source_index + variant_index * 7) % len(detail_opts)]
    approach = APPROACHES[(source_index * 17 + variant_index) % len(APPROACHES)]
    action = approach
    action2 = APPROACHES[(source_index * 19 + variant_index * 2) % len(APPROACHES)]
    important = IMPORTANT_POINTS[(source_index * 23 + variant_index * 3) % len(IMPORTANT_POINTS)]
    
    r_template = RESPONSE_TEMPLATES[variant_index % len(RESPONSE_TEMPLATES)]
    
    try:
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
            important_point=important,
            cultural_context=culture
        )
    except KeyError:
        doctor_response = f"For managing {topic} with {condition}, focus on {detail} and take small steps toward improvement."
    
    return ensure_question_mark(patient_query), doctor_response, category

# ============================================================================
# MAIN GENERATION LOGIC - 500K CAPACITY
# ============================================================================

def generate_500k_dataset(output_file: str, target_count: int = 200000) -> List[Dict]:
    """Generate up to 500,000 unique diverse questions."""
    
    generated: List[Dict] = []
    seen_queries = set()
    
    base_sources = len(CONDITIONS)
    variants_per_source = target_count // base_sources
    extra = target_count % base_sources
    
    print(f"\n{'='*70}")
    print(f"🚀 GENERATING {target_count:,} UNIQUE NCD QUESTIONS")
    print(f"{'='*70}")
    print(f"Base conditions: {base_sources}")
    print(f"Variants per source: {variants_per_source:,}")
    print(f"Extra variants: {extra}")
    print(f"Total NCD categories: {len(NCD_CATEGORIES)}")
    print(f"Unique personas: {len(PERSONAS)}")
    print(f"Unique topics: {len(TOPICS)}")
    print(f"Potential combinations: {len(CONDITIONS) * len(PERSONAS) * len(TOPICS):,}")
    print(f"{'='*70}\n")
    
    record_id = 1
    failed_count = 0
    
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
                
                if record_id % 25000 == 0:
                    percent = (len(generated) / target_count) * 100
                    print(f"✓ Generated {len(generated):>7,} questions ({percent:>5.2f}%)")
                
                if len(generated) >= target_count:
                    break
                    
            except Exception as e:
                failed_count += 1
                if failed_count < 10:
                    print(f"  ⚠ Warning: Generation error at variant {variant_idx}: {str(e)[:50]}")
                continue
        
        if len(generated) >= target_count:
            break
    
    generated = generated[:target_count]
    
    print(f"\n💾 Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated, f, ensure_ascii=False, indent=2)
    
    return generated

# ============================================================================
# SUMMARY AND VALIDATION
# ============================================================================

def print_summary(records: List[Dict]) -> None:
    print("\n" + "="*70)
    print("📊 DATASET GENERATION SUMMARY")
    print("="*70)
    print(f"\nTotal records generated: {len(records):,}")
    
    category_counts = Counter(r["category"] for r in records)
    print(f"\nCategory Distribution ({len(category_counts)} unique categories):")
    
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (category, count) in enumerate(sorted_cats[:15], 1):
        percent = (count / len(records)) * 100 if records else 0
        print(f"  {i:2d}. {category:.<45} {count:>7,} ({percent:>5.2f}%)")
    
    if len(sorted_cats) > 15:
        remaining_count = sum(count for _, count in sorted_cats[15:])
        print(f"  ... {len(sorted_cats)-15} more categories ........... {remaining_count:>7,}")
    
    seen = set()
    duplicates = 0
    for r in records:
        normalized = normalize_text(r["patient_query"])
        if normalized in seen:
            duplicates += 1
        seen.add(normalized)
    
    print(f"\n✓ Uniqueness Check:")
    print(f"  Total queries: {len(records):,}")
    print(f"  Unique queries: {len(seen):,}")
    print(f"  Duplicates detected: {duplicates}")
    if duplicates == 0:
        print(f"  All {len(records):,} queries are 100% unique!")
    
    file_size_mb = len(json.dumps(records, ensure_ascii=False)) / (1024*1024)
    avg_q_len = sum(len(r["patient_query"]) for r in records) / len(records)
    avg_r_len = sum(len(r["doctor_response"]) for r in records) / len(records)
    
    print(f"\n  File Statistics:")
    print(f"  Estimated file size: {file_size_mb:,.2f} MB")
    print(f"  Average question length: {avg_q_len:.0f} characters")
    print(f"  Average response length: {avg_r_len:.0f} characters")
    print(f"  Generation date: March 13, 2026")
    print("="*70 + "\n")

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate up to 500K diverse NCD questions with 50 categories"
    )
    parser.add_argument(
        "--output",
        default="ncd_dataset_500k.json",
        help="Output JSON file (default: ncd_dataset_500k.json)"
    )
    parser.add_argument(
        "--target",
        type=int,
        default=200000,
        help="Target question count (default: 00000)"
    )
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("NCD QUESTION-ANSWER DATASET GENERATOR v2.0")
    print("="*70)
    print(f"   NCD Categories: {len(NCD_CATEGORIES)}")
    print(f"   Base Conditions: {len(CONDITIONS)}")
    print(f"   Personas: {len(PERSONAS)}")
    print(f"   Topics: {len(TOPICS)}")
    print(f"   Settings: {len(SETTINGS)}")
    print(f"   Comorbidities: {len(COMORBIDITIES)}")
    print(f"   Resource Levels: {len(RESOURCE_LEVEL)}")
    print(f"   Tech Access Types: {len(TECH_ACCESS)}")
    print(f"   Health Literacy Levels: {len(HEALTH_LITERACY)}")
    print(f"   Motivation Levels: {len(MOTIVATION)}")
    print(f"   Cultural Contexts: {len(CULTURAL_CONTEXT)}")
    print(f"\n     Output: {args.output}")
    print(f"   Target: {args.target:,} questions")
    print("="*70 + "\n")
    
    records = generate_500k_dataset(args.output, args.target)
    print_summary(records)
    print(f" Dataset successfully saved to: {args.output}")

if __name__ == "__main__":
    main()