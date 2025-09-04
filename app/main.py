from jobs.commcare_to_postgresql.attendance_light import run_attendance_light_ft_job

payload_example = {
  "app_id": "f079b0daae1d4d34a89e331dc5a72fbd",
  "archived": False,
  "attachments": {
    "1756732229642.jpg": {
      "content_type": "image/jpeg",
      "length": 109730,
      "url": "https://www.commcarehq.org/a/tns-proof-of-concept/api/form_attachment/v1/2613f776-2865-4045-8a65-eeed29ed06ce/1756732229642.jpg"
    },
    "form.xml": {
      "content_type": "text/xml",
      "length": 2222,
      "url": "https://www.commcarehq.org/a/tns-proof-of-concept/api/form_attachment/v1/2613f776-2865-4045-8a65-eeed29ed06ce/form.xml"
    }
  },
  "build_id": "f5b36588a96c416d97074b13f73a9c48",
  "domain": "tns-proof-of-concept",
  "edited_by_user_id": None,
  "edited_on": None,
  "form": {
    "#type": "data",
    "@name": "Attendance Light - Current Module",
    "@uiVersion": "1",
    "@version": "95",
    "@xmlns": "http://openrosa.org/formdesigner/1DA997E2-7E69-44B6-AF80-023C252D06CE",
    "Current_session_participants": {
      "date": "2025-09-01",
      "female_attendance": "14",
      "male_attendance": "11",
      "total_attendance": "25"
    },
    "case": {
      "@case_id": "TEST_CC_CASE_ID",
      "@date_modified": "2025-09-01T13:10:36.908000Z",
      "@user_id": "149c951672be43c6a181c5fb3dc6f85e",
      "@xmlns": "http://commcarehq.org/case/transaction/v2",
      "update": {
        "Session_1_Date": "2025-09-01",
        "Session_1_Female": "14",
        "Session_1_Male": "11"
      }
    },
    "current_module_name": "Household Nutrition 1",
    "current_module_number": "16",
    "date_last_one_year": "2024-09-01",
    "date_tomorrow": "2025-09-02",
    "ffg_id": "a0JOj000004hciNMAQ",
    "ffg_name": "Odako",
    "gps_coordinates": "6.5438677 38.8053416 2255.0 4.5",
    "meta": {
      "@xmlns": "http://openrosa.org/jr/xforms",
      "appVersion": "CommCare Android, version \"2.53.1\"(464694). App v106. CommCare Version 2.53.1. Build 464694, built on: 2023-07-31",
      "app_build_version": 106,
      "commcare_version": "2.53.1",
      "deviceID": "commcare_3e2d2b37-cd74-4e3c-a78f-34dd03f3e93c",
      "drift": "0",
      "geo_point": None,
      "instanceID": "2613f776-2865-4045-8a65-eeed29ed06ce",
      "location": {
        "#text": "6.5439303 38.805317 2218.0 9.0",
        "@xmlns": "http://commcarehq.org/xforms"
      },
      "timeEnd": "2025-09-01T13:10:36.908000Z",
      "timeStart": "2025-09-01T13:09:03.008000Z",
      "userID": "149c951672be43c6a181c5fb3dc6f85e",
      "username": "mbeyene"
    },
    "photo": "1756732229642.jpg",
    "selected_training_module": "a0LOj00000CikUNMAZ",
    "session": "first_session",
    "session_1_note": "OK",
    "survey_type": "Attendance Light",
    "trainer": "TEST_SF_ID",
    "you_are_about_to_complete_this_training_observation_form_press_the_my_form_": "Form_Complete"
  },
  "id": "2613f776-2865-4045-8a65-eeed29ed06ce",
  "indexed_on": "2025-09-01T14:18:06.003164Z",
  "initial_processing_complete": True,
  "is_phone_submission": True,
  "metadata": {
    "appVersion": "CommCare Android, version \"2.53.1\"(464694). App v106. CommCare Version 2.53.1. Build 464694, built on: 2023-07-31",
    "app_build_version": 106,
    "commcare_version": "2.53.1",
    "deviceID": "commcare_3e2d2b37-cd74-4e3c-a78f-34dd03f3e93c",
    "drift": "0",
    "geo_point": None,
    "instanceID": "2613f776-2865-4045-8a65-eeed29ed06ce",
    "location": "6.5439303 38.805317 2218.0 9.0",
    "timeEnd": "2025-09-01T13:10:36.908000Z",
    "timeStart": "2025-09-01T13:09:03.008000Z",
    "userID": "149c951672be43c6a181c5fb3dc6f85e",
    "username": "mbeyene"
  },
  "problem": None,
  "received_on": "2025-09-01T13:47:40.017155Z",
  "resource_uri": "",
  "server_modified_on": "2025-09-01T13:47:40.088536Z",
  "submit_ip": "196.191.60.248",
  "type": "data",
  "uiversion": "1",
  "version": "95"
}

run_attendance_light_ft_job(payload_example)