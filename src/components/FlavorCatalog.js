import React from "react";
import flavors from "../data/flavors.js"
import FlavorItem from "./FlavorItem";

function FlavorCatalog({orderList, setOrderList}) {
    return (
       <div className="flavor-grid">
         {flavors.map(flavor => (
            <FlavorItem key={flavor.id} img={flavor.image} name={flavor.name} price={flavor.price} desc={flavor.description} orderList={orderList} setOrderList={setOrderList}/>
         ))}
       </div>
    );
}

export default FlavorCatalog;
