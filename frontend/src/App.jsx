import { createContext, useContext, useEffect, useState } from "react";
import { Routes, Route, Link, NavLink, useParams, useNavigate, useLocation } from "react-router-dom";
import { api } from "./api";

const T = {
  uz: { home: "Bosh sahifa", products: "Mahsulotlar", blog: "Blog", contact: "Aloqa", login: "Kirish", cart: "Savat", all: "Barchasi", add: "Savatga qo'shish", empty: "Savat bo'sh", order: "Buyurtma berish", send: "Yuborish", name: "Ismingiz", phone: "Telefon", msg: "Xabar", addr: "Manzil", sum: "so'm", ok: "Yuborildi!", reg: "Ro'yxatdan o'tish", pass: "Parol", more: "Batafsil", featured: "Tanlangan mahsulotlar", news: "Yangi kelganlar", total: "Jami", out: "Omborda yo'q" },
  ru: { home: "Главная", products: "Товары", blog: "Блог", contact: "Контакты", login: "Войти", cart: "Корзина", all: "Все", add: "В корзину", empty: "Корзина пуста", order: "Оформить заказ", send: "Отправить", name: "Имя", phone: "Телефон", msg: "Сообщение", addr: "Адрес", sum: "сум", ok: "Отправлено!", reg: "Регистрация", pass: "Пароль", more: "Подробнее", featured: "Избранное", news: "Новинки", total: "Итого", out: "Нет в наличии" },
  en: { home: "Home", products: "Products", blog: "Blog", contact: "Contact", login: "Login", cart: "Cart", all: "All", add: "Add to cart", empty: "Cart is empty", order: "Place order", send: "Send", name: "Name", phone: "Phone", msg: "Message", addr: "Address", sum: "UZS", ok: "Sent!", reg: "Sign up", pass: "Password", more: "Read more", featured: "Featured", news: "New arrivals", total: "Total", out: "Out of stock" },
};
const Ctx = createContext();
const useApp = () => useContext(Ctx);
const money = (n, t) => `${n} ${t.sum}`;
const list = d => d.results ?? d;

export default function App() {
  const [lang, setLang] = useState(localStorage.getItem("lang") || "uz");
  const [cart, setCart] = useState(JSON.parse(localStorage.getItem("cart") || "[]"));
  const [settings, setSettings] = useState({});
  const [authed, setAuthed] = useState(!!localStorage.getItem("access"));
  const t = T[lang];
  useEffect(() => { localStorage.setItem("lang", lang); document.documentElement.lang = lang; api.get("/settings/").then(r => setSettings(r.data)); }, [lang]);
  useEffect(() => localStorage.setItem("cart", JSON.stringify(cart)), [cart]);
  const add = p => setCart(c => c.find(i => i.id === p.id) ? c.map(i => i.id === p.id ? { ...i, qty: i.qty + 1 } : i) : [...c, { id: p.id, name: p.name, price: p.price, image: p.image, qty: 1 }]);
  const v = { lang, setLang, t, cart, setCart, add, settings, authed, setAuthed };
  return (
    <Ctx.Provider value={v}>
      <div className="top"><span>{settings.phone} · {settings.email}</span>
        <span>{["uz", "ru", "en"].map(l => <button key={l} className={l === lang ? "on" : ""} onClick={() => setLang(l)}>{l.toUpperCase()}</button>)}</span></div>
      <header className="nav"><Link to="/" className="logo"><b>G</b><span>GuliDesign<small>GULI DIZAYN</small></span></Link>
        <nav>{[["/", t.home], ["/products", t.products], ["/blog", t.blog], ["/contact", t.contact]].map(([to, l]) => <NavLink key={to} to={to} end={to === "/"}>{l}</NavLink>)}</nav>
        <div><Link to="/cart">🛍 {cart.reduce((s, i) => s + i.qty, 0)}</Link>
          {authed ? <button className="btn" onClick={() => { localStorage.removeItem("access"); localStorage.removeItem("refresh"); setAuthed(false); }}>↩</button> : <Link className="btn" to="/login">{t.login}</Link>}</div></header>
      <Routes>
        <Route path="/" element={<Home />} /><Route path="/products" element={<Products />} /><Route path="/products/:id" element={<Product />} />
        <Route path="/cart" element={<Cart />} /><Route path="/blog" element={<Blog />} /><Route path="/blog/:id" element={<Post />} />
        <Route path="/contact" element={<Contact />} /><Route path="/login" element={<Login />} /><Route path="/register" element={<Register />} />
      </Routes>
      <footer className="foot">© {new Date().getFullYear()} gulidesign.uz · {settings.address} · {settings.work_hours}
        {settings.instagram && <a href={settings.instagram}> Instagram</a>}{settings.telegram && <a href={settings.telegram}> Telegram</a>}</footer>
    </Ctx.Provider>
  );
}

const Hero = ({ title, sub }) => <section className="hero"><h1>{title}</h1>{sub && <p>{sub}</p>}</section>;
function Card({ p }) {
  const { t, add } = useApp();
  return <div className="card"><Link to={`/products/${p.id}`}>{p.badge && <i className="badge">{p.badge}</i>}<img src={p.image} alt={p.name} /></Link>
    <h3>{p.name}</h3><div className="row"><b>{money(p.price, t)}{p.old_price && <s> {p.old_price}</s>}</b>
      <button className="btn sm" disabled={!p.in_stock} onClick={() => add(p)}>{p.in_stock ? "+" : t.out}</button></div></div>;
}
function Home() {
  const { t, settings: s } = useApp(); const [f, setF] = useState([]);
  useEffect(() => { api.get("/products/", { params: { is_featured: true } }).then(r => setF(list(r.data))); }, [t]);
  return <>
    <section className="hero big"><h1>{s.hero_title}</h1><p>{s.hero_sub}</p><Link className="btn gold" to="/products">{t.products}</Link>
      <div className="stats"><div><b>{s.stat_products}+</b>{t.products}</div><div><b>{s.stat_clients}+</b>👥</div><div><b>{s.stat_masters}+</b>✂</div></div></section>
    <main className="wrap"><h2>{t.featured}</h2><div className="grid">{f.map(p => <Card key={p.id} p={p} />)}</div></main></>;
}
function Products() {
  const { t, lang } = useApp(); const [items, setItems] = useState([]); const [cats, setCats] = useState([]);
  const [q, setQ] = useState({ category: "", min: "", max: "", ordering: "-created", in_stock: "" });
  useEffect(() => { api.get("/categories/").then(r => setCats(list(r.data))); }, [lang]);
  useEffect(() => { const params = Object.fromEntries(Object.entries(q).filter(([, v]) => v)); api.get("/products/", { params }).then(r => setItems(list(r.data))); }, [q, lang]);
  const set = (k, v) => setQ(o => ({ ...o, [k]: v }));
  return <><Hero title={t.products} /><main className="wrap shop"><aside className="side">
    <h4>Kategoriya</h4>{[{ slug: "", name: t.all }, ...cats].map(c => <label key={c.slug}><input type="radio" checked={q.category === c.slug} onChange={() => set("category", c.slug)} /> {c.name}</label>)}
    <h4>Narx</h4><input placeholder="Min" value={q.min} onChange={e => set("min", e.target.value)} /><input placeholder="Max" value={q.max} onChange={e => set("max", e.target.value)} />
    <label><input type="checkbox" checked={!!q.in_stock} onChange={e => set("in_stock", e.target.checked ? "true" : "")} /> Omborda bor</label>
    <select value={q.ordering} onChange={e => set("ordering", e.target.value)}><option value="-created">Eng yangi</option><option value="price">Arzon</option><option value="-price">Qimmat</option></select></aside>
    <div className="grid">{items.map(p => <Card key={p.id} p={p} />)}</div></main></>;
}
function Product() {
  const { id } = useParams(); const { t, add, lang } = useApp(); const [p, setP] = useState(null);
  useEffect(() => { api.get(`/products/${id}/`).then(r => setP(r.data)); }, [id, lang]);
  if (!p) return null;
  return <main className="wrap detail"><img src={p.image} alt="" /><div><h1>{p.name}</h1><h2>{money(p.price, t)}</h2><p>{p.description}</p>
    <button className="btn" disabled={!p.in_stock} onClick={() => add(p)}>{t.add}</button></div></main>;
}
function Cart() {
  const { t, cart, setCart, authed, setAuthed } = useApp(); const nav = useNavigate();
  const [f, setF] = useState({ name: "", phone: "", address: "", note: "" });
  const [done, setDone] = useState(false); const [err, setErr] = useState("");
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const submit = async e => {
    e.preventDefault(); setErr("");
    try {
      await api.post("/orders/", { ...f, items: cart.map(i => ({ product: i.id, qty: i.qty })) });
      setCart([]); setDone(true);
    } catch (ex) {
      if (ex.response?.status === 401) {
        localStorage.removeItem("access"); localStorage.removeItem("refresh"); setAuthed(false);
        nav("/login", { state: { from: "/cart" } });
      } else setErr("Buyurtma yuborilmadi. Ma'lumotlarni tekshirib, qayta urinib ko'ring.");
    }
  };
  if (done) return <main className="wrap center"><h2>{t.ok}</h2><p>Tez orada siz bilan bog'lanamiz.</p><Link className="btn" to="/products">{t.products}</Link></main>;
  if (!cart.length) return <><Hero title={t.cart} /><main className="wrap center"><h3>{t.empty}</h3><Link className="btn" to="/products">{t.products}</Link></main></>;
  return <><Hero title={t.cart} /><main className="wrap">
    {cart.map(i => <div className="line" key={i.id}><img src={i.image} alt="" /><span>{i.name}</span>
      <input type="number" min="1" value={i.qty} onChange={e => setCart(cart.map(x => x.id === i.id ? { ...x, qty: +e.target.value || 1 } : x))} />
      <b>{money(i.price * i.qty, t)}</b><button onClick={() => setCart(cart.filter(x => x.id !== i.id))}>✕</button></div>)}
    <h3>{t.total}: {money(total, t)}</h3>
    {!authed ? <div className="box center"><p>Buyurtma berish uchun hisobingizga kiring. Savatingiz saqlanib qoladi.</p>
        <Link className="btn" to="/login" state={{ from: "/cart" }}>Kirish</Link>{" "}
        <Link className="btn gold" to="/register" state={{ from: "/cart" }}>Ro'yxatdan o'tish</Link></div>
      : <form className="form" onSubmit={submit}>
        {[["name", t.name], ["phone", t.phone], ["address", t.addr]].map(([k, l]) => <input key={k} required placeholder={l} value={f[k]} onChange={e => setF({ ...f, [k]: e.target.value })} />)}
        <textarea placeholder={t.msg} value={f.note} onChange={e => setF({ ...f, note: e.target.value })} />
        {err && <div className="alert">{err}</div>}<button className="btn">{t.order}</button></form>}
  </main></>;
}
function Blog() {
  const { t, lang } = useApp(); const [p, setP] = useState([]);
  useEffect(() => { api.get("/posts/").then(r => setP(list(r.data))); }, [lang]);
  return <><Hero title={t.blog} /><main className="wrap"><div className="grid">{p.map(x => <Link className="card" key={x.id} to={`/blog/${x.id}`}>{x.cover && <img src={x.cover} alt="" />}<h3>{x.title}</h3><small>{x.created.slice(0, 10)} · {t.more}</small></Link>)}</div></main></>;
}
function Post() {
  const { id } = useParams(); const { lang } = useApp(); const [p, setP] = useState(null);
  useEffect(() => { api.get(`/posts/${id}/`).then(r => setP(r.data)); }, [id, lang]);
  return p && <main className="wrap narrow"><h1>{p.title}</h1>{p.cover && <img src={p.cover} alt="" />}<p style={{ whiteSpace: "pre-wrap" }}>{p.body}</p></main>;
}
function Contact() {
  const { t, settings: s } = useApp(); const [f, setF] = useState({ name: "", email: "", phone: "", message: "" }); const [ok, setOk] = useState(false);
  const submit = async e => { e.preventDefault(); await api.post("/contact/", f); setOk(true); setF({ name: "", email: "", phone: "", message: "" }); };
  return <><Hero title={t.contact} /><main className="wrap two"><div className="info"><p>📍 {s.address}</p><p>📞 {s.phone}</p><p>✉ {s.email}</p><p>🕘 {s.work_hours}</p></div>
    <form className="form" onSubmit={submit}><input required placeholder={t.name} value={f.name} onChange={e => setF({ ...f, name: e.target.value })} />
      <input required type="email" placeholder="Email" value={f.email} onChange={e => setF({ ...f, email: e.target.value })} />
      <input placeholder={t.phone} value={f.phone} onChange={e => setF({ ...f, phone: e.target.value })} />
      <textarea required placeholder={t.msg} value={f.message} onChange={e => setF({ ...f, message: e.target.value })} /><button className="btn">{t.send}</button>{ok && <p>{t.ok}</p>}</form></main></>;
}
const parseErr = e => {
  if (!e.response) return { _: "Serverga ulanib bo'lmadi. Backend (python manage.py runserver) ishlayotganini tekshiring." };
  const { status, data } = e.response;
  if (status === 401) return { _: "Email yoki parol noto'g'ri." };
  if (data && typeof data === "object") {
    const o = {};
    for (const k in data) o[k === "detail" || k === "non_field_errors" ? "_" : k] = [].concat(data[k])[0];
    return o;
  }
  return { _: `Kutilmagan xatolik (${status}). Keyinroq urinib ko'ring.` };
};
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function Field({ label, error, type = "text", value, onChange, placeholder, autoComplete }) {
  const [show, setShow] = useState(false);
  const pw = type === "password";
  return <div className={"field" + (error ? " bad" : "")}>
    <label>{label}</label>
    <div className="inp"><input type={pw && show ? "text" : type} value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} autoComplete={autoComplete} />
      {pw && <button type="button" onClick={() => setShow(!show)}>{show ? "🙈" : "👁"}</button>}</div>
    {error && <span className="err">{error}</span>}
  </div>;
}

function AuthBox({ title, sub, children, foot }) {
  return <main className="wrap narrow"><div className="box authbox"><div className="logo big"><b>G</b></div>
    <h2>{title}</h2><p className="sub">{sub}</p>{children}<p className="foot2">{foot}</p></div></main>;
}

function useAuthSubmit() {
  const { setAuthed } = useApp(); const nav = useNavigate(); const loc = useLocation();
  const [errs, setErrs] = useState({}); const [busy, setBusy] = useState(false);
  const run = async (check, job) => {
    const local = check(); setErrs(local); if (Object.keys(local).length) return;
    setBusy(true);
    try {
      const r = await job();
      localStorage.setItem("access", r.data.access); localStorage.setItem("refresh", r.data.refresh);
      setAuthed(true); nav(loc.state?.from || "/", { replace: true });
    } catch (e) { setErrs(parseErr(e)); } finally { setBusy(false); }
  };
  return { errs, busy, run };
}

const emailErr = v => !v.trim() ? "Emailni kiriting." : !EMAIL_RE.test(v.trim()) ? "Email noto'g'ri yozilgan. Masalan: ali@mail.uz" : "";

function Login() {
  const loc = useLocation(); const { errs, busy, run } = useAuthSubmit(); const [f, setF] = useState({ email: "", password: "" });
  const submit = e => { e.preventDefault(); run(() => {
    const x = {}; const em = emailErr(f.email); if (em) x.email = em;
    if (!f.password) x.password = "Parolni kiriting."; return x;
  }, () => api.post("/auth/login/", { username: f.email.trim().toLowerCase(), password: f.password })); };
  return <AuthBox title="Kirish" sub="Hisobingizga kiring" foot={<>Hisobingiz yo'qmi? <Link to="/register" state={loc.state}>Ro'yxatdan o'tish</Link></>}>
    <form className="form" onSubmit={submit} noValidate>
      {errs._ && <div className="alert">{errs._}</div>}
      <Field label="Email" type="email" autoComplete="email" value={f.email} error={errs.email} onChange={v => setF({ ...f, email: v })} placeholder="ali@mail.uz" />
      <Field label="Parol" type="password" autoComplete="current-password" value={f.password} error={errs.password} onChange={v => setF({ ...f, password: v })} />
      <button className="btn" disabled={busy}>{busy ? "Kutilmoqda..." : "Kirish"}</button>
    </form></AuthBox>;
}

function Register() {
  const loc = useLocation(); const { errs, busy, run } = useAuthSubmit(); const [f, setF] = useState({ first_name: "", email: "", password: "", password2: "" });
  const submit = e => { e.preventDefault(); run(() => {
    const x = {}; const em = emailErr(f.email); if (em) x.email = em;
    if (f.password.length < 6) x.password = "Parol kamida 6 ta belgidan iborat bo'lishi kerak.";
    if (f.password2 !== f.password) x.password2 = "Parollar bir xil emas."; return x;
  }, async () => {
    const email = f.email.trim().toLowerCase();
    await api.post("/auth/register/", { first_name: f.first_name, email, password: f.password });
    return api.post("/auth/login/", { username: email, password: f.password });
  }); };
  return <AuthBox title="Ro'yxatdan o'tish" sub="Bir daqiqada hisob oching" foot={<>Hisobingiz bormi? <Link to="/login" state={loc.state}>Kirish</Link></>}>
    <form className="form" onSubmit={submit} noValidate>
      {errs._ && <div className="alert">{errs._}</div>}
      <Field label="Ismingiz (ixtiyoriy)" autoComplete="name" value={f.first_name} error={errs.first_name} onChange={v => setF({ ...f, first_name: v })} />
      <Field label="Email" type="email" autoComplete="email" value={f.email} error={errs.email} onChange={v => setF({ ...f, email: v })} placeholder="ali@mail.uz" />
      <Field label="Parol" type="password" autoComplete="new-password" value={f.password} error={errs.password} onChange={v => setF({ ...f, password: v })} placeholder="Kamida 6 ta belgi" />
      <Field label="Parolni takrorlang" type="password" autoComplete="new-password" value={f.password2} error={errs.password2} onChange={v => setF({ ...f, password2: v })} />
      <button className="btn" disabled={busy}>{busy ? "Kutilmoqda..." : "Ro'yxatdan o'tish"}</button>
    </form></AuthBox>;
}
