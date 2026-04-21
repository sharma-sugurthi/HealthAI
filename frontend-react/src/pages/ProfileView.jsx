import React, { useEffect, useState } from 'react'
import { User2 } from 'lucide-react'
import { getMedicalProfile } from '../lib/api'
import { Card } from '../components/common/UI'

export default function ProfileView() {
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    getMedicalProfile()
      .then(setProfile)
      .catch(() =>
        setProfile({
          conditions: [],
          medications: [],
          allergies: [],
          symptoms: [],
        }),
      )
  }, [])

  const section = (title, items) => (
    <Card title={title} subtitle={`${items.length} record(s)`} icon={User2}>
      {items.length ? (
        items.map((item, idx) => (
          <div key={idx} className="list-item">
            <p>
              {item.condition_name ||
                item.medication_name ||
                item.allergen ||
                item.symptom_description}
            </p>
          </div>
        ))
      ) : (
        <div className="empty-state">No records yet.</div>
      )}
    </Card>
  )

  return (
    <div className="page-stack">
      <div className="section-head">
        <div>
          <h2>Medical profile</h2>
          <p>Patient history, medications, allergies, and symptom logs in one place.</p>
        </div>
      </div>
      <div className="profile-grid">
        {section('Conditions', profile?.conditions || [])}
        {section('Medications', profile?.medications || [])}
        {section('Allergies', profile?.allergies || [])}
        {section('Symptoms', profile?.symptoms || [])}
      </div>
    </div>
  )
}
