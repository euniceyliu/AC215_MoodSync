import React, { useState, useEffect } from 'react';
import { Music, Play, Repeat2, Share2 } from 'lucide-react';

const parsePlaylist = (text) => {
  // More robust parsing strategy
  const songs = [];
  
  // Try to extract playlist title (optional)
  const titleMatch = text.match(/Playlist (?:Title|Name):\s*([^\n]+)/i);
  const playlistTitle = titleMatch ? titleMatch[1].trim() : "Personalized Playlist";

  // Enhanced parsing to handle multiple formats
  const songPatterns = [
    /(\d+)\.\s*song:\s*([^,]+),\s*description:\s*(.+)/g,  // Primary pattern
    /(\d+)\.\s*([^-\n]+)\s*-\s*(.+)/g,  // Alternate pattern
  ];

  let matches = [];
  for (const pattern of songPatterns) {
    matches = [...text.matchAll(pattern)];
    if (matches.length > 0) break;
  }

  // Process matches
  for (const match of matches) {
    songs.push({
      index: match[1],
      title: match[2].trim(),
      description: match[3].trim()
    });
  }

  // Fallback if no matches found
  if (songs.length === 0) {
    return { 
      title: "Mood Playlist", 
      songs: null 
    };
  }

  return { 
    title: playlistTitle, 
    songs: songs
  };
};

const PlaylistParser = ({ llmResponse }) => {
  const [playlist, setPlaylist] = useState(null);
  const [showRawResponse, setShowRawResponse] = useState(false);

  useEffect(() => {
    if (llmResponse) {
      const parsedPlaylist = parsePlaylist(llmResponse);
      setPlaylist(parsedPlaylist);
      console.log("Parsed Playlist:", parsedPlaylist);
    }
  }, [llmResponse]);

  // No response state
  if (!llmResponse) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center text-blue-400">
          <Music className="w-12 h-12 mx-auto mb-4" />
          <p>Create your personalized playlist</p>
        </div>
      </div>
    );
  }

  // Parsing failed or user wants to see raw response
  if (!playlist || !playlist.songs || showRawResponse) {
    return (
      <div className="h-full flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-blue-900 font-medium">Raw Response</h3>
          <button 
            onClick={() => setShowRawResponse(!showRawResponse)}
            className="text-blue-600 hover:text-blue-800 transition-colors"
          >
            {showRawResponse ? "Show Playlist" : "View Raw"}
          </button>
        </div>
        <div className="flex-1 overflow-y-auto bg-blue-50 rounded-xl p-4">
          <p className="text-blue-600 text-sm whitespace-pre-wrap">{llmResponse}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-blue-900 mb-2">{playlist.title}</h2>
        <p className="text-blue-600">Curated just for your mood</p>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto">
        {playlist.songs.map((song, index) => (
          <div
            key={index}
            className="group flex items-center space-x-4 p-4 rounded-xl hover:bg-white hover:shadow-md transition-all duration-200"
          >
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors duration-200">
              <Play className="w-5 h-5 text-blue-600 group-hover:text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-blue-900 font-medium">{song.index}. {song.title}</h3>
              <p className="text-blue-400 text-xs mt-1">{song.description}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 pt-6 border-t border-blue-100 flex space-x-3">
        <button className="flex-1 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center space-x-2">
          <Music className="w-5 h-5" />
          <span>Play All</span>
        </button>
        <button 
          onClick={() => setShowRawResponse(true)}
          className="py-3 px-4 bg-blue-50 text-blue-600 rounded-xl hover:bg-blue-100 transition-colors duration-200 flex items-center justify-center"
        >
          <Share2 className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default PlaylistParser;