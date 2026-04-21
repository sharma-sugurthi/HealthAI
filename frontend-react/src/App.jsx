import React, { useEffect, useState } from 'react'
import { Toaster, toast } from 'sonner'
import {
  getMe,
  loginUser,
  registerUser,
  setAuthToken,
} from './lib/api'
import LoginView from './components/auth/LoginView'
import AppShell from './components/layout/AppShell'
import { TABS } from './constants'
import ChatWorkspace from './pages/ChatWorkspace'
import AnalyticsView from './pages/AnalyticsView'
import PlansView from './pages/PlansView'
import ProfileView from './pages/ProfileView'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [user, setUser] = useState(null)
  const [tab, setTab] = useState(TABS.chat)
  const [token, setTokenState] = useState(localStorage.getItem('healthai_token') || '')

  useEffect(() => {
    if (token) setAuthToken(token)
  }, [token])

  useEffect(() => {
    const loadUser = async () => {
      if (!token) return
      try {
        const me = await getMe()
        setUser(me)
      } catch {
        setTokenState('')
        localStorage.removeItem('healthai_token')
        setAuthToken(null)
      }
    }
    loadUser()
  }, [token])

  const handleLogin = async ({ username, password }) => {
    setLoading(true)
    try {
      const data = await loginUser(username, password)
      localStorage.setItem('healthai_token', data.access_token)
      setTokenState(data.access_token)
      setAuthToken(data.access_token)
      const me = await getMe()
      setUser(me)
      toast.success('Login successful')
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (payload) => {
    setLoading(true)
    try {
      await registerUser(payload)
      toast.success('Account created. Please login.')
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Registration failed')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('healthai_token')
    setAuthToken(null)
    setUser(null)
    setTokenState('')
    setTab(TABS.chat)
    toast.message('Logged out')
  }

  return (
    <>
      <Toaster richColors position="top-right" />
      <div className="app-root">
        {!user ? (
          <LoginView onLogin={handleLogin} onRegister={handleRegister} loading={loading} />
        ) : (
          <AppShell user={user} onLogout={handleLogout} tab={tab} setTab={setTab}>
            {tab === TABS.chat ? <ChatWorkspace user={user} /> : null}
            {tab === TABS.analytics ? <AnalyticsView user={user} /> : null}
            {tab === TABS.plans ? <PlansView user={user} /> : null}
            {tab === TABS.profile ? <ProfileView /> : null}
          </AppShell>
        )}
      </div>
    </>
  )
}
