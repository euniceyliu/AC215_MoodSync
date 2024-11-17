// components/Header.jsx
'use client'

import { useState } from 'react'
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Home, HelpCircle, Menu, X, Music, Info } from 'lucide-react';

const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const pathname = usePathname();

    const navItems = [
        { name: 'Home', path: '/', icon: <Home className="w-5 h-5" /> },
        { name: 'About', path: '/about', icon: <Info className="w-5 h-5" /> },
        { name: 'Playlist', path: '/chat', icon: <Music className="w-5 h-5" /> },
        { name: 'Help', path: '/help', icon: <HelpCircle className="w-5 h-5" /> }
    ];

    return (
        <>
            <header className="bg-white/80 backdrop-blur-md fixed w-full top-0 z-50 border-b border-blue-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <Link href="/" className="flex items-center space-x-3">
                            <Image
                                src="/assets/logo.png"
                                alt="MoodSync Logo"
                                width={50}
                                height={50}
                                className="object-contain"
                                quality={100}
                                priority
                            />
                            <h1 className="text-[22px] font-['Playfair_Display'] font-bold text-blue-950">
                                MoodSync
                            </h1>
                        </Link>

                        <nav className="hidden md:flex items-center space-x-8">
                            {navItems.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.path}
                                    className={`flex items-center space-x-2 text-base font-medium transition-colors duration-200
                                        ${pathname === item.path 
                                            ? 'text-blue-600' 
                                            : 'text-blue-950 hover:text-blue-600'}`}
                                >
                                    {item.icon}
                                    <span>{item.name}</span>
                                </Link>
                            ))}
                        </nav>

                        <button
                            className="md:hidden p-2 text-blue-950 hover:text-blue-600 transition-colors"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            aria-label="Toggle menu"
                        >
                            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                        </button>
                    </div>
                </div>

                {/* Mobile menu */}
                <div className={`md:hidden absolute w-full bg-white/95 backdrop-blur-md transition-transform duration-300 ease-in-out ${
                    isMenuOpen ? 'translate-y-0' : '-translate-y-full'
                }`}>
                    <div className="px-4 py-2 space-y-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.name}
                                href={item.path}
                                className={`flex items-center space-x-2 p-3 rounded-lg transition-colors duration-200 text-base
                                    ${pathname === item.path
                                        ? 'text-blue-600 bg-blue-50'
                                        : 'text-blue-950 hover:bg-blue-50 hover:text-blue-600'}`}
                                onClick={() => setIsMenuOpen(false)}
                            >
                                {item.icon}
                                <span>{item.name}</span>
                            </Link>
                        ))}
                    </div>
                </div>
            </header>
            {isMenuOpen && (
                <div 
                    className="md:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
                    onClick={() => setIsMenuOpen(false)}
                />
            )}
        </>
    );
}

export default Header;