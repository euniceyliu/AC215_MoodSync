'use client'

import { useState } from 'react';
import { Music, Heart, Sparkles, Send, Play, Clock, Share2 } from 'lucide-react';
import DataService from "../../services/DataService";

export default function PlaylistPage() {
    const [userInput, setUserInput] = useState(""); // Initialize userInput state
    const [isGenerating, setIsGenerating] = useState(false);
    const [playlist, setPlaylist] = useState(null);
    const [llmResponse, setLlmResponse] = useState(""); // LLM's response

    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload
        console.log("handleSubmit triggered with input:", userInput);
        try {
          const response = await DataService.chatWithLLM(userInput); // Call backend
          setLlmResponse(response.response); // Update state with the response
          setUserInput(""); // Clear the input field
          console.log(llmResponse)
        } catch (error) {
          console.error("Error chatting with LLM:", error);
        }
      };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 p-6">
            <div className="max-w-5xl mx-auto rounded-3xl bg-white shadow-xl overflow-hidden border border-blue-100">
                <div className="h-[80vh] flex">
                    {/* Left Sidebar - Chat Interface */}
                    <div className="w-1/2 border-r border-blue-100 flex flex-col">
                        <div className="flex-1 overflow-y-auto p-6 space-y-6">
                            {playlist ? (
                                <>
                                    <div className="flex justify-end">
                                        <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-6 py-4 max-w-[80%]">
                                            {playlist.mood}
                                        </div>
                                    </div>
                                    <div className="flex justify-start">
                                        <div className="bg-blue-50 rounded-2xl rounded-tl-sm px-6 py-4 max-w-[80%]">
                                            <p className="text-blue-800 font-medium mb-2">
                                                I've crafted a playlist that matches your mood perfectly
                                            </p>
                                            <p className="text-blue-600 text-sm">
                                                Swipe right to see your personalized playlist →
                                            </p>
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <div className="flex items-center justify-center h-full">
                                    <div className="text-center space-y-4">
                                        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                                            <Heart className="w-8 h-8 text-blue-600" />
                                        </div>
                                        <p className="text-blue-800 font-medium">Share Your Mood</p>
                                        <p className="text-blue-600 text-sm max-w-xs">
                                            Tell me how you're feeling and I'll create the perfect playlist for you
                                        </p>
                                    </div>
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
                        <div className="h-full flex flex-col">
                            <div className="mb-6">
                                <h2 className="text-2xl font-semibold text-blue-900 mb-2">Your Mood Playlist</h2>
                                <p className="text-blue-600">Curated just for you</p>
                            </div>
                            <div className="flex-1">
                            <h3 className="text-blue-900 font-medium">LLM Response</h3>
                            <p className="text-blue-600 text-sm">{llmResponse}</p> {/* Displays LLM Response */}
                            </div>

                            {/* {playlist ? ( */}
                                <>    
   
                                    {/* <div className="flex-1 space-y-3">
                                        {playlist.songs.map((song, index) => (
                                            <div
                                                key={index}
                                                className="group flex items-center space-x-4 p-4 rounded-xl hover:bg-white hover:shadow-md transition-all duration-200"
                                            >
                                                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors duration-200">
                                                    <Play className="w-5 h-5 text-blue-600 group-hover:text-white" />
                                                </div>
                                                <div className="flex-1">
                                                    <h3 className="text-blue-900 font-medium">{song.title}</h3>
                                                    <p className="text-blue-600 text-sm">{song.artist}</p>
                                                </div>
                                                <div className="flex items-center space-x-4">
                                                    <span className="text-blue-400 text-sm">{song.duration}</span>
                                                    <Share2 className="w-4 h-4 text-blue-400 hover:text-blue-600 cursor-pointer" />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="mt-6 pt-6 border-t border-blue-100">
                                        <button className="w-full py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center space-x-2">
                                            <Music className="w-5 h-5" />
                                            <span>Play All</span>
                                        </button>
                                    </div> */}

                                </>
                            {/* ) : (
                                <div className="flex-1 flex items-center justify-center">
                                    <div className="text-center text-blue-400">
                                        <Music className="w-12 h-12 mx-auto mb-4" />
                                        <p>Share your mood to generate a playlist</p>
                                    </div>
                                </div>
                            )} */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}