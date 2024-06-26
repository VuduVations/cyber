'''
Takes a predefined list of words.
Appends numerical suffixes (00 to 09) to each word.
Prepends special characters (! and @) to each formatted word.
Writes the resulting formatted words to a file named formatted_words.lst.

Produces:
!protected00
@protected00
!protected01
@protected01
...
!ultricies09
@ultricies09
'''

words = [
    "protected", "Research", "Oxytocin", "Paracetamol", "Cortisol", "appointment", "Cardiology", "February", "providing",
    "treatment", "commonly", "hospital", "Template", "tooplate", "Pregnancy", "Saturday", "Copyright", "Laboratory",
    "Departments", "Insurance", "healthier", "Exercise", "customised", "Lifestyle", "Balanced", "nutrition", "Benefits",
    "clinical", "innovative", "technology", "experience", "multidisciplinary", "surgeons", "researchers", "specialists",
    "together", "medicine", "pressing", "findings", "medicines", "treatments", "President", "Weronika", "Phillips",
    "released", "reaction", "connections", "stressful", "situations", "reliever", "alleviate", "referred", "response",
    "APPOINTMENT", "Department", "Additional", "location", "affiliated", "professionals", "establishing", "maintaining",
    "qualified", "physicians", "committed", "tailored", "specific", "requirements", "official", "Medicalmedical",
    "porttitor", "imperdiet", "vestibulum", "molestie", "Phasellus", "vulputate", "Vestibulum", "vehicula", "placerat",
    "venenatis", "eleifend", "Technology", "Consultant", "thmredteam", "Professional", "interdum", "condimentum",
    "pellentesque", "fringilla", "volutpat", "tincidunt", "Maecenas", "lobortis", "facilisis", "pulvinar", "dignissim",
    "Suspendisse", "Facebook", "maecenas", "voluptate", "Introducing", "Categories", "pharetra", "Curabitur", "consequat",
    "ultricies"
]

formatted_words = []

for word in words:
    for num in range(10):
        formatted_words.append(f"!{word}{num:02d}")
        formatted_words.append(f"@{word}{num:02d}")

with open("formatted_words.lst", "w") as file:
    file.write("\n".join(formatted_words))
