from typing import Dict, List, Tuple


def clean_template(item: Tuple) -> Tuple[str, List[str]]:
    '''Utility for cleaning template texts'''
    item = list(item)
    summary = item[1][0].replace("\n", "").replace(" " * 8, "")
    template = item[1][1].replace("\n", "").replace(" " * 8, "")
    item = (item[0], [summary, template])
    return item


def clean_question(item: Tuple) -> Tuple[str, str]:
    '''Utility for cleaning question texts'''
    item = list(item)
    question = item[1].replace("\n", "").replace(" " * 4, "")
    item = (item[0], question)
    return item


ABOUT_CYPHERCRESCENT = {
    "1" : [
        '''
        ABOUT CYPHERCRESCENT SUMMARY
        ''',
        '''
        ABOUT CYPHERCRESCENT
        CypherCrescent is a fast-growing wholly indigenous company that provides services in
        energy, technology and human capacity development with core expertise in mathematical
        modelling, petroleum engineering, software development and oil & gas asset management
        consulting. We are committed to providing innovative and cost-effective business
        intelligence solutions for E&P companies to increase production, reduce cost and enhance
        HSE across their hydrocarbon value chain.
        '''
    ],
}


OUR_TEAM = {
    "1" : [
        '''
        OUR TEAM SUMMARY
        ''',
        '''
        Our dedicated team of experts are drawn from diverse backgrounds, with skills and experience garnered
        from the E&P industry, project management, information technology and academia. Our motivation is
        anchored on the desire to continuously innovate and create values by closing existing technical gaps in the
        E&P value chain. The team’s expertise covers areas such as geoscience, petrophysics, reservoir engineering,
        production technology, well completions, production operations, mathematical modelling, advanced
        analytics, economic analyses and software development.
        • Our experts and consultants are in-country and can be available to provide face-to-face
        support at client’s offices within 24 hours of notice.
        • Our competitive edge is continually shaped by uncompromising product & service quality, and
        passionate client support services.
        '''
    ],
}

OUR_COMMITMENT = {
    "1" : [
        '''
        OUR COMMITMENT SUMMARY
        ''',
        '''
        We are committed to partnering and assisting our clients to gain valuable understanding of their assets
        through the integration of acquired data and in-depth technical insight. This we achieve through the
        provision of cost-effective business intelligence solutions, which does not only provide a collaborative
        platform but also improves operational excellence through optimal allocation of resources and
        elimination of non-productive time (NPT)
        '''
    ],
}

OUR_CLIENTS = {
    "1" : [
        '''
        Our clients are [industry leaders] who believe in leveraging [data], [technology], and [innovation]
        to drive [business growth]. We have rendered services and collaborated with them in
        deploying [data-driven transformation] across their operations. These clients include:
 '''
    ]
}

INTRODUCTION_TEMPLATES = {
    "1": [
        '''
        INTRODUCTION SUMMARY ONE
        ''',
        '''
        The [Organization's Name] annual business planning process is a key
        strategic activity which mirrors the [Name of the Organization] CHQ planning cycle.
        In this vein, [Organization's Name] usually embarks upon a [Number]-year strategic
        planning process which involves an asset-by-asset reserve evaluation,
        opportunities screening, economic evaluation of projects as well as budget needs which will enable
        [Organization's Name] meet the financial and production targets set by [Organization's CHQ]
        within the stipulated period.
        The business planning process involves reserve update, production and cost forecasting, economic analysis,
        portfolio optimization, capital allocation, work program creation, budget development, and
        business performance monitoring. In a bid to find a smarter and more efficient way of achieving this goal
        at the barest minimum man-hour possible, the planning team sought the services of a renowned technology
        provider – [Technology Provider's Name], to customize and deploy its enterprise planning and budgeting
        system for [Organization's Name], hereafter, referred to as Enterprise Planning System (EPS).
        [Technology Provider's Name] in collaboration with the highly skilled professionals in the [Organization's Name]
        P&C department have embarked on intensive research to customize and deploy a software application with robust
        functionalities to adequately automate the business planning process at [Organization's Name].

        The system will add the following benefits to [Organization's Name]'s business planning operations:

        • Significant man-hour savings in delivering strategic business plans
        • Quick sensitivity analyses on the impact of project addition/removal on the production, cost, and revenue projections
        • Robust audit trail for all business planning elements – reserves, projects portfolio, project readiness checklist, budgets, etc.
        • Single-source-of-truth information on inputs and outputs in the business planning process as well as democratization of key
        planning information to all stakeholders (with view permission)

        '''
    ],
    "2": [
        '''
        INTRODUCTION SUMMARY TWO
        ''',
        '''
        Finding an efficient way to manage the large amount of data required for effective [well and reservoir management (WRM)] is one of
        the greatest challenges of [industry or niche] practice. The time spent in searching and validating [industry-specific] related
        datasets reduces the time available for actual analysis to support [business or project] decisions. This is because based on current
        industry practice, there is little or no integration at the level of [relevant discipline] interpretations and databases are not
        democratized implying that data are still hosted in different locations, different applications and sometimes, dissimilar and incompatible formats.
        The resulting data inconsistency, low data integrity, and error-prone analysis exposes the [company or operator] to high risk of missed opportunities
        for [specific goal or outcome].
        [Your Company Name] prides itself as the only [industry or niche] tech company that has developed a [industry-specific] tool with the ability to
        integrate related disciplines at data level. This ensures that a consistent story emanates from [specific discipline] review exercises leading to
        robust value creation outcomes.
        The aim of this project is to improve the success rate of [specific goal] and improve [related outcome] via [Describe the key action or focus of the project].
        The scope of work comprises [mention key project activities, e.g., data gathering, data QA/QC, data migration, integration of [discipline] interpretations,
        and [specific workflow] to aid [relevant goal or task].
        The project will commence with [initial project activities] and [describe the anticipated benefits of these activities].

        2.0 [Project-specific Background]
        Based on information available in public domain, [Project Name] is a [description of the project location or context]. The [field or site] [further details on the project location].
        According to [industry-specific source], the [project context or field] is [additional details about the context]. [Provide relevant statistics or data about the project context].
        [Optional: Add more sections or details as needed for your specific proposal.]

        '''
    ],
}

OVERVIEW_TEMPLATE = {
    "1" : [
        '''OVERVIEW TEMPLATE SUMMARY
        ''',
        '''
        /* Insert the Title of Your Proposal Here */
        OVERVIEW OF [Project Name]

        [Insert Brief Introduction or Context Relevant to Your Proposal]
        [Description of the Challenge or Problem Your Proposal Addresses]

        For [Target Audience, e.g., Companies, Organizations, Industries] looking to [Objective, e.g., Optimize Production, Improve Efficiency], our [Your Company Name]'s
        [Solution/Service Name] offers a [Brief Description of the Solution].

        [Optional: Highlight any unique features or benefits of your solution.]

        [Optional: Provide statistics or evidence supporting the effectiveness of your solution.]

        With [Your Company Name], you can:
        1. [Benefit/Feature 1]
        2. [Benefit/Feature 2]
        3. [Benefit/Feature 3]

        [Include a call to action, contact information, or any next steps if necessary.]

        [Optional: Insert Relevant Figures, Charts, or Visual Aids]

        [Optional: Add any additional information, testimonials, or references as needed.]

        [Closing statement and thank your audience for considering your proposal.]
        '''
    ],
}

OVERVIEW_QUESTIONS = {
    "QUESTION 1": ''' How can your company's Cutting-Edge Production Optimization System effectively address the manufacturing efficiency challenges faced by oil companies in their quest to optimize production, and what distinguishes this solution from others in the market?'''
}

INTRODUCTION_DESCRIPTION_QUESTIONS = {
    "Question 1": '''
    What are the key benefits and objectives of implementing the Enterprise Planning System (EPS)
    in your organisation's business planning process?
    ''',
    "Question 2": "How will the implementation of Cyphercescent's digitalised tools enhance data integration and consistency, ultimately leading to improved success rates for [specific goal] and [related outcome]?"

}

PROBLEM_TEMPLATE = {
    "1" : [
        '''
        This problem states that The oil and gas industry has abundant data but
        struggles with effectively validating and utilizing it, particularly for
        timely well production monitoring and allocation due to reliance on periodic
        tests that miss crucial in-between changes
        ''',
        '''
        In [Industry or Niche], we are data rich but information poor. Real-time data
        gathering is not an issue, but validation and usage of such data is. For example,
        [Specific Problem or Challenge in Your Industry].
        Traditionally this problem is often attempted using [Traditional Solution].
        This method cannot capture important changes in between [Specific Events or Tests]
        [Explanation of Why Current Method is Inadequate].
        ''',
    ],
    "2" : [
        '''
        This problem asks how a forward-thinking company leverage its history of innovation
        to revolutionize a key aspect of its industry.
        ''',
        '''
        Template
        '''
    ],
    "3" : [
        '''
        Third problem
        ''',
        '''
        Third problem template
        '''
    ],
    "4" : [
        '''
        Fourth problem
        ''',
        '''
        Fourth problem template
        '''
    ],
}

PROBLEM_DESCRIPTION_QUESTIONS = {
    "QUESTION 1": '''
    How can the oil and gas industry better validate and utilize its abundant data for
    well production monitoring and allocation?
    ''',
    "QUESTION 2": '''
    What methods can be employed to address the industry's reliance on periodic tests
    and capture crucial in-between changes more effectively?
    ''',
    "QUESTION 3": '''
    QUESTIONS
    ''',
    "QUESTION 4": '''
    QUESTIONS
    ''',
}

PROPOSED_SOLUTION_TEMPLATE = {
    "1": [
        '''
        The proposed solution combines physical models with real-time data-driven neural networks
        (PINNs) to monitor and surveil well and network flows in the oil and gas industry,
        utilizing the benefits of PINNs in capturing physical laws and enhancing data-driven learning.
        ''',
        '''
        The solution we are proposing combines (i) [Describe the First Component of Your Solution] and
        (ii) [Describe the Second Component of Your Solution] for [Purpose or Objective of Your Solution].
        [More Details About How the Two Components Work Together]. Model in (i) is used to prime and
        bootstrap model (ii).[Explain More About Component (ii) and How It Overcomes Data Limitations and
        Enhances Learning Process].
        '''
    ],
    "2": [
        '''
        SECOND PROPOSED SOLUTION DESCRIPTION
        ''',
        '''
        SECOND PROPOSED SOLUTION TEMPLATE
        '''
    ],
    "3": [
        '''
        THIRD PROPOSED SOLUTION DESCRIPTION
        ''',
        '''
        THIRD TEMPLATE
        '''
    ],
    "4": [
        '''
        FOURTH PROPOSED SOLUTION DESCRIPTION
        ''',
        '''
        FOURTH TEMPLATE
        '''
    ],

}

PROPOSED_SOLUTION_QUESTIONS = {
   "QUESTION 1": '''
    How can the combination of physical models and real-time data-driven neural networks, specifically PINNs,
    improve the monitoring of well and network flows in the oil and gas industry?
    ''',
    "QUESTION 2": '''
    What specific challenges or limitations may arise when implementing this solution, and how do you plan to
    address them effectively?
    ''',
    "QUESTION 3": '''
    QUESTIONS
    ''',
    "QUESTION 4": '''
    QUESTIONS
    '''
}

IMPORTANCE_TEMPLATE = {
        "1": [
        '''
        fIRST IMPORTANCE DESCRIPTION
        ''',
        '''
        IMPORTANCE TEMPLATE
        '''
    ],
    "2": [
        '''
        SECOND IMPORTANCE DESCRIPTION
        ''',
        '''
        SECOND IMPORTANCE TEMPLATE
        '''
    ],
    "3": [
        '''
        THIRD IMPORTANCE DESCRIPTION
        ''',
        '''
        THIRD TEMPLATE
        '''
    ],
    "4": [
        '''
        FOURTH IMPORTANCE DESCRIPTION
        ''',
        '''
        FOURTH TEMPLATE
        '''
    ],
}

IMPORTANCE_DESCRIPTION_QUESTION ={
    "QUESTION 1": '''
    QUESTION
    ''',
    "QUESTION 2": '''
    QUESTIONS
    ''',
    "QUESTION 3": '''
    QUESTIONS
    ''',
    "QUESTION 4": '''
    QUESTIONS
    ''',
}

BENEFITS_TEMPLATE = {
    "1": [
        '''
        fIRST BENEFIT DESCRIPTION
        ''',
        '''
        BENEFIT TEMPLATE
        '''
    ],
    "2": [
        '''
        SECOND BENEFIT DESCRIPTION
        ''',
        '''
        SECOND BENEFIT TEMPLATE
        '''
    ],
    "3": [
        '''
        THIRD BENEFIT DESCRIPTION
        ''',
        '''
        THIRD TEMPLATE
        '''
    ],
    "4": [
        '''
        FOURTH BENEFIT DESCRIPTION
        ''',
        '''
        FOURTH TEMPLATE
        '''
    ],
}

BENEFITS_DESCRIPTION_QUESTION = {
    "QUESTION 1": '''
    QUESTION
    ''',
    "QUESTION 2": '''
    QUESTIONS
    ''',
    "QUESTION 3": '''
    QUESTIONS
    ''',
    "QUESTION 4": '''
    QUESTIONS
    ''',
}
EXECUTIVE_SUMMARY_TEMPLATE = {
     "1": [
        '''
        fIRST SUMMARY DESCRIPTION
        ''',
        '''
        [Squeeze More Metrics (e.g., Barrels or SCFs)] from your [Resource/Asset/Reservoir] is [Positive Descriptor] business,
        especially in a [Challenging Economic Environment]. A thorough understanding of [Specific Aspects of your Operation]
        and potential [Short and Long-Term Improvement Opportunities] invariably leads to [Positive Outcome].
        Extracting [Critical Information/Key Insights] from a [Large Volume of Relevant Data] is one of the greatest challenges
        in [Industry/Field] practice. This is largely because [Reason for Data Challenges]. [Data Challenges] often result
        in [Negative Consequences], making it crucial to leverage [Cutting-Edge Technologies] and the expertise of highly skilled
        [Industry Experts].
        By submitting this proposal, [Your Company Name] seeks to provide [Type of Expertise] with the purpose of [Project Objective]
        at [Cost Level].
        Managing the [Size/Complexity] of data required for effective [Operations/Management] is one of the greatest challenges of
        [Industry/Field] practice. The time spent in [Searching/Validating/Processing] [Relevant Data] leaves little time for
        [Specific Task]. This is because [Reason for Data Challenges]. [Data Challenges] often result in [Negative Consequences],
        making it essential to explore [Cutting-Edge Solutions].
        In the quest to address [Industry/Field] challenges, [Your Company Name] introduced an innovative service - [Project/Service Name],
        with the aim of [Objective/Goal]. This will enable [Target Audience] enhance their opportunities for [Specific Improvement] and
        [Additional Benefit].
        This project would ensure that the right [Type of Data] is available to the right [Key Stakeholders] tasked with [Responsibility] at
        the right time
        to guarantee [Desired Outcome]. [Integration/Implementation] is the first of the [Number]-stage scope of work detailed in this proposal.
        The project encompasses a [Number]-stage process which includes [Stage 1], [Stage 2], [Stage 3], [Stage 4], and [Stage 5].

        '''
    ],
    "2": [
        '''
        SECOND SUMMARY DESCRIPTION
        ''',
        '''
        At [Company Name], we apply innovative [digital technologies/processes] to narrow the gaps of assumptions, enhance processes to optimize
        [asset review/study] outcomes.
        We infuse the elements of [digitalization/WRFM analytics] to provide reliable value creation that leads to remarkable value realization.
        To achieve this, we leverage our proprietary technology, [Proprietary Technology Name] – an innovative end-to-end integrated and
        collaboration technology, developed with the principle of integration of WRFM interpretations ([IoI]) and powered robust analytics
        functionalities for efficient well, reservoir & facility management. With [Proprietary Technology Name]-driven production system review,
        we have successfully connected data to proposals that leads to higher intervention success rates for our clients.
        This proposal outlines the methodology to be applied in reviewing the existing well, reservoir and facility data for your delineated field(s).
        It also shows how the historic data provided will be digitized, dynamic well and reservoir models would be developed and integrated;
        and how advanced analytics would be used to identify and scientifically ranked to select well intervention candidates for
        [short term/long term] [goal] for [Client Name].
        The project will comprise of the following stages in line with the scope of work:
        a) Data gathering and digitization
        b) Data wrangling
        c) Well and reservoir modeling with [MBAL/PROSPER]
        d) Integration of WRFM data and interpretations using [Proprietary Technology Name] Enterprise,
        e) Production optimization opportunity identification using [Proprietary Technology Name] Analytics
        f) Detailed review/screening of identified opportunities
        g) Well intervention proposal generation
        In addition to our proprietary solutions- [Proprietary Technology Name], and [Additional Proprietary Solution], a third-party tool -[Third-Party Tool Name]
        suite will be used by our vastly experienced experts to deliver a reliable production optimization review and proposal to [Client Name] at a net cost of [Cost].

        '''
    ],
    "3": [
        '''
        THIRD SUMMARY DESCRIPTION
        ''',
        '''
        [Your Project Name] is an innovative technology-driven service designed to provide a digital platform that supports efficient [E&P Asset Management] in [Your Niche].
        It offers a smarter way of managing the plethora of data churned out daily by [Companies/Niche], embedded with advanced asset surveillance & analytics capabilities.
        This invariably reveals hidden opportunities and threats behind the plethora of data available to your [Organization/Company]. The service is designed to help [Companies/Niche]
        stay efficient and focused on [Specific Focus Area] in order to identify high-value opportunities to [Optimize Value/Improve Outcomes] from [Assets/Resources].
        The technology employed is a highly innovative [Technology Type] tool for [End-to-End Surveillance, Documentation, Well Integrity, Production, and Reservoir Performance Management].
        The project will be executed using [Your Technology/Software Name], a robust analytical tool that enables informed business decision-making through its unique features and functionalities.

        The service scope covers:
        ▪ Establishing a single source of truth for all [Niche] related data through [Enterprise Data Integration (EDI)] technology.
        ▪ Provision of a smart solution ([Your Technology/Software Name]) to assist teams operate their [Assets/Resources] efficiently on a single digital platform with a shared database.
        ▪ Identifying data gaps and propose recommendations for gap closure plans.
        ▪ Creating workflows and embedded analytics features to automate routine processes and drive efficient [Focus Area] reviews for quick [Type of Decision] making.

        Benefits to [Your Target Audience]:
        ▪ Maintain a centralized digital & analytics-enabled database for efficient [Asset/Resource Management].
        ▪ Enhance [Teams/Professionals] collaboration with a shared [Niche] database.
        ▪ Eliminate complexity of [Data Type] retrieval for informed decision making.
        ▪ Easily identify hidden opportunities for [Specific Improvement] from [Your Assets/Resources].
        ▪ Increase the success rate of [Type of Activities] by leveraging a curated database of integrated [Niche] data.
        ▪ Seamlessly carry out [Analysis Type] and quick integrated [Forecast Type] analysis to aid effective [Type of Planning] and [Scheduling Type].

        We look forward to working with [Your Target Audience] on this project to achieve the above objectives while establishing a mutually beneficial relationship.

        '''
    ],
    "4": [
        '''
        FOURTH SUMMARY DESCRIPTION
        ''',
        '''
        CypherCrescent (CCL) is the foremost WRM technology company in Nigeria. Her proprietary SEPAL software is currently revolutionalising WRM practice across the industry in Nigeria
        with a clear strategy to expand beyond the frontiers of the country. CCL’s integration of interpretation is poised to deepen WRM practice in Shell Nigeria.
        Following a successful presentation to a select audience of Asset Development representatives, Central WRFM team and IT, CCL’s is pleased to present this proposal targeted at
        democratizing Shell Nigeria’s WRFM and set them up for improved WRM practice enabled by data-level integration of interpretations from various concerned disciplines of WRM.
        Shell has selected EA field for the pilot application of this technology.
        The scope covers 66 wells, 10 of which democratized free of charge. The discounted cost for the remaining 56 wells is USD245,000 after due consideration for the vantage position
        Shell Nigeria will offer to the growth and further development of the technology.

        '''
    ],
}
EXECUTIVE_SUMMARY_QUESTION = {
    "QUESTION 1": '''
    How can we enhance metrics extraction from our resource/reservoir in a challenging economic environment by leveraging specific aspects of our operation and identifying short and
    long-term improvement opportunities, ultimately leading to positive outcomes, given the data challenges in our industry, and what cutting-edge technologies and expertise will be
    employed in the proposed project to manage data effectively?
    ''',
    "QUESTION 2": '''
    "How can cyphercrescent leverage its innovative digital technologies/processes and Technology to optimize your well, reservoir, and facility data, with a short term/long term focus goal,
    in order to enhance value realization, and what key stages are involved in this project's scope of work?"
    ''',
    "QUESTION 3": '''
    How can Cyphercrescent's digital technology  contribute to improving your efficiency and decision-making processes?.
    ''',
    "QUESTION 4": '''
    How will the implementation of CCL's SEPAL software and data-level integration of interpretations impact the overall effectiveness and efficiency of Shell Nigeria's WRM practice,
    and what specific benefits and challenges are expected in the pilot application in the EA field?
    ''',
}

section_templates: Dict[str, List[Dict]] = {
    "introduction": [
        INTRODUCTION_TEMPLATES, INTRODUCTION_DESCRIPTION_QUESTIONS
    ],
    "Problems": [
        PROBLEM_TEMPLATE, PROBLEM_DESCRIPTION_QUESTIONS
    ],
    "proposed_solution": [
        PROPOSED_SOLUTION_TEMPLATE, PROPOSED_SOLUTION_QUESTIONS
    ],
    "importance": [
        IMPORTANCE_TEMPLATE, IMPORTANCE_DESCRIPTION_QUESTION
    ],
    "benefits": [
        BENEFITS_TEMPLATE, BENEFITS_DESCRIPTION_QUESTION
    ],
    "executive_summary": [
        EXECUTIVE_SUMMARY_TEMPLATE, EXECUTIVE_SUMMARY_QUESTION
    ]
}
