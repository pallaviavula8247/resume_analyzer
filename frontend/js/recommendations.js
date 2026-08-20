requireAuth();
const id = getResumeId();

async function loadRecommendations(){
  if(!id){ document.querySelector("#message").textContent="Upload a resume first."; return; }
  try{
    const data = await apiFetch(`/recommendations/resume/${id}/`);
    document.querySelector("#topJobs").innerHTML = data.top_jobs.slice(0,6).map(job=>`
      <article class="card"><div class="job-title"><h3>${job.job_title}</h3><div class="match">${job.match_percentage}%</div></div><p>${job.why_recommended[0]}</p><div class="tag-list">${job.missing_skills.slice(0,6).map(x=>`<span class="tag missing">${x}</span>`).join("")}</div></article>`).join("");

    document.querySelector("#skills").innerHTML = data.skill_recommendations.map(s=>`
      <article class="card"><span class="tag">${s.priority} priority</span><h3>${s.skill}</h3><p>${s.reason}</p><p class="muted">Related: ${s.related_jobs.join(", ")}</p></article>`).join("") || `<div class="card"><p>No skill recommendations were generated from the current job dataset.</p></div>`;
  }catch(err){ document.querySelector("#message").textContent=err.message; }
}
loadRecommendations();
