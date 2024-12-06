'use client'

import { useState } from 'react';
import { Music, Heart, Sparkles, Send, Play, Clock, Share2 } from 'lucide-react';
import DataService from "../../services/DataService";
import PlaylistParser from './PlaylistParser';

export default function PlaylistPage() {
    const [userInput, setUserInput] = useState("");
    const [isGenerating, setIsGenerating] = useState(false);
    const [llmResponse, setLlmResponse] = useState("");
    const [chatHistory, setChatHistory] = useState([]);

    const extractConversationalResponse = (response) => {
        // Look for common playlist markers
        const markers = [
            "**Playlist:**",
            "1. song:",
            "Playlist Title:",
            "Here's a playlist",
            "I've put together"
        ];
        
        for (const marker of markers) {
            const index = response.indexOf(marker);
            if (index !== -1) {
                // Get only the introductory text before the playlist
                const conversationalPart = response.substring(0, index).trim();
                return conversationalPart || "Here's what I've created for you:";
            }
        }
        return response;
    };

    const MessageBubble = ({ message, type }) => (
        <div className={`flex ${type === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
            <div
                className={`${
                    type === 'user'
                        ? 'bg-blue-600 text-white rounded-2xl rounded-tr-sm'
                        : 'bg-blue-50 text-blue-800 rounded-2xl rounded-tl-sm'
                } px-6 py-4 max-w-[80%]`}
            >
                <p className="font-medium">{message}</p>
            </div>
        </div>
    );

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (userInput.trim() !== "") {
            const newUserMessage = userInput.trim();
            
            // Add user message immediately
            setChatHistory(prev => [
                ...prev,
                { type: 'user', content: newUserMessage }
            ]);
            
            setUserInput("");
            setIsGenerating(true);
            
            try {
                const response = await DataService.chatWithLLM(newUserMessage);
                const conversationalPart = extractConversationalResponse(response.response);
                
                // Add assistant message
                setChatHistory(prev => [
                    ...prev,
                    { type: 'assistant', content: conversationalPart }
                ]);
                
                setLlmResponse(response.response);
                setIsGenerating(false);
            } catch (error) {
                console.error("Error chatting with LLM:", error);
                setChatHistory(prev => [
                    ...prev,
                    { type: 'assistant', content: "I apologize, but I encountered an error. Could you try again?" }
                ]);
                setIsGenerating(false);
            }
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 p-6">
            <div className="max-w-5xl mx-auto rounded-3xl bg-white shadow-xl overflow-hidden border border-blue-100">
                <div className="h-[80vh] flex">
                    {/* Left Sidebar - Chat Interface */}
                    <div className="w-1/2 border-r border-blue-100 flex flex-col">
                        <div className="flex-1 overflow-y-auto p-6">
                            {chatHistory.length === 0 ? (
                                <div className="flex items-center justify-center h-full">
                                    <div className="text-center space-y-4">
                                        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                                            <Heart className="w-8 h-8 text-blue-600" />
                                        </div>
                                        <h2 className="text-3xl font-bold text-blue-900">Share Your Mood</h2>
                                        <p className="text-blue-600 max-w-sm mx-auto leading-relaxed">
                                            Tell me how you're feeling and I'll create the perfect playlist for you
                                        </p>
                                    </div>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {chatHistory.map((message, index) => (
                                        <MessageBubble
                                            key={index}
                                            message={message.content}
                                            type={message.type}
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                        <div className="p-4 border-t border-blue-100">
                            <div className="flex space-x-3">
                                <input
                                    type="text"
                                    value={userInput}
                                    onChange={(e) => setUserInput(e.target.value)}
                                    placeholder="How are you feeling today?"
                                    className="flex-1 px-4 py-3 rounded-xl bg-blue-50 text-blue-900 placeholder-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-200"
                                />
                                <button
                                    onClick={handleSubmit}
                                    disabled={isGenerating}
                                    className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all duration-200 flex items-center space-x-2 disabled:opacity-50"
                                >
                                    {isGenerating ? (
                                        <span>Creating...</span>
                                    ) : (
                                        <>
                                            <span>Generate</span>
                                            <Sparkles className="w-4 h-4" />
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Right Side - Playlist Display */}
                    <div className="w-1/2 bg-gradient-to-br from-blue-50 to-white p-6">
                        <PlaylistParser llmResponse={llmResponse} />
                    </div>
                </div>
            </div>
        </div>
    );
}