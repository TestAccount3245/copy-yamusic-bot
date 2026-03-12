import { HashRouter as BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Search from './pages/Search'
import Track from './pages/Track'
import Album from './pages/Album'
import Artist from './pages/Artist'
import Wave from './pages/Wave'
import Downloads from './pages/Downloads'
import Upload from './pages/Upload'
import Settings from './pages/Settings'
import NavBar from './components/NavBar'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen pb-20">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/track/:id" element={<Track />} />
          <Route path="/album/:id" element={<Album />} />
          <Route path="/artist/:id" element={<Artist />} />
          <Route path="/wave" element={<Wave />} />
          <Route path="/downloads" element={<Downloads />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
        <NavBar />
      </div>
    </BrowserRouter>
  )
}
