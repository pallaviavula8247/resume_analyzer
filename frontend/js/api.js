const API_BASE = "/api";

function getAccessToken(){ return localStorage.getItem("access_token"); }
function getResumeId(){ return localStorage.getItem("current_resume_id"); }
function setResumeId(id){ if(id) localStorage.setItem("current_resume_id", String(id)); }

async function apiFetch(path, options = {}, retry = true){
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();
  if(token) headers.set("Authorization", `Bearer ${token}`);
  if(!(options.body instanceof FormData) && !headers.has("Content-Type")){
    headers.set("Content-Type", "application/json");
  }

  let response;
  try{
    response = await fetch(`${API_BASE}${path}`, {...options, headers});
  }catch(error){
    throw new Error("Network error: the backend could not be reached.");
  }

  if(response.status === 401 && retry){
    const refresh = localStorage.getItem("refresh_token");
    if(refresh){
      const refreshResponse = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({refresh})
      });
      if(refreshResponse.ok){
        const data = await refreshResponse.json();
        localStorage.setItem("access_token", data.access);
        return apiFetch(path, options, false);
      }
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    throw new Error("Your session has expired. Please log in again.");
  }

  const raw = await response.text();
  let data = {};
  try{ data = raw ? JSON.parse(raw) : {}; }catch{ data = {detail: raw}; }

  if(!response.ok){
    const detail = data.detail || data.message || Object.values(data).flat().join(" ");
    throw new Error(detail || `Request failed with HTTP ${response.status}.`);
  }
  return data;
}

function requireAuth(){
  if(!getAccessToken()) window.location.href = "/login/";
}
