import React, { useEffect, useState } from 'react'
import { Activity, CalendarDays, ChartColumnBig, Plus } from 'lucide-react'
import { toast } from 'sonner'
import { getHealthMetrics, getHealthStats, recordHealthMetric } from '../lib/api'
import { HEALTH_METRICS } from '../constants'
import { Button, Card, MetricBadge } from '../components/common/UI'

export default function AnalyticsView() {
  const [metric, setMetric] = useState(HEALTH_METRICS[0])
  const [metrics, setMetrics] = useState([])
  const [stats, setStats] = useState(null)
  const [form, setForm] = useState({ value: '', unit: 'bpm', notes: '' })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const units = {
      'Heart Rate': 'bpm',
      'Blood Pressure (Systolic)': 'mmHg',
      'Blood Pressure (Diastolic)': 'mmHg',
      'Blood Glucose': 'mg/dL',
      Weight: 'kg',
      Temperature: '°F',
      'Oxygen Saturation': '%',
    }
    setForm((prev) => ({ ...prev, unit: units[metric] }))
  }, [metric])

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const [metricData, statData] = await Promise.all([
          getHealthMetrics(metric),
          getHealthStats(metric).catch(() => null),
        ])
        setMetrics(metricData)
        setStats(statData)
      } catch {
        setMetrics([])
        setStats(null)
      }
    }
    fetchMetrics()
  }, [metric])

  const submit = async () => {
    setLoading(true)
    try {
      await recordHealthMetric({
        metric_type: metric,
        value: Number(form.value),
        unit: form.unit,
        notes: form.notes,
      })
      toast.success('Metric recorded')
      setForm((prev) => ({ ...prev, value: '', notes: '' }))
      const [metricData, statData] = await Promise.all([
        getHealthMetrics(metric),
        getHealthStats(metric).catch(() => null),
      ])
      setMetrics(metricData)
      setStats(statData)
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Failed to record metric')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-stack">
      <div className="section-head">
        <div>
          <h2>Health analytics</h2>
          <p>Track vitals, view trends, and capture context with notes.</p>
        </div>
      </div>

      <div className="analytics-grid">
        <Card
          title="Add health data"
          subtitle="Structured data entry with clear units."
          icon={Activity}
        >
          <div className="field-grid metric-grid">
            <label>
              Metric
              <select value={metric} onChange={(e) => setMetric(e.target.value)}>
                {HEALTH_METRICS.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </label>
            <label>
              Unit
              <input value={form.unit} readOnly />
            </label>
          </div>
          <div className="field-grid metric-grid">
            <label>
              Value
              <input
                type="number"
                value={form.value}
                onChange={(e) => setForm({ ...form, value: e.target.value })}
              />
            </label>
            <label>
              Notes
              <input
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                placeholder="Optional note"
              />
            </label>
          </div>
          <Button onClick={submit} disabled={loading || !form.value}>
            <Plus size={16} /> Record metric
          </Button>
        </Card>

        <Card title="Current snapshot" subtitle="Most recent values and statistics." icon={ChartColumnBig}>
          <div className="stats-grid">
            <MetricBadge label="Latest" value={stats ? `${stats.latest} ${stats.unit}` : '—'} />
            <MetricBadge
              label="Average"
              value={stats ? `${stats.average.toFixed(1)} ${stats.unit}` : '—'}
            />
            <MetricBadge label="Minimum" value={stats ? `${stats.minimum} ${stats.unit}` : '—'} />
            <MetricBadge label="Maximum" value={stats ? `${stats.maximum} ${stats.unit}` : '—'} />
          </div>
        </Card>
      </div>

      <Card title={`Recent ${metric}`} subtitle="Chronological record of entries." icon={CalendarDays}>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Value</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {metrics.length ? (
                metrics.map((item) => (
                  <tr key={item.id}>
                    <td>{new Date(item.recorded_at).toLocaleString()}</td>
                    <td>
                      {item.value} {item.unit}
                    </td>
                    <td>{item.notes || '—'}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" className="empty">
                    No data yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
