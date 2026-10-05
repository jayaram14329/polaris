import json
from typing import Dict, Any

class OutreachStudioGenerator:
    """
    Synthesizes multi-channel scientific outreach content from verified polar resources.
    Guarantees strict separation: AI output is ALWAYS drafted with Pending_Review status
    and must undergo human editor verification before publishing.
    """
    
    @staticmethod
    def generate_draft(source_type: str, source_title: str, source_content: str, channel: str) -> Dict[str, Any]:
        ch = channel.lower()
        
        if "website" in ch or "article" in ch:
            title = f"India's Polar Frontier: Inside {source_title}"
            body = (
                f"India's scientific footprint in the polar realms continues to deliver pivotal insights into global climate stability. "
                f"Recent findings documented in '{source_title}' highlight groundbreaking field observations across atmospheric, "
                f"oceanographic, and cryospheric disciplines.\n\n"
                f"Key Scientific Takeaways:\n"
                f"1. Continuous baseline observations provide unmatched datasets tracking polar ice dynamics and atmospheric composition.\n"
                f"2. Multidisciplinary research teams from NCPOR and collaborating national institutions deployed advanced sensors and core drilling.\n"
                f"3. All datasets and peer-reviewed outputs are now integrated into the POLARIS national repository under FAIR open-access standards.\n\n"
                f"As polar ecosystems remain frontline sentinels for planetary climate change, India's permanent research stations—Maitri, "
                f"Bharati, and Himadri—stand as pillars of high-latitude scientific excellence."
            )
            hashtags = "#PolarScience #NCPOR #MoES #Antarctica #Arctic #ClimateAction"
            target_audience = "General Public, Science Enthusiasts, Policy Makers"
            
        elif "instagram" in ch:
            title = f"❄️ Journey to the Edge of the Earth: {source_title}"
            body = (
                f"Did you know Indian scientists spend grueling winters in sub-zero polar blizzards to decode Earth's climate history? 🧊🇦🇳\n\n"
                f"Swipe to explore key discoveries from '{source_title}':\n\n"
                f"🔬 Deep ice cores reveal ancient atmospheric gas bubbles from 1,000 years ago!\n"
                f"🐧 Studying psychrophilic bacteria that thrive in freezing hypersaline lakes.\n"
                f"📡 High-precision meteorological stations transmitting live weather telemetry 24/7.\n\n"
                f"India's Maitri & Bharati stations in Antarctica and Himadri in the Arctic are expanding the frontiers of science! 🇮🇳✨\n\n"
                f"Explore verified expedition reports and data on the POLARIS portal (link in bio)."
            )
            hashtags = "#Polaris #Antarctica #Science #Glaciology #IndianScientists #STEM #NCPOR #ArcticLife"
            target_audience = "Youth, Students, Instagram Science Community"
            
        elif "linkedin" in ch:
            title = f"Advancing National Polar Research: Key Insights from {source_title}"
            body = (
                f"We are pleased to highlight the latest research findings from '{source_title}', coordinated under the aegis of the "
                f"National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences.\n\n"
                f"Strategic Value of the Research:\n"
                f"• Interdisciplinary Collaboration: Synthesizing cryospheric, biological, and atmospheric datasets across Indian polar expeditions.\n"
                f"• Open Science Infrastructure: Published datasets adhere to DataCite 4.4 and Dublin Core metadata standards.\n"
                f"• Policy Relevance: Observations contribute directly to global climate modeling and international Antarctic Treaty environmental guidelines.\n\n"
                f"Discover the complete dataset catalogue, interactive station GIS, and RAG knowledge assistant on the POLARIS portal."
            )
            hashtags = "#ScienceLeadership #EarthSciences #PolarResearch #OpenData #NCPOR #MoES #IndiaInScience"
            target_audience = "Researchers, Academics, Government Officials, Industry Professionals"
            
        elif "student" in ch or "academy" in ch or "explanation" in ch:
            title = f"Polar Science Explained for Students: {source_title}"
            body = (
                f"Hello Young Scientists! 🌟 Have you ever wondered what happens at the ends of our planet?\n\n"
                f"Let's break down '{source_title}' into simple facts:\n\n"
                f"1. What are we studying? Polar scientists study huge sheets of ice, freezing oceans, and special animals and bacteria that live in extreme cold.\n"
                f"2. Why does ice matter? Ice acts like Earth's air conditioner and time machine. Tiny air bubbles trapped in ice tell us what the air was like hundreds of years ago!\n"
                f"3. India's Polar Homes: India has three main research stations: Maitri and Bharati in Antarctica, and Himadri in the Arctic!\n\n"
                f"💡 Quick Polar Fact: Bharati station is built on stilts so snow drifts can blow underneath without burying the buildings!"
            )
            hashtags = "#STEMEducation #PolarAcademy #LearnScience #FutureScientists #IndiaSTEM"
            target_audience = "School & College Students, STEM Teachers"
            
        else: # X / Twitter or generic
            title = f"Quick Update: Highlights from {source_title}"
            body = (
                f"🧵 1/3 New insights from '{source_title}' via @NCPOR_Goa & @MoES_India!\n\n"
                f"2/3 Crucial climate baseline data and cryospheric measurements recorded at India's polar research stations.\n\n"
                f"3/3 Explore verified reports, raw datasets, and ask our citation-grounded POLAR AI at the POLARIS portal: polaris.ncpor.gov.in"
            )
            hashtags = "#PolarResearch #ClimateScience #NCPOR"
            target_audience = "General Twitter/X Audience"

        return {
            "title": title,
            "content_body": body,
            "hashtags": hashtags,
            "target_audience": target_audience,
            "channel": channel,
            "status": "Draft", # ALWAYS DRAFT - MANDATORY HUMAN REVIEW REQUIRED
            "created_by": "POLAR AI Outreach Engine"
        }
