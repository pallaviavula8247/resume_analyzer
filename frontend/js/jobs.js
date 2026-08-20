requireAuth();
const id = getResumeId();

async function loadJobs(){
  if(!id){ document.querySelector("#message").textContent="Upload a resume first."; return; }
  try{
    const data = await apiFetch(`/resumes/${id}/jobs/`);
    document.querySelector("#jobs").innerHTML = data.jobs.map(job=>`
      <article class="card">
        <div class="job-title"><h2>${job.job_title}</h2><div class="match">${job.match_percentage}%</div></div>
        <p class="muted">Explainable match based on skills, education, experience and projects.</p>
        <h4>Matched skills</h4>
        <div class="tag-list">${job.matched_skills.map(x=>`<span class="tag">${x}</span>`).join("") || "<span class='empty'>None detected</span>"}</div>
        <h4>Missing required skills</h4>
        <div class="tag-list">${job.missing_skills.map(x=>`<span class="tag missing">${x}</span>`).join("") || "<span class='tag'>No required skill gap</span>"}</div>
        <h4>Why it matches</h4><ul class="list">${job.why_recommended.map(x=>`<li>${x}</li>`).join("")}</ul>
      </article>`).join("");
  }catch(err){ document.querySelector("#message").textContent=err.message; }
}
loadJobs();
