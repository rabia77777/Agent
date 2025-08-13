import React from 'react'

export default function VoiceRecorder({ onResult }) {
	const handleStart = () => {
		const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
		if (!SpeechRecognition) {
			alert('SpeechRecognition not supported in this browser')
			return
		}
		const recognition = new SpeechRecognition()
		recognition.lang = 'en-US'
		recognition.interimResults = false
		recognition.maxAlternatives = 1
		recognition.onresult = (event) => {
			const text = event.results[0][0].transcript
			onResult?.(text)
		}
		recognition.onerror = () => {}
		recognition.start()
	}
	return (
		<button onClick={handleStart} className="px-3 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700">
			🎙️ Speak
		</button>
	)
}