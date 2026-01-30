ACTION_VERBS = {
    'leadership': [
        'Led', 'Directed', 'Managed', 'Supervised', 'Coordinated',
        'Orchestrated', 'Spearheaded', 'Mentored', 'Guided', 'Facilitated'
    ],
    'technical': [
        'Developed', 'Engineered', 'Programmed', 'Designed', 'Architected',
        'Built', 'Implemented', 'Coded', 'Debugged', 'Optimized'
    ],
    'analytical': [
        'Analyzed', 'Evaluated', 'Assessed', 'Investigated', 'Researched',
        'Examined', 'Audited', 'Measured', 'Calculated', 'Forecasted'
    ],
    'creative': [
        'Designed', 'Created', 'Conceptualized', 'Innovated', 'Invented',
        'Crafted', 'Produced', 'Authored', 'Illustrated', 'Composed'
    ],
    'improvement': [
        'Improved', 'Enhanced', 'Optimized', 'Streamlined', 'Upgraded',
        'Revamped', 'Transformed', 'Modernized', 'Automated', 'Refined'
    ],
    'achievement': [
        'Achieved', 'Accomplished', 'Delivered', 'Exceeded', 'Surpassed',
        'Attained', 'Completed', 'Earned', 'Won', 'Secured'
    ]
}

# Common weak words to avoid
WEAK_WORDS = [
    'responsible for', 'duties included', 'worked on', 'helped with',
    'assisted with', 'participated in', 'involved in', 'was part of'
]

# Keywords for different industries
INDUSTRY_KEYWORDS = {
    'software': [
        'agile', 'scrum', 'CI/CD', 'microservices', 'API', 'cloud',
        'testing', 'deployment', 'DevOps', 'git', 'docker', 'kubernetes'
    ],
    'data': [
        'machine learning', 'data analysis', 'SQL', 'Python', 'statistics',
        'visualization', 'ETL', 'big data', 'ML models', 'algorithms'
    ],
    'product': [
        'roadmap', 'stakeholders', 'user research', 'product strategy',
        'metrics', 'A/B testing', 'KPIs', 'market analysis', 'user stories'
    ],
    'marketing': [
        'campaigns', 'ROI', 'analytics', 'SEO', 'content strategy',
        'social media', 'conversion', 'engagement', 'branding', 'growth'
    ]
}
