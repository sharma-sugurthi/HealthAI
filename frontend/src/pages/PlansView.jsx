import React, { useEffect, useState } from 'react'
import { Bot, FlaskConical, LoaderCircle, MessageSquareText, Sparkles } from 'lucide-react'
import { toast } from 'sonner'
import { createTreatmentPlan, getTreatmentPlans } from '../lib/api'
import { Button, Card } from '../components/common/UI'

export default function PlansView() {
  const [condition, setCondition] = useState('')
  const [plans, setPlans] = useState([])
  const [savedPlans, setSavedPlans] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getTreatmentPlans().then(setSavedPlans).catch(() => setSavedPlans([]))
  }, [])

  const createPlan = async () => {
    setLoading(true)
    try {
      const result = await createTreatmentPlan({
        title: `Plan for ${condition}`,
        condition,
        plan_details: `General wellness-oriented plan for ${condition}.`,
      })
      setPlans((prev) => [result, ...prev])
      toast.success('Plan created')
      setCondition('')
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Failed to generate plan')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-stack">
      <div className="section-head">
        <div>
          <h2>Treatment plans</h2>
          <p>Draft patient-friendly recommendations and manage saved plans.</p>
        </div>
      </div>
      <div className="plan-grid">
        <Card
          title="Generate new plan"
          subtitle="Create a concise care plan for a condition."
          icon={FlaskConical}
        >
          <div className="tool-form">
            <label>
              Condition
              <input
                value={condition}
                onChange={(e) => setCondition(e.target.value)}
                placeholder="e.g., hypertension"
              />
            </label>
            <Button className="full" onClick={createPlan} disabled={loading || !condition.trim()}>
              {loading ? <LoaderCircle size={16} className="spin" /> : <Sparkles size={16} />}
              Generate plan
            </Button>
          </div>
        </Card>
        <Card title="Drafts" subtitle="Recently generated drafts." icon={Bot}>
          {plans.length ? (
            plans.map((plan, index) => (
              <div key={index} className="list-item">
                <strong>{plan.title || plan.condition}</strong>
                <p>{plan.plan_details || plan.plan || plan.treatment_plan}</p>
              </div>
            ))
          ) : (
            <div className="empty-state">No generated draft yet.</div>
          )}
        </Card>
      </div>
      <Card title="Saved treatment plans" subtitle="Plans already stored in your account." icon={MessageSquareText}>
        {savedPlans.length ? (
          savedPlans.map((plan) => (
            <div key={plan.id} className="list-item">
              <strong>{plan.title}</strong>
              <p>{plan.condition}</p>
            </div>
          ))
        ) : (
          <div className="empty-state">No saved plans available.</div>
        )}
      </Card>
    </div>
  )
}
