import React from 'react'
import {
  ChartColumnBig,
  FlaskConical,
  LogOut,
  MessageSquareText,
  User2,
} from 'lucide-react'
import { TABS } from '../../constants'
import { Button } from '../common/UI'

export default function AppShell({ user, onLogout, tab, setTab, children }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo">H</div>
          <div>
            <strong>Susruta</strong>
            <span>AI healthcare workspace</span>
          </div>
        </div>

        <nav className="nav-list">
          <button
            className={tab === TABS.chat ? 'nav-item active' : 'nav-item'}
            onClick={() => setTab(TABS.chat)}
          >
            <MessageSquareText size={18} /> Patient chat
          </button>
          <button
            className={tab === TABS.analytics ? 'nav-item active' : 'nav-item'}
            onClick={() => setTab(TABS.analytics)}
          >
            <ChartColumnBig size={18} /> Analytics
          </button>
          <button
            className={tab === TABS.plans ? 'nav-item active' : 'nav-item'}
            onClick={() => setTab(TABS.plans)}
          >
            <FlaskConical size={18} /> Treatment plans
          </button>
          <button
            className={tab === TABS.profile ? 'nav-item active' : 'nav-item'}
            onClick={() => setTab(TABS.profile)}
          >
            <User2 size={18} /> Medical profile
          </button>
        </nav>

        <div className="sidebar-card">
          <span>Signed in as</span>
          <strong>{user.full_name}</strong>
          <small>
            {user.age} yrs • {user.gender}
          </small>
        </div>

        <Button variant="secondary" onClick={onLogout} className="logout-btn">
          <LogOut size={16} /> Logout
        </Button>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  )
}
