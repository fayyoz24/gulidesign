import axios from "axios";
export const api = axios.create({ baseURL: import.meta.env.VITE_API || "/api" });
api.interceptors.request.use(c => { const t = localStorage.getItem("access"); if (t) c.headers.Authorization = `Bearer ${t}`; c.params = { lang: localStorage.getItem("lang") || "uz", ...c.params }; return c; });
