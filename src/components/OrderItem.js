import React from "react";
import flavors from "../data/flavors.js"

function OrderItem({order, orderList, setOrderList}) {
   const flavor = flavors.find(f => f.name === order);
   if (!flavor) return null;

   return (
      <div>
      <p id="flavorName">{order}</p>
      <p id="flavorQuantity">Quantity: {orderList[order]}</p>
      <p id="flavorPrice">Total: ${ (parseFloat(flavor.price.replace('$','')) * orderList[order]).toFixed(2) }</p>
      <button type="button" className="remove" onClick={ ()=> {
         setOrderList(prev => {
            const qty = prev[order] - 1;
            if (qty > 0) return { ...prev, [order]: qty };
            const { [order]: _, ...rest } = prev;
            return rest;
         })
      }}>Remove Item</button>
      </div>
   )
}

export default OrderItem;
