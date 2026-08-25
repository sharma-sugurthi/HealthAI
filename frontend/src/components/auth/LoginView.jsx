import React, { useState } from 'react'
import { Activity, Bot, ShieldAlert, Sparkles } from 'lucide-react'
import { Button } from '../common/UI'

export default function LoginView({ onLogin, onRegister, loading }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({
    username: '',
    password: '',
    full_name: '',
    age: 30,
    gender: 'Prefer not to say',
  })

  const submit = async (e) => {
    e.preventDefault()
    if (mode === 'login') {
      await onLogin({ username: form.username, password: form.password })
    } else {
      await onRegister(form)
      setMode('login')
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-hero">
        <div className="brand-pill">
          <Sparkles size={14} /> Susruta
        </div>
        <h1>Modern AI healthcare workspace</h1>
        <p>
          Clean patient chat, structured health tracking, treatment planning, and safety-first
          medical guidance.
        </p>
        <div className="hero-points">
          <span>
            <Bot size={14} /> ChatGPT-style assistant
          </span>
          <span>
            <ShieldAlert size={14} /> Medical safety checks
          </span>
          <span>
            <Activity size={14} /> Health analytics
          </span>
        </div>
      </div>

      <div className="auth-card card">
        <div className="auth-toggle">
          <button
            className={mode === 'login' ? 'toggle active' : 'toggle'}
            onClick={() => setMode('login')}
            type="button"
          >
            Login
          </button>
          <button
            className={mode === 'register' ? 'toggle active' : 'toggle'}
            onClick={() => setMode('register')}
            type="button"
          >
            Register
          </button>
        </div>

        <form onSubmit={submit} className="auth-form">
          <div className="field-grid">
            <label>
              Username
              <input
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
            </label>
          </div>

          {mode === 'register' ? (
            <>
              <label>
                Full name
                <input
                  value={form.full_name}
                  onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                />
              </label>
              <div className="field-grid">
                <label>
                  Age
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={form.age}
                    onChange={(e) => setForm({ ...form, age: Number(e.target.value) })}
                  />
                </label>
                <label>
                  Gender
                  <select
                    value={form.gender}
                    onChange={(e) => setForm({ ...form, gender: e.target.value })}
                  >
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                    <option>Prefer not to say</option>
                  </select>
                </label>
              </div>
            </>
          ) : null}

          <Button type="submit" disabled={loading}>
            {mode === 'login' ? 'Login' : 'Create account'}
          </Button>
        </form>
      </div>
    </div>
  )
}
