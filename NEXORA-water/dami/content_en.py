"""English edition of all DAMI content (mirrors content.py and the DAMI record in data/p25_31.py)."""

NAME = "DAMI"
NAME_AR = "دَمي"
SLOGAN = "The right blood unit, to the right hospital, before it's requested… and by drone when there's no time"
ONE_LINER = ("A Jordanian AI platform that forecasts hospitals' blood needs, rebalances stock before it expires, "
             "calls the right donors, and in emergencies launches a cooled medical drone that carries blood from the blood bank to the hospital in minutes.")
CLOSER = "Because blood that arrives late… doesn't arrive."

PROBLEM = ("Blood banks face a hard equation: shortages of certain blood types when they are needed, while units expire elsewhere. "
           "In major accidents or shortage crises, hospitals need urgent units from the blood bank or another hospital, but vehicles get stuck in traffic "
           "or delayed on mountain and remote roads, and in severe bleeding every minute counts.")
EVIDENCE = ["Blood and its components have limited shelf life; some, such as platelets, expire within days.",
            "Major accidents cause sudden spikes in demand for specific types, especially O negative.",
            "Drone delivery of blood has been operating worldwide for years; the best-known example is Zipline in Rwanda and Ghana.",
            "General donation campaigns don't precisely target the types that are short."]
SOLUTION = ("A three-layer smart platform: (1) it forecasts demand for each blood type at each hospital and rebalances stock between hospitals before it expires; "
            "(2) it calls eligible nearby donors by type and last-donation date; (3) in emergencies it launches a medical drone with a smart cooling box (2–6°C) "
            "that carries units from the blood bank, or the nearest hospital holding the type, to the hospital in need, with live tracking of temperature, position and ETA.")
AI = ["Time-series forecasting of demand per blood type", "Optimization of stock distribution and best-source selection",
      "Drone route planning around weather and restricted zones", "Selecting the donors most likely to respond"]
DATA = ["Blood bank inventories", "Request history", "Donor database (with consent)", "Weather and airspace data", "Temperature sensor readings from transport boxes"]
WOW = ("A simulated accident on a main road: a hospital requests 6 units of O negative immediately. Within seconds the system picks the blood bank and shows the comparison: "
       "car 34 minutes vs drone 9 minutes. The drone takes off on the map, the box holds steady at 4°C, and eligible donors receive messages to restock.")
RISKS = [("Sensitivity of health data", "Formal partnership, encryption and consent"),
         ("Licensing drone flights in Jordanian airspace", "Start with simulation, then a pilot route approved by the Civil Aviation Regulatory Commission and security authorities"),
         ("Maintaining the cold chain", "Medically certified boxes with live temperature monitoring and alarms"),
         ("Slow government contracting", "Start with private hospitals and corporate sponsorship")]
LEGAL = ("Work in coordination with the Ministry of Health and the National Blood Bank, complying with blood transfusion, cold-chain and data-privacy standards. "
         "Drone operations require permits from the Civil Aviation Regulatory Commission and the relevant security authorities.")
IMPACT = ["Units saved from expiry", "Minutes saved in emergency delivery", "Share of shipments within safe temperature", "Number of active donors"]
MVP = [("1–3", "Realistic synthetic stock and demand data"), ("4–6", "Forecasting, balancing and source-selection models"),
       ("7–9", "Drone simulator and donor app"), ("10–12", "Mass-casualty scenario and a drone test inside a closed campus")]
MARKET = "Assumption: 3 private hospitals in year 1, then 10, then 20, with drone flights starting in year 2 after licensing."
STREAM_NAMES = [("Hospital subscription", "hospital/year"), ("Emergency drone delivery", "flight"),
                ("National dashboard contract", "annual contract"), ("Donor-app sponsorship", "sponsor/year")]
CAPEX_NOTE = "CAPEX"

FACTS = [
    ("35–42 days", "Shelf life of red blood cells stored at 2–6°C"),
    ("5–7 days", "Shelf life of platelets only, so some are wasted unless distributed smartly"),
    ("O negative", "The type requested first in severe bleeding, before the patient's type is known"),
    ("Since 2016", "Drone blood delivery operates in Rwanda, then Ghana and other countries (Zipline)"),
]

LAYERS = [
    ("🧠", "Forecasting & balancing", "A model forecasts 14-day demand for each type at each hospital, warns before shortages, and proposes moving units close to expiry to a hospital that will use them."),
    ("🫂", "Smart donor call-up", "Selects eligible donors (last donation 90+ days ago) who are nearby and most likely to respond, and invites them for exactly the type that's short."),
    ("🚁", "Blood ambulance drone", "In emergencies the system picks the nearest source holding the type, compares drone vs car time, and launches a drone with a smart cooling box and live temperature and position tracking."),
]

MISSION = [
    ("Emergency request", "The hospital requests 6 units of O negative in the app with “critical” priority."),
    ("Source selection", "The system checks live stock and picks the blood bank or the nearest hospital holding the type."),
    ("Launch decision", "Comparison: car 34 min at peak vs drone 9 min; the operator approves with one tap."),
    ("Packing & flight", "Units packed in a 2–6°C cooled box, on a safe route that avoids restricted zones."),
    ("Delivery & restock", "Landing on the hospital pad, receipt and flight temperature confirmed, and donors called to restock."),
]

DRONE_SPEC = [
    ("Type", "Multirotor drone for the pilot, then fixed-wing VTOL for longer distances"),
    ("Payload", "2–4 kg: 4–6 blood units with the cooled box"),
    ("Range & speed", "15–40 km for urban pilots, at 60–90 km/h"),
    ("Cooling box", "Thermal insulation and phase-change material holding 2–6°C, with a temperature logger and live alarm"),
    ("Connectivity", "4G/5G cellular with backup link, streaming position, temperature and battery every second"),
    ("Safety", "Emergency parachute, automatic return on link loss, and geofencing"),
    ("Delivery", "Landing on a dedicated pad on the hospital roof or a small-parachute drop in a safe zone"),
    ("Operations", "A licensed pilot monitors from the operations center, on pre-approved routes"),
]

APP_SCREENS = [
    ("dash", "Dashboard", "Stock of 8 blood types at the blood bank and 7 hospitals, color-coded shortage and expiry alerts, and one-tap transfer or drone request."),
    ("sos", "Emergency drone request", "Best-source selection, drone vs car time comparison, then launch and tracking: temperature, battery, altitude and distance."),
    ("forecast", "Demand forecast", "14-day demand curve per type and hospital with a confidence band, a target stock and a call-up recommendation."),
    ("donors", "Donors", "Selects eligible donors by type, distance and last donation, sends invitations and tracks replies."),
    ("mci", "Mass-casualty mode", "3 hospitals request blood at the same moment; the system dispatches drones automatically and calls donors."),
]

COMPETITION = [
    ("Status quo", "Phone calls between blood banks, transport by car, general donation drives", "Slow in emergencies, expiry waste, no type targeting"),
    ("Blood bank management systems", "Stock records inside one hospital", "No forecasting, no national view, no delivery"),
    ("Zipline (global)", "Drone delivery in Africa and the US", "Not present in Jordan per our preliminary research; focused on delivery only"),
    ("DAMI", "Forecasting + balancing + donors + drone in one platform", "Built for Jordan; starts with simulation and phases into licensed operations"),
]

GTM = [
    ("Phase 1 · Months 0–6", "Prototype and full simulator (ready) + synthetic data + interviews with 10 blood banks and hospitals."),
    ("Phase 2 · Months 6–12", "Software pilot in 3 private hospitals at a discounted subscription: forecasting, balancing and donors."),
    ("Phase 3 · Months 12–24", "Pilot drone route between a blood bank and a hospital after flight permits, with paid flights."),
    ("Phase 4 · Months 24–36", "National dashboard under a government contract, expanding the fleet to remote governorates and mass-casualty response."),
]

FR = [
    ("FR-01", "Show live stock for each type at each site, with the expiry date of every unit."),
    ("FR-02", "Alert automatically when stock drops below the safety level or nears expiry."),
    ("FR-03", "Forecast 14-day demand per type and hospital with a confidence band."),
    ("FR-04", "Propose transferring units between hospitals before they expire."),
    ("FR-05", "Create an emergency request (hospital, type, quantity, priority) from the app."),
    ("FR-06", "Rank possible sources by availability, distance and arrival time."),
    ("FR-07", "Compare drone and car arrival times, accounting for peak traffic."),
    ("FR-08", "Launch a drone mission only after approval by a licensed operator."),
    ("FR-09", "Track position, altitude, speed, battery and box temperature live."),
    ("FR-10", "Alarm immediately if temperature leaves 2–6°C, with a fallback action."),
    ("FR-11", "Confirm receipt and store the full temperature log for every shipment."),
    ("FR-12", "Select eligible donors by type, distance and last donation, and send invitations."),
    ("FR-13", "Mass-casualty mode: automatically distribute simultaneous requests across the fleet."),
    ("FR-14", "Impact reports: units saved, minutes saved, share of safe shipments."),
]

NFR = [
    ("Security & privacy", "Encryption in transit and at rest, role-based access, explicit donor consent."),
    ("Reliability", "99.9% availability for the emergency service, backups, and a manual fallback on any failure."),
    ("Performance", "Source suggestion in under 5 seconds, tracking updated every second."),
    ("Auditability", "Tamper-proof log of every request, decision and flight."),
    ("Usability", "Arabic/English interface; an emergency request in fewer than 4 taps."),
    ("Integration", "APIs for existing blood bank and hospital systems."),
]

BOM = [
    ("Medical multirotor drone, 3–5 kg payload", 2, 11000),
    ("Smart cooling box with phase-change material and temperature logger", 4, 750),
    ("Spare batteries and fast charger", 1, 2000),
    ("Landing pad and ground control station", 1, 3000),
    ("Software platform and forecasting model (development)", 1, 15000),
    ("Donor app (development)", 1, 8000),
    ("Cybersecurity and compliance", 1, 5000),
]

STACK = [
    ("Front end", "Web dashboard + mobile donor app (React / Flutter)"),
    ("Back end", "Python (FastAPI) + PostgreSQL + real-time streaming over WebSocket"),
    ("AI", "Time-series models (Prophet / LightGBM) for forecasting, and mathematical optimization for source selection and fleet dispatch"),
    ("Drone", "Integration via MAVLink with the ground station, plus restricted-zone maps"),
    ("Cooling sensors", "IoT temperature loggers reporting every second over cellular"),
    ("Hosting", "Cloud inside Jordan or the health authority's servers, per data-protection requirements"),
]

LICENSES = [
    ("Civil Aviation Regulatory Commission", "Drone operating permit, approval of routes and licensed pilot, starting with a pilot route."),
    ("Relevant security authorities", "Approvals for flights over residential areas and near sensitive sites."),
    ("Ministry of Health & National Blood Bank", "Partnership agreement and compliance with transfusion and cold-chain standards."),
    ("Data protection", "Privacy policy, donor consent and compliance with the Personal Data Protection Law."),
    ("Insurance", "Civil liability insurance on the fleet and shipments."),
    ("Company registration", "Register a startup and protect the name and trademark."),
]

SUBMISSION = [
    "Full proposal (PDF)", "Business Model Canvas with all nine blocks", "Financial, technical and legal feasibility study",
    "Requirements and equipment document", "Pitch deck PDF + editable PPTX", "5-minute pitch script and expected judge questions",
    "Interactive simulator/app for the live demo", "Fill in university, supervisor and team names on the cover",
    "Check the official competition rules and deadlines with the university",
]

DEMO_DAY = ["Charged laptop with the simulator open in advance (works offline)", "PDF of the deck on a backup USB stick",
            "Rehearse the live scenario 3 times before going in", "Assign roles: who speaks and who runs the simulator",
            "Printed copies of the BMC and summary for the judges", "A timer to stay within 5 minutes"]

SCRIPT = [
    ("0:00–0:30", "Opening (the story)", "“5 p.m., an accident on the Airport Road. A hospital needs 6 units of O negative, now. The car from the blood bank needs 34 minutes in traffic. In severe bleeding, every minute matters.”"),
    ("0:30–1:10", "The problem", "“It's not only accidents. Blood expires: platelets last only 5 to 7 days. So one hospital runs short while units expire at another, and general donation drives don't target the missing type.”"),
    ("1:10–2:00", "The solution", "“We are NEXORA, and this is DAMI: a three-layer platform. It forecasts demand and rebalances stock before it's wasted, calls the right donor, and in emergencies launches a cooled medical drone from the blood bank to the hospital in minutes.”"),
    ("2:00–3:00", "Live demo", "Open the simulator → Emergency drone → “Find best source” → point at drone vs car → “Launch drone now” → point at 4°C → press “Simulate cooling failure” so the judges see the alarm → switch to Mass casualty."),
    ("3:00–3:45", "Business model", "“Our customers are hospitals and the blood bank. We earn from an annual hospital subscription, a fee per emergency flight, a national dashboard contract and donor-app sponsorship. Gross margin in year 3 is about 72%.”"),
    ("3:45–4:30", "Plan & realism", "“We start with software in 3 hospitals, then a pilot drone route approved by the Civil Aviation Regulatory Commission. We know licensing is the biggest challenge, so our plan creates value before the first flight.”"),
    ("4:30–5:00", "Ask & close", "“We are asking for about JOD 90,000 in seed funding and a pilot partnership with a blood bank and a hospital. Because blood that arrives late… doesn't arrive. Thank you.”"),
]

QA = [
    ("Are drones allowed in Jordan?", "They need permits from the Civil Aviation Regulatory Commission and security authorities. That's why we start with simulation and software, then one approved pilot route, and our first year doesn't depend financially on flying."),
    ("How do you keep blood safe in flight?", "A certified box holding 2–6°C, a logger reporting every second, an instant alarm, and a full temperature log delivered with every shipment. Any out-of-range shipment is flagged and not used."),
    ("What if a drone falls?", "Emergency parachute, automatic return on link loss, routes away from crowds, liability insurance, and a licensed pilot monitoring every flight."),
    ("Where will the data come from?", "The prototype runs on realistic synthetic data. In the pilot we connect partner hospitals' stock under a formal agreement, with encryption and consent."),
    ("Why no break-even within 3 years?", "Drones and licensing are an early investment. In the optimistic scenario we break even in month 27. To cut risk we fund the pilot fleet with a health grant or donor partner, so the software side turns profitable faster."),
    ("How are you different from Zipline?", "Zipline is a delivery company. DAMI is a full decision platform: it forecasts, balances and calls donors, and the drone is its emergency layer. We could partner with any drone operator in future."),
    ("Who pays?", "Private hospitals first because they decide faster, then the Ministry of Health through the national dashboard contract, and companies sponsor the donor app as CSR."),
    ("What have you actually built?", "A complete working simulator: stock dashboard, forecasting, donors, emergency drone request with temperature tracking, and mass-casualty mode, plus the business model and feasibility study."),
    ("How many units does a drone carry?", "4–6 units per flight in the pilot, enough for the first emergency need until the larger batch arrives by car."),
    ("What are your success metrics?", "Units saved from expiry, minutes saved in emergencies, share of shipments within safe temperature, and number of active donors."),
]

TEAM = [("Project Lead / AI Lead", "Technical architecture, forecasting models and coordination"),
        ("Data Scientist", "Stock and demand data, and model evaluation"),
        ("Systems Engineer / Drones & IoT", "Drone, cooling box and sensor integration"),
        ("App Developer", "Dashboard, donor app and live demo"),
        ("Business & Pitch Lead", "Health and regulatory partnerships, business model and pitch")]

BMC = dict(
    kp=["Ministry of Health & National Blood Bank", "Private and public hospitals, Royal Medical Services", "Medical drone operators and manufacturers",
        "Civil Aviation Regulatory Commission & security authorities", "Jordan Red Crescent", "Telecom and insurance companies, CSR sponsors"],
    ka=["Building forecasting and balancing models", "Running the emergency ops center and fleet", "Cold-chain and quality management",
        "Running the donor app and call-up campaigns", "Building partnerships and obtaining permits"],
    kr=["Software platform and AI models", "Drone fleet and smart cooling boxes", "Consented donor database",
        "Tech team, licensed pilots and a blood bank expert", "Permits and agreements"],
    vp=["Hospitals: emergency units in minutes instead of half an hour", "Blood banks: less waste by rebalancing before expiry",
        "Ministry: a live national dashboard and mass-casualty readiness", "Donors: invited at the right time and see their impact",
        "Patients: blood available when they need it"],
    cr=["Annual service contract with an account manager", "24/7 emergency operations center", "Monthly impact reports", "Donor community, rewards and badges"],
    ch=["Direct sales to hospital management", "Partnership with the Ministry of Health and the blood bank", "Health conferences and exhibitions",
        "Media campaigns and universities for donors", "Mobile app and web dashboard"],
    cs=["Private hospitals (beachhead)", "Ministry of Health hospitals and Royal Medical Services", "National Blood Bank",
        "Red Crescent and Civil Defense", "Donors (free users)"],
    cost=["Software and AI development", "Drones and cooling boxes, purchase and maintenance", "Insurance, permits and compliance",
          "Team and pilot salaries", "Servers, connectivity and marketing"],
    rev=["Annual hospital subscription: JOD 6,000", "Emergency drone flight fee: JOD 90", "National dashboard contract: JOD 40,000/year",
         "Corporate sponsorship of the donor app: JOD 10,000/year"],
)
BMC_BLOCKS = [("kp", "Key Partnerships"), ("ka", "Key Activities"), ("kr", "Key Resources"), ("vp", "Value Propositions"),
              ("cr", "Customer Relationships"), ("ch", "Channels"), ("cs", "Customer Segments"), ("cost", "Cost Structure"), ("rev", "Revenue Streams")]
ALIGN = ["Supports health-sector readiness for emergencies and mass-casualty events.",
         "Aligns with the digital transformation of health services and data protection.",
         "Reduces waste of a scarce medical resource and improves fair access across governorates.",
         "Builds Jordanian expertise in medical drones that can be exported regionally."]
WHO_PAYS = ["Private hospitals pay the subscription because it cuts waste from expired units and secures rare types.",
            "Hospitals pay the emergency flight fee only when needed, which is less than the cost of delayed care for a bleeding patient.",
            "The Ministry of Health pays the national dashboard contract for emergency and mass-casualty readiness.",
            "Companies sponsor the donor app as CSR and get their brand inside it."]
OPS = ["A small 24/7 operations center with an operator and a licensed pilot on every shift.",
       "Routine drone maintenance, box inspection and monthly temperature-sensor calibration.",
       "Fallback: if flying is not possible (weather, fault), the request automatically switches to road transport from the nearest source.",
       "Training blood bank staff to pack boxes and receive shipments."]
VALIDATION = ["Interview 10–15 blood bank and private hospital managers to test willingness to pay JOD 6,000 per year.",
              "Collect real data on expiry waste rates and current emergency transport times.",
              "Get real quotes for two drones and certified cooling boxes.",
              "Hold an introductory meeting with the Civil Aviation Regulatory Commission to understand the pilot-permit path."]
DISC = ("Financial figures are preliminary planning assumptions set by the team, not market research or supplier quotes, and must be validated before any decision. "
        "“Not available in Jordan” means no equivalent was found in preliminary research. The simulator uses synthetic data and schematic locations.")
