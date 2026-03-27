import React from "react";
import { useEffect, useState } from "react";
import flavors from "../data/flavors";

function FeaturedFlavors() {
  const [featuredFlavors, setFeaturedFlavors] = useState([]);

  useEffect(() => {
    const randomThree = [...flavors]
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);

    setFeaturedFlavors(randomThree);
  }, []);

  return (
    <div className="flavor-grid">
      {featuredFlavors.map(function (flavor) {
        return (
          <div key={flavor.id}>
            <h3>{flavor.name}</h3>
            <p>{flavor.description}</p>
            <p>Price: {flavor.price}</p>
            <img src={flavor.image} alt={flavor.name} />
          </div>
        );
      })}
    </div>
  );
}

export default FeaturedFlavors;