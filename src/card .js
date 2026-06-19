import { useContext, useEffect } from "react"
import {api} from "./App"



export default function Card(){
  
  // useEffect(()=>{

    let apidata=useContext(api);
    console.log(api)

  // })
  

  return(<div className="container card">
    <div className="row s8 pt-4 " >
<div class="col s3 m6  ">
  <div class="card #ffcdd2 red lighten-4 death">
    <div class="card-content black-text">
      <span class="card-title">Deathes</span>
      {/* <h2>{apidata[0]}</h2> */}
    </div>
    </div>
</div>
<div class="col s3 m6 ">
  <div class="card #e3f2fd blue lighten-5 confirmrd">
    <div class="card-content black-text">
      <span class="card-title">Confirmed</span>
      {/* <h2>{apidata[1]}</h2> */}
      
    </div>
    
  </div>
</div>
<div class="col s3 m6 ">
  <div class="card #c8e6c9 green lighten-4 active">
    <div class="card-content black-text">
      <span class="card-title">Active</span>
      {/* <h2>{apidata[2]}</h2> */}
      
    </div>
    
  </div>
</div>
</div>
</div>    )
    }