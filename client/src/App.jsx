import './App.css'
import {BrowserRouter, Route, Routes, useNavigate} from "react-router-dom"
import Home from './pages/Home'
import SignIn from './pages/SignIn'
import SignUp from './pages/SignUp'
import Landing from './pages/Landing'
import About from './pages/About'

function App() {
  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing/>}></Route>
          <Route path="/signin" element={<SignIn/>}></Route>
          <Route path="/signup" element={<SignUp/>}></Route>
          <Route path='/home' element={<Home />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App
