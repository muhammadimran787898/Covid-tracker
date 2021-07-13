import { Bar } from 'react-chartjs-2';

import {api} from "./App"
import { useContext } from "react";



export default function Mychart(){
  

    const data1 = useContext(api);
    // console.log(data1);
  
    const data = {
      labels: ['Deaths','Confirmed', 'Active'],
      datasets: [
        {
          label: 'Detail of COVID-19',
          data: data1,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(134, 240, 13 0.2)',
  
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
  
          ],
          borderWidth: 2,
        },
      ],
    };
  
    const options = {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    };
  
    return (
      <>
        < div className="Chart" >
          <div className=''>
            <h1 className='titl'>COVID-19 Bar Chart</h1>
          </div>
          <Bar data={data} options={options} />
        </div >
      </>
    )
  }
  
