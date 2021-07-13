import Header from "./header.js";
import Card from "./card.js";
import './App.css';
import Mychart from "./chart"
import { createContext, useState, useEffect } from "react";


export let api = createContext(20);

export default function App() {
  let [mydata, setMydata] = useState();
console.log(mydata);
  
  useEffect(() => {
    
    
    async function Api() {
      let responce = await fetch('https://covid19.mathdro.id/api');
      let coviddata = await responce.json();
      const { confirmed, deaths, recovered } = coviddata;
      let cdv = [confirmed.value, deaths.value, recovered.value]
    
      setMydata(cdv);
    }
    Api();
    
    
  }, [])
  
  return (<div className="App">
    <Header />
    <api.Provider value={mydata}>
      <Card />
      <Mychart/>
    </api.Provider>




  </div>
  );
}


// export { api };