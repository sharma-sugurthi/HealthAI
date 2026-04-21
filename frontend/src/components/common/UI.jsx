import React from 'react'

export function Button({ children, variant = 'primary', className = '', ...props }) {
  const styles = {
    primary: 'btn btn-primary',
    secondary: 'btn btn-secondary',
    ghost: 'btn btn-ghost',
    danger: 'btn btn-danger',
  }

  return (
    <button className={`${styles[variant]} ${className}`.trim()} {...props}>
      {children}
    </button>
  )
}

export function Card({ title, subtitle, icon: Icon, children, actions }) {
  return (
    <section className="card">
      <div className="card-header">
        <div className="card-title-wrap">
          {Icon ? (
            <span className="card-icon">
              <Icon size={18} />
            </span>
          ) : null}
          <div>
            <h3>{title}</h3>
            {subtitle ? <p>{subtitle}</p> : null}
          </div>
        </div>
        {actions}
      </div>
      <div className="card-body">{children}</div>
    </section>
  )
}

export function MetricBadge({ label, value }) {
  return (
    <div className="metric-badge">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}
