"""
Dataset generator for University Query Management System.
Run: python data/generate_datasets.py
"""
import csv
import os
import random

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "training")
os.makedirs(OUT, exist_ok=True)

# ── Seed templates ────────────────────────────────────────────────────────────

TEMPLATES = {
    "Admission": {
        "Negative": [
            "My admission application has been pending for {n} weeks with no update.",
            "I submitted all documents but my admission status still shows incomplete.",
            "The admission portal keeps showing an error when I try to submit my form.",
            "My merit list position was not updated even after re-verification.",
            "I was asked to submit documents twice but still no confirmation.",
            "Admission office is not responding to my emails for {n} days.",
            "My application was rejected without any reason given.",
            "Wrong category was assigned to me during the admission process.",
            "I missed the counselling round due to no notification from the portal.",
            "The seat allotment letter has not been issued after {n} days of payment.",
        ],
        "Neutral": [
            "What is the last date for admission form submission?",
            "How do I check my admission status online?",
            "What documents are required for the admission process?",
            "Is there a provision for sports quota admission?",
            "What is the fee structure for the new academic year?",
            "How many seats are available in the Computer Science branch?",
            "Can I change my branch after the first year?",
            "What is the process for NRI admission?",
            "When will the second merit list be published?",
            "Is direct admission available for lateral entry students?",
        ],
        "Positive": [
            "Thank you, my admission documents were verified quickly.",
            "The admission process was smooth and well-organised this year.",
            "I received my admission confirmation letter on time.",
            "The staff at the admission office was very helpful.",
            "My seat allotment was updated within {n} hours as promised.",
        ],
    },
    "Examination": {
        "Negative": [
            "My admit card has not been generated even though exams start tomorrow.",
            "There is a spelling mistake in my name on the hall ticket.",
            "I was marked absent in the exam even though I was present.",
            "My result shows fail but I had submitted all answers correctly.",
            "The exam timetable was changed without prior notice.",
            "I could not find my roll number on the examination portal.",
            "My internal marks have not been updated for {n} subjects.",
            "Revaluation result is pending for over {n} months.",
            "The examination fee was deducted but the form was not submitted.",
            "My backlog exam date clashes with my regular exam schedule.",
            "I was not allowed into the exam hall due to a portal error.",
            "My grade sheet shows incorrect marks for the third semester.",
            "The practical exam was scheduled without any prior intimation.",
            "I have been allotted a wrong exam centre far from my address.",
        ],
        "Neutral": [
            "When will the end semester exam schedule be released?",
            "What is the process to apply for revaluation?",
            "How many attempts are allowed for a backlog paper?",
            "What is the passing criteria for practical exams?",
            "Can I appear in exam if attendance is below 75 percent?",
            "When will semester results be declared?",
            "What is the exam form fill-up last date?",
            "Is there a grace mark policy in the university?",
            "How do I download my admit card from the portal?",
            "What is the procedure for exam form correction?",
        ],
        "Positive": [
            "My admit card was generated on time, thank you.",
            "The exam schedule was shared well in advance this time.",
            "Result was declared faster than expected, appreciated.",
            "The revaluation process was handled efficiently.",
            "I got my corrected mark sheet within {n} days.",
        ],
    },
    "Hostel": {
        "Negative": [
            "There has been no water supply in the hostel for {n} days.",
            "The hostel room allotted to me is not clean.",
            "Wi-Fi in the hostel has not been working for {n} days.",
            "The mess food quality has deteriorated significantly.",
            "I reported a maintenance issue {n} weeks ago but it is still unresolved.",
            "My roommate is causing disturbance but the warden is not taking action.",
            "The hostel gate is being closed before the permitted time.",
            "There are insects in the mess food, this is unacceptable.",
            "The hostel fee receipt has not been generated after payment.",
            "Power cuts in the hostel are happening every day.",
            "The common bathroom tiles are broken and pose a safety risk.",
            "I was denied entry to the hostel without any valid reason.",
        ],
        "Neutral": [
            "What is the process to apply for hostel accommodation?",
            "When does hostel allotment happen for new students?",
            "What are the hostel rules for late-night entry?",
            "Is air conditioning available in hostel rooms?",
            "What is the monthly hostel fee for postgraduate students?",
            "How do I apply for a room change?",
            "Is laundry service available in the hostel?",
            "What items are allowed and not allowed in the hostel?",
            "Are parents allowed to visit the hostel?",
            "What is the procedure to vacate the hostel at year end?",
        ],
        "Positive": [
            "The hostel room was clean and well-maintained on arrival.",
            "The warden resolved my complaint within {n} hours.",
            "Hostel Wi-Fi speed has improved a lot recently.",
            "The mess menu has improved significantly this month.",
            "I appreciate the timely maintenance work done in my room.",
        ],
    },
    "Finance": {
        "Negative": [
            "I paid the fee online but the portal still shows dues pending.",
            "My fee refund has not been processed even after {n} months.",
            "The challan generated has incorrect details.",
            "I was charged late fee even though I paid before the deadline.",
            "My scholarship amount was deducted from my fee but still shows balance.",
            "The finance department is not responding to my refund request.",
            "I was asked to pay the fee again even after showing the receipt.",
            "My transaction failed but the amount was debited from my account.",
            "The fee receipt is not downloadable from the portal.",
            "Wrong fee head was applied to my account causing confusion.",
            "I have been charged hostel fee even though I am a day scholar.",
        ],
        "Neutral": [
            "What is the last date for fee payment this semester?",
            "Is there an EMI option available for fee payment?",
            "How do I download my fee receipt from the portal?",
            "What happens if I miss the fee deadline?",
            "What is the refund policy for withdrawn students?",
            "How can I get a duplicate fee receipt?",
            "What are the accepted modes of fee payment?",
            "Is there any concession for single-parent students?",
            "Can I pay the fee in installments?",
            "What is the fee structure for international students?",
        ],
        "Positive": [
            "The fee portal worked smoothly and I received the receipt instantly.",
            "My refund was processed within {n} working days, thank you.",
            "The finance staff resolved my billing error quickly.",
            "The online payment system is very convenient.",
            "I appreciate the extended fee deadline during exam time.",
        ],
    },
    "Placement": {
        "Negative": [
            "I was not notified about the campus drive that happened yesterday.",
            "My resume was not shortlisted without any feedback.",
            "The placement cell has not updated the company list for this year.",
            "I have not received my offer letter even after {n} months of selection.",
            "The pre-placement talk was cancelled without informing students.",
            "I missed the registration deadline because no reminder was sent.",
            "The placement portal login is not working for me.",
            "My profile on the placement portal shows incorrect CGPA.",
            "The company I was placed in has deferred joining by {n} months.",
            "I was removed from the placement list due to a clerical error.",
        ],
        "Neutral": [
            "When will campus placements begin this year?",
            "What is the minimum CGPA required for placement registration?",
            "How do I register on the placement portal?",
            "Which companies visited last year?",
            "Is there a training program before placements?",
            "Can final year students from all branches register?",
            "What documents are needed for placement registration?",
            "Is off-campus placement assistance provided?",
            "What was the highest package offered last year?",
            "Are there any internship opportunities through the placement cell?",
        ],
        "Positive": [
            "I got placed in a good company, thank you to the placement cell.",
            "The placement training sessions were very useful.",
            "The placement cell kept us informed about every drive.",
            "I received my offer letter within {n} days of the interview.",
            "The mock interviews organised by placement cell were excellent.",
        ],
    },
    "Scholarship": {
        "Negative": [
            "My scholarship application has been pending for {n} months with no update.",
            "The scholarship amount was not credited to my account this semester.",
            "I submitted all documents but my application still shows incomplete.",
            "I was declared ineligible for scholarship without any explanation.",
            "My scholarship was cancelled despite fulfilling all criteria.",
            "The scholarship portal is not accepting my Aadhaar number.",
            "I have not received any communication regarding my scholarship status.",
            "The renewal form for scholarship is not available on the portal.",
        ],
        "Neutral": [
            "What scholarships are available for meritorious students?",
            "What is the income limit for need-based scholarship?",
            "When is the scholarship application portal open?",
            "What documents are required for scholarship application?",
            "Is there a scholarship for differently-abled students?",
            "How is the scholarship amount disbursed?",
            "Can I apply for multiple scholarships simultaneously?",
            "What is the renewal process for continuing scholarship?",
            "Is there a government scholarship tie-up with this university?",
            "What is the deadline for scholarship form submission?",
        ],
        "Positive": [
            "My scholarship was approved quickly, I am very grateful.",
            "The scholarship cell staff helped me complete my application.",
            "I received the scholarship amount before the semester began.",
            "The merit scholarship process was transparent and fair.",
            "Thank you for processing my scholarship renewal on time.",
        ],
    },
    "Complaint": {
        "Negative": [
            "A faculty member is giving biased marks to certain students.",
            "I am being harassed by a senior student and no action is being taken.",
            "My complaint submitted {n} days ago has not been acknowledged.",
            "There is a case of ragging in my hostel block.",
            "The faculty is not conducting classes regularly.",
            "I was threatened by a classmate and reported it but nothing happened.",
            "Discriminatory remarks were made by a professor in class.",
            "My grievance has been ignored by the department for {n} weeks.",
            "The anti-ragging committee is not accessible to students.",
            "I was wrongly penalised for something I did not do.",
        ],
        "Neutral": [
            "How do I file a formal complaint against a faculty member?",
            "What is the anti-ragging policy of the university?",
            "Where can I report a case of harassment?",
            "What is the procedure for the internal complaints committee?",
            "Is there an anonymous complaint submission option?",
            "How long does it take to resolve a grievance?",
            "Who is the grievance redressal officer?",
            "Can I escalate my complaint if it is not resolved?",
            "What action is taken against proven ragging cases?",
            "Is there a student ombudsman at this university?",
        ],
        "Positive": [
            "My complaint was taken seriously and resolved within {n} days.",
            "The student affairs office handled my case professionally.",
            "I appreciate the quick action taken on my grievance.",
            "The anti-ragging cell responded to my complaint immediately.",
            "Thank you for ensuring a safe environment in the hostel.",
        ],
    },
    "General": {
        "Negative": [
            "The university website has been down for {n} days.",
            "I cannot find any information about the upcoming event.",
            "The help desk is not responding to my queries.",
            "My ID card has not been issued even after {n} weeks of joining.",
            "The library is closed during exam preparation time.",
            "The transport bus schedule has changed without any notice.",
            "The notice board has outdated information.",
            "My email ID was not created even after {n} weeks of registration.",
        ],
        "Neutral": [
            "What are the library timings on weekends?",
            "How do I get a duplicate ID card?",
            "What is the academic calendar for this year?",
            "How do I access the university Wi-Fi?",
            "What clubs and societies are active this semester?",
            "How do I apply for a bonafide certificate?",
            "What is the process for obtaining a migration certificate?",
            "Where is the medical centre located on campus?",
            "What are the transport routes available for students?",
            "How do I update my contact details on the portal?",
        ],
        "Positive": [
            "The new student portal is very user-friendly.",
            "The orientation program was well-organised.",
            "The campus facilities have improved a lot this year.",
            "Staff at the help desk were very cooperative.",
            "I received my ID card within {n} days, thank you.",
        ],
    },
}

DEPT_MAP = {
    "Admission":   "Admission Department",
    "Examination": "Examination Department",
    "Hostel":      "Hostel Department",
    "Finance":     "Finance Department",
    "Placement":   "Placement Cell",
    "Scholarship": "Scholarship Cell",
    "Complaint":   "Student Affairs",
    "General":     "Help Desk",
}

SENTIMENT_PRIORITY = {
    "Negative": ["High", "High", "Medium"],
    "Neutral":  ["Medium", "Medium", "Low"],
    "Positive": ["Low", "Low", "Medium"],
}


def _render(template: str) -> str:
    return template.replace("{n}", str(random.randint(2, 30)))


def _pick(intent: str, sentiment: str) -> str:
    pool = TEMPLATES[intent][sentiment]
    return _render(random.choice(pool))


def _weighted_sentiment() -> str:
    return random.choices(
        ["Negative", "Neutral", "Positive"], weights=[45, 35, 20]
    )[0]


# ── 1. student_queries.csv (2000 rows) ────────────────────────────────────────
def gen_student_queries():
    intents = list(TEMPLATES.keys())
    rows = []
    per_intent = 2000 // len(intents)  # 250 each
    for intent in intents:
        for _ in range(per_intent):
            sentiment = _weighted_sentiment()
            query = _pick(intent, sentiment)
            priority = random.choice(SENTIMENT_PRIORITY[sentiment])
            rows.append({
                "query": query,
                "intent": intent,
                "department": DEPT_MAP[intent],
                "priority": priority,
                "sentiment": sentiment,
            })
    random.shuffle(rows)
    path = os.path.join(OUT, "student_queries.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query","intent","department","priority","sentiment"])
        w.writeheader(); w.writerows(rows)
    print(f"✓ student_queries.csv  ({len(rows)} rows)")


# ── 2. intents.csv (1000 rows) ────────────────────────────────────────────────
def gen_intents():
    intents = list(TEMPLATES.keys())
    rows = []
    per = 1000 // len(intents)
    for intent in intents:
        sentiments = list(TEMPLATES[intent].keys())
        for _ in range(per):
            s = random.choice(sentiments)
            rows.append({"query": _pick(intent, s), "intent": intent})
    random.shuffle(rows)
    path = os.path.join(OUT, "intents.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query","intent"])
        w.writeheader(); w.writerows(rows)
    print(f"✓ intents.csv          ({len(rows)} rows)")


# ── 3. priorities.csv (1000 rows) ─────────────────────────────────────────────
def gen_priorities():
    rows = []
    intents = list(TEMPLATES.keys())
    per = 1000 // 3
    for priority, sentiments in [("High","Negative"), ("Medium","Neutral"), ("Low","Positive")]:
        for _ in range(per):
            intent = random.choice(intents)
            rows.append({"query": _pick(intent, sentiments), "priority": priority})
    # fill remainder
    while len(rows) < 1000:
        intent = random.choice(intents)
        s = _weighted_sentiment()
        rows.append({"query": _pick(intent, s), "priority": random.choice(SENTIMENT_PRIORITY[s])})
    random.shuffle(rows)
    path = os.path.join(OUT, "priorities.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query","priority"])
        w.writeheader(); w.writerows(rows)
    print(f"✓ priorities.csv       ({len(rows)} rows)")


# ── 4. sentiments.csv (1000 rows) ─────────────────────────────────────────────
def gen_sentiments():
    rows = []
    intents = list(TEMPLATES.keys())
    per = 1000 // 3
    for sentiment in ["Negative", "Neutral", "Positive"]:
        for _ in range(per):
            intent = random.choice(intents)
            rows.append({"query": _pick(intent, sentiment), "sentiment": sentiment})
    while len(rows) < 1000:
        intent = random.choice(intents)
        s = _weighted_sentiment()
        rows.append({"query": _pick(intent, s), "sentiment": s})
    random.shuffle(rows)
    path = os.path.join(OUT, "sentiments.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["query","sentiment"])
        w.writeheader(); w.writerows(rows)
    print(f"✓ sentiments.csv       ({len(rows)} rows)")


# ── 5. departments.csv ────────────────────────────────────────────────────────
def gen_departments():
    rows = [{"intent": k, "department": v} for k, v in DEPT_MAP.items()]
    path = os.path.join(OUT, "departments.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["intent","department"])
        w.writeheader(); w.writerows(rows)
    print(f"✓ departments.csv      ({len(rows)} rows)")


# ── 6. faq_dataset.csv (300 rows) ─────────────────────────────────────────────
FAQ_DATA = [
    # Admissions (30)
    ("What is the last date to apply for admission?","The last date for admission applications is published on the official university website and varies by programme. Check the admissions portal for the current cycle deadline."),
    ("How do I apply for undergraduate admission?","Visit the admissions portal, register with your email, fill the application form, upload required documents, and pay the application fee online."),
    ("What documents are required for admission?","You need 10th and 12th mark sheets, transfer certificate, migration certificate, passport-size photos, ID proof, and category certificate if applicable."),
    ("Is there a management quota for admission?","Yes, a certain percentage of seats are available under management quota. Contact the admissions office for current availability and eligibility criteria."),
    ("Can I apply for multiple programmes simultaneously?","Yes, you can apply for up to three programmes in a single application cycle by selecting preferences during form fill-up."),
    ("When is the second merit list released?","The second merit list is released approximately 5 to 7 working days after the first list. Check the admissions portal regularly."),
    ("What is the process for lateral entry admission?","Lateral entry is available for diploma holders into the second year of engineering programmes. Apply through the lateral entry portal with your diploma mark sheets."),
    ("Is there a sports quota for admission?","Yes, students with state or national level sports achievements may apply under sports quota. Submit relevant certificates to the sports department."),
    ("How do I check my admission application status?","Log in to the admissions portal using your application number and date of birth to view your current application status."),
    ("What is the minimum percentage required for admission?","The minimum percentage requirement varies by programme. Generally, 50% in 12th standard is required for most undergraduate programmes."),
    ("Can I defer my admission to next year?","Deferral is not permitted. If you are unable to join, you must re-apply in the next admission cycle."),
    ("How do I cancel my admission and get a refund?","Submit a written cancellation request to the admissions office along with your original receipts. Refund is processed as per university refund policy."),
    ("What is the NRI admission process?","NRI students should apply through the international admissions portal. Seats are limited and the fee structure differs from regular admissions."),
    ("Are there reserved seats for differently-abled students?","Yes, 5% seats are reserved for differently-abled students as per government norms. Submit a valid disability certificate during application."),
    ("How long does document verification take?","Document verification typically takes 3 to 5 working days after submission. You will be notified by email once completed."),
    ("What if I have a gap year after 12th?","A gap certificate or affidavit explaining the gap year must be submitted along with your admission documents."),
    ("Is there an entrance exam for admission?","Some programmes require clearing the university entrance exam. Refer to the programme-specific admission criteria on the website."),
    ("How do I get an admission confirmation letter?","After completing fee payment and document verification, the admission confirmation letter is available for download on the portal."),
    ("Can I change my programme after admission?","Branch change requests may be submitted after the first semester results, subject to seat availability and CGPA criteria."),
    ("What is the tuition fee for BTech first year?","The fee structure is published annually on the university website. Contact the finance department for the latest fee details."),
    ("Is there any relaxation in marks for SC/ST students?","Yes, a 5% relaxation in minimum qualifying marks is provided for SC/ST students as per government reservation policy."),
    ("When does the new academic session start?","The new academic session typically begins in July or August. The exact date is published in the academic calendar."),
    ("How do I get a bonafide certificate after admission?","Submit a bonafide certificate application at the administrative office or apply online through the student portal."),
    ("What is the procedure for online document submission?","Log in to the admissions portal, navigate to document upload section, and upload clear scanned copies in PDF or JPEG format under 2MB each."),
    ("Can foreign nationals apply for admission?","Yes, foreign nationals may apply through the international admissions office. A valid passport and student visa are required."),
    ("What is the process for hostel allotment during admission?","Hostel allotment forms are available after admission confirmation. Submit the form with preference to the hostel office before the deadline."),
    ("Is there any age limit for admission?","As per UGC guidelines, there is no upper age limit for admission to regular programmes. Minimum age criteria vary by course."),
    ("How do I report a discrepancy in my admission documents?","Contact the admissions helpdesk immediately with the specific discrepancy details. Do not submit incorrect documents."),
    ("What is the process for obtaining a provisional admission letter?","Provisional admission letters are issued at the time of admission for students whose final results are awaited. Apply at the admissions office."),
    ("Can I take admission if my 12th result is awaited?","Yes, provisional admission is granted on submission of a declaration. Original mark sheets must be submitted within 30 days of result declaration."),
    # Examinations (30)
    ("How do I download my admit card?","Log in to the examination portal using your enrolment number, navigate to admit card section, and download your hall ticket before the exam date."),
    ("What should I do if there is an error on my admit card?","Contact the examination section immediately with your enrolment number and a written application describing the error for correction."),
    ("When are semester results declared?","Results are generally declared 30 to 45 days after the last examination. Check the examination portal for notifications."),
    ("How do I apply for revaluation?","Apply for revaluation through the examination portal within 15 days of result declaration. A per-subject fee is charged for revaluation."),
    ("What is the passing criteria for theory exams?","Students must secure a minimum of 40% marks in theory and 50% overall in each subject to pass."),
    ("How many attempts are allowed for a backlog paper?","Students are allowed a maximum of 5 attempts for a backlog paper, including the regular attempt."),
    ("Can I appear in exams if my attendance is below 75%?","Students with attendance below 75% are generally not permitted to appear in exams. A medical exemption may be considered by the HOD."),
    ("What is the process for exam form fill-up?","Log in to the exam portal, verify your subject list, fill the exam form, and pay the exam fee before the deadline."),
    ("How do I get a certified copy of my answer sheet?","Apply for a certified copy through the exam portal within 30 days of result declaration, along with the prescribed fee."),
    ("What happens if I miss an exam due to medical emergency?","Submit a medical certificate and application to the examination controller within 7 days. A medical exam may be conducted subject to approval."),
    ("Is grace marks policy applicable at this university?","Yes, a grace marks policy is applicable for students falling short by a marginal percentage. Details are available in the examination regulations."),
    ("How do I check my internal marks?","Internal marks are updated on the student portal at the end of each semester. Contact your department if marks are missing."),
    ("What is the fee for revaluation?","The revaluation fee is charged per subject. Refer to the latest examination notification for the current fee."),
    ("When is the exam timetable published?","The exam timetable is published at least 30 days before the commencement of examinations on the university website."),
    ("How do I correct a spelling mistake in my name on certificates?","Submit an affidavit and the original admission documents to the examination section for name correction. A gazette notification may be required."),
    ("What is the procedure to obtain a provisional certificate?","Apply for a provisional certificate at the examination section after clearing all subjects. It is issued within 7 working days."),
    ("How do I apply for a duplicate mark sheet?","Submit a written application with an affidavit and prescribed fee to the examination section. A duplicate is issued within 15 working days."),
    ("Can I challenge the revaluation result?","If unsatisfied with revaluation, you may apply for a personal review of your answer sheet by paying the review fee within 10 days."),
    ("What is the procedure for supplementary exams?","Students who fail in up to two subjects are eligible for supplementary exams held within two months of the regular result declaration."),
    ("How is internal assessment calculated?","Internal assessment includes assignments, class tests, attendance, and lab performance. The breakdown is available in the course syllabus."),
    ("What documents are needed to collect my original degree?","Original degree collection requires your provisional certificate, fee clearance, library NOC, and a valid ID proof."),
    ("Is there any provision for open book exams?","Open book exams are conducted for specific subjects as notified by the examination department. Check the official notification."),
    ("How do I report a discrepancy in my marks?","Submit a written complaint with the question paper and your answer sheet reference to the examination controller within 15 days of result."),
    ("What is the process for ex-student examination?","Ex-students may apply for examination through the university examination portal. Eligibility and fee details are available on the portal."),
    ("Are online exams conducted for any subjects?","Online exams are conducted for certain elective and open elective subjects. Details are notified by the examination department."),
    ("What is the late fee for exam form submission?","A late fee is charged for exam forms submitted after the deadline. Refer to the current examination notification for the exact amount."),
    ("Can I opt out of an elective subject before exams?","Subject opt-out requests must be submitted to the academic section before the exam form fill-up deadline."),
    ("How long are answer scripts retained by the university?","Answer scripts are retained for a period of two years from the date of examination as per university regulations."),
    ("What is the procedure to get a migration certificate?","Apply for a migration certificate at the examination section after completing your degree. Submit the application with the prescribed fee and NOC."),
    ("When is the admit card released before exams?","Admit cards are released approximately 10 to 15 days before the examination commencement date."),
    # Hostel (30)
    ("How do I apply for hostel accommodation?","Hostel application forms are available on the student portal. Submit before the deadline along with the fee receipt and medical fitness certificate."),
    ("When is hostel allotment done for new students?","Hostel allotment is done after admission confirmation, generally one week before the commencement of classes."),
    ("What is the monthly hostel fee?","Hostel fee varies by room type. Refer to the fee structure on the university website for the current academic year."),
    ("What are the hostel visiting hours for parents?","Parents may visit on Sundays between 10 AM and 5 PM. Prior intimation to the warden is required."),
    ("Is air conditioning available in hostel rooms?","AC rooms are available in premium blocks at a higher fee. Allotment is subject to availability."),
    ("What is the rule for late entry into the hostel?","Students must return to the hostel by 10 PM on weekdays and 11 PM on weekends. Late entry requires prior written permission from the warden."),
    ("How do I apply for a room change?","Submit a room change request to the hostel warden with valid reasons. Changes are approved subject to availability."),
    ("Is laundry service available?","Yes, laundry service is available at a nominal charge. Contact the hostel office for the schedule and pricing."),
    ("What items are not allowed in the hostel?","Electric stoves, heaters, candles, pets, and alcohol are strictly prohibited inside the hostel premises."),
    ("How do I report a maintenance issue in my room?","Register your complaint on the student portal under hostel maintenance or inform the warden in writing. Maintenance is typically addressed within 48 hours."),
    ("What is the procedure to vacate the hostel?","Submit a vacating request to the warden, clear all dues, return room keys, and obtain a no dues certificate before the checkout date."),
    ("Is Wi-Fi available in hostels?","Yes, Wi-Fi is available in all hostel blocks. Contact the IT department with your student ID for credentials."),
    ("What is the mess timing?","Mess timings are Breakfast 7-9 AM, Lunch 12-2 PM, Snacks 5-6 PM, and Dinner 7:30-9:30 PM."),
    ("Can I opt out of the mess and cook myself?","Cooking in hostel rooms is not permitted. However, students may apply to opt out of mess with warden approval."),
    ("Is there a common room with TV in the hostel?","Yes, each hostel block has a common room with TV, indoor games, and newspaper facilities."),
    ("What should I do if I lose my room key?","Report the lost key immediately to the warden and pay the key replacement charge to receive a duplicate."),
    ("Is there a gym facility in the hostel?","A gym facility is available in the main sports complex. Hostel students may use it during designated hours."),
    ("How are hostel wardens allocated?","Each hostel block is managed by a resident warden and supported by a chief warden. Contact details are posted on the hostel notice board."),
    ("What is the process for hostel fee refund on withdrawal?","Submit a written refund request to the hostel office. Refund is processed after deducting one month retention fee as per policy."),
    ("Are separate hostels available for male and female students?","Yes, separate hostel blocks are available for male and female students with independent wardens and entry gates."),
    ("Can I stay in the hostel during semester breaks?","Hostel access during semester breaks requires prior approval from the warden and is subject to available accommodation."),
    ("How do I get a hostel no dues certificate?","Clear all pending dues and return room inventory. Apply for no dues at the hostel office and collect after verification."),
    ("Is there a medical facility near the hostel?","The university medical centre is located within campus and provides first aid and basic medical services to hostel residents."),
    ("What is the policy on guests staying overnight?","Overnight guest stays are not permitted in student hostels under any circumstances."),
    ("How do I complain about mess food quality?","Register your complaint in the mess complaint register or email the hostel mess committee. Feedback is reviewed weekly."),
    ("Is there a curfew during examination period?","Yes, a strict curfew of 9 PM applies during examination periods to ensure a quiet study environment."),
    ("How are hostel room allocations decided?","Rooms are allocated by lottery system based on seniority and preferences indicated in the hostel application form."),
    ("Can I bring a personal refrigerator to the hostel?","Small personal refrigerators are permitted with prior approval from the warden and payment of electricity surcharge."),
    ("What is the process for hostel block transfer?","Submit a block transfer request to the chief warden with valid reasons. Transfers are done at the beginning of each semester."),
    ("Is 24-hour security available at the hostel?","Yes, trained security personnel and CCTV surveillance are available 24 hours at all hostel entry and exit points."),
]

FAQ_DATA += [
    # Fees (30)
    ("What is the last date for fee payment?","Fee payment deadlines are published in the academic calendar. Late fee charges apply after the due date."),
    ("What payment methods are accepted for fee payment?","Fee can be paid online via net banking, UPI, debit/credit card, or through a bank challan at designated bank branches."),
    ("How do I download my fee receipt?","Log in to the student portal, go to Finance section, and download the receipt for your latest payment."),
    ("Is there an EMI option for fee payment?","EMI options are available through select bank tie-ups. Contact the finance department for participating banks and terms."),
    ("What is the late fee charge per day?","A late fee of a fixed amount per day is charged beyond the due date. Refer to the current finance notification for the exact amount."),
    ("Can I pay fees in installments?","An installment facility is available for economically weaker sections. Apply to the finance department with supporting income documents."),
    ("What is the fee refund policy?","Refund policy follows UGC guidelines. Full refund is given up to 15 days before classes begin, with graduated deductions thereafter."),
    ("How long does a fee refund take?","Refunds are processed within 15 to 30 working days after the cancellation is approved by the finance department."),
    ("My online transaction failed but money was deducted. What should I do?","Do not pay again. Contact the finance department with your bank transaction reference number. The amount will be reconciled within 5 working days."),
    ("How do I get a duplicate fee receipt?","Apply at the finance office with a written request and your original payment details. A duplicate receipt is issued within 3 working days."),
    ("Is there a concession for single-parent students?","Fee concession for single-parent students may be available. Submit relevant documents to the finance department for review."),
    ("How do I check my pending dues?","Log in to the student portal and navigate to Finance to view your current dues and payment history."),
    ("Can scholarship amounts be adjusted against fee?","Yes, approved scholarship amounts are directly adjusted against your fee balance on the portal."),
    ("What happens if I do not pay fees on time?","Unpaid fees may result in suspension of portal access, and students may not be permitted to appear in examinations."),
    ("Is the application fee refundable?","The application fee is non-refundable under any circumstances."),
    ("Can I get a fee waiver on medical grounds?","Medical fee waivers are considered on a case-by-case basis. Submit a medical certificate and application to the finance department."),
    ("What is the fee for certificate courses offered by the university?","Certificate course fees vary by programme. Contact the continuing education department or check the website."),
    ("How do I get a fee clearance certificate?","Clear all dues and apply for a fee clearance certificate at the finance office. It is issued within 2 working days."),
    ("What is the exam fee and when is it charged?","Exam fees are charged each semester at the time of exam form fill-up. The amount is listed in the fee structure."),
    ("Is there a separate fee for laboratory practicals?","Lab fees are included in the overall semester fee and are not charged separately for most programmes."),
    ("How do I pay if I am an international student?","International students may pay via wire transfer or through the international fee payment gateway on the admissions portal."),
    ("Can a parent pay the fee on behalf of a student?","Yes, parents can pay using the student's portal login or through a bank challan mentioning the student's enrolment number."),
    ("What is the annual increase in fees?","Fee revision is decided by the university finance committee annually. The revised structure is published before each academic year."),
    ("Is there a development fee charged separately?","Yes, a one-time development fee is charged at the time of admission and is non-refundable."),
    ("What is the fine for library book overdue?","An overdue fine is charged per book per day beyond the return date. Check the library notice board for the current fine schedule."),
    ("Is transport fee included in the main fee?","Transport fee is optional and charged separately based on the route selected by the student."),
    ("How do I get a no dues certificate from the finance department?","Clear all dues, then apply at the finance counter. No dues certificate is issued within 2 working days."),
    ("Can I pay the fee from abroad?","International payments can be made via SWIFT transfer. Contact the finance office for account details and transfer instructions."),
    ("Are there any hidden charges in the fee structure?","The published fee structure includes all mandatory charges. Optional services like transport and hostel are charged separately."),
    ("What is the process for fee correction if the wrong amount was paid?","Approach the finance office immediately with proof of payment. Excess amounts are adjusted in the next semester fee cycle."),
    # Scholarships (30)
    ("What scholarships are available for meritorious students?","Merit scholarships are awarded to top rankers in each department. Check the scholarship portal for eligibility and application deadlines."),
    ("What is the income limit for need-based scholarship?","The family income limit for need-based scholarships is as per government guidelines, typically below 2.5 lakh per annum."),
    ("When does the scholarship portal open?","The scholarship portal opens at the start of each academic year. Notifications are sent via university email and the portal."),
    ("What documents are required for scholarship application?","Required documents include income certificate, caste certificate if applicable, previous year mark sheet, bank passbook copy, and Aadhaar card."),
    ("Is there a scholarship for differently-abled students?","Yes, a dedicated scholarship is available for differently-abled students. Submit a valid disability certificate with your application."),
    ("How is the scholarship amount disbursed?","Approved scholarship amounts are directly credited to the student's registered bank account within 30 working days of approval."),
    ("Can I apply for more than one scholarship?","You may apply for multiple scholarships but may receive only one government-funded scholarship as per policy."),
    ("What is the renewal process for scholarship?","Renew your scholarship each academic year by maintaining the required CGPA and resubmitting income and other updated documents."),
    ("How do I check my scholarship application status?","Log in to the scholarship portal with your application ID to check the current status of your application."),
    ("What is the minimum CGPA required to maintain a scholarship?","Most merit scholarships require a minimum CGPA of 7.0. Refer to the specific scholarship terms for exact criteria."),
    ("What happens if I fail to maintain the CGPA for scholarship?","Failure to maintain the required CGPA results in scholarship suspension for one semester. You may reapply after improving your CGPA."),
    ("Is there an SC/ST scholarship available?","Yes, SC/ST students may apply for government post-matric scholarships. Apply through the national scholarship portal with university verification."),
    ("How do I get my scholarship certificate?","Scholarship certificates are issued by the scholarship cell upon request after the scholarship amount has been disbursed."),
    ("What is the PM Vidyalakshmi scholarship?","PM Vidyalakshmi is a government scholarship for students of recognised institutions. Apply online at the official government scholarship portal."),
    ("Is there a minority scholarship?","Yes, minority community students may apply for central and state government minority scholarships. Documents include minority community certificate."),
    ("Can I transfer my scholarship to a different bank account?","Bank account changes require a formal request to the scholarship cell along with a new passbook copy and cancelled cheque."),
    ("What is the sports scholarship?","Sports scholarships are awarded to students with outstanding achievements at state or national level. Apply with relevant certificates to the sports department."),
    ("Is there a scholarship for girls in STEM?","Yes, specific scholarships for female students in science and technology programmes are available. Check the scholarship portal for details."),
    ("What should I do if scholarship money is not credited?","Contact the scholarship cell with your disbursement reference number. They will coordinate with the nodal bank for resolution."),
    ("Is a fresh application required every year?","Yes, a fresh application must be submitted each academic year for most scholarships, including updated income and performance documents."),
    ("What is the deadline for scholarship application?","Scholarship deadlines are published on the portal at the beginning of each semester. Late applications are not accepted."),
    ("Can a scholarship student also avail of a fee waiver?","Scholarship and fee waiver are separate schemes. Consult the finance department to understand how they can be combined."),
    ("What is the Central Sector Scholarship?","The Central Sector Scholarship is for students from families with income below 8 lakh per year who scored above 80% in 12th board exams."),
    ("How do I apply for an education loan instead of a scholarship?","Education loans are available through nationalised banks. The university provides income and bonafide certificates for loan applications."),
    ("Is the scholarship taxable?","Most government scholarships are exempt from income tax. Consult a tax professional for specific advice based on your situation."),
    ("What is the duration of merit scholarship?","Merit scholarships are renewed annually for the entire duration of the programme, subject to maintaining the required academic performance."),
    ("Can a student with backlog apply for scholarship?","Most scholarships require a clean academic record. Students with active backlogs are generally not eligible for merit scholarships."),
    ("What is the university's own scholarship programme?","The university offers institutional scholarships funded by its own corpus for top performers. Details are published at the start of each year."),
    ("How do I request a scholarship verification letter?","Apply at the scholarship cell with your award letter. A verification letter is issued within 3 working days for bank or external use."),
    ("What happens to my scholarship if I take a break from studies?","Scholarship is suspended during the break period and may be reinstated upon resumption based on re-evaluation of eligibility."),
    # Placements (30)
    ("When do campus placements begin?","Campus placement season typically begins in October for final year students. Registration opens in September on the placement portal."),
    ("What is the minimum CGPA for placement registration?","The general minimum CGPA requirement is 6.0, though individual companies may set higher criteria. Check company-specific requirements on the portal."),
    ("How do I register on the placement portal?","Visit the placement portal, log in with your university credentials, complete your profile, upload your resume, and submit for verification."),
    ("What companies participated in placements last year?","A list of companies that visited campus last year is available on the placement portal under the past recruiters section."),
    ("Is there any pre-placement training?","Yes, the placement cell conducts training in aptitude, technical skills, group discussions, and mock interviews before placement season."),
    ("What is the highest package offered last year?","The highest package offered in the last placement cycle is published in the placement report available on the university website."),
    ("Can students from all branches register for placements?","Yes, all final year students who meet the eligibility criteria can register for campus placements regardless of their branch."),
    ("How do I update my resume on the placement portal?","Log in to the placement portal, go to your profile, and upload the latest version of your resume in PDF format."),
    ("Is off-campus placement assistance provided?","The placement cell shares off-campus opportunities via email and portal notifications. Students are encouraged to apply independently as well."),
    ("What is the process after getting a placement offer?","After receiving an offer letter, submit a copy to the placement cell and attend the pre-joining formalities as instructed by the company."),
    ("Can I participate in placements if I have a backlog?","Most companies do not allow students with active backlogs to participate. Clear your backlogs before the placement season begins."),
    ("How long does the offer letter take to arrive?","Offer letters are typically issued within 30 to 60 days of selection. Contact the company HR through the placement cell if delayed."),
    ("Are internship opportunities provided through the placement cell?","Yes, the placement cell coordinates paid internship programmes with partner companies. Opportunities are listed on the placement portal."),
    ("What is the dress code for placement interviews?","Formal business attire is expected. Specific guidelines are shared by the placement cell before each company's interview schedule."),
    ("Can I accept multiple job offers?","Accepting multiple offers and reneging is strictly prohibited. Students who renege on an offer may be debarred from future placements."),
    ("What documents do I need for placement registration?","Resume, CGPA certificate, identity proof, and recent photographs are required. Some companies may request additional documents."),
    ("Is there a placement guarantee?","The university does not guarantee placement but makes best efforts to invite companies across sectors for campus recruitment."),
    ("What happens during a pre-placement talk?","Companies present their organisation, job profile, compensation, and selection process. Attendance is often mandatory for registered students."),
    ("Can I participate in placements after completing my degree?","Placement eligibility is generally restricted to students enrolled in their final year. Alumni placement support may be available separately."),
    ("How is the placement cell connected to companies?","The placement cell maintains relationships with HR teams across industries. Alumni networks and industry tie-ups are key to bringing companies on campus."),
    ("What sectors visit campus for placements?","Sectors include IT, core engineering, banking, finance, consulting, FMCG, and public sector units depending on the available programmes."),
    ("Is there a mock aptitude test available?","Yes, the placement training programme includes regular mock aptitude tests. Additional resources are shared on the placement portal."),
    ("Can I request placement cell support for a startup offer?","Yes, the placement cell can assist in verifying startup offers and guiding you through the acceptance process."),
    ("What is a PPO and how do I get one?","A Pre-Placement Offer is given by companies to outstanding interns. Perform well in your internship to secure a PPO."),
    ("Are government job notifications shared by the placement cell?","Yes, government job and exam notifications are shared on the placement notice board and student portal."),
    ("How is placement data reported by the university?","Placement data including number of students placed, companies visited, and average and highest packages is published in the annual placement report."),
    ("Can I request a reference letter from the placement cell?","Yes, the placement cell issues experience and reference letters for students who completed company-assigned projects or internships through the cell."),
    ("What is the notice period for placement interviews?","Companies typically give 3 to 5 days notice before interviews. Ensure your placement portal notifications are active."),
    ("Is there any fee for placement registration?","Placement registration is free for all eligible final year students. No fees are charged for participation in campus placement drives."),
    ("What support is available for students who are not placed?","The placement cell offers extended support through additional drives, career counselling, and skill development workshops for unplaced students."),
    # Attendance (20)
    ("What is the minimum attendance requirement?","A minimum of 75% attendance is required in each subject to be eligible to appear in end semester examinations."),
    ("How do I check my attendance on the portal?","Log in to the student portal and navigate to the Attendance section to view subject-wise attendance percentage."),
    ("What is the process for attendance regularisation?","Submit an attendance regularisation application to the HOD with supporting documents such as medical certificate or event participation proof."),
    ("Is medical leave counted in attendance?","Medical leave may be condoned with a valid medical certificate submitted within 7 days of joining back. Decision rests with the HOD."),
    ("What happens if my attendance falls below 75%?","Students below 75% are debarred from sitting in end semester exams unless attendance is condoned by the competent authority."),
    ("Can I get attendance for participating in university events?","Yes, attendance may be granted for university-sanctioned events. Submit the participation certificate to your department."),
    ("How is attendance recorded?","Attendance is recorded biometrically or manually by faculty at the start of each class and updated on the portal daily."),
    ("Is there an attendance relaxation for sports students?","Yes, students representing the university at state or national level may get attendance relaxation as per the sports policy."),
    ("Who do I contact if my attendance is not updated on the portal?","Contact your class teacher or department coordinator with the specific dates. Portal entries are corrected within 48 hours."),
    ("What is the attendance policy for online classes?","Online class attendance is recorded via the learning management system. Joining and active participation are counted as attendance."),
    ("Can I get attendance for NCC or NSS activities?","NCC and NSS camp attendance may be considered for condonation. Submit the camp participation certificate to your HOD."),
    ("Is there a grace for one extra absent day?","No automatic grace is given. Attendance condonation is at the discretion of the department based on valid reasons only."),
    ("What is proxy attendance and what are the consequences?","Proxy attendance means marking present on behalf of an absent student. It is a serious disciplinary offence resulting in suspension."),
    ("How do I apply for on-duty attendance?","Submit an on-duty application to your department with supporting documents before or immediately after the event."),
    ("Is attendance considered in internal marks?","In many programmes, attendance contributes a small percentage to internal assessment marks. Check your course regulations."),
    ("What is the attendance requirement for lab sessions?","Lab attendance requirements are the same as theory, at 75% or above. Missing lab sessions may affect practicals assessment."),
    ("Can I appeal an attendance decision?","Yes, attendance-related appeals can be submitted to the Dean of Academics within 7 days of receiving the debarment notice."),
    ("How is attendance calculated for a student who joined late?","Attendance is calculated from the date of joining for late admissions, not from the start of the semester."),
    ("Are attendance records shared with parents?","Yes, attendance alerts are sent to registered parent contact details when attendance falls below 75% in any subject."),
    ("What is the policy for students on internship regarding attendance?","Students on approved internships are marked on-duty for the internship period. Submit the internship offer letter to your department."),
    # Library (20)
    ("What are the library timings?","The central library is open Monday to Saturday, 8 AM to 8 PM. On Sundays and holidays, timings are 10 AM to 4 PM."),
    ("How many books can I borrow at a time?","Undergraduate students can borrow up to 3 books, postgraduate students up to 5 books, and research scholars up to 8 books simultaneously."),
    ("What is the loan period for library books?","The standard loan period is 14 days for students and 30 days for faculty. Renewal is possible if no other reservation exists."),
    ("How do I renew a library book?","Log in to the library portal, go to My Loans, and click Renew. Renewal can also be done in person at the circulation desk."),
    ("What is the fine for overdue books?","An overdue fine is charged per book per day after the due date. Check the library notice board for the current fine amount."),
    ("Does the library provide access to online journals?","Yes, the library subscribes to databases like IEEE, Scopus, Springer, and JSTOR. Access is available on campus or via VPN off campus."),
    ("How do I access e-resources from home?","Use the university VPN client with your student credentials to access all subscribed e-resources from off campus."),
    ("Can I request a book that is not available in the library?","Yes, submit a book purchase request on the library portal. The library committee reviews requests periodically."),
    ("How do I issue a library no dues certificate?","Return all borrowed books, clear any fines, and apply at the library counter. No dues certificate is issued within one working day."),
    ("Is there a reading room available in the library?","Yes, the library has a quiet reading room with seating for over 100 students, available during library hours."),
    ("Can I access previous year question papers in the library?","Yes, previous year question papers are available both in the physical reserve section and digitally on the library portal."),
    ("What is the process for inter-library loan?","Submit an inter-library loan request at the reference desk. The library coordinates with network libraries to source the required material."),
    ("Are newspapers and magazines available in the library?","Yes, a wide range of national newspapers and subject-specific magazines are available in the periodicals section."),
    ("How do I find a specific book in the library?","Use the Online Public Access Catalogue on the library portal to search by title, author, subject, or ISBN."),
    ("Can final year students extend their book loan period?","Final year students may request an extended loan period during their project work on approval by the chief librarian."),
    ("Is there a digital library section?","Yes, the digital library section has dedicated computers for accessing e-books, research databases, and past dissertations."),
    ("How do I report a damaged book?","Report damaged books to the circulation desk immediately. Replacement cost may be charged if damage occurred during your loan period."),
    ("Are audio-visual resources available in the library?","Yes, the media section of the library has audio-visual resources including lecture recordings and documentary DVDs."),
    ("What is the process for donating books to the library?","Book donations are accepted at the library front desk. Donated books are assessed and added to the collection if relevant."),
    ("Is the library accessible for differently-abled students?","Yes, the library has ramp access, and the staff assist differently-abled students with material retrieval and accessibility support."),
    # Transport (15)
    ("What bus routes are available from the university?","The university operates buses on multiple routes covering major areas. Route maps are available on the transport office notice board."),
    ("How do I apply for a university bus pass?","Submit a transport application form at the transport office at the beginning of each semester with the route fee."),
    ("What are the bus timings for the morning route?","Morning buses depart from designated stops between 7 AM and 8 AM. Check the transport schedule on the notice board for your route."),
    ("Is there a late bus available for evening classes?","Late buses are available for students with evening classes. Schedule is updated at the start of each semester."),
    ("What should I do if I miss the university bus?","The university is not responsible for missed buses. Students are advised to reach the bus stop at least 5 minutes before departure."),
    ("Is the transport fee refundable if I do not use the bus?","Transport fee is refundable on a pro-rata basis if formally surrendered before the mid-semester date."),
    ("How is the bus route fee determined?","Bus route fee is based on the distance from the boarding point to the university. Fee slabs are available at the transport office."),
    ("Can I change my bus route mid-semester?","Route changes are permitted at the start of a new semester. Mid-semester changes are allowed only in exceptional cases."),
    ("Is there a student concession on public transport?","The transport office helps students apply for government-issued student concession passes for public buses and trains."),
    ("What is the contact number for the transport office?","The transport office contact details are available on the university website under the Administrative Offices section."),
    ("Are GPS-tracked buses available?","Yes, university buses are GPS-tracked. You can view live bus locations on the university transport app."),
    ("Is private vehicle parking available on campus?","Designated parking areas for two-wheelers and four-wheelers are available on campus. Students must register their vehicles at the security office."),
    ("What happens if a bus breaks down mid-route?","The transport office is notified immediately and a replacement vehicle is arranged. Students are informed via the university notification system."),
    ("Is there a transport facility for exam days?","Special transport arrangements are made on exam days if exams are held on Sundays or public holidays. Check the exam notice for details."),
    ("Can I request a new bus route?","You may submit a route addition request to the transport office with a minimum of 20 student signatures from the proposed pickup area."),
    # Certificates (15)
    ("How do I apply for a bonafide certificate?","Apply at the administrative office or through the student portal. Bonafide certificates are issued within 2 working days."),
    ("What is the process for obtaining a character certificate?","Submit a character certificate request at the administrative office with your ID. It is issued within 3 working days after HOD approval."),
    ("How do I apply for a migration certificate?","Apply at the examination section after completing or withdrawing from the programme. Submit the prescribed form with a fee and NOC."),
    ("What documents are needed for a provisional degree certificate?","You need a no dues certificate, fee clearance, library clearance, and an application form to obtain the provisional degree certificate."),
    ("How long does it take to get the original degree certificate?","Original degree certificates are awarded at the annual convocation. Digital copies may be available earlier through the examination portal."),
    ("Can I get an apostille on my university certificates?","For apostille, you need to get the certificates attested by the state education department. The university provides the original attested copies."),
    ("How do I verify my degree certificate online?","Degree certificate verification is available through the examination portal using the certificate number and date of issue."),
    ("What is the fee for a duplicate degree certificate?","A fee is charged for issuing a duplicate degree certificate. Contact the examination section for the current fee structure."),
    ("How do I get my transcripts sent to a foreign university?","Apply at the examination section with the foreign university's address. Official transcripts are sent in sealed envelopes."),
    ("Is a digital version of my certificates available?","Yes, digitally signed certificates are available on the DigiLocker platform linked to your Aadhaar or student ID."),
    ("How do I get a medium of instruction certificate?","Apply at the academic section with a written request. The certificate is issued within 5 working days."),
    ("What is the process for name correction on a degree certificate?","Submit a court affidavit and documentary proof of the correct name. The university forwards to the examination board for correction."),
    ("How do I get an attestation of my documents by the university?","Submit original documents with copies at the administrative office. Attestation is done within 2 working days."),
    ("Can I get an experience certificate for internship done through the university?","If the internship was arranged through the placement cell, apply there for an experience letter or coordinate with the company directly."),
    ("Is a WES evaluation supported by the university?","The university provides required documents for WES evaluation. Contact the international office for the procedure and timeline."),
    # IT & Portal (15)
    ("How do I reset my university portal password?","Visit the portal login page and click Forgot Password. An OTP will be sent to your registered email or mobile number."),
    ("My university email is not working. What should I do?","Contact the IT helpdesk with your enrolment number. Email accounts are restored within one working day."),
    ("How do I access the student portal for the first time?","Use the credentials provided during admission. Your username is typically your enrolment number and default password is your date of birth."),
    ("Is there a mobile app for the student portal?","Yes, the UniPortal mobile app is available on Google Play and the Apple App Store. Log in with your portal credentials."),
    ("What should I do if my biometric attendance is not registering?","Report to the department coordinator immediately. Manual attendance will be recorded and the biometric issue escalated to the IT department."),
    ("How do I connect to the university Wi-Fi?","Select the university SSID, log in with your student ID and portal password. Contact IT support if you face connection issues."),
    ("What is the data limit on university Wi-Fi?","A fair usage policy applies on student Wi-Fi. The daily data limit is published on the IT department notice board."),
    ("How do I submit assignments on the learning management system?","Log in to the LMS with your portal credentials, navigate to your course, and upload the assignment before the due date."),
    ("How do I access recorded lectures?","Recorded lectures are available on the LMS under each course. Access is available for the duration of the semester."),
    ("What should I do if I cannot access an e-journal from home?","Install the university VPN client and connect before accessing subscribed e-resources. Contact IT support if VPN issues persist."),
    ("How do I update my mobile number on the portal?","Log in to the portal, go to Profile Settings, and update your mobile number. An OTP verification is required for the change."),
    ("What is the procedure if I receive a phishing email on my university account?","Do not click any links. Forward the email to the IT security team and report it through the IT helpdesk portal immediately."),
    ("Is there a 24-hour IT helpdesk?","The IT helpdesk is available during working hours, Monday to Saturday. Emergency IT support contacts are listed on the university website."),
    ("How do I get software required for my course?","The IT department provides licensed software through the campus agreement. Submit a software request at the IT helpdesk."),
    ("Can I access the student portal outside India?","Yes, the student portal is accessible globally. Use the university VPN for accessing restricted internal resources from abroad."),
    # Academic General (20)
    ("What is the grading system used by the university?","The university follows a 10-point CGPA grading system. Grade letters range from O for outstanding to F for fail."),
    ("How do I apply for a leave of absence from the programme?","Submit a leave of absence application to the dean with valid reasons. Approval is at the discretion of the academic committee."),
    ("What elective subjects are available this semester?","The list of electives offered each semester is published on the academic portal. Register for electives during the registration window."),
    ("How do I change my elective subject after registration?","Elective change requests are accepted only during the first week of the semester. Contact the academic section with your preference."),
    ("What is the process for withdrawing from the programme?","Submit a withdrawal application to the registrar's office. Fee refund will follow the university refund policy."),
    ("Is there a provision for credit transfer from another university?","Credit transfer is possible for approved exchange students. Credits are evaluated by the academic committee on a case-by-case basis."),
    ("How are CGPA and SGPA calculated?","SGPA is the grade point average for a single semester weighted by credit hours. CGPA is the cumulative average across all semesters."),
    ("What is the maximum number of subjects I can register for?","Students can register for a maximum of seven subjects per semester including lab and elective subjects."),
    ("How do I get the syllabus for my programme?","The syllabus is available on the academic portal under your programme page and can also be obtained from the department office."),
    ("Is there a provision for semester freeze?","Semester freeze is available in genuine cases such as medical emergencies. Apply to the dean with supporting documents before the semester starts."),
    ("What is the dual degree programme?","Dual degree programmes allow students to earn two degrees simultaneously. Check the academic portal for available combinations and eligibility."),
    ("How do I join a student club or society?","Club registrations are open at the start of each academic year. Visit the student affairs office or club stalls during orientation week."),
    ("What is the anti-plagiarism policy?","The university uses plagiarism detection software. Submissions above the allowed similarity threshold result in grade penalties or disciplinary action."),
    ("How do I access the academic calendar?","The academic calendar is published at the start of each academic year and is available on the university website and student portal."),
    ("Is there any provision for a fast-track degree?","Fast-track degree options are not available for regular students. Additional courses can be taken as open electives or audit courses."),
    ("What is an audit course?","An audit course is taken for learning without credit. No grades are awarded, but attendance and completion may be noted on the transcript."),
    ("How do I request a recommendation letter from a faculty member?","Approach the faculty member personally with your request at least 3 weeks before the deadline. Provide your CV and a brief description of the need."),
    ("What is the process for changing my registered programme?","Programme change requests are considered at the end of the first year based on merit and seat availability. Apply to the dean's office."),
    ("Are there any short-term certification courses offered?","Yes, the university offers short-term certification courses in collaboration with industry partners. Check the continuing education portal for listings."),
    ("How do I get a consolidated mark sheet?","Apply for a consolidated mark sheet at the examination section after completing all semesters. It is issued within 7 working days."),
    # Medical & Wellness (15)
    ("Where is the university medical centre located?","The medical centre is located near the main administrative block. It provides first aid, basic OPD services, and referrals to empanelled hospitals."),
    ("What are the medical centre timings?","The medical centre is open Monday to Saturday from 9 AM to 5 PM. Emergency contact numbers are displayed at the hostel notice boards."),
    ("Is there a counsellor available on campus?","Yes, the student wellness centre has qualified counsellors available for appointment. You can book a session through the student portal."),
    ("What should I do in a medical emergency on campus?","Call the campus emergency number displayed across campus. The medical team and security staff will respond immediately."),
    ("Is health insurance provided to students?","Yes, group health insurance is provided to all enrolled students. Insurance details and the claim process are available at the medical centre."),
    ("How do I get a medical certificate from the university doctor?","Visit the medical centre with your student ID. The doctor will issue a certificate after examination. It is accepted for attendance condonation."),
    ("Is there a pharmacy on campus?","Yes, a pharmacy is located adjacent to the medical centre and is stocked with basic medicines and first aid supplies."),
    ("Are there yoga or fitness classes available?","Yes, yoga and fitness classes are conducted by the sports department. Schedule and registration details are on the student portal."),
    ("What mental health resources are available for students?","The student wellness centre offers individual counselling, group sessions, and stress management workshops throughout the academic year."),
    ("How do I report a fellow student who appears to be in distress?","Contact the student wellness centre or any faculty member immediately. Anonymous reporting is also available on the student portal."),
    ("Is dental care available at the medical centre?","Basic dental consultation is available at the medical centre on specific days. A referral is provided for advanced dental treatment."),
    ("What is the procedure for claiming health insurance?","Obtain a claim form from the medical centre, fill it with treatment details and bills, and submit to the insurance desk for processing."),
    ("Are COVID or vaccination camps organised on campus?","The university coordinates with district health authorities for periodic vaccination camps. Notifications are sent via the student portal."),
    ("What anti-ragging helpline numbers are available?","The University Grants Commission anti-ragging helpline number is 1800-180-5522. The university also has an internal anti-ragging committee."),
    ("Is there a grievance redressal mechanism for student welfare?","Yes, the student affairs office handles welfare grievances. Students can also submit complaints online through the student portal grievance section."),
]


def gen_faq():
    path = os.path.join(OUT, "faq_dataset.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["question","answer"])
        w.writeheader()
        for q, a in FAQ_DATA:
            w.writerow({"question": q, "answer": a})
    print(f"✓ faq_dataset.csv      ({len(FAQ_DATA)} rows)")


# ── Run all ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    gen_student_queries()
    gen_intents()
    gen_priorities()
    gen_sentiments()
    gen_departments()
    gen_faq()
    print("\nAll datasets saved to:", OUT)
