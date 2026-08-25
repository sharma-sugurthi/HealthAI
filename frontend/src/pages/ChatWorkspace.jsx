import React, { useMemo, useState } from 'react'
import {
  FlaskConical,
  HeartPulse,
  LoaderCircle,
  Send,
  ShieldAlert,
  Stethoscope,
  Trash2,
} from 'lucide-react'
import { toast } from 'sonner'
import { analyzeSymptoms, generateTreatmentPlan, sendMessage } from '../lib/api'
import { SAMPLE_CONVERSATION } from '../constants'
import { Button, Card, MetricBadge } from '../components/common/UI'
import ToolForm from '../components/chat/ToolForm'

export default function ChatWorkspace({ user }) {
  const [messages, setMessages] = useState(SAMPLE_CONVERSATION)
  const [loading, setLoading] = useState(false)
  const [draft, setDraft] = useState('')

  const quickPrompts = useMemo(
    () => [
      'I have headache and fever. What should I do?',
      'Suggest a healthy meal plan for weight management.',
      'When should I seek urgent care for chest pain?',
    ],
    [],
  )

  const submitMessage = async (text) => {
    if (!text.trim()) return

    const next = [...messages, { role: 'user', content: text }]
    setMessages(next)
    setDraft('')
    setLoading(true)

    try {
      const response = await sendMessage(text)
      setMessages([
        ...next,
        { role: 'assistant', content: response.response, meta: { tag: 'AI response' } },
      ])
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Failed to send message')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="workspace-grid">
      <section className="workspace-panel">
        <div className="workspace-header">
          <div>
            <h2>Patient chat</h2>
            <p>Conversational health assistance with embedded clinical tools.</p>
          </div>
          <div className="workspace-actions">
            <Button variant="ghost" onClick={() => setMessages(SAMPLE_CONVERSATION)}>
              <Trash2 size={16} /> Reset
            </Button>
          </div>
        </div>

        <div className="chat-thread">
          {messages.map((message, index) => (
            <div key={index} className={`chat-row ${message.role}`}>
              <div className="chat-bubble">
                <div className="bubble-meta">
                  <span>{message.role === 'user' ? user.full_name : 'Susruta'}</span>
                  {message.meta?.tag ? <small>{message.meta.tag}</small> : null}
                </div>
                <p>{message.content}</p>
              </div>
            </div>
          ))}
          {loading ? (
            <div className="chat-row assistant">
              <div className="chat-bubble typing">
                <LoaderCircle size={16} className="spin" /> Generating response...
              </div>
            </div>
          ) : null}
        </div>

        <div className="quick-prompts">
          {quickPrompts.map((prompt) => (
            <button key={prompt} className="prompt-chip" type="button" onClick={() => setDraft(prompt)}>
              {prompt}
            </button>
          ))}
        </div>

        <div className="composer">
          <textarea
            rows="4"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Ask about symptoms, medications, next steps, or health tracking..."
          />
          <div className="composer-actions">
            <span className="composer-note">
              <ShieldAlert size={14} /> Educational guidance only — not a diagnosis.
            </span>
            <Button onClick={() => submitMessage(draft)} disabled={loading || !draft.trim()}>
              <Send size={16} /> Send
            </Button>
          </div>
        </div>
      </section>

      <aside className="tools-column">
        <Card
          title="Symptom analyzer"
          subtitle="Quick triage from a structured prompt."
          icon={Stethoscope}
        >
          <ToolForm
            label="Describe symptoms"
            placeholder="e.g., fever, fatigue, cough for 3 days"
            actionLabel="Analyze symptoms"
            onSubmit={async (value) => {
              const result = await analyzeSymptoms(value)
              setMessages((prev) => [
                ...prev,
                {
                  role: 'assistant',
                  content: result.analysis,
                  meta: { tag: 'Symptom analysis' },
                },
              ])
              toast.success('Analysis added to chat')
            }}
          />
        </Card>

        <Card
          title="Treatment planner"
          subtitle="Draft general care plans for a condition."
          icon={FlaskConical}
        >
          <ToolForm
            label="Condition"
            placeholder="e.g., Type 2 Diabetes"
            actionLabel="Generate plan"
            onSubmit={async (value) => {
              const result = await generateTreatmentPlan(value)
              setMessages((prev) => [
                ...prev,
                {
                  role: 'assistant',
                  content: result.plan || result.treatment_plan,
                  meta: { tag: 'Treatment draft' },
                },
              ])
              toast.success('Plan added to chat')
            }}
          />
        </Card>

        <Card title="Patient snapshot" subtitle="Profile and status summary." icon={HeartPulse}>
          <MetricBadge label="Age" value={user.age} />
          <MetricBadge label="Gender" value={user.gender} />
          <MetricBadge label="Status" value="Active" />
        </Card>
      </aside>
    </div>
  )
}
