import React from 'react'
import { Link } from 'react-router-dom'
function About() {
  return (
    <div>
      <nav className="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600">
        <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <a href="https://flowbite.com/" className="flex items-center space-x-3 rtl:space-x-reverse">
            <img src="https://flowbite.com/docs/images/logo.svg" className="h-8" alt="Flowbite Logo"/>
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
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
              </svg>
          </button>
        </div>
        <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
          <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <li>
              <Link to="/home" className="block py-2 px-3  bg-blue-700 rounded md:bg-transparent  md:p-0 md:dark:text-blue-500" aria-current="page">Home</Link>
            </li>
            <li>
              <Link to="/about" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:text-blue-700 md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">About</Link>
            </li>
            {/* <li>
              <a href="#" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Services</a>
            </li>
            <li>
              <a href="#" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Contact</a>
            </li> */}
          </ul>
        </div>
        </div>
      </nav>
            
      <img src="about.jpeg" id="selectedImage" className='ml-32 size-7/12 pl-96 pt-24'/>
      <div>
          <p class="pt-8 p-28 text-base leading-relaxed dark:text-gray-400">
          Adverserial Pertubations pose a major threat for machine learning systems, majorly affecting their reliability especially in critical applications
          like healthcare, autonomous driving, finance, etc. This project proposes
          a novel approach for adverserial pertubation detection uses autoencoders'
          anomaly detection combined with transfer learning. This method lever-
          ages pretrained model to extract robust feature representations, which are
          then used to train an autoencoder. The autoencoder learns to reconstruct
          clean inputs accurately while producing higher reconstruction errors for
          adversarially perturbed inputs. By measuring these reconstruction errors
          the systems can effectively adverserial attacks in real time. The use of
          transfer learning accelerates training and enhances the models ability to
          generalize across diverse datasets reducing the need for extensive labeled
          data.<br></br><br></br>
          Adversarial attacks typically involve the deliberate manipulation of input
          data to deceive a machine learning model. These attacks can be catego-
          rized into two types: white-box and black-box attacks. In a white-box
          attack, the adversary has complete knowledge of the model’s parameters,
          architecture, and training data, allowing them to craft specific perturba-
          tions. In contrast, black-box attacks assume that the adversary has no
          prior knowledge of the model and must rely on observing its behavior
          through queries to generate adversarial examples.
          Several attack methods have been proposed, such as the Fast Gradient
          Sign Method (FGSM), Projected Gradient Descent (PGD), and Carlini
          & Wagner (C&W) attacks, which can successfully deceive state-of-the-art
          ML models.<br></br><br></br>
          Autoencoders, a class of unsupervised neural networks, have shown promise
          in detecting anomalies in data, including adversarial perturbations. Au-
          toencoders are designed to learn an efficient representation of input data
          by compressing it into a lower-dimensional latent space and then recon-
          structing it. The key idea behind using autoencoders for perturbation
          detection is that they can reconstruct clean data more effectively than
          perturbed data, leading to higher reconstruction errors for adversarially
          altered inputs.
          By training autoencoders on non-adversarial data, the model learns to cap-
          ture the inherent structure of the data. When adversarial examples are
          introduced, the reconstruction error increases, signaling potential pertur-
          bations. This makes autoencoders a valuable tool for detecting adversarial
          attacks, particularly in real-time systems where identifying attacks quickly
          is critical.
          Transfer learning is a machine learning technique that enables models to
          leverage knowledge learned from one task to improve performance on a
          different but related task. It is particularly useful when there is limited
          labeled data for the target task, allowing models to benefit from pre-trained
          models on large datasets.
          In the context of adversarial perturbation detection, transfer learning can
          be applied to enhance the performance of autoencoders by using pre-
          trained models from similar domains. This reduces the time and resources
          needed to train the model from scratch and helps achieve better general-
          ization in detecting adversarial attacks across various types of inputs.
          </p>
          <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
          
          </p>
      </div>

    </div>
  )
}

export default About