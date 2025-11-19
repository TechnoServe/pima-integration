"""Dictionaties used to generate string values from input from input JSONs"""

MIGRATED_FORM_TYPES = [
    "Farmer Registration",
    "Attendance Full - Current Module",
    "Edit Farmer Details",
    "Training Observation",
    "Attendance Light - Current Module",
    "Participant",
    "Training Group",
    "Training Session",
    "Project Role",
    "Household Sampling",
    "Demo Plot Observation",
    "Farm Visit Full",
    "Farm Visit - AA",
    "Field Day Farmer Registration",
    "Field Day Attendance Full",
    "Wet Mill Registration Form",
    "Wet Mill Visit",
]

# ---------------------------------
# 1. DEMO PLOT OBSERVATION MAPPING
# ---------------------------------

DPO_MAPPINGS = {
    # 1. Stumped trees
    "stumped_trees": {
        "No_stumped_demo_plot": "No stumped demo plot",
        "Yes_demo_plot_of_10m_x_10m": "Yes, demo plot of 10m x 10m",
    },
    # 2. Sucker selection
    "Sucker_Selection_Taken_Place": {
        "No_Many_suckers": "No, Many suckers",
        "Yes_Sucker_selection_completed": "Yes, Sucker selection completed",
    },
    # 3. Compost Heap
    "present_compost_heap": {
        "No": "No",
        "Yes_compost_or_manure_heap_seen": "Yes, compost or manure heap seen",
        "1": "Yes, compost or manure heap seen",
        "0": "No compost or manure heap seen",
    },
    # 4. Weeding
    "has_the_demo_plot_been_dug": {
        "No_sign_of_digging": "No sign of digging",
        "Yes_field_dug": "Yes, field dug",
        "1": "Yes, field dug",
        "0": "No sign of digging",
    },
    "how_many_weeds_are_under_the_tree_canopy": {
        "No_weeds_under_the_tree_canopy": "No weeds under the tree canopy",
        "Few_weeds_under_the_tree_canopy": "Few weeds under the tree canopy",
        "Many_weeds_under_the_tree_canopy": "Many weeds under the tree canopy",
        "0": "No weeds under the tree canopy",
        "1": "Few weeds under the tree canopy",
        "2": "Many weeds under the tree canopy",
    },
    "how_big_are_the_weeds": {
        "Weeds_are_less_than_30cm_tall_or_30cm_spread_for_grasses": "Weeds are less than 30cm tall or 30cm spread for grasses",
        "Weeds_are_more_than_30cm_tall_or_30cm_spread_for_grasses": "Weeds are more than 30cm tall or 30cm spread for grasses",
        "1": "Weeds are less than 30cm tall or 30cm spread for grasses",
        "2": "Weeds are more than 30cm tall or 30cm spread for grasses",
    },
    # 5. Shade Management
    "level_of_shade_present": {
        "NO_shade,_less_than_5%": "NO shade, less than 5%",
        "Light_shade,_5_to_20%": "Light shade, 5 to 20%",
        "Medium_shade,_20_to_40%": "Medium shade, 20 to 40%",
        "Heavy_shade,_over_40%": "Heavy shade, over 40%",
        "0": "NO shade, less than 5%",
        "1": "Light shade, 5 to 20%",
        "2": "Medium shade, 20 to 40%",
        "3": "Heavy shade, over 40%",
    },
    # 6. Mulching
    "mulch_under_the_canopy": {
        "No": "No",
        "Yes_Some_mulch_seen": "Yes, Some mulch seen",
        "1": "Yes, Some mulch seen",
        "0": "No mulch seen",
    },
    "thickness_of_mulch": {
        "Soil_can_be_seen_clearly,_less_than_2cm_of_mulch.": "Soil can be seen clearly, less than 2cm of mulch",
        "Soil_can_not_be_seen,_more_than_2cm_of_mulch.": "Soil can not be seen, more than 2cm of mulch",
        "1": "Soil can be seen clearly, less than 2cm of mulch",
        "2": "Soil can not be seen, more than 2cm of mulch",
    },
    # 7. Vetiver
    "vetiver_planted": {
        "No_Vetiver_not_planted": "No. Vetiver not planted",
        "Yes_Row_of_vetiver_planted": "Yes. Row of vetiver planted",
        "1": "Yes. Row of vetiver planted",
        "0": "No. Vetiver not planted",
    },
    # 8. Pruning
    "pruning_methods": {
        "1": "Centers opened",
        "2": "Unwanted suckers removed",
        "3": "Dead branches removed",
        "4": "Branches touching the ground removed",
        "5": "Broken/unproductive stems and/or branches removed",
        "0": "No pruning methods used",
    },
    # 9. Rejuvenation
    "rejuvenation_plot": {
        "1": "Yes. There is a rejuvenated plot",
        "0": "No rejuvenated plot",
    },
    "suckers_three": {
        "1": "Yes. Sucker selection is complete",
        "0": "No. Sucker selection has not been done",
    },
    # 10. Cover crops
    "covercrop_present": {
        "1": "Arachis",
        "2": "Beans",
        "3": "Mulch",
        "0": "No Covercropping Practice",
    },
}

DPO_RESULT_CRITERIA = {
    "compost_heap": "Compost Heap",
    "mulch": "Mulch",
    "shade_management": "Shade Management",
    "vetiver": "Vetiver Planted",
    "weed_management": "Weed Management",
    "rejuvenation": "Rejuvenation",
    "sucker_selection": "Sucker Selection",
    "stumped": "Stumped Trees",
    "pruning": "Pruning",
    "covercropping": "Covercrop Planted",
}

# ---------------------------------
# 2. FARM VISIT MAPPING
# ---------------------------------

FV_BP_MULTISELECT = [
    "pruning_method_on_majority_trees",
    "type_chemical_applied_on_coffee_last_12_months",
    "which_product_have_you_used",
    "methods_of_controlling_coffee_berry_borer",
    "methods_of_controlling_white_stem_borer",
    "methods_of_controlling_coffee_leaf_rust",
    "methods_of_erosion_control",
    "which_pests_cause_you_problems",
    "do_you_spray_any_of_the_following_on_your_farm_for_leaf_miner_or_rust",
]

FV_QUESTIONS_IGNORE_LIST = [
    "#type",
    "@name",
    "@uiVersion",
    "@version",
    "@xmlns",
    "attendance_count",
    "case",
    "closing",
    "current_module",
    "current_module_name",
    "date_1",
    "date_last_60_days",
    "date_of_visit",
    "date_tomorrow",
    "farm_being_visted",
    "farm_visit_comments",
    "farm_visit_photo",
    "introduction",
    "mark_complete",
    "meta",
    "present_participants",
    "previous_module",
    "secondary_farmer",
    "secondary_farmer_firstname",
    "secondary_farmer_fullname",
    "secondary_farmer_lastname",
    "secondary_farmer_available",
    "signature_of_farmer",
    "signature_of_farmer_trainer",
    "signature_of_agronomy_advisor",
    "survey_type",
    "trainer",
    "training_session",
    "field_inventory_survey",
    "best_practice_questions",
    "survey_type_2",
    "updated_fis_list",
    "instruction____you_will_now_proceed_ask_the_farmers_about_their_attendance_",
    "count_selected_farmers",
    "household_tns_id"
]

FV_QUESTIONS_MAPPINGS = {
    # Kenya Special questions
    "variety": {
        "1": "SL34 or SL28",
        "2": "Ruiru 11",
        "3": "Batien",
        "4": "French mission/other",
    },
    # Zimbabwe
    "planted_on_land_that_have_previously_been_planted_with_woodland_or_forest": {
        "1": "Natural woodland or forest",
        "2": "Eucalyptus or other tree plantation",
        "0": "No sign the field(s) was previously woodland or forest.",
    }
}

YN = {
    "1": True,
    "0": False
}

YN_QUESTIONS = [
    "attended_training"
]

FV_BP_VISIT_TYPE_FILTER = [
    "type_chemical_applied_on_coffee_last_12_months",
    "methods_of_controlling_coffee_berry_borer",
    "do_you_have_a_record_book",
    "are_there_records_on_the_record_book",
]

# Keep updating every year for new cohorts. Until we find out a way to globalize the entries
FV_STUMPING_PROGRAM_FILTER = {
    "dd10fc19040d40f0be48a447e1d2727c": "2024",  # Regrow 2025
    "f079b0daae1d4d34a89e331dc5a72fbd": "2024",  # CREW 2025
    "521097abbcfd4fa79668cb6ca3dca28a": "2025",  # Regrow 2024
    "0c9b5791828b4baea6c1eaa4d6979c5a": "2025",  # CREW 2024
}

FV_BP_MAPPINGS = {
    # 1. Pruning
    "pruning_method_on_majority_trees": {
        "1": "Centers opened",
        "2": "Unwanted suckers removed",
        "3": "Dead branches removed",
        "4": "Branches touching the ground removed",
        "5": "Broken / unproductive stems and/or branches removed",
        "0": "No pruning methods used",
    },
    # 2. Health of New Planting
    "health_of_new_planting_choice": {
        "1": "The majority of trees are green and healthy and have grown well",
        "2": "The majority of trees look stressed and growth is slow",
        "3": "The majority of trees have dried up or died",
    },
    # 3. Nutrition
    "are_the_leave_green_or_yellow_pale_green": {
        "1": "Nearly all leaves are dark green and less than 5% (less than 5 in 100) are yellow, pale green, or brown.",
        "2": "5% or more (5 or more in 100) of the leaves are yellow, pale green or brown.",
    },
    "type_chemical_applied_on_coffee_last_12_months": {
        "Farm Visit Full - ZM": {
            "1": "Compost",
            "2": "Manure",
            "3": "Lime",
            "4": "Compound S",
            "5": "Compound J",
            "6": "Single Super Phosphate (SSP)",
            "7": "Zinc/Boron Foliar Feed (Tracel)",
            "8": "Ammonium Nitrate",
            "0": "Did NOT apply any fertilizer in past 12 months",
        },
        "Farm Visit Full - ET": {
            "1": "Compost, homemade or pulp compost",
            "2": "Manure",
            "0": "Did NOT apply any organic fertilizer in past 12 months",
        },
        "Farm Visit Full - KE": {
            "1": "Compost",
            "2": "Manure",
            "3": "NPK 22:6:12",
            "4": "NPK 17:17:17",
            "5": "Other NPK",
            "6": "Zinc/Boron Foliar feed",
            "7": "General Foliar feed",
            "8": "LIME",
            "9": "CAN",
            "10": "WonderGro",
            "0": "Did NOT apply any fertilizer in past 12 months",
        },
        "Farm Visit Full - PR": {
            "1": "NPK 10:10:5-10",
            "2": "NPK 10:10:5-10",
            "3": "NPK 10:5:15-20",
            "4": "NPK 10:5:15-20",
            "5": "NPK 10:5:15-20",
            "6": "NPK 10:5:15-20",
            "7": "NPK 10:5:15-20",
            "8": "NPK 15:5:10-19",
            "9": "NPK 15:5:10-19",
            "10": "NPK 15:5:10-19",
            "11": "NPK 15:15:15",
            "12": "NPK 20:5:10-20",
            "13": "NPK 20:5:10-20",
            "14": "DAP",
            "15": "Urea",
            "16": "Compost or Manure",
            "17": "Agricultural Lime - Calcium Carbonate",
            "18": "Nutrical (cal dolomita)",
            "19": "Foliar Zinc or Boron",
            "20": "General Foliar Feed (Nurish, Ferquido Ferqan)",
            "0": "Did NOT apply any fertilizer in past 12 months",
        },
    },
    # 4. Weeding
    "how_many_weeds_under_canopy_and_how_big_are_they": {
        "1": "Few small weeds (less than 30cm) under the tree canopy",
        "2": "Many small weeds under the tree canopy (ground is covered with weeds)",
        "3": "Many large weeds under the tree canopy (ground is covered with weeds)",
    },
    "used_herbicides": {"yes": "Yes", "no": "No"},
    "which_product_have_you_used": {  # PR naming is slightly differen't but retaining this mapping
        "1": "Glyphosate (Eg Round Up)",
        "2": "Paraquat (Eg. Gramoxone)",
        "3": "Other",
    },
    "look_has_the_coffee_field_been_dug": {
        "0": "No sign of digging",
        "1": "Yes field dug",
    },
    # 5. IPDM
    "methods_of_controlling_coffee_berry_borer": {
        "Farm Visit Full - ZM": {
            "1": "Reduce pesticide use and/or encourage natural predators and parasites - beneficial insects.",
            "2": "Strip all berries at the end of harvest, known as crop hygiene",
            "3": "Harvest ripe cherries regularly - to reduce pest and disease levels",
            "4": "Use berry borer traps",
            "5": "Collect fallen berries at the end of the season - crop hygiene",
            "6": "Feed the tree well to keep it healthy",
            "7": "Use good agricultural practices such as weeding or mulching to reduce stress and keep trees healthy",
            "8": "Prune to keep the canopy open",
            "9": "Renovate (new planting) or rejuvenate regularly to keep main stems less than 8 years old",
            "10": "Plant and grow disease resistant varieties",
            "11": "Smooth the bark to reduce egg laying sites for While Coffee Borer",
            "12": "Spray regular pesticides",
            "13": "Spray homemade herbal or botanical pesticides",
            "0": "Does not use any methods",
        },
        "Farm Visit Full - PR": {
            "1": "Reduce pesticide use and encourage natural predators",
            "2": "Strip all berries at the end of harvest",
            "3": "Harvest ripe cherries regularly",
            "4": "Collect fallen berries",
            "5": "Use berry borer traps",
            "6": "Spray pesticides",
            "0": "Does not use any methods",
        },
        "Farm Visit Full - KE": {
            "1": "Reduce pesticide use and/or encourage natural predators and parasites - beneficial insects.",
            "2": "Strip all berries at the end of harvest, known as crop hygiene",
            "3": "Harvest ripe cherries regularly - to reduce pest and disease levels",
            "4": "Use berry borer traps",
            "5": "Collect fallen berries at the end of the season - crop hygiene",
            "6": "Feed the tree well to keep it healthy",
            "7": "Use good agricultural practices such as weeding or mulching to reduce stress and keep trees healthy",
            "8": "Prune to keep the canopy open",
            "9": "Renovate (new planting) or rejuvenate regularly to keep main stems less than 8 years old",
            "10": "Plant and grow disease resistant varieties",
            "11": "Smooth the bark to reduce egg laying sites for While Coffee Borer",
            "12": "Spray regular pesticides",
            "13": "Spray homemade herbal or botanical pesticides",
            "0": "Does not know any methods",
        },
    },
    "methods_of_controlling_white_stem_borer": {
        "1": "Encourage natural predators and parasites",
        "2": "Strip all berries at the end of the harvest or collect fallen berries",
        "3": "Harvest ripe cherries regularly",
        "4": "Use Berry Borer traps",
        "5": "Use compost or manure, to keep the tree healthy",
        "6": "Use good agricultural practices such as weeding or mulching to reduce stress and keep trees healthy",
        "7": "Stump old coffee",
        "8": "Plant disease resistant varieties",
        "9": "Prune or keep the canopy open",
        "10": "Uproot wilt infected coffee trees and burn",
        "11": "Smooth the bark at the base of the tree",
        "0": "Farmer does not know",
    },
    "methods_of_controlling_coffee_leaf_rust": {
        "1": "Feed the tree well to keep it healthy",
        "2": "Use good agricultural practices such as weeding or mulching to reduce stress and keep trees healthy",
        "3": "Prune or keep canopy open",
        "4": "Spray fungicides",
        "5": "Grow resistant varieties",
        "0": "Does not know any methods",
    },
    # 6. Erosion Control (ET is a bit different, but the numbering matches)
    "methods_of_erosion_control": {
        "1": "Stabilizing grasses",
        "2": "Mulch",
        "3": "Water traps or trenches",
        "4": "Physical barriers. (e.g. rocks)",
        "5": "Terraces",
        "6": "Contour planting",
        "7": "Bean or Arachis cover crop between the rows",
        "0": "No erosion control method seen",
    },
    # 7. Shade Management
    "level_of_shade_present_on_the_farm": {
        "0": "NO shade, less than 5%",
        "1": "Light shade, 5 to 20%",
        "2": "Medium shade, 20 to 40%",
        "3": "Heavy shade, over 40%",
    },
    "planted_intercrop_bananas": {"yes": "Yes", "no": "No"},
    "new_shade_trees_in_the_last_3_years": {
        "0": "No new shade trees planted in the last 3 years",
        "1": "YES, enough new shade trees planted in the last 3 years to give 20% shade when mature",
        "2": "Few new shade trees planted in the last 3 years",
    },
    # 8. Record Keeping
    "do_you_have_a_record_book": {
        "Farm Visit Full - ZM": {  # Kenya uses this too
            "0": "NO Record Book received",
            "1": "YES, Farmer received a Record Book",
        },
        "Farm Visit Full - KE": {
            "0": "NO Record Book received",
            "1": "YES, Farmer received a Record Book",
        },
        "Farm Visit Full - PR": {
            "0": "NO Record Book received",
            "1": "YES, Farmer received a Record Book",
        },
        "Farm Visit Full - ET": {
            "0": "NO Record Book",
            "1": "YES, Farmer has a Record Book",
        },
    },
    "are_there_records_on_the_record_book": {
        "Farm Visit Full - ZM": {
            "0": "NO records of coffee weight, income or expenses",
            "1": "YES, some records of  coffee weight, income or expenses",
        },
        "Farm Visit Full - KE": {
            "0": "NO records of coffee weight, income or expenses",
            "1": "YES, some records of  coffee weight, income or expenses",
        },
        "Farm Visit Full - PR": {
            "0": "NO records of coffee weight, income or expenses",
            "1": "YES, some records of  coffee weight, income or expenses",
        },
        "Farm Visit Full - ET": {
            "0": "NO records of coffee weight, income received for coffee sold, labour or other costs",
            "1": "YES records of coffee weight, income received for coffee sold, labour or other costs",
        },
    },
    # 9. Compost
    "do_you_have_compost_manure": {
        "0": "NO",
        "1": "YES, compost or manure heap seen",
    },
    # 10. Stumping
    "stumping_methods_used_on_majority_of_trees": {
        "0": "No trees stumped",
        "1": "Yes, some trees stumped and trees seen",
    },
    "year_stumping": {  # Needs fixing
        "2024": {
            "0": "January to March 2024 at the start of the first year of training",
            "1": "January to March 2025 at the start of the second year of training",
            "both_periods": "Both periods",
        },
        "2025": {
            "0": "January to March 2025 at the start of the first year of training",
            "1": "January to March 2026 at the start of the second year of training",
            "both_periods": "Both periods",
        },
        "2026": {
            "0": "January to March 2026 at the start of the first year of training",
            "1": "January to March 2027 at the start of the second year of training",
            "both_periods": "Both periods",
        },
    },
    # 11. Pesticide Use
    "used_pesticides": {"1": "Yes", "0": "No"},
    "pesticide_spray_type": {
        "1": "Routine spray",
        "2": "After scouting and seeing a pest",
    },
    "which_pests_cause_you_problems": {
        "1": "Leaf miner",
        "2": "Coffee Berry Borer",
        "3": "Scles and Mealy bugs",
        "4": "None pest issue",
    },
    "do_you_need_to_spray_to_manage_leaf_rust": {"no": "No", "yes": "Yes"},
    "do_you_spray_any_of_the_following_on_your_farm_for_leaf_miner_or_rust": {
        "1": "Products containing Imidacloprid which include Acronyx, Admire Pro, Alias, Midash Forte and Nuprid?",
        "2": "Products containing Propiconazole which includes Tilt?",
        "3": "None of the products used",
    },
    
    # 12. Kitchen garden
    "is_there_a_kitchen_garden" : {
        "1": "Yes. There is a kitchen garden on the farm",
        "0": "No kitchen garden planted"
    },
    
    "vegetables_planted": {
        "1": "Carrots",
        "2": "Beetroot",
        "3": "Swiss chard",
        "4": "Kale",
        "99": "Other"
    }
}

FV_BP_TYPE = {
    "record_keeping": "Record Keeping",
    "stumping": "Stumping",
    "nutrition": "Nutrition",
    "weeding": "Weeding",
    "pest_disease_management": "Integrated Pest & Disease Management",
    "erosion_control": "Erosion Control",
    "shade_control": "Shade Management",
    "compost": "Compost",
    "main_stems": "Main Stems",
    "pruning": "Pruning",
    "safe_use_of_pesticides": "Pesticide Use",
    "health_of_new_planting": "Health of New Planting",
    "pesticide_use": "Pesticide Use",
    "other": "General FV Questions",
}

# ---------------------------------
# 3. WETMILL MAPPING
# ---------------------------------

EXPORTING_STATUS_MAP = {
    "1": "Exporter",
    "2": "Non exporter",
}

VERTICAL_INTEGRATION_MAP = {
    "1": "Yes",
    "0": "No",
}

MANAGER_ROLE_MAP = {
    "Wet Mill Registration - ET": {"1": "General manager", "2": "Site/factory manager"},
    "Wet Mill Registration - BU": {"1": "General manager", "2": "Site/factory manager"},
    "Wet Mill Registration - KE": {
        "1": "Cooperative board of management",
        "2": "CEO/Secretary Manger",
        "3": "Factory/Wet Mill Manager",
    },
}

WET_MILL_STATUS_MAP = {
    "Wet Mill Registration - ET": {"1": "Cooperative", "2": "Private"},
    "Wet Mill Registration - KE": {"1": "Cooperative", "2": "Estate"},
}

INFRASTRUCTURE_WATER_SOURCE_MAP = {
    "1": "River",
    "2": "Dam",
    "3": "Water pan",
    "4": "Piped system (local municipality)",
    "5": "Borehole",
    "6": "Spring",
    "7": "Roof catchment (rainwater)",
}

# 1. Infrastructure Mapping

# Mapping for infrastructure needs repair options (1–16, 0 = None)
INFRASTRUCTURE_REPAIR_MAP = {
    "1": "Constant, clean source of water",
    "2": "Water circulation and/or treatment",
    "3": "Water meter for measurement",
    "4": "Floatation tank",
    "5": "Cherry reception hopper",
    "6": "Fermentation tanks",
    "7": "Grading channels",
    "8": "Pulp hopper",
    "9": "General mills area clean and orderly",
    "10": "Drying tables in a good state of repair",
    "11": "Storage area clean",
    "12": "Weighing scale is calibrated",
    "13": "Pulp machine calibrated and oiled",
    "14": "Moisture meter, thermometer, hygrometer",
    "15": "Cherry purchasing receipts in stock",
    "16": "Covering materials available",
    "0": "None",
}

INFRASTRUCTURE_PULPING_BRAND_MAP = {  # Add Kenya brands (7, 8, and 9)
    "1": "Penagos",
    "2": "Mckinnon",
    "3": "Bendal",
    "4": "Pinhalense",
    "5": "Pre-agard",
    "6": "Agard",
    "7": "JM Estrada",
    "8": "Pallin & Alvis",
    "9": "Marshall Fowler",
}
INFRASTRUCTURE_PULPING_TYPE_MAP = {"1": "Disc", "2": "Drum", "3": "Scree"}
INFRASTRUCTURE_NETWORK_COVERAGE_MAP = {"1": "2G", "2": "3G", "3": "4G"}

# 2. Manager Needs Assessment Mapping
MANAGER_DOCS_MAP = {
    # Ethiopia
    "Wet Mill Visit - ET": {
        "1": "Registration license",
        "2": "Tax number",
        "3": "Production or operational license for current year",
        "4": "Export license/number",
        "0": "None",
    },
    # Kenya
    "Wet Mill Visit - KE": {
        "1": "Tax number",
        "2": "Cooperative registration with the ministry of cooperatives",
        "3": "Wet mill operation permit from the county",
        "4": "County business permit",
        "0": "None",
    },
    # Burundi
    "Wet Mill Visit - BU": {
        "1": "Registration license",
        "2": "Tax number",
        "3": "Production or operational license for current year",
        "4": "Export license/number",
        "0": "None",
    },
}

COFFEE_SALE_PERIOD_MAP = {
    "1": "Before the season, in order to access working capital",
    "2": "Late in the harvest season, as coffee accumulates in the warehouse",
    "3": "After the harvest season",
}

PRIMARY_BUYER_SERVICES_MAP = {
    "1": "Working capital to purchase coffee",
    "2": "Agronomic support",
    "3": "Processing training/quality support",
    "0": "No additional services offered",
}

MANAGER_BANKING_MAP = {
    "1": "No significant challenges accessing loans",
    "2": "Lack of physical assets for bank collateral",
    "3": "High interest rates",
    "4": "Need for existing purchase order from coffee buyer",
    "5": "Poor performance of coffee washing station",
    "6": "Lack of financial statements and information needed for financial institutions",
}

TECHNOLOGY_INFO_MAP = {
    "1": "Farmer names (e.g., Excel list of farmers)",
    "2": "Coffee volumes delivered to the coffee washing station",
    "3": "Accounting (e.g., regular entries and reconciliation in Excel or other tool)",
    "4": "Traceability (e.g., tracking daily batches and coffee washing station operations)",
    "5": "Farmer payments (e.g., digital record of farmer payments)",
    "6": "Do not use any digital tool",
}

# 3. Training Attendance Mapping (Dropped Burundi topics)
TRAINING_TOPIC_MAP = {
    "old": {
        "1": "Environmental Responsibility",
        "2": "Social Responsibility and Ethics",
        "3": "Gender Training",
        "4": "Occupational Health and Safety",
        "5": "Sustainability Standards Overview",
        "6": "Finance and Bookkeeping",
        "7": "Post-Harvest Coffee Processing and Quality Training",
        "8": "TASQ Overview ",
        "9": "Inclusive Training",
        "10": "Gender Training",
        "11": "Regenerative Agriculture",
        "12": "Farm-level Traceability",
        "13": "Cooperative Good Governance",
        "14": "Bookkeeping",
        "15": "Quality Control and Processing Overview",
    },
    "new": {
        "1": "Post Harvest Coffee Quality and Processing",
        "2": "Sustainability Standards Overview (SSO)",
        "3": "Social Responsibility and Ethics (SRE)",
        "4": "Gender",
        "5": "Environmental Responsibility (ER)",
        "6": "Occupational Health and Safety (OHS)",
        "7": "Finance and Bookkeeping",
        "8": "Wet Mill Processing and Quality Control",
        "9": "TASQ Overview",
        "10": "TASQ Inclusive Pillar",
        "11": "TASQ Regenerative Pillar",
        "12": "Bookkeeping",
        "13": "Cooperative Governance",
        "14": "Farm Level Traceability",
        "15": "Wet Mill Processing and Quality Control",
        "16": "Wet Mill coffee processing Parchment Traceability",
        "17": "Pulping Machine Operations and Maintenance",
        "18": "Nespresso AAA Regenerative Pillar Lesson Plan",
        "19": "IPDM Lesson Plan for Coop leaders and Agrochemical Storekeepers",
        "20": "Nespresso AAA TASQ Overview",
        "21": "Nespresso AAA Inclusive Pillar Lesson Plan",
        "22": "Safe use handling and storage",
        "23": "Kenya AAA POSA (Producer Organization Sustainability Assessment)",
    },
}

TRAINING_STATUS_MAP = {"1": "New", "2": "Refresher"}

# 4. Waste Water Management Mapping

# Lagoon material mapping
LAGOON_MATERIAL_MAP = {"1": "Earth", "2": "Concrete"}
# Vetiver wetland mappings
VETIVER_TYPE_MAP = {"1": "Single wetland", "2": "Stepped wetland (multiple wetlands)"}
VETIVER_MAINTENANCE_MAP = {
    "1": "Leveling/correction",
    "2": "Soil bund maintenance",
    "3": "Vetiver grass replacement",
    "4": "Weeding",
    "5": "Vetiver cutting",
    "6": "Connecting channel maintenance",
    "0": "None",
}

# Advice to wetmill
WASTE_WATER_ADVICE_TYPES = {
    "1": "Pulp separation advice",
    "2": "Lagoon or pond maintenance or location advice",
    "3": "Vetiver wetland maintenance advice",
}

# Pulp
WASTE_WATER_MANAGEMENT_METHODS = {
    "1": "Open lagoon or pond",
    "2": "Vetiver Wetland",
    "0": "No wastewater management, released onto land or into river",
}

# 5. Water and Energy Use
WATER_MANAGEMENT_PULP_SEPARATION = {
    "1": "Pulp hopper",
    "2": "Re-circulation pump with skin tower",
    "eco-pulper": "Eco-pulper",
}

WATER_USE_METHODS = {
    "1": "Water meter",
    "2": "Dip stick and tank size",
    "0": "No method used",
}

WATER_USE_EFFORTS = {
    "1": "Turning water taps off when not in use",
    "2": "Recirculation pump",
    "3": "Eco pulper",
    "4": "Repairing all leaks in tanks, pipes and gate valves",
    "0": "No efforts being made to reduce water consumption",
}

ENERGY_USE_SOURCES = {
    "1": "Mains electricity",
    "2": "Diesel generator",
    "3": "Solar panels",
}

# 6. Routine Visits
PURPOSE_OF_VISIT = {
    "1": "Performance of last year (Q1 and Q2)",
    "2": "Process quality check",
    "3": "SWOT analysis (Q1 and Q2)",
    "4": "Gender action plan meeting",
    "5": "Perform annual audit",
    "6": "Discuss annual audit feedback",
    "7": "Review visit (prior to advice from previous visits)",
}

# 7. KPIs
FARMER_PAYMENT_METHOD = {"1": "Direct payment", "2": "Broker"}

ALLOWED_SURVEYS = [
    "wet_mill_training",
    "routine_visit",
    "manager_needs_assessment",
    "infrastructure",
    "waste_water_management",
    "cpqi",
    "cherry_weekly_price",
    "kpis",
    "water_and_energy_use",
    "financials",
    "employees",
    "gender_equitable_business_practices",
]


def map_status(value, mapping_dict, default="Undefined"):
    return mapping_dict.get(value, default)


def map_manager_role(
    value, role_map, role_other, survey_type, default="undefined"
):  # changed default to "undefined". To make sure it is actually working.
    return (
        role_other
        if value == "99"
        else role_map.get(survey_type, {}).get(value, default)
    )


def map_mill_status(value, mill_status_map, survey_type, default="undefined"):
    return mill_status_map.get(survey_type, {}).get(value, default)


def update_photo_url(energy_use, field_name, url_string):
    pic = energy_use.get(field_name)
    energy_use[field_name] = f"{url_string}/{pic}" if pic else None
    return energy_use


def transform_water_and_energy_use(survey_data, url_string, form):
    transformed = survey_data.copy()

    # 1. water_usage
    water_usage = transformed.get("water_usage")
    if isinstance(water_usage, dict):

        methods = water_usage.get("what_method_is_used_to_measure_water_use")
        if isinstance(methods, str) and methods in WATER_USE_METHODS:
            water_usage["what_method_is_used_to_measure_water_use"] = WATER_USE_METHODS[
                methods
            ]

        efforts = water_usage.get(
            "are_there_any_efforts_going_on_to_reduce_water_consumption"
        )
        if isinstance(efforts, str):
            water_usage[
                "are_there_any_efforts_going_on_to_reduce_water_consumption"
            ] = [
                WATER_USE_EFFORTS.get(code)  # Get Multiple values e.g: 1 4 5 6
                for code in efforts.split()  # Split by empty space
                if code in WATER_USE_EFFORTS  # Map to text values
            ]

        # Add other efforts
        other_efforts = water_usage.get(
            "please_specify_the_other_efforts_going_on_to_reduce_the_water_consumption"
        )
        water_usage[
            "are_there_any_efforts_going_on_to_reduce_water_consumption"
        ].append(other_efforts)

        is_there_a_record_book = water_usage.get("is_there_a_record_book")
        water_usage["is_there_a_record_book"] = (
            "yes" if is_there_a_record_book == "1" else "no"
        )

        pic = water_usage.get("photo_fo_the_office_records")
        if pic:
            water_usage["photo_fo_the_office_records"] = f"{url_string}/{pic}"
        else:
            water_usage["photo_fo_the_office_records"] = None

        water_meter_photo = water_usage.get("photo_of_water_meter")
        if water_meter_photo:
            water_usage["photo_of_water_meter"] = f"{url_string}/{water_meter_photo}"
        else:
            water_usage["photo_of_water_meter"] = None

        transformed["water_usage"] = water_usage

    # 2. energy_use
    energy_use = transformed.get("energy_use")
    if isinstance(energy_use, dict):
        energy_source = energy_use.get("which_energy_source_is_used_at_the_wet_mill")
        if isinstance(energy_source, str):
            energy_use["which_energy_source_is_used_at_the_wet_mill"] = [
                ENERGY_USE_SOURCES.get(code)  # Get Multiple values e.g: 1 4 5 6
                for code in energy_source.split()  # Split by empty space
                if code in ENERGY_USE_SOURCES  # Map to text values
            ]

        energy_rb = energy_use.get("is_there_an_energy_record_book_to_track_energy")
        energy_use["is_there_an_energy_record_book_to_track_energy"] = (
            "yes" if energy_rb == "1" else "no"
        )

        photo_fields = [
            "photo_of_the_electric_meter",
            "photo_of_the_diesel_generator",
            "photo_of_the_solar_panels",
            "photo_of_energy_record_book",
        ]

        for field in photo_fields:
            energy_use = update_photo_url(energy_use, field, url_string)

        transformed["energy_use"] = energy_use

    return transformed


def transform_waste_water_management(survey_data, url_string, form):

    transformed = survey_data.copy()
    # 1. Lagoons mapping
    lagoons = transformed.get("lagoons")
    if isinstance(lagoons, dict):
        mat = lagoons.get("material")
        if isinstance(mat, str) and mat in LAGOON_MATERIAL_MAP:
            lagoons["material"] = LAGOON_MATERIAL_MAP[mat]

        pic = lagoons.get("photo")
        if pic:
            lagoons["photo"] = f"{url_string}/{pic}"

        transformed["lagoons"] = lagoons

    # 2. Vetiver wetland mapping
    vet = transformed.get("vetiver_wetland")
    if isinstance(vet, dict):
        # type of wetland
        tw = vet.get("type_of_wetland")
        if isinstance(tw, str) and tw in VETIVER_TYPE_MAP:
            vet["type_of_wetland"] = VETIVER_TYPE_MAP[tw]

        # maintenance done
        maint = vet.get("maintenance_done")
        if isinstance(maint, str):
            vet["maintenance_done"] = [
                VETIVER_MAINTENANCE_MAP.get(code)
                for code in maint.split()
                if code in VETIVER_MAINTENANCE_MAP
            ]

        # photo of vetiver wetland
        pic = vet.get("photo")
        if pic:
            vet["photo"] = f"{url_string}/{pic}"
        else:
            vet["photo"] = None

        transformed["vetiver_wetland"] = vet

    # 3. Advise to wetmill
    advise = transformed.get("advice_to_wet_mill")
    if isinstance(advise, dict):
        advice_type = advise.get("advice_type")

        if isinstance(advice_type, str):
            advise["advice_type"] = [
                WASTE_WATER_ADVICE_TYPES.get(
                    code
                )  # Get Advice types string EG: 1 4 5 6
                for code in advice_type.split()  # Split by empty space
                if code in WASTE_WATER_ADVICE_TYPES  # Map to text values
            ]

        transformed["advice_to_wet_mill"] = advise

    # 4. Pulp
    pulp = transformed.get("pulp_separator")
    if isinstance(pulp, dict):
        ww_methods = pulp.get("waste_water_management_methods")

        if isinstance(ww_methods, str):
            pulp["waste_water_management_methods"] = [
                WASTE_WATER_MANAGEMENT_METHODS.get(code)
                for code in ww_methods.split()  # Split by empty space
                if code in WASTE_WATER_MANAGEMENT_METHODS  # Map to text values
            ]

        pulp_separation = pulp.get("how_is_the_pulp_separated")

        if isinstance(ww_methods, str):
            pulp["how_is_the_pulp_separated"] = [
                WATER_MANAGEMENT_PULP_SEPARATION.get(code)
                for code in pulp_separation.split()  # Split by empty space
                if code in WATER_MANAGEMENT_PULP_SEPARATION  # Map to text values
            ]

        transformed["pulp_separator"] = pulp

    return transformed


def transform_wetmill_training(survey_data, url_string, form):
    version = (
        "old"
        if form.get("survey_type", "") == "Wet Mill Visit - ET"
        and int(form.get("@version", "")) <= 54
        else "new"
    )
    transformed = survey_data.copy()

    # Delete training_topic_category if it exists
    if "training_topic_category" in transformed:
        del transformed["training_topic_category"]

    # 1. training topic
    topic = transformed.get("training_topic")
    if isinstance(topic, str) and topic in TRAINING_TOPIC_MAP[version]:
        transformed["training_topic"] = TRAINING_TOPIC_MAP[version][topic]
    # 2. training status
    status = transformed.get("training_status")
    if isinstance(status, str) and status in TRAINING_STATUS_MAP:
        transformed["training_status"] = TRAINING_STATUS_MAP[status]

    # 3. picture URL
    pic_trainees = transformed.get("picture_of_trainees_group")
    if pic_trainees:
        transformed["picture_of_trainees_group"] = f"{url_string}/{pic_trainees}"
    else:
        transformed["picture_of_trainees_group"] = None

    # 4. picture of attendance form
    pic_attendance = transformed.get("picture_of_training_attendance_form")
    if pic_attendance:
        transformed["picture_of_training_attendance_form"] = (
            f"{url_string}/{pic_attendance}"
        )
    else:
        transformed["picture_of_training_attendance_form"] = None

    return transformed


def transform_manager_needs_assessment(survey_data, url_string, form):
    """
    Manager Needs Assessment survey:
    - Map business_and_operations subfields (documents, coffee_sale_period, primary_buyer
    services).
    - Map banking challenges.
    - Map technology information_captured .
    """
    transformed = survey_data.copy()

    # Business & Operations
    bo = transformed.get("business_and_operations")
    if isinstance(bo, dict):
        # Documents
        docs = bo.get("documents")
        if isinstance(docs, str):
            bo["documents"] = [
                MANAGER_DOCS_MAP.get(form.get("survey_type"), {}).get(code)
                for code in docs.split()
                if MANAGER_DOCS_MAP.get(form.get("survey_type"), {}).get(code)
            ]
        # Coffee sale period
        csp = bo.get("coffee_sale_period")
        if isinstance(csp, str) and csp in COFFEE_SALE_PERIOD_MAP:
            bo["coffee_sale_period"] = COFFEE_SALE_PERIOD_MAP[csp]
        # Primary buyer additional services
        pbas = bo.get("primary_buyer_additional_services_yn")
        if isinstance(pbas, str):
            bo["primary_buyer_additional_services_yn"] = [
                PRIMARY_BUYER_SERVICES_MAP.get(code)
                for code in pbas.split()
                if PRIMARY_BUYER_SERVICES_MAP.get(code)
            ]

        # NOTE: this is extra JSON level deep than normal questions, I am flattening it NOTE: Better solution can be used :)
        dist = bo.get("distribution_of_revenues")
        if isinstance(dist, dict):
            # bring nested keys up one level
            for dk, dv in dist.items():
                # skip label fields
                if dk.endswith("_label"):
                    continue
                bo[dk] = dv
            # remove the nested dict
            bo.pop("distribution_of_revenues", None)
        transformed["business_and_operations"] = bo

    # Banking
    banking = transformed.get("banking")
    if isinstance(banking, dict):
        chal = banking.get("significant_challenges_accessing_loans")
        if isinstance(chal, str) and chal in MANAGER_BANKING_MAP:
            banking["significant_challenges_accessing_loans"] = MANAGER_BANKING_MAP[
                chal
            ]
        transformed["banking"] = banking

    # Technology
    tech = transformed.get("technology")
    if isinstance(tech, dict):
        info = tech.get("information_captured")
        if isinstance(info, str):
            tech["information_captured"] = [
                TECHNOLOGY_INFO_MAP.get(code)
                for code in info.split()
                if TECHNOLOGY_INFO_MAP.get(code)
            ]
        transformed["technology"] = tech

    # operations.biggest_problems
    ops = transformed.get("operations")
    if isinstance(ops, dict) and "biggest_problems" in ops:
        del ops["biggest_problems"]
        transformed["operations"] = ops

    # perspective_of_manager.coffee_station_issues
    pom = transformed.get("perspective_of_manager")

    # perspective_of_manager_extra
    pom_extra = transformed.get("perspective_of_manager_extra")

    # add this to perspective_of_manager
    pom.update(pom_extra)

    if isinstance(pom, dict) and "coffee_station_issues" in pom:
        del pom["coffee_station_issues"]
        transformed["perspective_of_manager"] = pom

    return transformed


def transform_kpis(survey_data, url_string, form):
    transformed = survey_data.copy()
    pic = transformed.get("photo_of_cherry_receipts")
    if pic:
        transformed["photo_of_cherry_receipts"] = f"{url_string}/{pic}"

    fpm = transformed.get("farmer_payment_method")
    if isinstance(fpm, str) and fpm in FARMER_PAYMENT_METHOD:
        transformed["farmer_payment_method"] = FARMER_PAYMENT_METHOD[fpm]

    return transformed


def transform_infrastructure(survey_data, url_string, form):
    """
    Transformation for Infrastructure survey:
    - Map 'main_water_source' numeric codes to descriptive text.
    - which_of_the_following_needs_repair AND are_the_following_in_good_state_of_repair are multiple questions
    """
    transformed = survey_data.copy()
    # main_water_source
    code = transformed.get("main_water_source")
    if isinstance(code, str) and code in INFRASTRUCTURE_WATER_SOURCE_MAP:
        transformed["main_water_source"] = INFRASTRUCTURE_WATER_SOURCE_MAP[code]

    # are_the_following_in_good_state_of_repair
    good = transformed.get("are_the_following_in_good_state_of_repair")
    if isinstance(
        good, str
    ):  # Changed the logic since CommCare logic was changed too. These are now ALL equipment whether they need repair or not
        transformed["are_the_following_in_good_state_of_repair"] = [
            INFRASTRUCTURE_REPAIR_MAP[c]
            for c in good.split()
            if c in INFRASTRUCTURE_REPAIR_MAP
            and c
            not in transformed.get(
                "which_of_the_following_needs_repair_check_all_that_apply", ""
            ).split()
        ]

    # which_of_the_following_needs_repair
    rep = transformed.get("which_of_the_following_needs_repair_check_all_that_apply")
    if isinstance(rep, str):
        transformed["which_of_the_following_needs_repair"] = [
            INFRASTRUCTURE_REPAIR_MAP[c]
            for c in rep.split()
            if c in INFRASTRUCTURE_REPAIR_MAP
        ]
    # pulping_machine_brand
    brand = transformed.get("pulping_machine_brand")
    if isinstance(brand, str) and brand in INFRASTRUCTURE_PULPING_BRAND_MAP:
        transformed["pulping_machine_brand"] = INFRASTRUCTURE_PULPING_BRAND_MAP[brand]
    # pulping_machine_type
    ptype = transformed.get("pulping_machine_type")
    if isinstance(ptype, str) and ptype in INFRASTRUCTURE_PULPING_TYPE_MAP:
        transformed["pulping_machine_type"] = INFRASTRUCTURE_PULPING_TYPE_MAP[ptype]
    # network_coverage
    net = transformed.get("network_coverage")
    if isinstance(net, str) and net in INFRASTRUCTURE_NETWORK_COVERAGE_MAP:
        transformed["network_coverage"] = INFRASTRUCTURE_NETWORK_COVERAGE_MAP[net]

    return transformed


def transform_cpqi(survey_data, url_string, form):
    """
    For CPQI convert all values '1'/'0' to yes or no.
    """
    transformed = survey_data.copy()
    # Map cherry_reception fields
    cherry = transformed.get("cherry_reception")
    if isinstance(cherry, dict):
        for field in [
            "cherry_sorting",
            "cherry_weighing_essentials",
            "quality_cherry_delivery",
        ]:
            val = cherry.get(field)
            if val in ("1", "0"):
                cherry[field] = "yes" if val == "1" else "no"
    # Map pulping fields
    pulping = transformed.get("pulping")
    if isinstance(pulping, dict):
        for field in [
            "machine_calibration",
            "machine_cleanliness",
            "timely_cherry_pulping",
            "water_source_cleanliness",
        ]:
            val = pulping.get(field)
            if val in ("1", "0"):
                pulping[field] = "yes" if val == "1" else "no"
    # Map drying fields
    drying = transformed.get("drying")
    if isinstance(drying, dict):
        for field in [
            "bean_moisture_measurement",
            "covering_coffee",
            "drying_table_bean_depth",
            "drying_table_flatness",
            "parchment_sorting",
        ]:
            val = drying.get(field)
            if val in ("1", "0"):
                drying[field] = "yes" if val == "1" else "no"
    # Map fermentation fields
    fermentation = transformed.get("fermentation")
    if isinstance(fermentation, dict):
        for field in ["fermentation_monitoring", "fermentation_tank_cleanliness"]:
            val = fermentation.get(field)
            if val in ("1", "0"):
                fermentation[field] = "yes" if val == "1" else "no"
    # Map storage fields
    storage = transformed.get("storage")
    if isinstance(storage, dict):
        for field in ["orderly_store_registry", "store_cleanliness"]:
            val = storage.get(field)
            if val in ("1", "0"):
                storage[field] = "yes" if val == "1" else "no"

    # Map washing fields
    washing = transformed.get("washing")
    if isinstance(washing, dict):
        for field in ["washing_channel_cleanliness", "washing_monitoring"]:
            val = washing.get(field)
            if val in ("1", "0"):
                washing[field] = "yes" if val == "1" else "no"

    return transformed


# Transformation for financials survey
def transform_financials(survey_data, url_string, form):
    """
    - Remove the 'survey_6___financials' key.
    - Remove any keys ending with '_label'.
    - Leave all other fields and values unchanged.
    """

    def clean(d):
        result = {}
        for k, v in d.items():
            if k == "survey_6___financials" or k.endswith("_label"):
                continue
            if isinstance(v, dict):
                nested = clean(v)
                if nested is not None:
                    result[k] = nested
            else:
                result[k] = v
        return result

    return clean(survey_data)


# Transformation for employees survey
def transform_employees(survey_data, url_string, form):
    """
    Specific transformation for Employees survey:
    - Maps 'accountant' and 'sustainability_officer' from "1"/"0" to "yes"/"no"
    - Leaves all other fields as numeric values (floats).
    """
    transformed = {}
    for key, val in survey_data.items():
        if key in (
            "accountant",
            "sustainability_officer",
            "community_manager",
            "certification_officer",
            "machine_operator",
        ) and val in ("1", "0"):
            transformed[key] = "yes" if val == "1" else "no"
        else:
            try:
                transformed[key] = float(val)
            except:
                transformed[key] = val
    return transformed


# Transformation of Routine visit
def transformation_routine_visit(survey_data, url_string, form):

    transformed = {}

    # 1. map the purpose of visit (Include other)

    if survey_data.get("purpose_of_visit") == "99":
        transformed["purpose_of_visit"] = (
            f"Other: {survey_data.get('specify_the_purpose_of_visit')}"
        )
    else:
        transformed["purpose_of_visit"] = PURPOSE_OF_VISIT.get(
            survey_data.get("purpose_of_visit")
        )

    # 2. Summary of activity
    transformed["summary_of_activity"] = survey_data.get("summary_of_activity")

    # 3. Picture of activity
    pic = survey_data.get("picture_of_activity")
    if pic:
        transformed["picture_of_activity"] = f"{url_string}/{pic}"
    else:
        transformed["picture_of_activity"] = None

    transformed["general_feedback"] = survey_data.get("general_feedback")

    return transformed


# Transformation for Cherry Weekly Price
def transform_cherry_weekly_price(survey_data, url_string, form):
    transformed = {}

    transformed["date"] = survey_data.get("cherry_week")
    date = survey_data.get("cherry_week")
    if date:
        # Convert date string to datetime object
        import datetime

        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        transformed["cherry_week"] = str(date.isocalendar().week)

    else:
        transformed["cherry_week"] = None

    transformed["cherry_price"] = survey_data.get("cherry_price")
    transformed["general_feedback"] = survey_data.get("general_feedback")

    return transformed


# Transformation for Gender Equitable Business Practices
def transform_gender_equitable_business_practices(survey_data, url_string, form):
    """
    - Remove the 'survey_12___gender_equitable_business_practices' key.
    - Remove any keys ending with '_label'.
    - Find keys at second level and merge with keys of first level to completely remove the second level so that third level is the final level.
    - Change all values 'y'/'n' to 'Yes, most of the time'/'No, rarely or never' for any key that is under the dictionary 'delivers_meetings_and_training_in_ways_women_and_men_prefer'
    - Change all values 'y'/'n' to 'Equal to or more than 40 percent'/'Less than 40 percent' for any key that is under the dictionary 'delivers_resources_and_services_women_and_men_need'
    - Change any other values of 'y'/'n' to 'Yes'/'No' for any key that is under any other dictionaries
    - Leave all other fields and values unchanged.
    - Merge first nested dictionaries into the top level dictionary so that the final output includes only two levels of keys.

    """

    def clean(d):
        result = {}
        for k, v in d.items():
            if (
                k == "survey_12___gender_equitable_business_practices"
                or k.endswith("_label")
                or k == "table"
            ):
                continue
            if isinstance(v, dict):
                # Merge second level keys into the first level
                for sub_k, sub_v in v.items():
                    if isinstance(sub_v, dict):
                        result[f"{k}-{sub_k}"] = sub_v
                    else:
                        result[sub_k] = sub_v
            else:
                # If it's not a dict, just copy the value
                result[k] = v
        return result

    cleaned_assessment_form = clean(survey_data["assessment_form"])
    cleaned_action_plan = clean(survey_data.get("action_plan", {}))
    general_feedback = survey_data.get("general_feedback", None)

    cleaned = {
        **cleaned_assessment_form,
        **cleaned_action_plan,
    }  # Merge both cleaned dictionaries

    cleaned["general_feedback"] = (
        general_feedback  # Add general feedback to the cleaned data
    )

    # print(f"Cleaned Data: {cleaned}")  # Debugging line to check transformed data

    # Now change the values based on the specified conditions
    for k, v in cleaned.items():
        if (
            "delivers_meetings_and_training_in_ways_women_and_men_prefer" in k
            and isinstance(v, dict)
        ):
            for sub_k, sub_v in v.items():
                if sub_v == "y":
                    v[sub_k] = "Yes, most of the time"
                elif sub_v == "n":
                    v[sub_k] = "No, rarely or never"
        elif "delivers_resources_and_services_women_and_men_need" in k and isinstance(
            v, dict
        ):
            for sub_k, sub_v in v.items():
                if sub_v == "y":
                    v[sub_k] = "Equal to or more than 40 percent"
                elif sub_v == "n":
                    v[sub_k] = "Less than 40 percent"
        elif isinstance(v, dict):
            for sub_k, sub_v in v.items():
                if sub_v == "y":
                    v[sub_k] = "Yes"
                elif sub_v == "n":
                    v[sub_k] = "No"
        else:
            if v == "y":
                cleaned[k] = "Yes"
            elif v == "n":
                cleaned[k] = "No"

    # print(f"Transformed Data: {cleaned}")  # Debugging line to check cleaned data

    return cleaned


# Map survey names to their transformation functions
SURVEY_TRANSFORMATIONS = {
    "cpqi": transform_cpqi,
    "employees": transform_employees,
    "financials": transform_financials,
    "infrastructure": transform_infrastructure,
    "kpis": transform_kpis,
    "manager_needs_assessment": transform_manager_needs_assessment,
    "wet_mill_training": transform_wetmill_training,
    "waste_water_management": transform_waste_water_management,
    "water_and_energy_use": transform_water_and_energy_use,
    "routine_visit": transformation_routine_visit,
    "cherry_weekly_price": transform_cherry_weekly_price,
    "gender_equitable_business_practices": transform_gender_equitable_business_practices,
}
