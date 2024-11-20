'use client'

import React, { useState } from 'react';
import { Music, Heart, Brain, Sparkles, Users, Lock, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export default function AboutPage() {
    const [hoveredFeature, setHoveredFeature] = useState(null);
    const [hoveredMember, setHoveredMember] = useState(null);

    const features = [
        {
            icon: <Brain className="w-8 h-8" />,
            title: "Emotional Intelligence",
            description: "Our advanced AI understands the complex relationship between music and emotions, creating perfectly tailored playlists for every mood."
        },
        {
            icon: <Music className="w-8 h-8" />,
            title: "Musical Expertise",
            description: "Drawing from a vast library of songs across genres, we craft diverse playlists that resonate with your emotional state."
        },
        {
            icon: <Heart className="w-8 h-8" />,
            title: "Personal Touch",
            description: "Every playlist is uniquely crafted to match your specific mood, preferences, and musical journey."
        },
        {
            icon: <Lock className="w-8 h-8" />,
            title: "Privacy First",
            description: "Your emotional expressions and music preferences are kept secure and confidential at all times."
        }
    ];

    const team = [
        {
            name: "Eunice Liu",
            role: "Co-Founder",
            description: "G2 MS in Data Science & flutist for 6 years & classical music enthusiast",
            image: "/assets/mem1.png"
        },
        {
            name: "Megan Luu",
            role: "Co-Founder",
            description: "G2 MS in Data Science & violinist/pianist for 8 years",
            image: "/assets/mem2.png"
        },
        {
            name: "Xinyu Chen",
            role: "Co-Founder",
            description: "G2 MS in biomedical informatics & pianist & jack of all trades in music from singing to composing",
            image: "/assets/mem3.png"
        }
    ];

    return (
        <div className="h-screen overflow-y-scroll snap-y snap-mandatory">
            {/* Hero Section */}
            <section className="h-screen flex items-center justify-center relative bg-gradient-to-b from-blue-100 to-white snap-start">
                <div className="max-w-6xl mx-auto px-8 text-center">
                    <div className="relative space-y-6">
                        <h1 className="text-6xl font-bold text-blue-950 tracking-tight">
                            About{" "}
                            <span className="inline-block animate-bounce text-blue-600">
                                MoodSync
                            </span>
                        </h1>
                        <p className="text-xl text-blue-700 max-w-2xl mx-auto leading-relaxed">
                            We blend artificial intelligence with musical artistry to create personalized playlists that match your emotional journey.
                        </p>
                    </div>
                </div>
            </section>

            {/* Mission Section */}
            <section className="h-screen flex items-center justify-center bg-gradient-to-b from-white to-blue-50 snap-start">
                <div className="max-w-6xl mx-auto px-8">
                    <div className="bg-white/80 backdrop-blur-lg rounded-3xl shadow-xl p-12">
                        <div className="max-w-4xl mx-auto text-center space-y-6">
                            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-8 transform hover:rotate-180 transition-transform duration-500">
                                <Sparkles className="w-10 h-10 text-blue-700" />
                            </div>
                            <h2 className="text-4xl font-bold text-blue-950">Our Mission</h2>
                            <p className="text-xl text-blue-800 leading-relaxed">
                                At MoodSync, we believe that music has the power to transform emotions, enhance experiences, and connect people with their feelings in profound ways. Our mission is to harness artificial intelligence to create deeply personal musical experiences that resonate with your emotional state.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 to-white snap-start">
                <div className="max-w-6xl mx-auto px-8">
                    <div className="text-center mb-12">
                        <h2 className="text-4xl font-bold text-blue-950 mb-4">What Makes Us Unique</h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {features.map((feature, index) => (
                            <div 
                                key={index} 
                                className="group bg-white/90 rounded-3xl shadow-lg p-8 backdrop-blur-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-1"
                                onMouseEnter={() => setHoveredFeature(index)}
                                onMouseLeave={() => setHoveredFeature(null)}
                            >
                                <div className={`w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mb-6 transform transition-transform duration-500 ${hoveredFeature === index ? 'scale-110 rotate-12' : ''}`}>
                                    <div className="text-blue-700">
                                        {feature.icon}
                                    </div>
                                </div>
                                <h3 className="text-2xl font-bold text-blue-950 mb-4">{feature.title}</h3>
                                <p className="text-blue-700 leading-relaxed">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Team Section */}
            <section className="h-screen flex items-center justify-center bg-gradient-to-b from-white to-blue-100 snap-start">
                <div className="max-w-6xl mx-auto px-8">
                    <div className="bg-white/90 rounded-3xl shadow-xl backdrop-blur-lg p-12">
                        <div className="text-center mb-12">
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <Users className="w-8 h-8 text-blue-700" />
                            </div>
                            <h2 className="text-4xl font-bold text-blue-950">Our Team</h2>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {team.map((member, index) => (
                                <div 
                                    key={index} 
                                    className="group text-center space-y-4 p-6 rounded-2xl transition-all duration-300 hover:bg-blue-50"
                                    onMouseEnter={() => setHoveredMember(index)}
                                    onMouseLeave={() => setHoveredMember(null)}
                                >
                                    <div className="relative w-32 h-32 mx-auto mb-4">
                                        <div className={`absolute inset-0 bg-blue-200 rounded-full transform transition-transform duration-500 ${hoveredMember === index ? 'scale-110' : ''}`} />
                                        <Image
                                            src={member.image}
                                            alt={member.name}
                                            width={128}
                                            height={128}
                                            className="relative rounded-full w-full h-full object-cover"
                                        />
                                    </div>
                                    <h3 className="text-2xl font-bold text-blue-950">{member.name}</h3>
                                    <p className="text-blue-800 font-medium">{member.role}</p>
                                    <p className="text-blue-700">{member.description}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="h-screen flex items-center justify-center bg-gradient-to-b from-blue-100 to-blue-50 snap-start">
                <div className="max-w-6xl mx-auto px-8 text-center space-y-8">
                    <h2 className="text-4xl font-bold text-blue-950">Ready to Start Your Musical Journey?</h2>
                    <p className="text-xl text-blue-800">Experience the perfect harmony between your emotions and music.</p>
                    <div className="flex justify-center">
                        <Link 
                            href="/chat" 
                            className="inline-flex items-center group px-12 py-4 bg-blue-700 text-white rounded-2xl hover:bg-blue-800 hover:shadow-xl transition-all duration-300 text-lg"
                        >
                            <span>Get Started Now</span>
                            <ArrowRight className="ml-2 transform group-hover:translate-x-1 transition-transform" />
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
}