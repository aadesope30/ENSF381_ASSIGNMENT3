import React from "react";
import OrderItem from "./OrderItem";

function OrderList({ orderList = {}, setOrderList }) {
  const keys = Object.keys(orderList);

  return (
    <div className="order-list">
      {keys.length > 0 ? (
        keys.map(key => (
          <OrderItem
            key={key}
            order={key}
            orderList={orderList}
            setOrderList={setOrderList}
          />
        ))
      ) : (
        <p>No items in your order.</p>
      )}
    </div>
  );
}

export default OrderList;
