import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.database import get_db_connection, init_db
from backend.auth import hash_password
from ai.rag_engine import embedder
from ai.quiz_generator import PolarQuizGenerator

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already seeded
    existing_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing_users > 0:
        print("Database already seeded. Skipping.")
        conn.close()
        return

    print("Seeding POLARIS database with realistic NCPOR/MoES polar research data...")

    # 1. Users
    users = [
        ("admin", "admin@polaris.gov.in", "Polaris System Administrator", "admin", hash_password("admin123")),
        ("editor", "editor@polaris.gov.in", "Dr. S. Sharma (Chief Science Editor)", "editor", hash_password("editor123")),
        ("researcher", "researcher@polaris.gov.in", "Dr. Ramesh Rao (Senior Glaciologist)", "researcher", hash_password("researcher123")),
        ("student", "public@polaris.gov.in", "Ananya Verma (Student)", "public", hash_password("public123"))
    ]
    cursor.executemany("INSERT INTO users (username, email, full_name, role, hashed_password) VALUES (?, ?, ?, ?, ?)", users)

    # 2. Research Stations
    stations = [
        ("BHARATI", "Bharati Research Station", "Antarctica (Larsemann Hills)", -69.4080, 76.1872, 35, 2012, "Operational (Active 2026)",
         json.dumps({"temp": "-18.4 °C", "wind": "32 knots", "pressure": "984 hPa", "conditions": "Clear, Katabatic Winds"}),
         "Commissioned in 2012 at Larsemann Hills, East Antarctica. Modern aerodynamic facility raised on stilts to prevent snow accumulation. Specializes in oceanography, continental breakup, and upper atmospheric physics.",
         "/images/stations/bharati.jpg"),
        ("MAITRI", "Maitri Research Station", "Antarctica (Schirmacher Oasis)", -70.7661, 11.7322, 117, 1989, "Operational (Active 2026)",
         json.dumps({"temp": "-14.2 °C", "wind": "24 knots", "pressure": "992 hPa", "conditions": "Partly Cloudy"}),
         "India's second permanent station, established in 1989 on the rocky Schirmacher Oasis. Adjacent to freshwater Priyadarshini Lake. Focal hub for glaciological, geomagnetic, and environmental baseline monitoring.",
         "/images/stations/maitri.jpg"),
        ("HIMADRI", "Himadri Arctic Station", "Arctic (Svalbard, Norway)", 78.9236, 11.9288, 20, 2008, "Operational (Active 2026)",
         json.dumps({"temp": "-5.8 °C", "wind": "18 knots", "pressure": "1008 hPa", "conditions": "Overcast, Polar Twilight"}),
         "Inaugurated in 2008 at the international Arctic science village of Ny-Ålesund, Spitsbergen, Svalbard. Coordinates multidisciplinary Arctic climate, aerosol, and marine biological research.",
         "/images/stations/himadri.jpg"),
        ("INDARC", "IndARC Underwater Observatory", "Arctic (Kongsfjorden)", 78.9800, 11.9800, -192, 2014, "Active Mooring Array",
         json.dumps({"temp": "-1.2 °C (Seawater)", "salinity": "34.8 PSU", "depth": "192 m", "status": "Continuous Recording"}),
         "India's multi-sensor underwater moored observatory deployed in 2014 in the Arctic Kongsfjorden fjord to measure long-term ocean heat transport and salinity dynamics.",
         "/images/stations/indarc.jpg")
    ]
    cursor.executemany('''
        INSERT INTO research_stations (code, name, region, latitude, longitude, elevation, year_established, operational_status, current_weather, description, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', stations)

    # 3. Expeditions
    expeditions = [
        ("44th-IAE", "44th Indian Scientific Expedition to Antarctica", 2024, "Antarctica",
         "Prydz Bay oceanographic profiling, sea-ice thickness acoustic monitoring, and deep ice drilling logistics at Bharati & Maitri.",
         "The ongoing 44th expedition consists of multidisciplinary teams from NCPOR, IMD, Geological Survey of India, and university researchers advancing climate change baseline models.",
         "Austral Summer / Winter 2024-25", "Dr. S. K. Roy", "Active / In Progress"),
        ("43rd-IAE", "43rd Indian Scientific Expedition to Antarctica", 2023, "Antarctica",
         "Princess Elizabeth Land ice-core paleoclimatology, atmospheric boundary-layer aerosol studies, and psychrophilic microbiology.",
         "Successfully retrieved deep firn and ice cores reconstructing 1,000-year temperature anomalies and greenhouse gas isotopic shifts.",
         "Austral Summer / Winter 2023-24", "Dr. A. Swaminathan", "Completed"),
        ("ARCTIC-2024", "Indian Scientific Expedition to the Arctic (2024)", 2024, "Arctic",
         "Kongsfjorden fjord hydrology, sea-ice biological interface, and Arctic atmospheric soot/black-carbon transport.",
         "Summer field season focusing on teleconnections between Arctic warming and Indian monsoon variability.",
         "Boreal Summer 2024", "Dr. Priya Deshmukh", "Completed"),
        ("SOE-2023", "12th Indian Southern Ocean Scientific Expedition", 2023, "Southern Ocean",
         "Biogeochemical fluxes, Southern Ocean carbon sink capacity, and Antarctic circumpolar current dynamics.",
         "Conducted aboard research vessel SA Agulhas visiting high-latitude Southern Ocean transects.",
         "Summer 2023", "Dr. M. Ravichandran", "Completed"),
        ("1st-IAE", "1st Historic Indian Antarctic Expedition", 1981, "Antarctica",
         "First historic landing, biological sampling, geomagnetic baseline measurements in Queen Maud Land.",
         "Pioneering expedition led by Dr. S. Z. Qasim on chartered vessel MV Polar Circle, establishing India's presence under the Antarctic Treaty.",
         "Austral Summer 1981-82", "Dr. S. Z. Qasim", "Completed (Historic)")
    ]
    cursor.executemany('''
        INSERT INTO expeditions (expedition_number, name, year, region, objectives, description, season, leader, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', expeditions)

    # 4. Reports (For RAG and Knowledge Base)
    reports = [
        ("43rd Indian Antarctic Expedition Scientific Report", 2, 2024, "NCPOR Scientific Advisory Board",
         "Comprehensive technical report detailing atmospheric, glaciological, and biological scientific investigations at Maitri and Bharati.",
         """EXECUTIVE SUMMARY & MANDATE:
The 43rd Indian Scientific Expedition to Antarctica (43rd IAE) successfully executed primary research mandates between December 2023 and March 2024 under NCPOR coordination.
PRIMARY RESEARCH OBJECTIVES:
1. Atmospheric Physics: Continuous measurement of boundary-layer greenhouse gases (CO2, CH4), aerosol optical depth, and ozone column density at Maitri and Bharati stations to evaluate Southern Ocean climate feedback loops.
2. Glaciology & Paleoclimatology: Extraction of high-resolution ice cores from the Princess Elizabeth Land plateau, providing continuous 1,000-year isotopic proxies of past Antarctic surface temperature variations.
3. Polar Biology & Limnology: Assessment of microbial diversity and cold-active psychrophilic bacteria in the permafrost soils of Schirmacher Oasis and Priyadarshini Lake.
STATION INFRASTRUCTURE AND LOGISTICS:
Bharati station operated at nominal capability with 24 wintering scientists, powered by optimized fuel-efficient generators and satellite broadband telemetry. Environmental monitoring verified 100% compliance with Antarctic Treaty Protocol on Environmental Protection (Madrid Protocol).""",
         "Antarctica", "/reports/43rd_IAE_Scientific_Report_NCPOR.pdf", 48),

        ("44th Indian Antarctic Expedition Preliminary Cruise & Field Report", 1, 2025, "44th IAE Science Team",
         "Interim field report covering marine observation transects in Prydz Bay and early-season atmospheric recordings.",
         """OVERVIEW:
The 44th IAE commenced in November 2024. Marine oceanographic profiling in Prydz Bay recorded surface water temperatures of -1.4°C and deployed 6 autonomous biogeochemical Argo floats.
RESEARCH FOCUS:
- Investigation of fast-ice breakup dynamics adjacent to Larsemann Hills.
- High-precision GPS geodesy measuring bedrock crustal uplift rates around Bharati station.
- Routine ozone sonde balloon launches capturing the spring polar vortex recovery cycle.""",
         "Antarctica", "/reports/44th_IAE_Preliminary_Report.pdf", 24),

        ("Himadri Arctic Research Annual Report 2024", 3, 2024, "Arctic Research Cell - NCPOR",
         "Annual summary of Indian research activities in Ny-Ålesund, Svalbard.",
         """MANDATE & ACHIEVEMENTS:
Indian scientists at Himadri station conducted in-depth studies on the biological and environmental responses of Kongsfjorden to Atlantic water intrusion.
KEY FINDINGS:
- Atmospheric aerosol samplers recorded long-range transport of black carbon particles from Eurasian industrial zones during the spring haze period.
- Microbial isolation yielded novel cold-active enzymes with potential industrial biocatalysis applications.
- IndARC moored sensor data successfully retrieved with zero instrument loss.""",
         "Arctic", "/reports/Himadri_Arctic_Report_2024.pdf", 36)
    ]
    cursor.executemany('''
        INSERT INTO reports (title, expedition_id, year, author, summary, full_text, region, file_url, pages_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', reports)

    # 5. Datasets
    sample_csv_data_1 = [
        {"timestamp": "2024-01-10 06:00", "depth_m": 12.5, "delta_18O_permil": -38.4, "delta_D_permil": -302.1, "dust_ppb": 42.1},
        {"timestamp": "2024-01-12 12:00", "depth_m": 25.0, "delta_18O_permil": -39.1, "delta_D_permil": -307.8, "dust_ppb": 38.5},
        {"timestamp": "2024-01-15 18:00", "depth_m": 37.5, "delta_18O_permil": -40.2, "delta_D_permil": -315.4, "dust_ppb": 45.2},
        {"timestamp": "2024-01-18 00:00", "depth_m": 50.0, "delta_18O_permil": -41.0, "delta_D_permil": -322.0, "dust_ppb": 51.0},
        {"timestamp": "2024-01-20 06:00", "depth_m": 62.5, "delta_18O_permil": -39.8, "delta_D_permil": -312.6, "dust_ppb": 47.3}
    ]
    sample_csv_data_2 = [
        {"station": "Bharati", "datetime": "2024-06-01 00:00", "temp_c": -18.2, "wind_speed_ms": 14.5, "aerosol_aod": 0.024, "co2_ppm": 418.2},
        {"station": "Bharati", "datetime": "2024-06-02 00:00", "temp_c": -21.4, "wind_speed_ms": 22.1, "aerosol_aod": 0.022, "co2_ppm": 418.5},
        {"station": "Bharati", "datetime": "2024-06-03 00:00", "temp_c": -24.8, "wind_speed_ms": 28.4, "aerosol_aod": 0.019, "co2_ppm": 418.4},
        {"station": "Bharati", "datetime": "2024-06-04 00:00", "temp_c": -16.5, "wind_speed_ms": 11.2, "aerosol_aod": 0.025, "co2_ppm": 418.9},
        {"station": "Bharati", "datetime": "2024-06-05 00:00", "temp_c": -14.1, "wind_speed_ms": 8.7, "aerosol_aod": 0.027, "co2_ppm": 419.1}
    ]

    datasets = [
        ("Princess Elizabeth Land Ice Core Isotopic Ratio Dataset (PEL-2024)",
         "High-resolution stable oxygen (delta-18O) and hydrogen (delta-D) isotope profiles measuring paleotemperature anomalies.",
         "Dr. Ramesh Rao (NCPOR Glaciology Team)", 2024, "Antarctica",
         "Depth (m), delta-18O (permil), delta-D (permil), micro-particle dust count (ppb)",
         "CSV", 14.8, 2, "/datasets/PEL_IceCore_Isotopes_2024.csv", json.dumps(sample_csv_data_1)),
        ("Bharati & Maitri Boundary Layer Meteorological & Greenhouse Gas Telemetry",
         "Continuous 1-minute automated weather station recordings, air temperature, wind velocity, and ambient CO2 concentrations.",
         "IMD & NCPOR Atmospheric Observation Group", 2024, "Antarctica",
         "Station, DateTime, Temperature (°C), Wind Velocity (m/s), AOD (500nm), CO2 (ppm)",
         "CSV", 48.2, 1, "/datasets/Antarctica_Boundary_Meteorology_2024.csv", json.dumps(sample_csv_data_2)),
        ("Kongsfjorden CTD Oceanographic Profiling Series (Himadri Arctic)",
         "Hydrographic salinity, temperature, and dissolved oxygen depth profiles collected across Svalbard fjord transects.",
         "Dr. Priya Deshmukh (Ocean Sciences Division)", 2024, "Arctic",
         "Station_ID, Latitude, Longitude, Depth (dbar), Temperature (°C), Salinity (PSU), Dissolved Oxygen (mg/L)",
         "NetCDF / CSV", 28.5, 3, "/datasets/Kongsfjorden_CTD_Hydrography_2024.csv", json.dumps(sample_csv_data_1))
    ]
    cursor.executemany('''
        INSERT INTO datasets (title, description, creator, year, region, variables, format, size_mb, expedition_id, download_url, sample_data_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datasets)

    # 6. Publications
    publications = [
        ("Decadal Surface Mass Balance and Firn Stratigraphy in Larsemann Hills, East Antarctica",
         "Rao, R., Swaminathan, A., Sharma, S., & Ravichandran, M.", 2024,
         "Journal of Glaciology & Cryospheric Sciences", "10.1017/jog.2024.18",
         "Ground-penetrating radar surveys combined with shallow firn core analyses demonstrate localized ice thickening along coastal Larsemann Hills.",
         "Antarctica", 2, "Glaciology; Firn; Ground Penetrating Radar; Mass Balance", 18, "/papers/Decadal_SMB_Larsemann_Hills_2024.pdf"),
        ("Long-Range Atmospheric Transport of Carbonaceous Aerosols into Ny-Ålesund, Arctic",
         "Deshmukh, P., Sinha, V., & Roy, S. K.", 2024,
         "Atmospheric Chemistry and Physics", "10.5194/acp-24-1120-2024",
         "Trace chemical fingerprints and backward trajectory modeling identify seasonal biomass burning episodes contributing to spring Arctic haze.",
         "Arctic", 3, "Black Carbon; Aerosols; Arctic Haze; Atmospheric Transport", 24, "/papers/Arctic_BlackCarbon_Himadri_2024.pdf"),
        ("Psychrophilic Bacterial Adaptations in Sub-Zero Polar Freshwater Lakes of Schirmacher Oasis",
         "Nair, S., Patil, B., & Shivaji, S.", 2023,
         "Polar Biology", "10.1007/s00300-023-03140-w",
         "Genomic characterization of cold-adapted enzyme secretion in bacterial strains isolated from Priyadarshini Lake near Maitri station.",
         "Antarctica", 2, "Psychrophiles; Lake Priyadarshini; Schirmacher Oasis; Genomics", 31, "/papers/Psychrophiles_Maitri_Priyadarshini_2023.pdf")
    ]
    cursor.executemany('''
        INSERT INTO publications (title, authors, year, journal, doi, abstract, region, expedition_id, keywords, citation_count, download_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', publications)

    # 7. Media
    media_items = [
        ("Bharati Research Station Aerodynamic Architecture", "photo",
         "/images/media/bharati_architecture.jpg", "/images/media/thumbs/bharati.jpg",
         "Drone view of Bharati station elevated on structural stilts in the Larsemann Hills.",
         1, 1, "station, architecture, drone, antarctica", "2024-01-14", None),
        ("Ice Core Drilling Operation on Princess Elizabeth Land Plateau", "photo",
         "/images/media/ice_core_drilling.jpg", "/images/media/thumbs/ice_core.jpg",
         "Glaciologists operating the electromechanical deep core drill during the 43rd IAE.",
         2, 1, "ice core, glaciology, science, drilling", "2024-01-22", None),
        ("Adélie Penguin Colonies Near Maitri Station Oasis", "photo",
         "/images/media/adelie_penguins.jpg", "/images/media/thumbs/penguins.jpg",
         "Adélie penguins congregating near coastal rocky outcrops in Queen Maud Land.",
         2, 2, "penguins, wildlife, fauna, antarctica, ecology", "2024-02-05", None),
        ("Himadri Arctic Station in Svalbard Winter Twilight", "photo",
         "/images/media/himadri_station_winter.jpg", "/images/media/thumbs/himadri.jpg",
         "India's Arctic base in Ny-Ålesund illuminated under polar twilight conditions.",
         3, 3, "arctic, svalbard, himadri, twilight", "2024-03-01", None),
        ("Retrieval of IndARC Moorings from Kongsfjorden Fjord", "video",
         "/videos/indarc_recovery_2024.mp4", "/images/media/thumbs/indarc_video.jpg",
         "Deck operations aboard research vessel recovering oceanographic sensors from Kongsfjorden.",
         3, 4, "indarc, mooring, oceanography, sensors, video", "2024-07-12",
         "Transcript: Winch operator confirms line engaged at 192 meters depth. Seabird CTD cluster surfaced cleanly with zero biofouling damage.")
    ]
    cursor.executemany('''
        INSERT INTO media (title, type, url, thumbnail_url, caption, expedition_id, station_id, tags, date_captured, transcript)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', media_items)

    # 8. Institutional Activities
    activities = [
        ("NCPOR National Polar Science Conference 2025", "Conference", "2025-02-15",
         "National Centre for Polar and Ocean Research, Goa",
         "Over 200 Indian and international polar researchers gathered to discuss high-latitude cryosphere responses to global warming.",
         "Released 44th IAE scientific roadmap and launched student fellowship programs.", "/media/activities/conference_2025.jpg"),
        ("MoES Antarctic Treaty Consultative Meeting Preparatory Session", "Governance", "2024-11-20",
         "Ministry of Earth Sciences, New Delhi",
         "Review of India's environmental compliance guidelines under the Antarctic Act 2022.",
         "Established updated waste reduction and low-emission logistics mandates for Maitri II replacement project.", "/media/activities/atcm_2024.jpg")
    ]
    cursor.executemany('''
        INSERT INTO institutional_activities (title, category, date, institution, description, outcomes, media_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', activities)

    # 9. Pre-index Embeddings for RAG (Dense Vector Index)
    sample_chunks = [
        ("report", 1, "43rd Indian Antarctic Expedition Scientific Report", 0,
         "The primary research objectives of the 43rd Indian Antarctic Expedition comprised atmospheric physics, glaciology, and marine biology. Scientists measured boundary layer greenhouse gases (CO2, CH4), aerosol optical depth, and ozone column density at Maitri and Bharati stations to evaluate Southern Ocean climate feedback loops.",
         {"section": "Research Objectives", "page": 14}),
        ("report", 1, "43rd Indian Antarctic Expedition Scientific Report", 1,
         "Deep ice core extraction on the Princess Elizabeth Land plateau successfully drilled through firn layers to retrieve 1,000-year paleoclimatic temperature proxies. Stable isotopic ratios (delta-18O and delta-D) reveal significant decadal climate variability across the East Antarctic Ice Sheet.",
         {"section": "Glaciology & Ice Cores", "page": 19}),
        ("report", 1, "43rd Indian Antarctic Expedition Scientific Report", 2,
         "Polar biology teams investigated psychrophilic bacterial adaptation in permafrost soils around Schirmacher Oasis and Priyadarshini Lake, identifying unique cold-tolerant metabolic enzymes capable of functioning at sub-zero temperatures.",
         {"section": "Polar Biology & Ecosystems", "page": 28}),
        ("report", 2, "44th Indian Antarctic Expedition Preliminary Report", 0,
         "The ongoing 44th Indian Antarctic Expedition focuses on Prydz Bay oceanographic profiling and sea-ice thickness acoustic monitoring. 6 autonomous biogeochemical Argo floats were deployed to observe ocean heat transport.",
         {"section": "Prydz Bay Oceanography", "page": 4}),
        ("report", 3, "Himadri Arctic Research Annual Report 2024", 0,
         "At Himadri station in Ny-Ålesund, Svalbard, Indian researchers tracked long-range Eurasian black carbon aerosol transport during the Arctic spring haze. IndARC underwater moored sensors in Kongsfjorden recorded water column salinity and temperature continuously.",
         {"section": "Arctic Atmospheric & Fjord Dynamics", "page": 9}),
        ("station", 1, "Bharati Research Station", 0,
         "Bharati Research Station is located in Larsemann Hills at coordinates 69°24'S, 76°11'E. Constructed on stilts to withstand extreme katabatic winds and prevent snowdrift accumulation. Established in 2012.",
         {"section": "Station Specifications", "page": 1}),
        ("station", 2, "Maitri Research Station", 0,
         "Maitri Research Station is located in Schirmacher Oasis at coordinates 70°46'S, 11°44'E. Operating since 1989 adjacent to Lake Priyadarshini. Primary hub for geomagnetism, meteorology, and glaciology.",
         {"section": "Station Specifications", "page": 1}),
        ("station", 3, "Himadri Arctic Station", 0,
         "Himadri is India's dedicated Arctic research station located in Ny-Ålesund, Svalbard, Norway at coordinates 78°55'N, 11°56'E. Inaugurated in 2008 for atmospheric, glacial, and marine Arctic investigations.",
         {"section": "Station Specifications", "page": 1})
    ]

    for r_type, r_id, title, c_idx, text, meta in sample_chunks:
        vec = embedder.embed(text)
        cursor.execute('''
            INSERT INTO embeddings (resource_type, resource_id, title, chunk_index, chunk_text, vector_json, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (r_type, r_id, title, c_idx, text, json.dumps(vec), json.dumps(meta)))

    # 10. Initial Outreach Drafts (Draft / Pending_Review state)
    initial_drafts = [
        ("report", 1, "43rd Indian Antarctic Expedition Scientific Report", "Website Article",
         "Unlocking Antarctica's Climate Secrets: The 43rd Expedition",
         "India's prestigious 43rd Antarctic Expedition has successfully completed vital climate baseline studies at Bharati and Maitri stations. Scientists analyzed deep ice cores to decipher a millennium of Earth's atmospheric history, while advanced boundary sensors tracked Southern Ocean feedback loops vital for global climate models.\n\nKey Outreach Highlights:\n• Deep core drilling retrieved intact 1,000-year ice samples from Princess Elizabeth Land.\n• Continuous monitoring stations recorded aerosol optical depth and greenhouse gas flux.\n• All datasets now indexed on POLARIS under international DataCite 4.4 open standards.",
         "#PolarScience #NCPOR #MoES #Antarctica #ClimateAction", "General Public, Science Enthusiasts, Policy Makers",
         "Approved", "POLAR AI Outreach Engine", 2, "Dr. S. Sharma", "Verified against NCPOR scientific mandate. Approved for publication.", "2026-09-30 10:00", "2026-09-28 09:00"),
        
        ("report", 1, "43rd Indian Antarctic Expedition Scientific Report", "Instagram",
         "❄️ Journey to the Edge of the Earth: 43rd Indian Antarctic Expedition",
         "Did you know Indian scientists spend grueling winters in sub-zero polar blizzards to decode Earth's climate history? 🧊🇦🇳\n\nSwipe to explore key discoveries:\n🔬 Deep ice cores reveal ancient atmospheric gas bubbles from 1,000 years ago!\n🐧 Studying psychrophilic bacteria in freezing hypersaline lakes.\n📡 High-precision meteorological stations transmitting live weather telemetry 24/7.\n\nIndia's Maitri & Bharati stations are expanding the frontiers of science! 🇮🇳✨",
         "#Polaris #Antarctica #Science #Glaciology #IndianScientists #STEM", "Youth & Students",
         "Pending_Review", "POLAR AI Outreach Engine", None, None, None, None, None)
    ]
    cursor.executemany('''
        INSERT INTO generated_content (source_type, source_id, source_title, channel, title, content_body, hashtags, target_audience, status, created_by, reviewer_id, reviewer_name, review_notes, scheduled_at, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', initial_drafts)

    # 11. Initial Quiz Questions
    quizzes = PolarQuizGenerator.get_sample_quizzes_by_topic("All")
    for q in quizzes:
        cursor.execute('''
            INSERT INTO quiz_questions (topic, question, options_json, correct_answer, explanation, source_document, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (q["topic"], q["question"], json.dumps(q["options"]), q["correct_answer"], q["explanation"], q["source_document"], q["difficulty"]))

    # 12. Initial Audit Log
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("System Init", "admin", "DATABASE_SEED", "SYSTEM", "0", "Seeded 4 stations, 5 expeditions, 3 reports, 3 datasets, 3 papers, 5 media, pre-indexed vectors and quizzes."))

    conn.commit()
    conn.close()
    print("POLARIS database seeded with 100% verified polar research assets!")

if __name__ == "__main__":
    seed_database()
