'use client'

import React, { useState } from 'react';
import { Mail, Phone, Plus, Minus, ExternalLink, BookOpen, HelpCircle, MessageSquare } from 'lucide-react';
import Link from 'next/link';

export default function HelpPage() {
    const [openFaqIndex, setOpenFaqIndex] = useState(null);

    const faqs = [
        {
            question: "How does MoodSync generate playlists?",
            answer: "MoodSync uses advanced AI to analyze your current emotional state and musical preferences. It then creates personalized playlists that match your mood by considering factors like tempo, genre, lyrics, and musical elements that are known to influence emotions."
        },
        {
            question: "Can I customize the generated playlists?",
            answer: "Yes! If you're not satisfied with a generated playlist, you can always generate a new one that better matches your current mood and preferences. Each new generation takes into account different musical elements to provide fresh recommendations."
        },
        {
            question: "How often can I generate new playlists?",
            answer: "You can generate new playlists as often as you like! Your emotional state can change throughout the day, and MoodSync is designed to adapt to these changes, providing fresh music recommendations whenever you need them."
        },
        {
            question: "What music services does MoodSync work with?",
            answer: "We are currently working to integrate with major music streaming platforms. Stay tuned for updates as we expand our service compatibility!"
        },
        {
            question: "Is my emotional data kept private?",
            answer: "Absolutely! We take your privacy seriously. All your emotional data and music preferences are encrypted and stored securely. We never share your personal information with third parties without your explicit consent."
        }
    ];

    const supportResources = [
        {
            icon: <BookOpen className="w-6 h-6" />,
            title: "User Guide",
            description: "Step-by-step guides and tutorials to help you get the most out of MoodSync",
            link: "/guide"
        },
        {
            icon: <MessageSquare className="w-6 h-6" />,
            title: "Community Forum",
            description: "Connect with other users, share experiences, and get tips",
            link: "/community"
        },
        {
            icon: <HelpCircle className="w-6 h-6" />,
            title: "Video Tutorials",
            description: "Watch detailed explanations of all MoodSync features",
            link: "/tutorials"
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white pt-24 pb-16">
            {/* Hero Section */}
            <div className="max-w-6xl mx-auto px-8 mb-16">
                <div className="text-center space-y-6">
                    <h1 className="text-5xl font-bold text-blue-950">How Can We Help?</h1>
                    <p className="text-xl text-blue-700 max-w-2xl mx-auto">
                        We're here to help you make the most of your MoodSync experience. Find answers to common questions or reach out to our support team.
                    </p>
                </div>
            </div>

            {/* FAQ Section */}
            <div className="max-w-4xl mx-auto px-8 mb-16">
                <h2 className="text-3xl font-bold text-blue-950 mb-8 text-center">Frequently Asked Questions</h2>
                <div className="space-y-4">
                    {faqs.map((faq, index) => (
                        <div 
                            key={index} 
                            className="bg-white rounded-lg border border-blue-100 hover:shadow-md transition-shadow duration-300"
                        >
                            <button
                                className="w-full text-left px-6 py-4 flex items-center justify-between"
                                onClick={() => setOpenFaqIndex(openFaqIndex === index ? null : index)}
                            >
                                <h3 className="text-lg font-semibold text-blue-900">{faq.question}</h3>
                                {openFaqIndex === index ? 
                                    <Minus className="w-5 h-5 text-blue-600" /> : 
                                    <Plus className="w-5 h-5 text-blue-600" />
                                }
                            </button>
                            {openFaqIndex === index && (
                                <div className="px-6 pb-4 text-blue-700">
                                    {faq.answer}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Support Resources */}
            <div className="max-w-6xl mx-auto px-8 mb-16">
                <h2 className="text-3xl font-bold text-blue-950 mb-8 text-center">Support Resources</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {supportResources.map((resource, index) => (
                        <div 
                            key={index}
                            className="bg-white rounded-lg p-6 group hover:shadow-xl transition-shadow duration-300 border border-blue-100"
                        >
                            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-200 transition-colors duration-300">
                                <div className="text-blue-700">
                                    {resource.icon}
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-blue-950 mb-2">{resource.title}</h3>
                            <p className="text-blue-700 mb-4">{resource.description}</p>
                            <Link 
                                href={resource.link}
                                className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
                            >
                                Learn More
                                <ExternalLink className="ml-2 w-4 h-4" />
                            </Link>
                        </div>
                    ))}
                </div>
            </div>

            {/* Contact Section */}
            <div className="max-w-4xl mx-auto px-8">
                <div className="bg-white rounded-lg border border-blue-100 p-8">
                    <h2 className="text-3xl font-bold text-blue-950 mb-8 text-center">Still Need Help?</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-center">
                        <div className="space-y-4">
                            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                                <Mail className="w-6 h-6 text-blue-700" />
                            </div>
                            <h3 className="font-semibold text-blue-950">Email Support</h3>
                            <p className="text-blue-700">Get help within 24 hours</p>
                            <a href="mailto:support@moodsync.com" className="text-blue-600 hover:text-blue-800 font-medium">support@moodsync.com</a>
                        </div>
                        <div className="space-y-4">
                            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                                <Phone className="w-6 h-6 text-blue-700" />
                            </div>
                            <h3 className="font-semibold text-blue-950">Phone Support</h3>
                            <p className="text-blue-700">Mon-Fri, 9am-5pm EST</p>
                            <a href="tel:1-800-MOODSYNC" className="text-blue-600 hover:text-blue-800 font-medium">1-800-MOODSYNC</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}