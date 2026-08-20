// ==========================================
// RESUME UPLOAD
// ==========================================

requireAuth();


// ==========================================
// GET ELEMENTS
// ==========================================

const uploadForm = document.querySelector("#uploadForm");
const fileInput = document.querySelector("#resumeFile");
const message = document.querySelector("#message");


// ==========================================
// CHECK ELEMENTS
// ==========================================

if (!uploadForm) {
  console.error("Upload form not found.");
}

if (!fileInput) {
  console.error("Resume file input not found.");
}

if (!message) {
  console.error("Message element not found.");
}


// ==========================================
// UPLOAD RESUME
// ==========================================

uploadForm.addEventListener("submit", async (e) => {

  e.preventDefault();


  // ==========================================
  // GET SELECTED FILE
  // ==========================================

  const file = fileInput.files[0];


  // ==========================================
  // VALIDATE FILE
  // ==========================================

  if (!file) {

    message.textContent =
      "Please select a PDF.";

    return;
  }


  if (
    !file.name
      .toLowerCase()
      .endsWith(".pdf")
  ) {

    message.textContent =
      "Only PDF files are accepted.";

    return;
  }


  // ==========================================
  // CREATE FORM DATA
  // ==========================================

  const formData = new FormData();

  formData.append(
    "resume_file",
    file
  );


  // ==========================================
  // SHOW UPLOAD MESSAGE
  // ==========================================

  message.textContent =
    "Uploading and extracting your resume...";


  try {

    console.log(
      "Uploading resume:",
      file.name
    );


    // ==========================================
    // CALL DEPLOYED BACKEND
    // ==========================================

    const data = await apiFetch(
      "/resumes/upload/",
      {
        method: "POST",
        body: formData
      }
    );


    // ==========================================
    // DEBUG RESPONSE
    // ==========================================

    console.log(
      "UPLOAD RESPONSE:",
      data
    );


    // ==========================================
    // GET RESUME ID
    // ==========================================

    const resumeId =
      data.resume_id ||
      data.id ||
      data.resume?.id;


    // ==========================================
    // VERIFY RESUME ID
    // ==========================================

    if (!resumeId) {

      console.error(
        "Upload response does not contain resume ID:",
        data
      );

      throw new Error(
        "Resume uploaded, but the server did not return a resume ID."
      );
    }


    // ==========================================
    // SAVE RESUME ID
    // ==========================================

    setResumeId(resumeId);


    console.log(
      "CURRENT RESUME ID:",
      resumeId
    );


    // ==========================================
    // SUCCESS MESSAGE
    // ==========================================

    message.textContent =
      `Success. Resume #${resumeId} was processed.`;


    // ==========================================
    // GO TO ANALYSIS PAGE
    // ==========================================

    setTimeout(() => {

      window.location.href =
        "/analysis/";

    }, 700);


  } catch (error) {

    console.error(
      "RESUME UPLOAD ERROR:",
      error
    );


    message.textContent =
      error.message ||
      "Resume upload failed.";
  }

});