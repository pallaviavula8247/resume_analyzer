requireAuth();

async function loadDashboard(){
  try{
    const profile = await apiFetch("/auth/profile/");
    document.querySelector("#welcome").textContent = `Welcome, ${profile.username}`;

    const resumes = await apiFetch("/resumes/");
    const stats = document.querySelector("#stats");
    if(!resumes.length){
      stats.innerHTML=`<div class="card"><div class="stat">0</div><p class="muted">Resumes</p></div>`;
      document.querySelector("#resumeSummary").innerHTML=`<p class="empty">No resume yet. <a href="/upload/">Upload one</a> to begin.</p>`;
      return;
    }

    const resume = resumes[0];
    setResumeId(resume.id);
    let analysis = null;
    try{ analysis = await apiFetch(`/resumes/${resume.id}/analysis/`); }catch{}

    stats.innerHTML = `
      <div class="card"><div class="stat">${analysis?.ats_score ?? "—"}</div><p class="muted">ATS score</p></div>
      <div class="card"><div class="stat">${resume.skills?.length ?? 0}</div><p class="muted">Detected skills</p></div>
      <div class="card"><div class="stat">${resume.projects?.length ?? 0}</div><p class="muted">Projects</p></div>`;

    document.querySelector("#resumeSummary").innerHTML = `
      <h3>${resume.full_name || "Name not detected"}</h3>
      <p class="muted">${resume.email || "Email not detected"} · Resume #${resume.id}</p>
      <div class="tag-list">${(resume.skills||[]).slice(0,12).map(s=>`<span class="tag">${s}</span>`).join("")}</div>`;
  }catch(err){ document.querySelector("#message").textContent=err.message; }
}
document.querySelector("#logout").addEventListener("click",()=>{
  localStorage.clear(); window.location.href="/login/";
});
loadDashboard();
