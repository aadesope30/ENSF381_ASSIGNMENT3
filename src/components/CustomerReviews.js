import React from "react";
import { useEffect, useState } from "react";
import reviews from "../data/reviews";

function CustomerReviews() {
  const [selectedReviews, setSelectedReviews] = useState([]);

  useEffect(() => {
    let shuffledReviews = [...reviews];
    shuffledReviews.sort(() => Math.random() - 0.5);
    setSelectedReviews(shuffledReviews.slice(0, 2));
  }, []);

  return (
    <div>
      <h2>Customer Reviews</h2>

      {selectedReviews.map((review, index) => (
        <div key={index}>
          <p>{review.customerName}</p>
          <p>{review.review}</p>
          <p>{"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}</p>
        </div>
      ))}
    </div>
  );
}

export default CustomerReviews;