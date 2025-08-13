import React from 'react'
import ChatBox from './components/ChatBox'

export default function App() {
	return (
		<div className="min-h-screen flex flex-col">
			<header className="p-4 border-b border-gray-200 dark:border-gray-700">
				<h1 className="text-xl font-semibold">Logistics Dispatcher</h1>
			</header>
			<main className="flex-1">
				<ChatBox />
			</main>
			<footer className="p-4 text-xs text-gray-500 text-center">Demo system for dispatching, routing, and notifications</footer>
		</div>
	)
}