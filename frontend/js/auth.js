const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");

if(loginForm){
  loginForm.addEventListener("submit", async e=>{
    e.preventDefault();
    const message = document.querySelector("#message");
    try{
      const data = await apiFetch("/auth/login/", {
        method:"POST",
        body:JSON.stringify({
          username:document.querySelector("#username").value.trim(),
          password:document.querySelector("#password").value
        })
      });
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      window.location.href="/dashboard/";
    }catch(err){ message.textContent=err.message; }
  });
}

if(registerForm){
  registerForm.addEventListener("submit", async e=>{
    e.preventDefault();
    const message = document.querySelector("#message");
    try{
      await apiFetch("/auth/register/", {
        method:"POST",
        body:JSON.stringify({
          username:document.querySelector("#username").value.trim(),
          email:document.querySelector("#email").value.trim(),
          password:document.querySelector("#password").value
        })
      });
      message.textContent="Account created. Redirecting to login...";
      setTimeout(()=>window.location.href="/login/",700);
    }catch(err){ message.textContent=err.message; }
  });
}
