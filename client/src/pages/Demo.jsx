import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
function Demo() {
  const [file, setFile] = useState(false);
  const [output, setOutput] = useState("");
  const [show, setShow] = useState(false);
  const [loader, setLoader] = useState(false);
  const [anomaly, setAnamoly] = useState(false);
  const [url,setUrl] = useState(null);
  const [img_64, setImage] = useState(false);
  const [label, setLabel] = useState("");

  useEffect(()=>{
    if(!localStorage.getItem("token")){
      window.location.assign("/signin")
    }
  },[])
  return (
    <div>
      <nav className="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600">
        <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <a href="http://localhost:5173" className="flex items-center space-x-3 rtl:space-x-reverse">
            <img src="https://flowbite.com/docs/images/logo.svg" className="h-8" alt="Flowbite Logo" />
            <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">PDS</span>
          </a>
          <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
            <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" onClick={()=>{
              localStorage.clear();
              window.location.assign("/signin");
            }}>Log Out</button>
            <button data-collapse-toggle="navbar-sticky" type="button" className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-sticky" aria-expanded="false">
              <span className="sr-only">Open main menu</span>
              <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 1h15M1 7h15M1 13h15" />
              </svg>
            </button>
          </div>
          <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
            <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <li>
                <NavLink to="/home" className={({ isActive }) =>
                    isActive
                    ? 'block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500'
                    : 'block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700'
                }
                aria-current="page">Home</NavLink>
            </li>
            <li>
                <NavLink to="/about" className={({ isActive }) =>
                    isActive
                    ? 'block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500'
                    : 'block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700'
                }>
                About</NavLink>
            </li>
            <li>
                <NavLink to="/demo" className={({ isActive }) =>
                    isActive
                    ? 'block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500'
                    : 'block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700'
                }>
                Demo</NavLink>
            </li>   
          {/*<li>
            <a href="#" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Contact</a>
          </li> */}
            </ul>
          </div>
        </div>
      </nav>


      <form action="" onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', document.getElementById("dropzone-file").files[0]);

        try {
          setLoader(true);
          console.log(localStorage.getItem("token"))
          fetch('http://localhost:8000/model', {
            method: 'POST',
            body: formData,
            headers: {
              "token":localStorage.getItem("token")
            }
          })
            .then(resp => resp.json())
            .then(data => {
              if (!data.success) {
                if(data.msg)
                 alert(data.msg+" Please login to continue")

              }
              else {
                setTimeout(() => {
                  setLoader(false),
                  setShow(false);
                //   setTimeout(() => {
                    
                //     console.log("hi")
                //   }, 10000)
                  // setAnamoly(data.anomaly)
                  console.log(data.label)
                //   console.log(data.reconstruction_error)
                //   setOutput(data.reconstruction_error);
                    setImage(data.image);
                    setLabel(data.label);
                    setShow(true);
                }, 3000)
              }
            })
        } catch (e) {
          console.log(e);
        }
      }}>
        <div className="flex flex-col items-center justify-center w-full mt-20 p-10">

          <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
            {!(file)?<div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
              </svg>
              <p className="mb-2 text-sm text-gray-500 dark:text-gray-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">ZIP</p>
            </div>:
            <div><b>Selected File : </b>{file}</div>}
            <input id="dropzone-file" name='dataset' type="file" className="hidden" required onChange={function me(e) {

              console.log(e.target.files[0].mozFullPath);
              setFile(e.target.files[0].name);

              // const selectedImage = document.getElementById('selectedImage');

              // if (e.target.files && e.target.files[0]) {
              //   const reader = new FileReader();
              //   reader.onload = function(e) {
              //       selectedImage.src = e.target.result
              //       selectedImage.style.display = 'block';
              //       // console.log(e.target.result)
              //   }
              //   reader.readAsDataURL(e.target.files[0]);
              // }
            }} />
          </label>
          <div></div>
          <div className='mt-10'>
            <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
              {loader ?
                (<div role="status">
                  <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor" />
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill" />
                  </svg>
                  <span class="sr-only">Loading...</span>
                </div>)
                : "Submit"}

            </button>
          </div>
        </div>
      </form>
      <div>
        <div className={"bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md " + `${show ? "visible" : "invisible"}`} role="alert">
          <div className="flex">
          </div>
          <div className=''>
          {img_64 && <img src={`data:image/png;base64,${img_64}`} alt="Image" />}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Demo