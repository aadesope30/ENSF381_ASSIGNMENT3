import React from "react";
import { useState } from 'react';

function FlavorItem({img, name, price, desc, orderList, setOrderList}) {
   const [showDesc, setShowDesc] = useState(false);

   return (
      <div className ="flavor-card" onMouseEnter={() => setShowDesc(true)} onMouseLeave={()=> setShowDesc(false)}>
      <img src={"/" + img} alt={name}/>
      <p id="flavorName"> {name} </p>
      <p id="flavorPrice"> {price} </p>
      {showDesc && <p id="flavorDesc">{desc}</p>}
      <button id="addToOrderButton" type="button" onClick={ ()=> {
         setOrderList(prev => ({
            ...prev, [name]: prev[name] ? prev[name] + 1: 1
         }));
      }}> Add to Order</button>
      </div>
   )
}

export default FlavorItem;
