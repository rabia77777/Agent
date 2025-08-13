import React, { useEffect, useRef, useState } from 'react'
import VoiceRecorder from './VoiceRecorder'
import { chat, connectSocket } from '../services/api'

export default function ChatBox() {
	const [messages, setMessages] = useState([{
		role: 'system',
		text: 'Welcome to the Dispatcher. Try: "assign load L1001 to nearest", "eta from Los Angeles to San Francisco".'
	}])
	const [input, setInput] = useState('')
	const bottomRef = useRef(null)

	useEffect(() => {
		const ws = connectSocket((event) => {
			setMessages((prev) => [...prev, { role: 'event', text: JSON.stringify(event) }])
		})
		return () => ws.close()
	}, [])

	useEffect(() => {
		bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
	}, [messages])

	const handleSend = async () => {
		if (!input.trim()) return
		const userMessage = input
		setMessages((prev) => [...prev, { role: 'user', text: userMessage }])
		setInput('')
		try {
			const res = await chat(userMessage)
			setMessages((prev) => [...prev, { role: 'assistant', text: formatAssistant(res) }])
		} catch (e) {
			setMessages((prev) => [...prev, { role: 'assistant', text: 'Error: ' + e.message }])
		}
	}

	const formatAssistant = (res) => {
		const { action, data } = res
		if (action === 'route_eta') {
			if (data.error) return `Error: ${data.error}`
			return `Distance: ${data.distance_miles} mi, ETA: ${data.eta_hours} h`
		}
		if (action === 'assign_driver') {
			if (data.error) return `Error: ${data.error}${data.hos_reason ? ' (' + data.hos_reason + ')' : ''}`
			return `Assigned ${data.driver._id} to ${data.load._id}. ETA: ${data.assignment.eta_hours.toFixed(2)} h`
		}
		if (action === 'get_driver_status') {
			return `Driver status: ${JSON.stringify(data.driver)}`
		}
		if (action === 'notify') {
			return `Notification sent.`
		}
		return `Unknown command.`
	}

	return (
		<div className="flex flex-col h-full w-full max-w-3xl mx-auto">
			<div className="flex-1 overflow-y-auto p-4 space-y-2">
				{messages.map((m, idx) => (
					<div key={idx} className={
						m.role === 'user' ? 'text-right' : m.role === 'assistant' ? 'text-left' : 'text-center text-xs text-gray-500'
					}>
						<span className={
							`inline-block px-3 py-2 rounded ${m.role === 'user' ? 'bg-indigo-600 text-white' : m.role === 'assistant' ? 'bg-gray-200 dark:bg-gray-800' : ''}`
						}>{m.text}</span>
					</div>
				))}
				<div ref={bottomRef} />
			</div>
			<div className="p-4 border-t border-gray-200 dark:border-gray-700 flex gap-2 items-center">
				<input
					className="flex-1 px-3 py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
					placeholder="Type a command..."
					value={input}
					onChange={(e) => setInput(e.target.value)}
					onKeyDown={(e) => e.key === 'Enter' && handleSend()}
				/>
				<VoiceRecorder onResult={(t) => setInput(t)} />
				<button onClick={handleSend} className="px-3 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700">Send</button>
			</div>
		</div>
	)
}