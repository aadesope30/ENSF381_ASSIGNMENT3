import React from "react";
import FeaturedFlavors from "./FeaturedFlavors";
import CustomerReviews from "./CustomerReviews";


function MainSection() {


    return (
        <div className="main-section">
            <h3>About Sweet Scoop Ice Cream</h3>

            <p>Sweet Scoop Ice Cream is a family-owned business that has been serving delicious ice cream since 1990. We pride ourselves on using only the freshest ingredients to create our unique flavors. Whether you’re in the mood for a classic vanilla or something more adventurous like our signature “Chocolate Explosion,” we have something for everyone. Come visit us and treat yourself to a sweet scoop today!
            </p>
            <br/>
            <h2>Featured Flavors</h2>
            <FeaturedFlavors />
            <CustomerReviews />

        </div>
    
    );
}


export default MainSection;