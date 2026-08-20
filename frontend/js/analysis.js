// ==========================================
// ANALYSIS PAGE
// ==========================================

requireAuth();


// ==========================================
// GET RESUME ID
// ==========================================

const id = getResumeId();

const messageElement =
  document.querySelector("#message");

const analysisElement =
  document.querySelector("#analysis");

const reanalyzeButton =
  document.querySelector("#reanalyze");


// ==========================================
// CHECK RESUME ID
// ==========================================

if (!id) {

  if (messageElement) {
    messageElement.textContent =
      "No resume is selected. Upload a resume first.";
  }

} else {

  console.log(
    "ANALYZING RESUME ID:",
    id
  );


  // ==========================================
  // LOAD INITIAL ANALYSIS
  // ==========================================

  loadAnalysis();


  // ==========================================
  // RE-ANALYZE BUTTON
  // ==========================================

  if (reanalyzeButton) {

    reanalyzeButton.addEventListener(
      "click",
      async () => {

        try {

          messageElement.textContent =
            "Re-analyzing your resume...";


          console.log(
            "RE-ANALYZING RESUME:",
            id
          );


          await apiFetch(
            `/resumes/${id}/analyze/`,
            {
              method: "POST"
            }
          );


          messageElement.textContent =
            "Analysis completed successfully.";


          await loadAnalysis();


        } catch (error) {

          console.error(
            "RE-ANALYSIS ERROR:",
            error
          );

          messageElement.textContent =
            error.message ||
            "Re-analysis failed.";
        }
      }
    );
  }
}


// ==========================================
// LOAD ANALYSIS
// ==========================================

async function loadAnalysis() {

  if (!id) {
    return;
  }

  try {

    if (messageElement) {
      messageElement.textContent =
        "Loading your resume analysis...";
    }


    // ==========================================
    // GET RESUME + ANALYSIS
    // ==========================================

    const [
      resume,
      analysis
    ] = await Promise.all([

      apiFetch(
        `/resumes/${id}/`
      ),

      apiFetch(
        `/resumes/${id}/analysis/`
      )

    ]);


    // ==========================================
    // DEBUG
    // ==========================================

    console.log(
      "RESUME DATA:",
      resume
    );

    console.log(
      "ANALYSIS DATA:",
      analysis
    );


    // ==========================================
    // SAFE DATA
    // ==========================================

    const skills =
      Array.isArray(resume.skills)
        ? resume.skills
        : [];

    const education =
      Array.isArray(resume.education)
        ? resume.education
        : [];

    const experience =
      Array.isArray(resume.experience)
        ? resume.experience
        : [];

    const projects =
      Array.isArray(resume.projects)
        ? resume.projects
        : [];

    const strengths =
      Array.isArray(analysis.strengths)
        ? analysis.strengths
        : [];

    const weaknesses =
      Array.isArray(analysis.weaknesses)
        ? analysis.weaknesses
        : [];

    const scoreBreakdown =
      analysis.score_breakdown &&
      typeof analysis.score_breakdown === "object"
        ? analysis.score_breakdown
        : {};


    // ==========================================
    // ATS SCORE
    // ==========================================

    const atsScore =
      Number(analysis.ats_score) || 0;

    const safeAtsScore =
      Math.max(
        0,
        Math.min(
          100,
          atsScore
        )
      );


    // ==========================================
    // CANDIDATE INFORMATION
    // ==========================================

    const fullName =
      resume.full_name ||
      "Not detected";

    const email =
      resume.email ||
      "Email not detected";

    const phone =
      resume.phone ||
      "Phone not detected";


    // ==========================================
    // GENERATE SKILLS HTML
    // ==========================================

    const skillsHTML =
      skills.length > 0

        ? skills
            .map(
              skill =>
                `<span class="tag">${escapeHTML(skill)}</span>`
            )
            .join("")

        : `<span class="empty">
             No skills detected.
           </span>`;


    // ==========================================
    // GENERATE STRENGTHS HTML
    // ==========================================

    const strengthsHTML =
      strengths.length > 0

        ? strengths
            .map(
              item =>
                `<li>${escapeHTML(item)}</li>`
            )
            .join("")

        : `<li>
             No evidence-based strengths generated yet.
           </li>`;


    // ==========================================
    // GENERATE WEAKNESSES HTML
    // ==========================================

    const weaknessesHTML =
      weaknesses.length > 0

        ? weaknesses
            .map(
              item =>
                `<li>${escapeHTML(item)}</li>`
            )
            .join("")

        : `<li>
             No major gap detected by current rules.
           </li>`;


    // ==========================================
    // GENERATE EDUCATION HTML
    // ==========================================

    const educationHTML =
      education.length > 0

        ? education
            .map(item => {

              const degree =
                item.degree ||
                "Education record";

              const year =
                item.year
                  ? ` — ${item.year}`
                  : "";

              const score =
                item.score
                  ? ` — ${item.score}`
                  : "";

              return `
                <li>
                  ${escapeHTML(degree)}
                  ${escapeHTML(year)}
                  ${escapeHTML(score)}
                </li>
              `;
            })
            .join("")

        : `<li>Not detected.</li>`;


    // ==========================================
    // GENERATE EXPERIENCE HTML
    // ==========================================

    const experienceHTML =
      experience.length > 0

        ? experience
            .map(item => {

              const role =
                item.role ||
                "Role";

              const duration =
                item.duration
                  ? ` — ${item.duration}`
                  : "";

              return `
                <li>
                  <strong>
                    ${escapeHTML(role)}
                  </strong>
                  ${escapeHTML(duration)}
                </li>
              `;
            })
            .join("")

        : `<li>Not detected.</li>`;


    // ==========================================
    // GENERATE PROJECTS HTML
    // ==========================================

    const projectsHTML =
      projects.length > 0

        ? projects
            .map(item => {

              const title =
                item.title ||
                "Project";

              const description =
                item.description ||
                "No description available.";

              return `
                <li>
                  <strong>
                    ${escapeHTML(title)}
                  </strong>
                  — ${escapeHTML(description)}
                </li>
              `;
            })
            .join("")

        : `<li>Not detected.</li>`;


    // ==========================================
    // GENERATE ATS BREAKDOWN HTML
    // ==========================================

    const breakdownHTML =
      Object.keys(scoreBreakdown).length > 0

        ? Object.entries(scoreBreakdown)
            .map(([key, value]) => {

              const label =
                key
                  .replaceAll("_", " ");

              return `
                <div>
                  <strong>
                    ${escapeHTML(label)}
                  </strong>

                  <p>
                    ${escapeHTML(String(value))}
                    points
                  </p>
                </div>
              `;
            })
            .join("")

        : `
          <div>
            <p>
              No score breakdown available.
            </p>
          </div>
        `;


    // ==========================================
    // RENDER COMPLETE ANALYSIS
    // ==========================================

    analysisElement.innerHTML = `

      <!-- ATS + CANDIDATE -->

      <section class="grid two">

        <div class="card">

          <p class="muted">
            ATS score
          </p>

          <div class="score">
            ${safeAtsScore}
          </div>

          <div class="bar">

            <span
              style="width:${safeAtsScore}%"
            ></span>

          </div>

        </div>


        <div class="card">

          <p class="muted">
            Candidate
          </p>

          <h2>
            ${escapeHTML(fullName)}
          </h2>

          <p>
            ${escapeHTML(email)}
          </p>

          <p>
            ${escapeHTML(phone)}
          </p>

        </div>

      </section>


      <!-- STRENGTHS + WEAKNESSES -->

      <section class="two-col section">

        <div class="card">

          <h2>
            Strengths
          </h2>

          <ul class="list">
            ${strengthsHTML}
          </ul>

        </div>


        <div class="card">

          <h2>
            Weaknesses / gaps
          </h2>

          <ul class="list">
            ${weaknessesHTML}
          </ul>

        </div>

      </section>


      <!-- SKILLS -->

      <section class="card section">

        <h2>
          Detected skills
        </h2>

        <div class="tag-list">
          ${skillsHTML}
        </div>

      </section>


      <!-- EDUCATION -->

      <section class="card section">

        <h2>
          Education
        </h2>

        <ul class="list">
          ${educationHTML}
        </ul>

      </section>


      <!-- EXPERIENCE -->

      <section class="card section">

        <h2>
          Experience
        </h2>

        <ul class="list">
          ${experienceHTML}
        </ul>

      </section>


      <!-- PROJECTS -->

      <section class="card section">

        <h2>
          Projects
        </h2>

        <ul class="list">
          ${projectsHTML}
        </ul>

      </section>


      <!-- ATS BREAKDOWN -->

      <section class="card section">

        <h2>
          ATS breakdown
        </h2>

        <div class="grid two">
          ${breakdownHTML}
        </div>

      </section>

    `;


    // ==========================================
    // CLEAR MESSAGE
    // ==========================================

    if (messageElement) {

      messageElement.textContent =
        "Analysis loaded successfully.";

    }


  } catch (error) {

    console.error(
      "ANALYSIS LOAD ERROR:",
      error
    );


    if (messageElement) {

      messageElement.textContent =
        error.message ||
        "Unable to load resume analysis.";

    }
  }
}


// ==========================================
// HTML ESCAPE
// ==========================================
// Prevents resume text from being interpreted
// as HTML.

function escapeHTML(value) {

  if (
    value === undefined ||
    value === null
  ) {
    return "";
  }

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}