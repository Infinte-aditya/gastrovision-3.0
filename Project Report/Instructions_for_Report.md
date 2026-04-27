# Instructions for Writing Project Report

## General Guidelines

- Maintain formal and academic tone
- Use clear and concise language
- Avoid unnecessary jargon
- Ensure consistency across all sections
- Follow the provided Table of Contents strictly

---

## Abstract

- Write as a single paragraph (150–200 words)
- Follow IMRaD structure:
    - Background (why)
    - Objective (what)
    - Methodology (how)
    - Results (accuracy, speed)
    - Conclusion (impact)

---

## Chapter-wise Instructions

### Chapter 1: Introduction
-Must Includes:
-- Project overview
-- Problem statement
-- Motivation
-- Objectives
-- SDG Goals (ONLY SDG 3 and SDG 9)

- Explain project context clearly
- Define problem statement precisely
- Include motivation and objectives
- Mention SDG goals (only SDG 3 and SDG 9)

---

### Chapter 2: Literature Survey
- Discuss:
  - GI disease detection methods
  - CNN vs Transformer models
- Highlight:
  - Research gaps
- Keep content relevant to:
  - ViT
  - medical imaging
  - video-based analysis

- Discuss existing approaches (CNN, ViT, etc.)
- Highlight research gaps
- Keep content relevant to our project
- Avoid unrelated domains (e.g., skin lesions, unrelated models)

---

### Chapter 3: Sprint Planning

- Divide work into 3 sprints:
    1. Video Processing Pipeline
        - Frame extraction
        - Frame filtering
        - Metadata generation
    2. Pretrained Model Integration
        - Prediction system
        - Heatmaps
        - Scoring
    3. Fine-tuned ViT + Optimization
        - Improved accuracy (~94%)
        - Heatmap refinement
        - Bounding boxes
        - Performance optimization
- For each sprint include:
    - Objectives
    - Functional details
    - Architecture
    - Results
    - Retrospective

---

### Chapter 4: System Design

Include diagrams:

- Architecture diagram
- Data Flow Diagram (DFD)
- UML diagrams
- ER diagram
- Component diagram

---

### Chapter 5: Implementation

Explain modules:

- Video processing
- Frame selection
- Model integration
- Heatmap generation  
- Visualization
- API + frontend

---

### Chapter 6: Results

Include:

- Accuracy (~94%)
- Inference time (~0.2 sec/frame)
- Graphs (accuracy, loss)
- Confusion matrix
- Heatmap outputs
- Sample outputs (heatmaps)
- Frame scoring results


---

### Chapter 7: Conclusion

- Summarize achievements
- Mention & Highlight on system impact
- Also Mention real-world applicability
- Add future improvements

---

## Formatting Guidelines

- Use headings and subheadings properly
- Keep paragraphs ~150–200 words
- Maintain alignment and spacing
- Use consistent font and size
- Add figure/table captions properly

---

## Diagrams

Use tools like:

- [Draw.io](http://draw.io/)
- Lucidchart

Ensure:

- Clean layout
- Proper labeling
- Logical flow

---

## Tables & Figures

Include:

- Dataset distribution
- Model performance
- Inference comparison
- Frame statistics

---

## Common Mistakes to Avoid

- Copying unrelated content
- Missing results in report
- Overly long paragraphs
- Inconsistent formatting
- Lack of explanation for diagrams

---

## Final Checklist

- All chapters completed
- Figures and tables added
- References included
- No plagiarism
- Consistent formatting

---

## Submission Tip

Highlight:

- End-to-end pipeline
- Explainability (heatmaps)
- Real-world application
- Performance metrics

## **TABLE OF CONTENTS (being followed)**

ABSTRACT ........................................................................................................ v

TABLE OF CONTENTS .................................................................................. vi

LIST OF FIGURES ....................................................................................... vii

LIST OF TABLES ......................................................................................... viii

ABBREVIATIONS ........................................................................................ ix

---

## **CHAPTER 1: INTRODUCTION .............................................................. 1**

1.1 Introduction to the Project ............................................................. 2

1.2 Problem Statement and Description ............................................... 3

1.3 Motivation ..................................................................................... 4

1.4 Objectives of the Project ............................................................... 5

1.5 Sustainable Development Goals (SDG) ........................................... 6

---

## **CHAPTER 2: LITERATURE SURVEY ..................................................... 7**

2.1 Overview of Gastrointestinal Disease Detection ............................ 8

2.2 Existing Models and Techniques (CNN, ViT, etc.) ......................... 9

2.3 Limitations and Research Gaps .................................................... 11

2.4 Research Objectives .................................................................... 12

2.5 Product Backlog (User Stories) .................................................... 13

2.6 Project Roadmap ......................................................................... 15

---

## **CHAPTER 3: SPRINT PLANNING & EXECUTION .............................. 18**

### **3.1 Sprint I – Data Processing & Pipeline Setup**

3.1.1 Objectives & User Stories ....................................................... 19

3.1.2 Functional Design .................................................................... 20

3.1.3 Architecture Design .................................................................. 22

3.1.4 Results & Analysis ................................................................... 24

3.1.5 Sprint Retrospective ............................................................... 25

---

### **3.2 Sprint II – Model Development & Visualization**

3.2.1 Objectives & User Stories ....................................................... 26

3.2.2 Functional Design .................................................................... 27

3.2.3 Architecture Design .................................................................. 29

3.2.4 Results & Analysis ................................................................... 31

3.2.5 Sprint Retrospective ............................................................... 32

---

### **3.3 Sprint III – Integration & Deployment**

3.3.1 Objectives & User Stories ....................................................... 33

3.3.2 Functional Design .................................................................... 34

3.3.3 Architecture Design .................................................................. 36

3.3.4 Results & Analysis ................................................................... 38

3.3.5 Sprint Retrospective ............................................................... 39

---

## **CHAPTER 4: SYSTEM DESIGN ............................................................ 40**

4.1 Overall System Architecture ......................................................... 41

4.2 Data Flow Diagram (DFD) ............................................................ 42

4.3 UML Diagrams ............................................................................ 43

4.4 Database Design (ER Diagram) .................................................... 45

4.5 Component Design ...................................................................... 47

---

## **CHAPTER 5: IMPLEMENTATION ........................................................ 49**

5.1 Video Processing Module ............................................................ 50

5.2 Frame Extraction & Selection ...................................................... 52

5.3 Model Implementation (ViT) ......................................................... 54

5.4 Heatmap & Localization .............................................................. 56

5.5 API Development ........................................................................ 58

5.6 Frontend Implementation (PyQt) ................................................. 60

---

## **CHAPTER 6: RESULTS AND DISCUSSION .......................................... 62**

6.1 Model Performance (Accuracy, Loss) ........................................... 63

6.2 Inference Performance (Speed Analysis) ..................................... 65

6.3 Visualization Results (Heatmaps & Bounding Boxes) ................. 66

6.4 Comparison with Existing Methods ............................................. 68

---

## **CHAPTER 7: CONCLUSION AND FUTURE WORK ............................. 70**

7.1 Conclusion .................................................................................. 71

7.2 Future Enhancements ................................................................. 72

---

REFERENCES ............................................................................................. 74

---

## **APPENDIX**

A. Code Snippets ................................................................................ 76

B. Screenshots of UI .......................................................................... 80

C. Model Outputs .............................................................................. 83

D. Plagiarism Report ......................................................................... 85

# **LIST OF FIGURES (UPDATED AS PER OUR PROJECT)**

Use **only relevant figures**, NOT the sample ones:

- System Architecture Diagram
- Video Processing Pipeline
- Model Architecture (ViT)
- Heatmap Visualization Output
- UI Screens
- Confusion Matrix
- Accuracy/Loss Graph

---

# **📊 LIST OF TABLES (UPDATED)**

- Dataset Distribution (8 classes)
- Training Results (epoch vs accuracy)
- Inference Speed Comparison
- Frame Selection Statistics
- Model Performance Metrics