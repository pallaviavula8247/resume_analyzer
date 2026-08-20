// ==========================================
// API CONFIGURATION
// ==========================================

const API_BASE = "https://resume-analyzer-pld8.onrender.com/api";


// ==========================================
// AUTH / RESUME STORAGE
// ==========================================

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

function getResumeId() {
  return localStorage.getItem("current_resume_id");
}

function setResumeId(id) {
  if (id !== undefined && id !== null && id !== "") {
    localStorage.setItem("current_resume_id", String(id));
  }
}

function clearAuth() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}


// ==========================================
// REFRESH ACCESS TOKEN
// ==========================================

async function refreshAccessToken() {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    return false;
  }

  try {
    const response = await fetch(
      `${API_BASE}/auth/token/refresh/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      }
    );

    if (!response.ok) {
      console.error(
        "Token refresh failed:",
        response.status
      );

      return false;
    }

    const data = await response.json();

    if (!data.access) {
      console.error(
        "Refresh response does not contain access token."
      );

      return false;
    }

    localStorage.setItem(
      "access_token",
      data.access
    );

    return true;

  } catch (error) {
    console.error(
      "Token refresh error:",
      error
    );

    return false;
  }
}


// ==========================================
// MAIN API FUNCTION
// ==========================================

async function apiFetch(
  path,
  options = {},
  retry = true
) {

  const headers = new Headers(
    options.headers || {}
  );

  const token = getAccessToken();


  // ==========================================
  // ADD JWT ACCESS TOKEN
  // ==========================================

  if (token) {
    headers.set(
      "Authorization",
      `Bearer ${token}`
    );
  }


  // ==========================================
  // CONTENT TYPE
  // ==========================================
  // Do NOT set application/json for FormData.

  if (
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json"
    );
  }


  // ==========================================
  // SEND REQUEST
  // ==========================================

  let response;

  try {

    response = await fetch(
      `${API_BASE}${path}`,
      {
        ...options,
        headers
      }
    );

  } catch (error) {

    console.error(
      "NETWORK ERROR:",
      error
    );

    throw new Error(
      "Network error: the backend could not be reached."
    );
  }


  // ==========================================
  // HANDLE 401 - TOKEN EXPIRED
  // ==========================================

  if (
    response.status === 401 &&
    retry
  ) {

    const refreshed =
      await refreshAccessToken();


    // ==========================================
    // RETRY ORIGINAL REQUEST
    // ==========================================

    if (refreshed) {

      return apiFetch(
        path,
        options,
        false
      );
    }


    // ==========================================
    // REFRESH TOKEN ALSO FAILED
    // ==========================================

    clearAuth();

    throw new Error(
      "Your session has expired. Please log in again."
    );
  }


  // ==========================================
  // READ RESPONSE
  // ==========================================

  const raw =
    await response.text();

  let data = {};


  try {

    data = raw
      ? JSON.parse(raw)
      : {};

  } catch {

    data = {
      detail: raw
    };
  }


  // ==========================================
  // HANDLE API ERRORS
  // ==========================================

  if (!response.ok) {

    let detail =
      data.detail ||
      data.message ||
      data.error;


    // Handle Django REST Framework
    // validation errors.

    if (
      !detail &&
      typeof data === "object"
    ) {

      detail = Object.entries(data)
        .map(([key, value]) => {

          if (Array.isArray(value)) {

            return `${key}: ${value.join(", ")}`;

          }

          if (
            typeof value === "object" &&
            value !== null
          ) {

            return `${key}: ${JSON.stringify(value)}`;

          }

          return `${key}: ${value}`;

        })
        .join(" ");
    }


    throw new Error(
      detail ||
      `Request failed with HTTP ${response.status}.`
    );
  }


  // ==========================================
  // SUCCESS
  // ==========================================

  return data;
}


// ==========================================
// AUTH CHECK
// ==========================================

function requireAuth() {

  if (!getAccessToken()) {

    window.location.href = "/login/";

  }
}


// ==========================================
// GET REQUEST
// ==========================================

async function apiGet(path) {

  return apiFetch(
    path,
    {
      method: "GET"
    }
  );
}


// ==========================================
// POST REQUEST
// ==========================================

async function apiPost(
  path,
  body = {}
) {

  return apiFetch(
    path,
    {
      method: "POST",
      body: JSON.stringify(body)
    }
  );
}


// ==========================================
// PUT REQUEST
// ==========================================

async function apiPut(
  path,
  body = {}
) {

  return apiFetch(
    path,
    {
      method: "PUT",
      body: JSON.stringify(body)
    }
  );
}


// ==========================================
// PATCH REQUEST
// ==========================================

async function apiPatch(
  path,
  body = {}
) {

  return apiFetch(
    path,
    {
      method: "PATCH",
      body: JSON.stringify(body)
    }
  );
}


// ==========================================
// DELETE REQUEST
// ==========================================

async function apiDelete(path) {

  return apiFetch(
    path,
    {
      method: "DELETE"
    }
  );
}