import React from 'react';
import FileForm from './components/FileForm';
import './App.css';

const App = () => {

  let result = [];

  const callthisfromChild = (data) => {
    result = data;
    console.log(result);
    document.querySelector('h2').innerText = result[0];
  }; 
  
  return (
    <div>
      <FileForm callback={callthisfromChild}/>
      <div className='result'>
        <h2>{result}</h2>
      </div>
    </div>
  )
}

export default App;

