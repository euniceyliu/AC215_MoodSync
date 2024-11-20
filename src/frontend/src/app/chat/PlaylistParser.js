import React, { useState, useEffect } from 'react';
import { Music, Play, Share2, Heart } from 'lucide-react';

const parsePlaylist = (text) => {
  const songs = [];
  const titleMatch = text.match(/Playlist (?:Title|Name):\s*([^\n]+)/i);
  const playlistTitle = titleMatch ? titleMatch[1].trim() : "Your Mood Playlist";

  const songPatterns = [
    /(?:\d+)\.\s*song:\s*([^,]+),\s*description:\s*(.+)/g,
    /(?:\d+)\.\s*([^-\n]+)\s*-\s*(.+)/g,
  ];

  let matches = [];
  for (const pattern of songPatterns) {
    matches = [...text.matchAll(pattern)];
    if (matches.length > 0) break;
  }

  for (const match of matches) {
    songs.push({
      title: match[1] || match[2].trim(),
      description: match[2] || match[3].trim()
    });
  }

  return { 
    title: playlistTitle, 
    songs: songs.length > 0 ? songs : null 
  };
};

const PlaylistParser = ({ llmResponse }) => {
  const [playlist, setPlaylist] = useState(null);
  const [hoveredSong, setHoveredSong] = useState(null);

  useEffect(() => {
    if (llmResponse) {
      const parsedPlaylist = parsePlaylist(llmResponse);
      setPlaylist(parsedPlaylist);
    }
  }, [llmResponse]);

  if (!llmResponse || !playlist?.songs) {
    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-white p-8 rounded-3xl">
        <div className="text-center space-y-8">
          <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
            <Music className="w-10 h-10 text-blue-600" />
          </div>
          <div className="space-y-4">
            <h2 className="text-3xl font-bold text-blue-900">Discover YOUR Playlist</h2>
            <p className="text-blue-600 max-w-sm mx-auto leading-relaxed">
              Share how you're feeling, and we'll create a personalized playlist that matches your mood and emotion perfectly
            </p>
          </div>
          <div className="flex justify-center space-x-6">
            <div className="flex items-center text-blue-600">
              <Music className="w-5 h-5 mr-2" />
              <span className="text-sm font-medium">Curated tracks</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col p-6 bg-gradient-to-br from-blue-50 to-white rounded-3xl">
      <div className="mb-8 text-center space-y-4">
        <h2 className="text-3xl font-bold text-blue-900">{playlist.title}</h2>
        <p className="text-blue-600 font-medium">Perfectly matched to your current mood</p>
      </div>
      
      <div className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {playlist.songs.map((song, index) => (
          <div
            key={index}
            className="group relative bg-white rounded-2xl p-6 hover:shadow-lg transition-all duration-300 border border-blue-100 hover:border-blue-200"
            onMouseEnter={() => setHoveredSong(index)}
            onMouseLeave={() => setHoveredSong(null)}
          >
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
                {hoveredSong === index ? (
                  <Play className="w-6 h-6 text-blue-600" />
                ) : (
                  <Music className="w-6 h-6 text-blue-600" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-blue-900 font-semibold text-lg leading-tight mb-2">
                  {song.title}
                </h3>
                <p className="text-blue-500 text-sm leading-relaxed">
                  {song.description}
                </p>
              </div>
              <button className="opacity-0 group-hover:opacity-100 transition-opacity">
                <Heart className="w-5 h-5 text-blue-400 hover:text-blue-600 transition-colors" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PlaylistParser;