requireAuth();

document.querySelector("#uploadForm").addEventListener("submit", async e=>{
  e.preventDefault();
  const file = document.querySelector("#resumeFile").files[0];
  const message = document.querySelector("#message");

  if(!file){ message.textContent="Please select a PDF."; return; }
  if(!file.name.toLowerCase().endsWith(".pdf")){ message.textContent="Only PDF files are accepted."; return; }

  const formData = new FormData();
  formData.append("resume_file", file);

  message.textContent="Uploading and extracting your resume...";
  try{
    const data = await apiFetch("/resumes/upload/", {method:"POST", body:formData});
    setResumeId(data.resume_id);
    message.textContent=`Success. Resume #${data.resume_id} was processed.`;
    setTimeout(()=>window.location.href="/analysis/",700);
  }catch(err){ message.textContent=err.message; }
});
