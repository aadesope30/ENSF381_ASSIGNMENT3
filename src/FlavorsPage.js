import React from "react";
import Header from "./components/Header";
import FlavorItem from "./components/FlavorItem";
import OrderList from "./components/OrderList";
import FlavorCatalog from "./components/FlavorCatalog";
import Footer from "./components/Footer";
import { useState } from 'react';

function FlavorsPage() {

   const [orderList, setOrderList] = useState({});

   return (
      <div className="flavors-page">
         <Header />
         <div className="content">
            <h3> Ice Cream Flavors</h3>
            <FlavorCatalog orderList={orderList} setOrderList={setOrderList}/>
            <h3> Your Order</h3>
            <OrderList orderList={orderList} setOrderList={setOrderList}/>
         </div>
         <Footer />
      </div>
   );
}

export default FlavorsPage;
