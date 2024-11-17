'use client';

import Link from 'next/link';
import { Music, Heart, Sparkles } from 'lucide-react';

export default function Home() {
    return (
        <>
            {/* Font imports */}
            <style jsx global>{`
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
            `}</style>

            <div className="min-h-screen bg-gradient-to-b from-blue-100 to-white font-['Inter']">
                {/* Hero Section */}
                <section className="pt-40 pb-20 px-6 md:px-16">
                    <div className="max-w-4xl mx-auto text-center space-y-10">
                        <h1 className="text-4xl md:text-6xl font-['Playfair_Display'] font-bold text-blue-950 mb-8 leading-tight tracking-tight">
                            Your Emotions, Your Music
                        </h1>
                        <p className="text-lg md:text-xl text-blue-700 mb-12 max-w-2xl mx-auto tracking-wide font-light leading-relaxed">
                            Let AI craft the perfect playlist that resonates with your mood and enhances your musical journey
                        </p>
                        <div className="flex flex-wrap justify-center gap-6">
                            <Link 
                                href="/chat" 
                                className="px-8 py-4 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 font-medium text-lg shadow-lg hover:shadow-xl hover:-translate-y-0.5"
                            >
                                Get Started
                            </Link>
                            <Link 
                                href="/about" 
                                className="px-8 py-4 border-2 border-blue-600 text-blue-600 rounded-full hover:bg-blue-50 transition-all duration-300 font-medium text-lg hover:-translate-y-0.5"
                            >
                                Learn More
                            </Link>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-16 px-6 md:px-8">
                    <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            {
                                icon: <Heart className="w-10 h-10" />,
                                title: "Mood Analysis",
                                description: "Share your feelings and let our AI understand your emotional state to create the perfect musical journey."
                            },
                            {
                                icon: <Music className="w-10 h-10" />,
                                title: "Smart Playlists",
                                description: "Discover personalized playlists that match your current mood and musical preferences."
                            },
                            {
                                icon: <Sparkles className="w-10 h-10" />,
                                title: "AI Magic",
                                description: "Experience the power of AI as it curates the perfect soundtrack for your emotional state."
                            }
                        ].map((feature, index) => (
                            <div key={index} className="bg-white p-10 rounded-3xl shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                                <div className="text-blue-600 mb-8">
                                    {feature.icon}
                                </div>
                                <h3 className="text-2xl font-['Playfair_Display'] font-semibold text-blue-950 mb-4">
                                    {feature.title}
                                </h3>
                                <p className="text-blue-700 leading-relaxed font-light text-lg">
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        </>
    );
}