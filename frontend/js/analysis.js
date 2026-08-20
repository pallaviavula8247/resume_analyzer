requireAuth();
const id = getResumeId();

if(!id){
  document.querySelector("#message").textContent="No resume is selected. Upload a resume first.";
}else{
  loadAnalysis();
  document.querySelector("#reanalyze").addEventListener("click", async ()=>{
    try{
      document.querySelector("#message").textContent="Re-analyzing...";
      await apiFetch(`/resumes/${id}/analyze/`, {method:"POST"});
      await loadAnalysis();
    }catch(err){ document.querySelector("#message").textContent=err.message; }
  });
}

async function loadAnalysis(){
  try{
    const [resume, analysis] = await Promise.all([
      apiFetch(`/resumes/${id}/`),
      apiFetch(`/resumes/${id}/analysis/`)
    ]);
    document.querySelector("#analysis").innerHTML = `
      <section class="grid two">
        <div class="card"><p class="muted">ATS score</p><div class="score">${analysis.ats_score}</div><div class="bar"><span style="width:${analysis.ats_score}%"></span></div></div>
        <div class="card"><p class="muted">Candidate</p><h2>${resume.full_name || "Not detected"}</h2><p>${resume.email || "Email not detected"}</p><p>${resume.phone || "Phone not detected"}</p></div>
      </section>
      <section class="two-col section">
        <div class="card"><h2>Strengths</h2><ul class="list">${analysis.strengths.map(x=>`<li>${x}</li>`).join("") || "<li>No evidence-based strengths generated yet.</li>"}</ul></div>
        <div class="card"><h2>Weaknesses / gaps</h2><ul class="list">${analysis.weaknesses.map(x=>`<li>${x}</li>`).join("") || "<li>No major gap detected by current rules.</li>"}</ul></div>
      </section>
      <section class="card section"><h2>Detected skills</h2><div class="tag-list">${(resume.skills||[]).map(s=>`<span class="tag">${s}</span>`).join("") || "<span class='empty'>No skills detected.</span>"}</div></section>
      <section class="card section"><h2>Education</h2><ul class="list">${(resume.education||[]).map(x=>`<li>${x.degree || "Education record"}${x.year ? " — "+x.year : ""}${x.score ? " — "+x.score : ""}</li>`).join("") || "<li>Not detected.</li>"}</ul></section>
      <section class="card section"><h2>Experience</h2><ul class="list">${(resume.experience||[]).map(x=>`<li><strong>${x.role||"Role"}</strong>${x.duration ? " — "+x.duration : ""}</li>`).join("") || "<li>Not detected.</li>"}</ul></section>
      <section class="card section"><h2>Projects</h2><ul class="list">${(resume.projects||[]).map(x=>`<li><strong>${x.title}</strong> — ${x.description}</li>`).join("") || "<li>Not detected.</li>"}</ul></section>
      <section class="card section"><h2>ATS breakdown</h2><div class="grid two">${Object.entries(analysis.score_breakdown).map(([k,v])=>`<div><strong>${k.replaceAll("_"," ")}</strong><p>${v} points</p></div>`).join("")}</div></section>`;
  }catch(err){ document.querySelector("#message").textContent=err.message; }
}
