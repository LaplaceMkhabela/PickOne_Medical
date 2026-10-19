/*
 * Mock database for the static PickOne Medical demo.
 * Mirrors seed.py + app.py models so the demo runs with no backend.
 */
(function (global) {
  'use strict';

  const DB_KEY = 'pickone_demo_db_v1';
  const SEED_MAX_AGE_DAYS = 7;

  const SEED_USERS = [
    { user_name: 'Dr. Sarah Jenkins', user_id: 'DOC-100', user_email: 'dr.jenkins@pickone.com', user_role: 'doctor' },
    { user_name: 'Dr. Marcus', user_id: 'DOC-101', user_email: 'dr.marcus@pickone.com', user_role: 'doctor' },
    { user_name: 'Nurse Admin', user_id: 'NUR-100', user_email: 'nurse.admin@pickone.com', user_role: 'nurse' },
    { user_name: 'Sarah Jenkins', user_id: 'PAT-1042', user_email: 'sarah.j@example.com', user_role: 'patient' },
    { user_name: 'Marcus Chen', user_id: 'PAT-0891', user_email: 'marcus.c@example.com', user_role: 'patient' },
    { user_name: 'Elena Rodriguez', user_id: 'PAT-2055', user_email: 'elena.r@example.com', user_role: 'patient' }
  ];

  const SEED_PATIENTS = [
    {
      patient_id: 'PAT-1042', first_name: 'Sarah', last_name: 'Jenkins',
      dob: '1981-05-14', gender: 'F', blood_type: 'A+',
      allergies: 'Penicillin, Peanuts',
      active_medications: 'Lisinopril 10mg (Daily), Metformin 500mg (BID)'
    },
    {
      patient_id: 'PAT-0891', first_name: 'Marcus', last_name: 'Chen',
      dob: '1975-11-22', gender: 'M', blood_type: 'O-',
      allergies: 'None',
      active_medications: 'Albuterol Inhaler (As needed)'
    },
    {
      patient_id: 'PAT-2055', first_name: 'Elena', last_name: 'Rodriguez',
      dob: '1992-03-08', gender: 'F', blood_type: 'B+',
      allergies: 'Latex, Sulfa Drugs',
      active_medications: 'None'
    }
  ];

  const SEED_RECORDS = [
    {
      patient_id: 'PAT-1042', recorded_by: 'Dr. Marcus', days_ago: 90,
      bp: '140/90', heart_rate: 82, temperature: 36.6, spo2: 98, weight: 75.0, height: 165,
      nurse_notes: 'Patient reports frequent dizziness and fatigue.',
      diagnosis: 'Essential Hypertension. High fasting blood glucose indicating early Type 2 Diabetes.',
      prescriptions: 'Lisinopril 10mg once daily.'
    },
    {
      patient_id: 'PAT-1042', recorded_by: 'Dr. Marcus', days_ago: 45,
      bp: '135/85', heart_rate: 78, temperature: 36.5, spo2: 99, weight: 73.5, height: 165,
      nurse_notes: 'Follow-up on BP. Patient trying to improve diet.',
      diagnosis: 'Hypertension showing slight improvement. Confirmed Type 2 Diabetes after A1C test.',
      prescriptions: 'Metformin 500mg twice daily with meals. Continue Lisinopril.'
    },
    {
      patient_id: 'PAT-1042', recorded_by: 'Nurse Admin', days_ago: 2,
      bp: '125/82', heart_rate: 74, temperature: 36.7, spo2: 98, weight: 71.2, height: 165,
      nurse_notes: 'Routine triage check. Patient feels much better.',
      diagnosis: '', prescriptions: ''
    },
    {
      patient_id: 'PAT-0891', recorded_by: 'Nurse Admin', days_ago: 14,
      bp: '120/80', heart_rate: 88, temperature: 38.2, spo2: 94, weight: 82.0, height: 180,
      nurse_notes: 'Patient presents with high fever, persistent cough.',
      diagnosis: '', prescriptions: ''
    },
    {
      patient_id: 'PAT-0891', recorded_by: 'Dr. Sarah Jenkins', days_ago: 14,
      bp: '122/82', heart_rate: 85, temperature: 38.0, spo2: 95, weight: 82.0, height: 180,
      nurse_notes: 'Doctor consultation.',
      diagnosis: 'Acute Bronchitis.',
      prescriptions: 'Amoxicillin 500mg every 8 hours for 7 days. Albuterol inhaler PRN.'
    },
    {
      patient_id: 'PAT-0891', recorded_by: 'Dr. Sarah Jenkins', days_ago: 2,
      bp: '118/78', heart_rate: 70, temperature: 36.6, spo2: 99, weight: 81.5, height: 180,
      nurse_notes: 'Follow-up. Lungs clear.',
      diagnosis: 'Resolved Bronchitis.',
      prescriptions: 'Discontinue Amoxicillin.'
    }
  ];

  const SEED_APPOINTMENTS = [
    {
      patient_id: 'PAT-1042', doctor_name: 'Dr. Sarah Jenkins', in_days: 5,
      appointment_time: '10:00 AM', reason: 'Routine Diabetes Follow-up', status: 'Approved'
    },
    {
      patient_id: 'PAT-1042', doctor_name: 'Dr. Marcus', in_days: 21,
      appointment_time: '02:30 PM', reason: 'Cardiology Consult', status: 'Pending'
    },
    {
      patient_id: 'PAT-0891', doctor_name: 'Dr. Sarah Jenkins', in_days: 2,
      appointment_time: '09:15 AM', reason: 'Post-infection checkup', status: 'Approved'
    }
  ];

  const AI_SUMMARIES = {
    'PAT-1042': [
      'Sarah Jenkins is a 44-year-old female (A+) under management for essential hypertension and early type 2 diabetes, currently taking Lisinopril 10mg daily and Metformin 500mg BID. Her telemetry shows steady improvement: BP has fallen from 140/90 to 125/82, resting heart rate from 82 to 74 bpm, and body weight from 75.0kg to 71.2kg across the last three visits. The latest triage entry notes the patient feels much better, with no new symptoms reported.',
      '',
      'Automated Insights:',
      '• Blood pressure responding well to current regimen — continue Lisinopril 10mg daily.',
      '• Weight down 3.8kg over ~3 months; sustained dietary adherence is likely driving the BP trend.',
      '• Allergy alert: Penicillin, Peanuts — flag before prescribing any penicillin-class antibiotic.'
    ].join('\n'),
    'PAT-0891': [
      'Marcus Chen is a 50-year-old male (O-) who presented two weeks ago with fever (38.2°C), persistent cough and SpO2 of 94%, and was diagnosed with acute bronchitis by Dr. Sarah Jenkins. He was started on Amoxicillin 500mg Q8H for 7 days plus PRN Albuterol, and the most recent follow-up documents resolved bronchitis with clear lungs, afebrile vitals (36.6°C, SpO2 99%) and a resting heart rate of 70 bpm. Amoxicillin has been discontinued.',
      '',
      'Automated Insights:',
      '• Infection fully resolved — no further antibiotics indicated.',
      '• SpO2 recovered from 94% to 99%; oxygenation is back to baseline.',
      '• Continue PRN Albuterol only if respiratory symptoms recur.'
    ].join('\n'),
    'PAT-2055': [
      'Elena Rodriguez has no visit records on file yet. Once her first encounter is recorded by nursing or clinical staff, an AI-generated overview of her vitals, diagnoses and prescriptions will appear here.',
      '',
      'Automated Insights:',
      '• No historical telemetry available for analysis.',
      '• Known allergies on file: Latex, Sulfa Drugs.',
      '• Schedule an intake appointment to establish a clinical baseline.'
    ].join('\n')
  };

  function pad(n) { return String(n).padStart(2, '0'); }

  function toISODate(d) {
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }

  function toISOStamp(d) {
    return toISODate(d) + 'T' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
  }

  function shiftDays(days) {
    const d = new Date();
    d.setDate(d.getDate() + days);
    return d;
  }

  function daysSince(iso) {
    const then = new Date(iso).getTime();
    if (isNaN(then)) return Infinity;
    return (Date.now() - then) / 86400000;
  }

  function buildSeed() {
    let nextId = 1;
    const records = SEED_RECORDS.map((r) => {
      const copy = Object.assign({}, r);
      delete copy.days_ago;
      copy.id = nextId++;
      copy.timestamp = toISOStamp(shiftDays(-r.days_ago));
      return copy;
    });

    const appointments = SEED_APPOINTMENTS.map((a) => {
      const copy = Object.assign({}, a);
      delete copy.in_days;
      copy.id = nextId++;
      copy.appointment_date = toISODate(shiftDays(a.in_days));
      return copy;
    });

    return {
      _seeded: new Date().toISOString(),
      _nextId: nextId,
      users: SEED_USERS.map((u) => Object.assign({ password: 'password123', subscription_tier: 'trial' }, u)),
      patients: SEED_PATIENTS.map((p) => Object.assign({}, p)),
      records: records,
      appointments: appointments
    };
  }

  let cache = null;

  function persist(state) {
    cache = state;
    try {
      localStorage.setItem(DB_KEY, JSON.stringify(state));
    } catch (e) { /* storage unavailable — session-only demo */ }
  }

  function load() {
    if (cache) return cache;
    try {
      const raw = localStorage.getItem(DB_KEY);
      if (raw) {
        const state = JSON.parse(raw);
        if (state && state._seeded && daysSince(state._seeded) <= SEED_MAX_AGE_DAYS) {
          cache = state;
          return cache;
        }
      }
    } catch (e) { /* fall through to fresh seed */ }
    const fresh = buildSeed();
    persist(fresh);
    return fresh;
  }

  const DB = {
    reset() {
      const fresh = buildSeed();
      persist(fresh);
      return fresh;
    },

    state: load,

    users() { return load().users; },

    findUser(id, role) {
      return load().users.find((u) => u.user_id === id && (!role || u.user_role === role)) || null;
    },

    addUser(user) {
      const state = load();
      if (state.users.some((u) => u.user_id === user.user_id)) {
        return { ok: false, error: 'User ID already exists. Please choose another or login.' };
      }
      state.users.push(Object.assign({ subscription_tier: 'trial' }, user));
      persist(state);
      return { ok: true };
    },

    patients() { return load().patients; },

    findPatient(id) {
      if (!id) return null;
      const needle = String(id).trim().toUpperCase();
      return load().patients.find((p) => p.patient_id.toUpperCase() === needle) || null;
    },

    updatePatient(id, fields) {
      const state = load();
      const patient = state.patients.find((p) => p.patient_id === id);
      if (!patient) return false;
      Object.assign(patient, fields);
      persist(state);
      return true;
    },

    records(patientId, order) {
      const list = load().records.filter((r) => r.patient_id === patientId);
      list.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      if (order === 'desc') list.reverse();
      return list;
    },

    addRecord(record) {
      const state = load();
      const full = Object.assign({
        id: state._nextId,
        timestamp: toISOStamp(new Date()),
        bp: null, heart_rate: null, temperature: null, spo2: null,
        weight: null, height: null,
        nurse_notes: '', diagnosis: '', prescriptions: ''
      }, record);
      state._nextId += 1;
      state.records.push(full);
      persist(state);
      return full;
    },

    appointments(filter) {
      const list = load().appointments.filter((a) => !filter || a.patient_id === filter);
      list.sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date));
      return list;
    },

    addAppointment(appt) {
      const state = load();
      const full = Object.assign({ id: state._nextId, status: 'Pending' }, appt);
      state._nextId += 1;
      state.appointments.push(full);
      persist(state);
      return full;
    },

    setAppointmentStatus(id, status) {
      const state = load();
      const appt = state.appointments.find((a) => String(a.id) === String(id));
      if (!appt) return false;
      appt.status = status;
      persist(state);
      return true;
    },

    trendData(patientId) {
      const ascending = DB.records(patientId);
      const trend = { labels: [], heart_rate: [], temperature: [], weight: [], spo2: [] };
      ascending.forEach((r) => {
        if (!r.heart_rate && !r.temperature && !r.weight && !r.spo2) return;
        const d = new Date(r.timestamp);
        trend.labels.push(MONTHS[d.getMonth()] + ' ' + pad(d.getDate()));
        trend.heart_rate.push(r.heart_rate != null ? r.heart_rate : null);
        trend.temperature.push(r.temperature != null ? r.temperature : null);
        trend.weight.push(r.weight != null ? r.weight : null);
        trend.spo2.push(r.spo2 != null ? r.spo2 : null);
      });
      return trend;
    }
  };

  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  const ALLERGY_MAP = [
    { allergy: 'penicillin', triggers: ['penicillin', 'amoxicillin', 'ampicillin', 'amoxicil', 'nafcillin'] },
    { allergy: 'sulfa', triggers: ['sulfamethoxazole', 'sulfa', 'bactrim', ' sulfadiazine'] },
    { allergy: 'latex', triggers: [] },
    { allergy: 'peanuts', triggers: ['peanut'] }
  ];

  const INTERACTION_MAP = [
    { must: ['lisinopril'], triggers: ['potassium', 'spironolactone', 'ibuprofen'], note: 'NSAIDs / potassium-sparing agents can blunt the antihypertensive effect of Lisinopril and raise hyperkalaemia risk.' },
    { must: ['metformin'], triggers: ['contrast dye', 'iodinated'], note: 'Iodinated contrast dye with Metformin requires renal monitoring and a temporary hold.' }
  ];

  const AI = {
    summary(patient, records) {
      if (!patient) return 'No patient selected.';
      if (AI_SUMMARIES[patient.patient_id]) return AI_SUMMARIES[patient.patient_id];

      if (!records.length) {
        return 'No visit records on file for ' + patient.first_name + ' ' + patient.last_name +
          ' yet. Once encounters are recorded, an AI-generated clinical overview will appear here.';
      }

      const latest = records[0];
      const lines = [
        patient.first_name + ' ' + patient.last_name + ' (' + patient.patient_id + ') has ' + records.length +
        ' recorded encounter' + (records.length === 1 ? '' : 's') + ' on file. The most recent entry (' +
        formatDate(latest.timestamp) + ') was recorded by ' + latest.recorded_by +
        (latest.bp ? ' with BP ' + latest.bp + ', HR ' + latest.heart_rate + ' bpm' : '') +
        (latest.diagnosis ? ' and the diagnosis: ' + latest.diagnosis : '') + '.',
        '',
        'Automated Insights:',
        '• Active medications: ' + (patient.active_medications || 'None recorded') + '.',
        '• Allergies on file: ' + (patient.allergies || 'None recorded') + '.',
        '• Review the historical record list below for full telemetry context.'
      ];
      return lines.join('\n');
    },

    checkConflicts(patient, prescription) {
      if (!patient || !prescription) return { ok: true };
      const rx = ' ' + prescription.toLowerCase() + ' ';
      const allergies = (patient.allergies || '').toLowerCase();

      for (const map of ALLERGY_MAP) {
        if (allergies.includes(map.allergy)) {
          for (const trigger of map.triggers) {
            if (rx.includes(trigger)) {
              return {
                ok: false,
                warning: 'WARNING: Prescription appears to contain "' + trigger.trim() +
                  '" but the patient has a recorded ' + map.allergy + ' allergy.'
              };
            }
          }
        }
      }

      const meds = (patient.active_medications || '').toLowerCase();
      for (const map of INTERACTION_MAP) {
        if (map.must.some((m) => meds.includes(m)) && map.triggers.some((t) => rx.includes(t))) {
          return { ok: false, warning: 'WARNING: ' + map.note };
        }
      }

      return { ok: true };
    },

    chat(patient, records, message) {
      return new Promise((resolve) => {
        const reply = AI.buildReply(patient, records, message);
        const delay = 600 + Math.random() * 700;
        setTimeout(() => resolve(reply), delay);
      });
    },

    buildReply(patient, records, message) {
      const q = (message || '').toLowerCase();
      const name = patient.first_name + ' ' + patient.last_name;
      const latest = records[0];

      if (!records.length) {
        return 'There are no recorded encounters for ' + name + ' (' + patient.patient_id +
          ') yet, so I cannot answer from clinical history. Vitals and notes will appear here after the first recorded visit.';
      }

      if (/(allerg|contra)/.test(q)) {
        const allergies = patient.allergies && patient.allergies !== 'None'
          ? patient.allergies
          : 'no known allergies';
        return name + ' has recorded allergies: ' + allergies + '. Current medications on file: ' +
          (patient.active_medications || 'none') +
          '. Always cross-check any new prescription against this list before signing off.';
      }

      if (/(interact|conflict|safe|prescri|drug|rx|dosage)/.test(q)) {
        const rxList = records.filter((r) => r.prescriptions).map((r) => r.prescriptions);
        const current = rxList.length ? rxList[0] : 'none on file';
        return 'Current prescription history for ' + name + ' (most recent first): ' +
          (rxList.length ? rxList.join(' | ') : 'none on file') +
          '. The active regimen is: ' + current +
          '. No severe interaction is flagged in the recorded history, but verify against the allergy list (' +
          (patient.allergies || 'none') + ') before issuing anything new.';
      }

      if (/(vital|bp|blood pressure|heart|pulse|temperature|weight|spo2|oxygen|trend|telemetry)/.test(q)) {
        const r = latest;
        return 'Latest vitals for ' + name + ' (' + formatDate(r.timestamp) + '): BP ' + (r.bp || '--') +
          ', HR ' + (r.heart_rate || '--') + ' bpm, Temp ' + (r.temperature || '--') +
          '°C, SpO2 ' + (r.spo2 || '--') + '%, Weight ' + (r.weight || '--') + ' kg. ' +
          'Recorded by ' + r.recorded_by + ' across ' + records.length + ' encounter(s) in total.';
      }

      if (/(diagnos|condition|illness|disease)/.test(q)) {
        const dx = records.filter((r) => r.diagnosis);
        if (!dx.length) return 'No diagnoses have been recorded for ' + name + ' yet.';
        return 'Recorded diagnoses for ' + name + ', most recent first: ' +
          dx.map((r) => formatDate(r.timestamp) + ' — ' + r.diagnosis).join(' | ');
      }

      if (/(appointment|schedule|book|consult)/.test(q)) {
        const appts = DB.appointments(patient.patient_id);
        if (!appts.length) return name + ' has no upcoming appointments on the schedule.';
        return name + ' has ' + appts.length + ' upcoming appointment(s): ' +
          appts.map((a) => a.appointment_date + ' at ' + a.appointment_time + ' with ' + a.doctor_name + ' (' + a.status + ')').join('; ') + '.';
      }

      if (/(summary|summar|overview|summarize|history)/.test(q)) {
        return AI.summary(patient, records);
      }

      return 'Based on the record for ' + name + ' (' + patient.patient_id + '), the most recent encounter was on ' +
        formatDate(latest.timestamp) + ' with ' + latest.recorded_by +
        (latest.diagnosis ? ' documenting: ' + latest.diagnosis : '') +
        (latest.prescriptions ? ' and Rx: ' + latest.prescriptions : '') +
        '. Ask me about vitals, diagnoses, prescriptions, allergies or appointments for more detail.';
    }
  };

  function formatDate(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    return MONTHS[d.getMonth()] + ' ' + pad(d.getDate()) + ', ' + d.getFullYear();
  }

  function formatDateTime(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    let hours = d.getHours();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12;
    return MONTHS[d.getMonth()] + ' ' + pad(d.getDate()) + ', ' + d.getFullYear() + ' ' +
      pad(hours) + ':' + pad(d.getMinutes()) + ' ' + ampm;
  }

  function calculateAge(dob) {
    const parts = (dob || '').split('-');
    if (parts.length !== 3) return '--';
    const birth = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    if (isNaN(birth)) return '--';
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    if (today.getMonth() < birth.getMonth() || (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate())) {
      age -= 1;
    }
    return age;
  }

  global.POM = Object.assign(global.POM || {}, {
    DB: DB,
    AI: AI,
    MONTHS: MONTHS,
    pad: pad,
    formatDate: formatDate,
    formatDateTime: formatDateTime,
    calculateAge: calculateAge,
    toISODate: toISODate
  });
})(window);
