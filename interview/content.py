"""Accreditation interview prep for a Software Engineering student: English sentence ↔ Arabic sentence, line by line.
[brackets] = fill in your own real detail before the interview."""

INTRO = [
    ("Good morning, and welcome to our university.", "صباح الخير، وأهلًا بكم في جامعتنا."),
    ("My name is Abdulrahman Aburumman.", "اسمي عبد الرحمن أبورمان."),
    ("I am a Software Engineering student in my [third] year.", "أنا طالب هندسة برمجيات في سنتي [الثالثة]."),
    ("I am interested in building real software that solves real problems.", "أنا مهتم ببناء برمجيات حقيقية تحل مشاكل حقيقية."),
]

TIPS = [
    ("Speak slowly and clearly. Short sentences are better.", "تكلم ببطء ووضوح. الجمل القصيرة أفضل."),
    ("Be honest. They value honest answers more than perfect ones.", "كن صادقًا. هم يقدّرون الإجابة الصادقة أكثر من الإجابة المثالية."),
    ("Give one real example whenever you can.", "اذكر مثالًا حقيقيًا واحدًا كلما استطعت."),
    ("It is OK to say what can be improved, politely.", "لا بأس أن تذكر ما يمكن تحسينه، بأدب."),
    ("Replace every [bracket] with your real information before the interview.", "استبدل كل [قوس] بمعلوماتك الحقيقية قبل المقابلة."),
]

PHRASES = [
    ("Could you repeat the question, please?", "ممكن تعيد السؤال لو سمحت؟"),
    ("Do you mean …?", "هل تقصد …؟"),
    ("Let me give you an example.", "دعني أعطيك مثالًا."),
    ("In my experience, …", "من تجربتي، …"),
    ("I'm not 100% sure, but I believe …", "لست متأكدًا 100%، لكن أعتقد أن …"),
    ("That's a good question.", "هذا سؤال جيد."),
    ("One thing that could be improved is …", "من الأشياء التي يمكن تحسينها …"),
]

SECTIONS = [
 ("1. Educational Goals and Study Program", "الأهداف التعليمية والبرنامج الدراسي", [
  ("Why did you choose this study program?", "لماذا اخترت هذا التخصص؟", [
    ("I chose Software Engineering because I enjoy building things with code.", "اخترت هندسة البرمجيات لأنني أستمتع ببناء الأشياء بالبرمجة."),
    ("Software is part of every field today: health, banks, education and industry.", "البرمجيات موجودة اليوم في كل مجال: الصحة والبنوك والتعليم والصناعة."),
    ("This program teaches not only coding, but how to build reliable software as a team.", "هذا التخصص لا يعلّم البرمجة فقط، بل كيف نبني برمجيات موثوقة كفريق.")]),
  ("What are the main educational objectives of your program?", "ما الأهداف التعليمية الرئيسية لتخصصك؟", [
    ("The program prepares us to analyze problems and design software solutions.", "التخصص يجهّزنا لتحليل المشاكل وتصميم حلول برمجية."),
    ("It covers the full software life cycle: requirements, design, coding, testing and maintenance.", "يغطي دورة حياة البرمجيات كاملة: المتطلبات والتصميم والبرمجة والاختبار والصيانة."),
    ("It also builds teamwork, communication and professional ethics.", "ويطوّر أيضًا العمل الجماعي والتواصل وأخلاقيات المهنة.")]),
  ("What knowledge and skills do you expect to acquire upon graduation?", "ما المعارف والمهارات التي تتوقع اكتسابها عند التخرج؟", [
    ("Technical skills: programming, data structures, databases, web and mobile development.", "مهارات تقنية: البرمجة وهياكل البيانات وقواعد البيانات وتطوير الويب والموبايل."),
    ("Engineering skills: software design, testing and project management.", "مهارات هندسية: تصميم البرمجيات والاختبار وإدارة المشاريع."),
    ("Soft skills: teamwork, presentation and solving problems under deadlines.", "مهارات شخصية: العمل الجماعي والعرض وحل المشاكل ضمن مواعيد محددة.")]),
  ("Are you familiar with the Program Learning Outcomes (PLOs)?", "هل تعرف مخرجات التعلم للبرنامج (PLOs)؟", [
    ("Yes. They describe what every graduate should be able to do.", "نعم. هي تصف ما يجب أن يستطيع كل خريج فعله."),
    ("For example: solve complex engineering problems, design software that meets requirements, work in teams, and communicate effectively.", "مثلًا: حل مشاكل هندسية معقدة، وتصميم برمجيات تحقق المتطلبات، والعمل ضمن فريق، والتواصل بفعالية."),
    ("They are published [on the department website / in the study plan].", "وهي منشورة [على موقع القسم / في الخطة الدراسية].")]),
  ("Do you think your program prepares you for the labor market?", "هل تعتقد أن تخصصك يؤهلك لسوق العمل؟", [
    ("Yes, mostly. The practical projects and field training are very useful.", "نعم، في الغالب. المشاريع العملية والتدريب الميداني مفيدة جدًا."),
    ("For example, I worked as the software engineer of a team in a startup pitch competition (GEW Jordan).", "مثلًا، عملت كمهندس برمجيات في فريق شارك بمسابقة ريادية (GEW Jordan)."),
    ("We built a working simulator for an AI blood-delivery system called DAMI.", "بنينا محاكيًا يعمل لنظام ذكاء اصطناعي لتوصيل الدم اسمه دَمي."),
    ("More industry partnerships and internships would make it even better.", "المزيد من الشراكات مع الشركات والتدريب العملي سيجعله أفضل.")]),
 ]),
 ("2. Contents of Study", "محتوى المساقات والخطة الدراسية", [
  ("Are the courses relevant to your field of specialization?", "هل المساقات مرتبطة بتخصصك؟", [
    ("Yes. The courses build on each other step by step.", "نعم. المساقات مبنية على بعضها خطوة بخطوة."),
    ("We start with programming basics, then data structures, then software design and testing.", "نبدأ بأساسيات البرمجة، ثم هياكل البيانات، ثم تصميم البرمجيات والاختبار."),
    ("Everything comes together in the graduation project.", "وكل شيء يجتمع في مشروع التخرج.")]),
  ("Is there a good balance between theoretical and practical learning?", "هل يوجد توازن بين النظري والعملي؟", [
    ("Yes. Most core courses have labs or a practical project.", "نعم. معظم المساقات الأساسية فيها مختبرات أو مشروع عملي."),
    ("In [course name], we built a complete [web application] in a team.", "في مساق [اسم المساق] بنينا [تطبيق ويب] كاملًا ضمن فريق."),
    ("Some theory courses could have more practical examples.", "بعض المساقات النظرية يمكن أن تحتوي أمثلة عملية أكثر.")]),
  ("Are course contents regularly updated to reflect technological developments?", "هل يتم تحديث المساقات لتواكب التطور التقني؟", [
    ("Yes, in many courses. Instructors use modern tools like [Git, cloud, AI tools].", "نعم، في كثير من المساقات. المدرسون يستخدمون أدوات حديثة مثل [Git والسحابة وأدوات الذكاء الاصطناعي]."),
    ("Technology changes very fast, so continuous updating is important.", "التقنية تتغير بسرعة كبيرة، لذلك التحديث المستمر مهم.")]),
  ("Do you work on practical projects and real-world problems?", "هل تعمل على مشاريع عملية ومشاكل حقيقية؟", [
    ("Yes. My best example is DAMI, a system for managing and delivering blood in emergencies.", "نعم. أفضل مثال هو دَمي، نظام لإدارة الدم وتوصيله في الطوارئ."),
    ("I built the interactive simulator: dashboard, emergency request, drone tracking and alerts.", "بنيت المحاكي التفاعلي: لوحة القيادة والطلب الطارئ وتتبع الدرون والتنبيهات."),
    ("I applied what I learned: requirements, design, user interface and testing.", "طبّقت ما تعلمته: المتطلبات والتصميم وواجهة المستخدم والاختبار.")]),
  ("Are there any important topics you think should be added?", "هل هناك مواضيع مهمة تقترح إضافتها؟", [
    ("I would suggest more on Artificial Intelligence for software engineers.", "أقترح المزيد عن الذكاء الاصطناعي لمهندسي البرمجيات."),
    ("Also DevOps and cloud deployment, and cybersecurity in practice.", "وأيضًا DevOps والنشر على السحابة، والأمن السيبراني بشكل عملي."),
    ("These are in high demand in the job market.", "هذه المهارات مطلوبة جدًا في سوق العمل.")]),
 ]),
 ("3. Organization of Study", "تنظيم الدراسة", [
  ("Is the study plan clear and well organized?", "هل الخطة الدراسية واضحة ومنظمة؟", [
    ("Yes. We have a study plan that shows all courses by year and semester.", "نعم. لدينا خطة دراسية تبيّن كل المساقات حسب السنة والفصل."),
    ("It is available [on the university website / from the department].", "وهي متوفرة [على موقع الجامعة / من القسم].")]),
  ("Are course schedules announced in advance?", "هل يتم الإعلان عن الجداول مسبقًا؟", [
    ("Yes, before registration starts, so we can plan our semester.", "نعم، قبل بدء التسجيل، لنخطط لفصلنا."),
    ("Sometimes there are small changes, but we are informed in time.", "أحيانًا توجد تغييرات بسيطة، لكن يتم إبلاغنا في الوقت المناسب.")]),
  ("Are prerequisites and course registration procedures clear?", "هل المتطلبات السابقة وإجراءات التسجيل واضحة؟", [
    ("Yes. Prerequisites are shown in the study plan and in the registration system.", "نعم. المتطلبات السابقة موضحة في الخطة وفي نظام التسجيل."),
    ("If I have a problem, my academic advisor helps me.", "وإذا واجهت مشكلة يساعدني مرشدي الأكاديمي.")]),
  ("Are examinations and project deadlines reasonably distributed?", "هل الامتحانات ومواعيد المشاريع موزعة بشكل معقول؟", [
    ("Mostly yes. Exam dates are announced early.", "في الغالب نعم. مواعيد الامتحانات تُعلن مبكرًا."),
    ("Near the end of the semester, many projects can come together, so planning is important.", "في نهاية الفصل قد تجتمع مشاريع كثيرة، لذلك التخطيط مهم.")]),
  ("Can you complete your study program within the expected duration?", "هل يمكنك إنهاء تخصصك في المدة المتوقعة؟", [
    ("Yes, if I follow the study plan, I can graduate in [four] years.", "نعم، إذا التزمت بالخطة أستطيع التخرج خلال [أربع] سنوات."),
    ("Summer semesters also help if a student needs extra time.", "والفصول الصيفية تساعد أيضًا إذا احتاج الطالب وقتًا إضافيًا.")]),
 ]),
 ("4. Exams", "الامتحانات وأساليب التقييم", [
  ("What types of assessment are used in your courses?", "ما أنواع التقييم المستخدمة؟", [
    ("We have midterm and final exams, quizzes, assignments, lab work and projects.", "لدينا امتحانات منتصف ونهاية الفصل، واختبارات قصيرة، وواجبات، وعمل مختبر، ومشاريع."),
    ("In practical courses, the project and presentation are a big part of the grade.", "في المساقات العملية يكون المشروع والعرض جزءًا كبيرًا من العلامة.")]),
  ("Are grading criteria explained at the beginning of each semester?", "هل تُشرح أسس التقييم في بداية كل فصل؟", [
    ("Yes. The course syllabus shows how the grade is distributed.", "نعم. خطة المساق توضح كيف تتوزع العلامة."),
    ("For example: midterm 30%, final 40%, projects and assignments 30%.", "مثلًا: منتصف الفصل 30%، والنهائي 40%، والمشاريع والواجبات 30%.")]),
  ("Do exams reflect the topics and skills taught in the courses?", "هل تعكس الامتحانات ما تم تدريسه؟", [
    ("Yes. Exams are based on the course material and the learning outcomes.", "نعم. الامتحانات مبنية على مادة المساق ومخرجات التعلم."),
    ("Practical exams test what we did in the labs.", "والامتحانات العملية تختبر ما عملناه في المختبرات.")]),
  ("Do you receive feedback on your exam results and assignments?", "هل تحصل على تغذية راجعة على نتائجك وواجباتك؟", [
    ("Yes. We can see our marked exams and discuss them with the instructor.", "نعم. نستطيع رؤية أوراقنا المصححة ومناقشتها مع المدرس."),
    ("Feedback on projects helps me improve my next work.", "والتغذية الراجعة على المشاريع تساعدني على تحسين عملي القادم.")]),
  ("What procedures are available if you want to appeal an exam grade?", "ما إجراءات الاعتراض على علامة؟", [
    ("First, I talk to the instructor during office hours.", "أولًا، أتحدث مع المدرس في الساعات المكتبية."),
    ("If needed, I submit an official grade appeal [through the registration system / the department] within the allowed period.", "وإذا لزم الأمر أقدّم اعتراضًا رسميًا [عبر نظام التسجيل / القسم] خلال المدة المسموحة.")]),
 ]),
 ("5. Counseling and Support for Students", "الإرشاد الأكاديمي ودعم الطلبة", [
  ("Do you have an assigned academic advisor?", "هل لديك مرشد أكاديمي؟", [
    ("Yes, my academic advisor is Dr. [name].", "نعم، مرشدي الأكاديمي هو الدكتور [الاسم]."),
    ("I can contact my advisor by email, in person, or [through the university system].", "أستطيع التواصل مع المرشد بالإيميل أو شخصيًا أو [عبر نظام الجامعة].")]),
  ("How often do you meet your academic advisor?", "كم مرة تلتقي بمرشدك؟", [
    ("At least once every semester, mainly before registration.", "مرة على الأقل كل فصل، غالبًا قبل التسجيل."),
    ("And any time I need advice.", "وفي أي وقت أحتاج فيه نصيحة.")]),
  ("How does your advisor help you with registration and planning?", "كيف يساعدك المرشد في التسجيل والتخطيط؟", [
    ("My advisor checks my study plan and suggests the right courses for each semester.", "المرشد يراجع خطتي الدراسية ويقترح المساقات المناسبة لكل فصل."),
    ("This makes sure I take prerequisites in the right order.", "وهذا يضمن أنني آخذ المتطلبات السابقة بالترتيب الصحيح.")]),
  ("Are instructors available during office hours?", "هل المدرسون متاحون في الساعات المكتبية؟", [
    ("Yes. Office hours are announced at the start of the semester.", "نعم. الساعات المكتبية تُعلن في بداية الفصل."),
    ("Many instructors also answer questions by email.", "وكثير من المدرسين يجيبون على الأسئلة بالإيميل أيضًا.")]),
  ("What support is provided to students facing academic difficulties?", "ما الدعم المقدم للطلبة المتعثرين؟", [
    ("Students with low grades get follow-up from their advisor.", "الطلبة ذوو المعدلات المنخفضة يحصلون على متابعة من مرشدهم."),
    ("There is also help from instructors and [tutoring sessions].", "وهناك مساعدة من المدرسين و[جلسات دعم دراسي]."),
    ("Excellent students can get recognition like [the dean's list].", "والطلبة المتفوقون يحصلون على تقدير مثل [لوحة الشرف].")]),
  ("How can you submit complaints or suggestions?", "كيف تقدم شكوى أو اقتراحًا؟", [
    ("I can talk to my advisor or the head of department.", "أستطيع التحدث مع مرشدي أو رئيس القسم."),
    ("There is also an official channel [online complaints system / suggestions box].", "وهناك قناة رسمية [نظام شكاوى إلكتروني / صندوق اقتراحات].")]),
 ]),
 ("6. Conditions of Study", "البيئة التعليمية وظروف الدراسة", [
  ("Are classrooms and laboratories adequately equipped?", "هل القاعات والمختبرات مجهزة جيدًا؟", [
    ("Yes, our computer labs have the computers and software we need.", "نعم، مختبرات الحاسوب فيها الأجهزة والبرمجيات التي نحتاجها."),
    ("Sometimes some labs could use newer computers.", "أحيانًا بعض المختبرات تحتاج أجهزة أحدث.")]),
  ("Do you have access to the software and equipment required?", "هل تحصل على البرمجيات والأدوات المطلوبة؟", [
    ("Yes. We use tools like [Visual Studio Code, Java/Python, Git, MySQL].", "نعم. نستخدم أدوات مثل [Visual Studio Code وJava/Python وGit وMySQL]."),
    ("Many tools are free for students, so we can also use them at home.", "وكثير من الأدوات مجانية للطلاب فنستخدمها في البيت أيضًا.")]),
  ("Is the university library useful for your studies?", "هل المكتبة مفيدة لدراستك؟", [
    ("Yes. It has books and access to [online databases / e-books].", "نعم. فيها كتب ووصول إلى [قواعد بيانات إلكترونية / كتب رقمية]."),
    ("It is also a quiet place to study.", "وهي أيضًا مكان هادئ للدراسة.")]),
  ("Are study spaces suitable for individual and group work?", "هل أماكن الدراسة مناسبة للعمل الفردي والجماعي؟", [
    ("Yes, there are spaces for both.", "نعم، هناك أماكن للاثنين."),
    ("More group-study rooms would help during project season.", "المزيد من غرف الدراسة الجماعية سيساعد في وقت المشاريع.")]),
  ("Is the workload manageable throughout the semester?", "هل ضغط الدراسة مقبول خلال الفصل؟", [
    ("Generally yes, with good time management.", "بشكل عام نعم، مع تنظيم جيد للوقت."),
    ("The end of the semester is busier because of projects and finals.", "نهاية الفصل أكثر ضغطًا بسبب المشاريع والامتحانات النهائية.")]),
  ("Are students satisfied with the overall learning environment?", "هل الطلبة راضون عن البيئة التعليمية؟", [
    ("Overall, yes. Instructors are supportive and the environment is positive.", "بشكل عام نعم. المدرسون داعمون والبيئة إيجابية."),
    ("Students also have chances to join competitions and activities, like the startup competition I joined.", "وللطلبة فرص للمشاركة في مسابقات وأنشطة، مثل المسابقة الريادية التي شاركت فيها.")]),
 ]),
 ("7. Study Abroad", "الدراسة بالخارج والتبادل الأكاديمي", [
  ("Are you aware of any student exchange or study abroad opportunities?", "هل تعرف فرص تبادل طلابي أو دراسة بالخارج؟", [
    ("Yes, I have heard about programs like Erasmus+ and university partnerships.", "نعم، سمعت عن برامج مثل Erasmus+ وشراكات الجامعة."),
    ("[The international office] announces these opportunities.", "و[مكتب العلاقات الدولية] يعلن عن هذه الفرص.")]),
  ("Does the university provide information about international mobility programs?", "هل توفر الجامعة معلومات عن برامج التنقل الدولي؟", [
    ("Yes, through [emails, the website and the international office].", "نعم، من خلال [الإيميل والموقع ومكتب العلاقات الدولية]."),
    ("I think more information sessions for students would be helpful.", "أعتقد أن المزيد من الجلسات التعريفية للطلاب سيكون مفيدًا.")]),
  ("Have you participated in any international exchange or academic activity?", "هل شاركت في تبادل دولي أو نشاط أكاديمي؟", [
    ("Not an exchange yet, but I would like to.", "ليس تبادلًا بعد، لكنني أرغب بذلك."),
    ("I participated in the Jordan Students Pitch Competition, part of Global Entrepreneurship Week.", "شاركت في مسابقة Jordan Students Pitch، وهي جزء من أسبوع الريادة العالمي.")]),
  ("Can credits earned abroad be recognized toward your degree?", "هل يمكن احتساب الساعات التي تُدرس بالخارج؟", [
    ("Yes, if the course is equivalent to a course in our study plan.", "نعم، إذا كان المساق معادلًا لمساق في خطتنا."),
    ("The student should get approval from the department before traveling.", "ويجب أن يأخذ الطالب موافقة القسم قبل السفر.")]),
  ("What support would you need to participate in an exchange program?", "ما الدعم الذي تحتاجه للمشاركة في برنامج تبادل؟", [
    ("Mainly scholarships or financial support.", "بشكل رئيسي منح أو دعم مالي."),
    ("Also clear guidance on course equivalence and help with visas.", "وأيضًا إرشاد واضح عن معادلة المساقات ومساعدة في التأشيرة."),
    ("Germany would be very interesting for me because of its strong engineering.", "ألمانيا مهمة جدًا بالنسبة لي لقوتها في الهندسة.")]),
 ]),
]

CLOSING = [
    ("Thank you for your questions and for visiting our university.", "شكرًا على أسئلتكم وعلى زيارتكم لجامعتنا."),
    ("I'm proud of my program, and I believe it will keep improving.", "أنا فخور بتخصصي، وأؤمن أنه سيستمر بالتحسن."),
]
