import React from "react";

function Header() {
    return (
        <div>
            <header>
                <img src="/images/logo.webp" alt="Sweet Scoop Logo"/>
                <h1>SWEET SCOOP ICE CREAM SHOP</h1>
            </header>

            <div className="navbar">
                <a href='/'>Home</a>
                <a href='/flavors'>Flavors</a>
                <a href='/Login'>Login</a>
            </div>
        </div>
    );
}

export default Header;
