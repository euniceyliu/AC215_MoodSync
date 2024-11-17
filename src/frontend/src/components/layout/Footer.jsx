// components/Footer.jsx
'use client'

import { usePathname } from 'next/navigation';

const Footer = () => {
    const pathname = usePathname();
    if (pathname === '/chat') return null;

    return (
        <footer className="bg-white/80 backdrop-blur-md border-t border-blue-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex justify-center items-center">
                    <p className="text-sm text-blue-600">
                        Copyright © {new Date().getFullYear()} MoodSync - All Rights Reserved.
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;