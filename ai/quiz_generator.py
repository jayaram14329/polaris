import json
from typing import List, Dict, Any

class PolarQuizGenerator:
    """
    Generates interactive STEM quiz questions verified against primary polar expedition literature.
    """
    
    @staticmethod
    def get_sample_quizzes_by_topic(topic: str = "All") -> List[Dict[str, Any]]:
        bank = [
            {
                "topic": "Indian Polar Stations",
                "question": "Which is India's first permanent research station in Antarctica, established in 1983?",
                "options": ["Dakshin Gangotri", "Maitri", "Bharati", "Himadri"],
                "correct_answer": "Dakshin Gangotri",
                "explanation": "Dakshin Gangotri was established during the third Indian expedition in 1983-84 and served as the first wintering base before being replaced by Maitri in 1989.",
                "source_document": "Historical Indian Antarctic Expeditions Bulletin - NCPOR",
                "difficulty": "Easy"
            },
            {
                "topic": "Arctic Science",
                "question": "Where is India's Arctic research station 'Himadri' situated?",
                "options": ["Ny-Ålesund, Svalbard (Norway)", "Alert, Nunavut (Canada)", "Thule, Greenland", "Murmansk (Russia)"],
                "correct_answer": "Ny-Ålesund, Svalbard (Norway)",
                "explanation": "Himadri was inaugurated in 2008 at the international research base in Ny-Ålesund, Spitsbergen, Svalbard, dedicated to Arctic atmospheric and biological sciences.",
                "source_document": "NCPOR Arctic Research Programme Annual Report",
                "difficulty": "Medium"
            },
            {
                "topic": "Climate & Ice Cores",
                "question": "Why do glaciologists extract deep ice cores from Antarctic ice sheets?",
                "options": [
                    "To reconstruct past global atmospheric greenhouse gas concentrations from trapped air bubbles",
                    "To search for liquid gold beneath glaciers",
                    "To generate drinking water for coastal cities",
                    "To measure ocean salt density directly"
                ],
                "correct_answer": "To reconstruct past global atmospheric greenhouse gas concentrations from trapped air bubbles",
                "explanation": "Air bubbles trapped inside sequential layers of glacier ice preserve pristine samples of Earth's ancient atmosphere spanning hundreds of thousands of years.",
                "source_document": "Princess Elizabeth Land Paleoclimatology Study - 43rd IAE",
                "difficulty": "Medium"
            },
            {
                "topic": "Station Engineering",
                "question": "What architectural innovation protects Bharati station from being submerged in Antarctic snowdrifts?",
                "options": [
                    "Constructed on elevated stilts allowing katabatic winds and blowing snow to pass underneath",
                    "Built entirely underground beneath 50 meters of solid ice",
                    "Surrounded by heated electrical fences",
                    "Floating on pressurized air cushions"
                ],
                "correct_answer": "Constructed on elevated stilts allowing katabatic winds and blowing snow to pass underneath",
                "explanation": "Bharati station features a streamlined aerodynamic design elevated on stilts to prevent heavy snow accumulation on the leeward sides.",
                "source_document": "Polar Engineering and Station Design Guidelines - MoES",
                "difficulty": "Hard"
            },
            {
                "topic": "Polar Oceanography",
                "question": "What is 'IndARC', deployed by Indian scientists in 2014?",
                "options": [
                    "India's first multi-sensor underwater moored observatory in the Arctic Kongsfjorden fjord",
                    "A nuclear-powered icebreaker vessel",
                    "A polar satellite launched by ISRO",
                    "An unmanned aerial drone mapping penguin colonies"
                ],
                "correct_answer": "India's first multi-sensor underwater moored observatory in the Arctic Kongsfjorden fjord",
                "explanation": "IndARC is an underwater moored observatory deployed at Kongsfjorden in the Arctic to collect continuous sea-water temperature, salinity, and current measurements throughout the year.",
                "source_document": "IndARC Observatory Mandate & Technical Report - NCPOR",
                "difficulty": "Hard"
            }
        ]
        
        if topic and topic.lower() != "all":
            return [q for q in bank if topic.lower() in q["topic"].lower()]
        return bank
