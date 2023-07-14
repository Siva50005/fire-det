import React from "react";
import { useState } from "react";
import "./FileForm.css";
import Button from '@mui/material/Button';

const FileForm = ({callback}) => {
    
    const [file, setFile] = useState(null);

    const handleFileInputChange = (e) => {
        const fileTemp = e.target.files[0];
        setFile(fileTemp);
        console.log(fileTemp);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        console.log(formData.get('file'));
        document.querySelector('#img_render').src = URL.createObjectURL(file);
        
        try{
            const endpoint = 'http://localhost:8000/predict';
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            })

            if(response.ok){
                const jsonResponse = await response.json();
                callback(jsonResponse);
            }
            else{
                console.log('Request failed!');
            }

        } catch(error){
            console.log(error);
        }
    };
  
    return (
    <div className="container">
      <div className="card">
        <h1>Fire Detection</h1>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px" }}>
            <input type="file" onChange={handleFileInputChange}/>
          </div>
          {/* <button type="submit">Upload</button> */}
          <Button variant="contained" color="success" type="submit"> Upload </Button>
        </form>
        <img id="img_render" ></img>
        <button onClick={()=>{window.location.reload();}}>Refresh 🔃</button>
      </div>
    </div>
  );
};

export default FileForm;
