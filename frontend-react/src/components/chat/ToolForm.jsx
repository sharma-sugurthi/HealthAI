import React, { useState } from 'react'
import { LoaderCircle, Plus } from 'lucide-react'
import { Button } from '../common/UI'

export default function ToolForm({ label, placeholder, actionLabel, onSubmit }) {
  const [value, setValue] = useState('')
  const [loading, setLoading] = useState(false)

  return (
    <div className="tool-form">
      <label>
        {label}
        <input value={value} onChange={(e) => setValue(e.target.value)} placeholder={placeholder} />
      </label>
      <Button
        className="full"
        disabled={loading || !value.trim()}
        onClick={async () => {
          setLoading(true)
          try {
            await onSubmit(value)
            setValue('')
          } finally {
            setLoading(false)
          }
        }}
      >
        {loading ? <LoaderCircle size={16} className="spin" /> : <Plus size={16} />}
        {actionLabel}
      </Button>
    </div>
  )
}
