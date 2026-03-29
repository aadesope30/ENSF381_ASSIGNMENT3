import React from "react";

function LoginForm(){
   return (
      <div>
         <form>
            <br />
            <label htmlFor="username">Username </label>
            <input type="text" id="username" name="username" /><br /><br />
            <label htmlFor="password">Password </label>
            <input type="password" id="password" name="password" /><br /><br />
            <button type="button"> Login</button><br />
            <a href="#" style={{ all: "unset", cursor: "pointer" }}> Forgot Password?</a>
         </form>
      </div>
   )
}

export default LoginForm;
