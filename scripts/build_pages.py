#!/usr/bin/env python3
import os

BASE_URL = "https://angsumi.online"
PHONE = "+917896595109"
PHONE_DISPLAY = "+91 78965 95109"
EMAIL = "angudas62@gmail.com"

# Shared Navigation HTML
NAV_HTML = f"""  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="/">
        <span class="logo-mark"><img src="/logo.png" alt="Angsumi logo"></span>angsumi
      </a>
      <nav class="links">
        <a href="/#vp">Why Us</a>
        <a href="/#proof">Live Systems</a>
        <a href="{BASE_URL}/services/">Services</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/tools/">Tools</a>
        <a href="/#pricing">Pricing</a>
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
        <a href="/about/">About</a>
        <a href="/#cta">Contact</a>
      </nav>
      <a class="nav-cta" href="https://wa.me/917896595109" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">☰</button>
    </div>
  </header>"""

# Shared Clean Multi-Column Footer HTML
FOOTER_HTML = f"""  <footer>
    <div class="container footer-grid">
      <div class="footer-brand">
        <a class="logo" href="/">
          <span class="logo-mark"><img src="/logo.png" alt="Angsumi logo"></span>angsumi
        </a>
        <p>
          High-converting, ultra-fast digital systems &amp; websites engineered for growing businesses across Northeast India.
        </p>
        <div class="footer-contact">
          <a href="mailto:{EMAIL}">✉ {EMAIL}</a>
          <a href="https://wa.me/917896595109" target="_blank" rel="noopener">💬 {PHONE_DISPLAY}</a>
        </div>
      </div>

      <div class="footer-col">
        <h4>Digital Systems</h4>
        <ul class="footer-links">
          <li><a href="{BASE_URL}/services/doctor-clinic-website-design/">Doctor &amp; Clinic OPD</a></li>
          <li><a href="{BASE_URL}/services/school-management-system/">School &amp; Coaching Portals</a></li>
          <li><a href="{BASE_URL}/services/assam-silk-handloom-ecommerce/">Silk &amp; Handloom D2C</a></li>
          <li><a href="{BASE_URL}/services/tea-estate-factory-website-design/">Tea Estates &amp; Exports</a></li>
          <li><a href="{BASE_URL}/services/tourism-safari-cab-booking-system/">Safari &amp; Tour Booking</a></li>
          <li><a href="{BASE_URL}/services/mobile-app-development/">Mobile App Development</a></li>
          <li><a href="{BASE_URL}/services/" class="footer-more">All Systems Directory &rarr;</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Coverage Areas</h4>
        <ul class="footer-links">
          <li><a href="{BASE_URL}/locations/assam/">Assam (Guwahati, Dibrugarh, Silchar)</a></li>
          <li><a href="{BASE_URL}/locations/meghalaya/">Meghalaya (Shillong, Tura)</a></li>
          <li><a href="{BASE_URL}/locations/arunachal-pradesh/">Arunachal Pradesh (Itanagar)</a></li>
          <li><a href="{BASE_URL}/locations/tripura/">Tripura (Agartala)</a></li>
          <li><a href="{BASE_URL}/locations/nagaland/">Nagaland (Kohima, Dimapur)</a></li>
          <li><a href="{BASE_URL}/locations/west-bengal/">West Bengal (Siliguri)</a></li>
          <li><a href="{BASE_URL}/locations/" class="footer-more">All Locations Directory &rarr;</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Company &amp; Legal</h4>
        <ul class="footer-links">
          <li><a href="{BASE_URL}/about/">About Angsumi</a></li>
          <li><a href="{BASE_URL}/privacy-policy/">Privacy Policy</a></li>
          <li><a href="{BASE_URL}/terms/">Terms of Service</a></li>
          <li><a href="https://blog.angsumi.online" target="_blank" rel="noopener">Official Blog ↗</a></li>
          <li><a href="{BASE_URL}/tools/cost-calculator/">Live Cost Estimator</a></li>
          <li><a href="{BASE_URL}/tools/tech-detector/">Speed &amp; Tech Inspector</a></li>
          <li><a href="{BASE_URL}/cv/">Founder Profile &amp; CV</a></li>
        </ul>
      </div>
    </div>

    <div class="container footer-bottom">
      <div>&copy; 2026 Angsumi. Digital systems without the agency price tag.</div>
      <div class="footer-bottom-links">
        <a href="{BASE_URL}/about/">About</a>
        <a href="{BASE_URL}/privacy-policy/">Privacy Policy</a>
        <a href="{BASE_URL}/terms/">Terms</a>
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
        <a href="https://wa.me/917896595109" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <script>
    function toggleMenu() {{
      const links = document.querySelector('.links');
      const isVisible = links.style.display === 'flex';
      links.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {{
        links.style.position = 'absolute';
        links.style.top = '76px';
        links.style.left = '0';
        links.style.right = '0';
        links.style.padding = '20px 24px';
        links.style.background = 'rgba(247, 248, 250, 0.98)';
        links.style.flexDirection = 'column';
        links.style.alignItems = 'flex-start';
        links.style.borderBottom = '1px solid var(--line)';
        links.style.boxShadow = '0 10px 25px rgba(0,0,0,0.05)';
      }}
    }}
  </script>"""

# Shared Base CSS
BASE_CSS = """    :root {
      --bg: #f7f8fa;
      --surface: #ffffff;
      --ink: #0b1220;
      --muted: #5e6a7c;
      --line: #e4e8ef;
      --brand: #1257d6;
      --brand-dark: #0b3f9e;
      --accent: #10b981;
      --soft: #eef4ff;
      --radius: 20px;
      --shadow: 0 20px 45px rgba(11, 18, 32, 0.08);
      --max: 1180px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }
    a { text-decoration: none; color: inherit; }
    .container { width: min(var(--max), calc(100% - 40px)); margin: auto; }

    /* Sticky Nav */
    .nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 50;
      background: rgba(247, 248, 250, 0.92); backdrop-filter: blur(18px);
      border-bottom: 1px solid rgba(228, 232, 239, 0.85);
    }
    .nav-inner { height: 76px; display: flex; align-items: center; justify-content: space-between; }
    .logo { display: flex; align-items: center; gap: 10px; font-size: 22px; font-weight: 850; letter-spacing: -.05em; color: var(--ink); }
    .logo-mark img { width: 36px; height: 36px; object-fit: contain; display: block; }
    .links { display: flex; align-items: center; gap: 22px; font-size: 14px; font-weight: 650; color: #3e4755; }
    .links a { padding: 6px 10px; border-radius: 8px; transition: color .2s, background .2s; }
    .links a:hover, .links a.active { color: var(--brand); background: var(--soft); }
    .nav-cta {
      background: var(--ink); color: #fff; border: 0; border-radius: 999px; padding: 11px 20px;
      font-weight: 750; font-size: 13.5px; cursor: pointer; transition: transform .2s, background .2s; display: inline-flex; align-items: center; gap: 6px;
    }
    .nav-cta:hover { transform: translateY(-2px); background: #182233; color: #fff; }
    .menu { display: none; background: none; border: 0; font-size: 26px; cursor: pointer; padding: 4px; }

    /* Breadcrumbs */
    .breadcrumb-strip {
      padding-top: 96px; padding-bottom: 14px; background: #fff; border-bottom: 1px solid var(--line); font-size: 13px; font-weight: 600; color: var(--muted);
    }
    .breadcrumbs { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .breadcrumbs a { color: var(--brand); }
    .breadcrumbs span { color: #94a3b8; }

    /* Hero */
    .page-hero { padding: 60px 0 40px; background: linear-gradient(180deg, #ffffff 0%, #f7f8fa 100%); border-bottom: 1px solid var(--line); }
    .badge {
      display: inline-flex; align-items: center; gap: 8px; background: var(--soft); color: var(--brand);
      border: 1px solid #d9e6ff; border-radius: 999px; padding: 6px 14px; font-size: 12px; font-weight: 800;
      text-transform: uppercase; letter-spacing: .06em; margin-bottom: 18px;
    }
    h1 { font-size: clamp(32px, 4vw, 50px); line-height: 1.12; letter-spacing: -.04em; font-weight: 900; color: var(--ink); }
    .hero-sub { font-size: 17.5px; color: var(--muted); max-width: 800px; margin: 16px 0 0; line-height: 1.6; }

    /* Content Layout */
    .content-section { padding: 60px 0 80px; }
    .doc-card {
      background: #ffffff; border: 1px solid var(--line); border-radius: var(--radius);
      padding: 48px; box-shadow: var(--shadow); max-width: 900px; margin: auto;
    }
    .article-body { font-size: 15.5px; line-height: 1.8; color: #334155; }
    .article-body h2 { font-size: 22px; font-weight: 850; color: var(--ink); margin: 36px 0 14px; letter-spacing: -.03em; border-bottom: 1px solid var(--line); padding-bottom: 8px; }
    .article-body h2:first-of-type { margin-top: 0; }
    .article-body h3 { font-size: 17px; font-weight: 800; color: var(--ink); margin: 24px 0 10px; }
    .article-body p { margin-bottom: 16px; }
    .article-body ul, .article-body ol { margin: 0 0 20px 24px; }
    .article-body li { margin-bottom: 8px; }
    .article-body strong { color: var(--ink); }

    /* Footer */
    footer { border-top: 1px solid var(--line); padding: 60px 0 32px; color: #64748b; font-size: 14px; background: #fff; }
    .footer-grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 48px; }
    .footer-brand .logo { margin-bottom: 14px; }
    .footer-brand p { font-size: 13.5px; line-height: 1.6; color: #64748b; margin-bottom: 20px; max-width: 320px; }
    .footer-contact { display: flex; flex-direction: column; gap: 10px; }
    .footer-contact a { display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: var(--ink); }
    .footer-col h4 { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink); margin-bottom: 16px; }
    .footer-links { list-style: none; display: flex; flex-direction: column; gap: 10px; }
    .footer-links a { color: #64748b; font-size: 13.5px; transition: color .2s; }
    .footer-links a:hover { color: var(--brand); }
    .footer-links a.footer-more { font-weight: 750; color: var(--brand); }
    .footer-bottom { border-top: 1px solid var(--line); padding-top: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; font-size: 13px; color: #94a3b8; }
    .footer-bottom-links { display: flex; gap: 18px; flex-wrap: wrap; }
    .footer-bottom-links a { color: #64748b; transition: color .2s; }
    .footer-bottom-links a:hover { color: var(--brand); }

    @media (max-width: 900px) {
      .links { display: none; }
      .menu { display: block; }
      .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
      .doc-card { padding: 28px 20px; }
    }
    @media (max-width: 600px) {
      .footer-grid { grid-template-columns: 1fr; }
      .footer-bottom { flex-direction: column; text-align: center; }
      .footer-bottom-links { justify-content: center; }
    }"""

def build_about():
    os.makedirs("about", exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About Angsumi — Digital Infrastructure &amp; Web Engineering for Northeast India</title>
  <meta name="description" content="Discover Angsumi — building ultra-fast, affordable websites, clinic OPD management portals, school systems, and custom apps for businesses across Northeast India without agency markups.">
  <link rel="canonical" href="{BASE_URL}/about/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/about/">
  <meta property="og:title" content="About Angsumi — Engineering Digital Infrastructure for Northeast India">
  <meta property="og:description" content="Discover our mission to build fast, affordable, high-converting websites and management portals with 100% code ownership.">
  <meta property="og:image" content="{BASE_URL}/logo.png">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "AboutPage",
    "name": "About Angsumi",
    "url": "{BASE_URL}/about/",
    "description": "Angsumi engineers ultra-fast, affordable websites, clinic OPD management systems, school portals, and custom apps for businesses across Northeast India.",
    "publisher": {{
      "@type": "Organization",
      "name": "Angsumi",
      "url": "{BASE_URL}/",
      "logo": "{BASE_URL}/logo.png"
    }}
  }}
  </script>

  <style>
{BASE_CSS}
    .about-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 48px; }}
    .highlight-card {{
      background: #ffffff; border: 1px solid var(--line); border-radius: var(--radius);
      padding: 32px; box-shadow: var(--shadow); position: sticky; top: 100px;
    }}
    .highlight-card h3 {{ font-size: 18px; font-weight: 800; color: var(--ink); margin-bottom: 14px; }}
    .stat-list {{ display: flex; flex-direction: column; gap: 16px; margin: 20px 0; }}
    .stat-item {{ border-left: 3px solid var(--brand); padding-left: 14px; }}
    .stat-number {{ font-size: 22px; font-weight: 900; color: var(--brand); }}
    .stat-label {{ font-size: 13px; color: var(--muted); }}
    @media (max-width: 900px) {{
      .about-grid {{ grid-template-columns: 1fr; }}
      .highlight-card {{ position: static; }}
    }}
  </style>
</head>
<body>

{NAV_HTML}

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="/">Home</a> <span>/</span>
      <strong>About Angsumi</strong>
    </div>
  </div>

  <section class="page-hero">
    <div class="container">
      <div class="badge">🚀 Mission &amp; Engineering</div>
      <h1>Building Practical Digital Systems for Northeast India</h1>
      <p class="hero-sub">
        Eliminating agency bloat, slow WordPress templates, and recurring SaaS subscriptions with hand-crafted, high-converting digital infrastructure.
      </p>
    </div>
  </section>

  <section class="content-section">
    <div class="container about-grid">
      <div class="article-body">
        <h2>Who We Are</h2>
        <p>
          Angsumi is an independent software and digital systems engineering lab founded in Assam, dedicated to powering businesses, doctors, schools, handloom artisans, and local enterprises across Northeast India and beyond.
        </p>
        <p>
          In an era where traditional agencies charge ₹25,000–₹50,000 to configure slow, generic WordPress templates that take 6+ seconds to load on mobile 4G networks, Angsumi was founded on a simple premise: <strong>Software should be blistering fast, transparently priced, and owned 100% by the client.</strong>
        </p>

        <h2>Our Core Engineering Philosophy</h2>
        <ul>
          <li><strong>Hand-Coded Semantic Precision:</strong> We write clean, high-performance HTML, CSS, and modern JavaScript. No 30+ unvetted plugins, no SQL database bloat, and zero hidden security vulnerabilities.</li>
          <li><strong>Sub-Second Loading Speeds:</strong> Every system we deploy scores 100% on Google Core Web Vitals and loads in under 1 second on mobile networks across Assam, Meghalaya, Tripura, Nagaland, and Arunachal Pradesh.</li>
          <li><strong>100% Code &amp; Domain Ownership:</strong> We believe in empowering clients, not trapping them in monthly subscription lock-ins. You own your code, your assets, and your database forever.</li>
          <li><strong>Specialized Industry Workflows:</strong> Rather than generic "brochure" websites, we engineer actionable systems: OPD token counters for private clinics, online fee payment funnels for coaching institutes, and direct WhatsApp commerce engines for Northeast weavers.</li>
        </ul>

        <h2>Transparent Pricing Without Hostage Fees</h2>
        <p>
          Traditional SaaS platforms (Shopify, Wix, Squarespace) drain small businesses with monthly subscriptions of ₹2,000–₹4,000, plus transaction fee surcharges and plugin add-ons that add up to over ₹1,00,000 over two years.
        </p>
        <p>
          At Angsumi, starter platforms start from <strong>₹2,000 fixed price</strong>, and multi-page business web portals start from <strong>₹5,000</strong>. Once built, you pay zero monthly platform fees.
        </p>

        <h2>Direct Northeast Developer Collaboration</h2>
        <p>
          When you work with Angsumi, you communicate directly with the engineer building your system. No account managers, no ticket delays, and no miscommunications.
        </p>
        <p>
          <strong>Email:</strong> <a href="mailto:{EMAIL}" style="color:var(--brand); font-weight:700;">{EMAIL}</a><br>
          <strong>WhatsApp Consultation:</strong> <a href="https://wa.me/917896595109" target="_blank" rel="noopener" style="color:var(--brand); font-weight:700;">{PHONE_DISPLAY}</a>
        </p>
      </div>

      <div>
        <div class="highlight-card">
          <h3>The Angsumi Standard</h3>
          <div class="stat-list">
            <div class="stat-item">
              <div class="stat-number">&lt; 1.0s</div>
              <div class="stat-label">Mobile Page Load Speed</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">100%</div>
              <div class="stat-label">Client Code &amp; Domain Ownership</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">₹2,000</div>
              <div class="stat-label">Transparent Starting Price</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">8 States</div>
              <div class="stat-label">Northeast India &amp; Gateway Coverage</div>
            </div>
          </div>
          <a class="nav-cta" style="width:100%; justify-content:center;" href="/tools/cost-calculator/">
            Estimate Your Project &rarr;
          </a>
        </div>
      </div>
    </div>
  </section>

{FOOTER_HTML}
</body>
</html>"""
    with open("about/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Generated /about/index.html")

def build_privacy():
    os.makedirs("privacy-policy", exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy — Angsumi</title>
  <meta name="description" content="Angsumi Privacy Policy — how we protect your personal information, handle inquiries securely, and uphold data privacy across our web services.">
  <link rel="canonical" href="{BASE_URL}/privacy-policy/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/privacy-policy/">
  <meta property="og:title" content="Privacy Policy — Angsumi">
  <meta property="og:description" content="Learn about our commitment to your privacy, data security, and transparent communication.">
  <meta property="og:image" content="{BASE_URL}/logo.png">

  <style>
{BASE_CSS}
  </style>
</head>
<body>

{NAV_HTML}

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="/">Home</a> <span>/</span>
      <strong>Privacy Policy</strong>
    </div>
  </div>

  <section class="page-hero">
    <div class="container">
      <div class="badge">🔒 Trust &amp; Transparency</div>
      <h1>Privacy Policy</h1>
      <p class="hero-sub">
        Last updated: March 2026. Your privacy and data sovereignty are fundamental to how we build software.
      </p>
    </div>
  </section>

  <section class="content-section">
    <div class="container">
      <div class="doc-card article-body">
        <h2>1. Introduction</h2>
        <p>
          Angsumi ("we," "us," or "our") operates <strong>https://angsumi.online</strong> and associated digital systems. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website, use our interactive tools, or submit project inquiry forms.
        </p>

        <h2>2. Information We Collect</h2>
        <p>We collect information you provide directly to us when submitting inquiries or using our services:</p>
        <ul>
          <li><strong>Contact Details:</strong> Name, email address, phone/WhatsApp number provided in contact forms.</li>
          <li><strong>Project Requirements:</strong> Business type, budget range, and platform feature requests submitted via our inquiry form or cost calculator.</li>
          <li><strong>Technical Data:</strong> Anonymized browser type, operating system, and performance metrics collected solely to monitor Core Web Vitals and site availability.</li>
        </ul>

        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information strictly for legitimate business purposes:</p>
        <ul>
          <li>To respond to your project inquiries and provide tailored technical blueprints and cost estimates.</li>
          <li>To deliver software engineering, website development, and app deployment services.</li>
          <li>To operate, maintain, and optimize our website speed and security.</li>
          <li>To protect against fraudulent inquiries or malicious security attempts.</li>
        </ul>

        <h2>4. Zero Selling of Personal Data</h2>
        <p>
          <strong>We never sell, rent, trade, or monetize your personal information to third parties, data brokers, or advertising networks.</strong> Your contact details are used solely to communicate directly with you regarding your projects.
        </p>

        <h2>5. Cookies &amp; Analytics</h2>
        <p>
          Our website uses minimal, privacy-respecting cookies necessary for core website functionality (such as remembering user selections on interactive calculators). If Google Analytics or Google AdSense is enabled, standard anonymized cookies may be used by Google in accordance with Google's Privacy &amp; Terms.
        </p>

        <h2>6. Third-Party Services &amp; Form Processing</h2>
        <p>
          We use secure third-party processors such as Formspree for handling inquiry form transmissions over encrypted SSL/TLS connections. These providers process data strictly on our instructions and maintain industry-standard security protocols.
        </p>

        <h2>7. Data Security &amp; Retention</h2>
        <p>
          We implement industry-grade technical and organizational security measures to protect your personal information against unauthorized access, loss, or alteration. We retain inquiry information only as long as necessary to fulfill project requirements or comply with legal obligations.
        </p>

        <h2>8. Your Rights (DPDP Act &amp; GDPR)</h2>
        <p>
          In accordance with the Indian Digital Personal Data Protection (DPDP) Act and global privacy standards, you have the right to request access to, correction of, or permanent deletion of your personal data stored with us at any time.
        </p>

        <h2>9. Contact Us</h2>
        <p>
          If you have any questions or concerns regarding this Privacy Policy, please reach out to us at:
        </p>
        <p>
          <strong>Email:</strong> <a href="mailto:{EMAIL}" style="color:var(--brand); font-weight:700;">{EMAIL}</a><br>
          <strong>WhatsApp:</strong> <a href="https://wa.me/917896595109" target="_blank" rel="noopener" style="color:var(--brand); font-weight:700;">{PHONE_DISPLAY}</a>
        </p>
      </div>
    </div>
  </section>

{FOOTER_HTML}
</body>
</html>"""
    with open("privacy-policy/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Generated /privacy-policy/index.html")

def build_terms():
    os.makedirs("terms", exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Terms of Service &amp; Client Ownership Guarantee — Angsumi</title>
  <meta name="description" content="Angsumi Terms of Service — clear project milestones, 100% source code ownership guarantee, transparent pricing, and client rights.">
  <link rel="canonical" href="{BASE_URL}/terms/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/terms/">
  <meta property="og:title" content="Terms of Service &amp; Client Ownership Guarantee — Angsumi">
  <meta property="og:description" content="Transparent pricing terms, 100% code ownership guarantee, and project delivery commitments.">
  <meta property="og:image" content="{BASE_URL}/logo.png">

  <style>
{BASE_CSS}
  </style>
</head>
<body>

{NAV_HTML}

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="/">Home</a> <span>/</span>
      <strong>Terms of Service</strong>
    </div>
  </div>

  <section class="page-hero">
    <div class="container">
      <div class="badge">⚖ Fair &amp; Transparent Terms</div>
      <h1>Terms of Service</h1>
      <p class="hero-sub">
        Clear agreements, transparent fixed pricing, and an ironclad 100% client code ownership guarantee.
      </p>
    </div>
  </section>

  <section class="content-section">
    <div class="container">
      <div class="doc-card article-body">
        <h2>1. Overview &amp; Agreement</h2>
        <p>
          These Terms of Service ("Terms") govern your access to and use of services provided by Angsumi ("Developer," "we," "us"). By commissioning a project, using our web tools, or engaging our digital services, you agree to these Terms.
        </p>

        <h2>2. 100% Client Code &amp; Asset Ownership Guarantee</h2>
        <p>
          Unlike traditional software agencies and SaaS platforms that hold websites hostage under recurring monthly fees, <strong>Angsumi guarantees 100% intellectual property and code ownership to the client upon full project settlement</strong>.
        </p>
        <ul>
          <li>You own all custom HTML, CSS, JavaScript, database schemas, and media assets developed for your system.</li>
          <li>You own your registered domain name and cloud hosting accounts.</li>
          <li>You are free to modify, transfer, or migrate your website to any server or developer without restrictions.</li>
        </ul>

        <h2>3. Transparent Pricing &amp; Milestone Payments</h2>
        <p>
          We believe in complete pricing transparency without unexpected agency surcharges:
        </p>
        <ul>
          <li><strong>Fixed Scope Quotes:</strong> Every proposal clearly defines deliverables, features, and agreed one-time costs.</li>
          <li><strong>Milestone Structure:</strong> Projects generally follow a standard milestone schedule (e.g., 50% upfront to initiate development, 50% upon client preview approval and live deployment).</li>
          <li><strong>Zero Platform Hostage Fees:</strong> You will never be billed recurring monthly fees for code maintenance unless you specifically request an ongoing dedicated retainer.</li>
        </ul>

        <h2>4. Client Responsibilities</h2>
        <p>
          To ensure rapid sub-second delivery (typically 3–5 days for starter sites), clients agree to provide necessary business content (logos, service descriptions, menu items, or fee structures) and review milestone previews in a timely manner.
        </p>

        <h2>5. Warranty &amp; Launch Support</h2>
        <p>
          Every web system and application engineered by Angsumi comes with a <strong>30-day post-launch warranty</strong> covering bug fixes, responsive adjustments, domain DNS routing, and SSL certificate verification at zero additional cost.
        </p>

        <h2>6. Limitation of Liability</h2>
        <p>
          While we engineer all platforms to the highest standards of speed, security, and Core Web Vitals optimization, Angsumi shall not be held liable for third-party hosting outages, domain registrar disputes, or third-party payment gateway downtime outside our direct technical control.
        </p>

        <h2>7. Contact Information</h2>
        <p>
          For contract inquiries or questions regarding project agreements:
        </p>
        <p>
          <strong>Email:</strong> <a href="mailto:{EMAIL}" style="color:var(--brand); font-weight:700;">{EMAIL}</a><br>
          <strong>WhatsApp:</strong> <a href="https://wa.me/917896595109" target="_blank" rel="noopener" style="color:var(--brand); font-weight:700;">{PHONE_DISPLAY}</a>
        </p>
      </div>
    </div>
  </section>

{FOOTER_HTML}
</body>
</html>"""
    with open("terms/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Generated /terms/index.html")

def build_404():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 — Page Not Found | Angsumi</title>
  <meta name="robots" content="noindex, follow">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">

  <style>
{BASE_CSS}
    .error-wrap {{
      min-height: 55vh; display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center; padding: 80px 20px;
    }}
    .error-code {{ font-size: clamp(72px, 12vw, 120px); font-weight: 950; color: var(--brand); line-height: 1; letter-spacing: -.05em; }}
    .error-title {{ font-size: 26px; font-weight: 850; color: var(--ink); margin: 16px 0 10px; }}
    .error-desc {{ font-size: 16px; color: var(--muted); max-width: 520px; margin-bottom: 28px; }}
    .quick-links {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; margin-top: 10px; }}
    .quick-link {{
      background: #fff; border: 1px solid var(--line); padding: 8px 16px; border-radius: 999px;
      font-size: 13.5px; font-weight: 700; color: var(--ink); transition: all .2s;
    }}
    .quick-link:hover {{ background: var(--soft); border-color: #b0ccff; color: var(--brand); }}
  </style>
</head>
<body>

{NAV_HTML}

  <main class="error-wrap">
    <div class="error-code">404</div>
    <h1 class="error-title">Page Not Found</h1>
    <p class="error-desc">
      The page or resource you are looking for has moved or no longer exists. Explore our high-speed digital services and tools below:
    </p>

    <div style="display:flex; gap:12px; margin-bottom:24px; flex-wrap:wrap; justify-content:center;">
      <a class="nav-cta" href="/">← Return to Homepage</a>
      <a class="nav-cta" style="background:var(--brand);" href="/tools/cost-calculator/">Launch Cost Estimator →</a>
    </div>

    <div class="quick-links">
      <a class="quick-link" href="{BASE_URL}/services/">Digital Systems Directory</a>
      <a class="quick-link" href="{BASE_URL}/locations/">Northeast Locations</a>
      <a class="quick-link" href="{BASE_URL}/tools/">Interactive Tools</a>
      <a class="quick-link" href="https://blog.angsumi.online" target="_blank" rel="noopener">Official Blog</a>
    </div>
  </main>

{FOOTER_HTML}
</body>
</html>"""
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Generated /404.html")

def build_tech_detector():
    os.makedirs("tools/tech-detector", exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Website Speed, Bloat &amp; CMS Cost Audit Tool — Angsumi Tools</title>
  <meta name="description" content="Audit any website tech stack, calculate CMS plugin bloat vs custom code speed savings, and estimate annual savings from eliminating SaaS monthly fees. Free instant tool.">
  <link rel="canonical" href="{BASE_URL}/tools/tech-detector/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/tools/tech-detector/">
  <meta property="og:title" content="Website Speed, Bloat &amp; Cost Audit Tool — Angsumi">
  <meta property="og:description" content="Calculate plugin bloat, mobile 4G latency, and 2-year cost savings by switching from Wix/Shopify/WordPress to custom code.">
  <meta property="og:image" content="{BASE_URL}/logo.png">

  <!-- Schema Markup -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebApplication",
        "name": "Angsumi Website Speed & Bloat Audit Tool",
        "url": "{BASE_URL}/tools/tech-detector/",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "All",
        "description": "Interactive calculator and audit tool to analyze website platform bloat, mobile speed impact, and 2-year SaaS cost savings.",
        "offers": {{
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "INR"
        }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "Why are WordPress, Wix, and Shopify websites slow on mobile in Northeast India?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "WordPress sites often load 30+ unvetted plugins, heavy SQL queries, and megabytes of unused CSS/JS. Platforms like Wix inject hundreds of third-party tracking scripts that cause high latency on mobile 4G networks in Northeast India."
            }}
          }},
          {{
            "@type": "Question",
            "name": "How much money can a small business save by switching to custom code?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "By switching from SaaS subscriptions (Wix/Shopify) to clean custom code with zero recurring fees, businesses typically save between ₹60,000 and ₹1,20,000 over 2 years."
            }}
          }},
          {{
            "@type": "Question",
            "name": "What is considered a good Core Web Vitals score?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "A Largest Contentful Paint (LCP) under 1.2 seconds, Interaction to Next Paint (INP) under 100ms, and Cumulative Layout Shift (CLS) of 0 is considered excellent for top Google rankings."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
{BASE_CSS}
    .tool-box {{
      background: #ffffff; border: 1px solid var(--line); border-radius: var(--radius);
      padding: 36px; box-shadow: var(--shadow); margin-bottom: 48px;
    }}
    .audit-form-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .form-group {{ display: flex; flex-direction: column; gap: 8px; }}
    .form-group label {{ font-size: 14px; font-weight: 750; color: var(--ink); }}
    .form-group select, .form-group input {{
      padding: 13px 16px; border: 1px solid var(--line); border-radius: 12px;
      font-size: 14.5px; background: #fff; outline: none; transition: border-color .2s;
    }}
    .form-group select:focus, .form-group input:focus {{ border-color: var(--brand); }}
    
    .results-card {{
      background: linear-gradient(145deg, #0b1220 0%, #111d2e 100%); color: #fff;
      border-radius: var(--radius); padding: 32px; border: 1px solid #1e2d45;
      display: flex; flex-direction: column; justify-content: space-between;
    }}
    .res-metric {{ margin-bottom: 18px; }}
    .res-metric .val {{ font-size: 32px; font-weight: 900; color: #38bdf8; line-height: 1.1; }}
    .res-metric .label {{ font-size: 13px; color: #94a3b8; margin-top: 4px; }}
    .res-badge {{
      display: inline-block; padding: 4px 10px; border-radius: 999px;
      font-size: 12px; font-weight: 800; text-transform: uppercase; margin-bottom: 12px;
    }}

    .guide-article {{ max-width: 860px; margin: auto; }}
    .guide-article h2 {{ font-size: 26px; font-weight: 850; color: var(--ink); margin: 44px 0 16px; letter-spacing: -.03em; }}
    .guide-article h2:first-of-type {{ margin-top: 0; }}
    .guide-article h3 {{ font-size: 19px; font-weight: 800; color: var(--ink); margin: 28px 0 12px; }}
    .guide-article p {{ font-size: 16px; line-height: 1.75; color: #334155; margin-bottom: 18px; }}
    .guide-article ul, .guide-article ol {{ margin: 0 0 24px 24px; font-size: 16px; color: #334155; line-height: 1.75; }}
    .guide-article li {{ margin-bottom: 10px; }}

    .compare-table-wrap {{
      overflow-x: auto; background: #fff; border: 1px solid var(--line); border-radius: 16px; margin: 28px 0;
    }}
    .compare-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14.5px; }}
    .compare-table th {{ background: #f8fafc; padding: 14px 18px; border-bottom: 2px solid var(--line); font-weight: 800; color: var(--ink); }}
    .compare-table td {{ padding: 14px 18px; border-bottom: 1px solid var(--line); color: #334155; }}
    .compare-table tr:last-child td {{ border-bottom: 0; }}

    @media (max-width: 850px) {{
      .audit-form-grid {{ grid-template-columns: 1fr; }}
      .tool-box {{ padding: 24px 18px; }}
    }}
  </style>
</head>
<body>

{NAV_HTML}

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="/">Home</a> <span>/</span>
      <a href="/tools/">Tools</a> <span>/</span>
      <strong>Speed &amp; Tech Audit Tool</strong>
    </div>
  </div>

  <section class="page-hero">
    <div class="container">
      <div class="badge">⚡ Free Interactive Audit Tool</div>
      <h1>Website Speed, Plugin Bloat &amp; SaaS Cost Inspector</h1>
      <p class="hero-sub">
        Analyze how heavy WordPress plugins or monthly SaaS platforms (Wix, Shopify) impact your mobile load speed in Northeast India and calculate 2-year cost savings with custom code.
      </p>
    </div>
  </section>

  <section class="content-section">
    <div class="container">
      <!-- Interactive Tool UI -->
      <div class="tool-box">
        <h2 style="font-size:22px; font-weight:850; color:var(--ink); margin-bottom:20px;">Configure Your Audit Simulator</h2>
        <div class="audit-form-grid">
          <div style="display:flex; flex-direction:column; gap:16px;">
            <div class="form-group">
              <label for="platform-select">Current Platform or Tech Stack:</label>
              <select id="platform-select" onchange="calculateAudit()">
                <option value="wordpress">WordPress (Typical 25+ Plugins Setup)</option>
                <option value="wix">Wix / Squarespace (Drag-and-Drop Builder)</option>
                <option value="shopify">Shopify Store (With Essential App Add-ons)</option>
                <option value="custom_agency">Heavy Agency Custom Theme (Webpack / Next.js)</option>
                <option value="angsumi_static">Angsumi Clean Static Code (Sub-Second)</option>
              </select>
            </div>

            <div class="form-group">
              <label for="traffic-monthly">Monthly Visitors (Estimated):</label>
              <select id="traffic-monthly" onchange="calculateAudit()">
                <option value="1000">1,000 Visitors / month (Local Business / Clinic)</option>
                <option value="5000">5,000 Visitors / month (School / Active Store)</option>
                <option value="20000">20,000+ Visitors / month (Growing E-Commerce)</option>
              </select>
            </div>

            <div class="form-group">
              <label for="plugins-count">Active Plugins / 3rd-Party Scripts:</label>
              <input type="range" id="plugins-count" min="0" max="40" value="22" oninput="calculateAudit()" style="accent-color:var(--brand); cursor:pointer;">
              <span id="plugins-display" style="font-size:13px; color:var(--muted); font-weight:700;">22 active plugins / tracking scripts</span>
            </div>
          </div>

          <div class="results-card">
            <div>
              <div id="res-badge" class="res-badge" style="background:#ef4444; color:#fff;">Heavy Bloat Detected</div>
              <div class="res-metric">
                <div class="val" id="res-loadtime">4.8s</div>
                <div class="label">Estimated Mobile 4G Load Time</div>
              </div>
              <div class="res-metric">
                <div class="val" id="res-weight">2.4 MB</div>
                <div class="label">Initial Asset Payload Size</div>
              </div>
              <div class="res-metric">
                <div class="val" id="res-cost">₹72,000</div>
                <div class="label">Estimated 2-Year Platform Cost / Overheads</div>
              </div>
            </div>

            <div style="border-top:1px solid #23344d; padding-top:16px; margin-top:10px;">
              <a href="https://wa.me/917896595109?text=Hi%20Angsumi%2C%20I%20tested%20my%20website%20speed%20on%20your%20audit%20tool." target="_blank" rel="noopener" class="nav-cta" style="background:#10b981; color:#022c22; width:100%; justify-content:center;">
                <span>💬 Fix My Speed with Angsumi</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- 600+ Word SEO Guide -->
      <article class="guide-article">
        <h2>Why Website Speed Matters for Google Search Rankings in 2026</h2>
        <p>
          Google's search ranking algorithm prioritizes user experience above all else. With Google's <strong>Core Web Vitals</strong> (Largest Contentful Paint, Interaction to Next Paint, and Cumulative Layout Shift), websites that take longer than 2.5 seconds to load are penalized in organic search results and pushed down the rankings.
        </p>
        <p>
          In Northeast India (Assam, Meghalaya, Tripura, Nagaland, Arunachal Pradesh, Mizoram, and Manipur), a vast majority of website visitors access the internet via mobile 4G and 5G networks. If your clinic, school, homestay, or online store takes 5 to 7 seconds to load heavy JavaScript bundles, over <strong>53% of potential customers will bounce</strong> before even seeing your phone number or services.
        </p>

        <h2>The Hidden Cost of WordPress Plugin Bloat</h2>
        <p>
          Most traditional web design agencies in Guwahati, Silchar, and Dibrugarh download pre-made WordPress themes and stack 25 to 40 plugins to add basic features: contact forms, sliders, WhatsApp buttons, caching, and SEO plugins.
        </p>
        <p>
          Every plugin adds external stylesheets, database queries, and blocking scripts. The result is a slow website that consumes excessive mobile data and requires constant security updates to prevent SQL injection vulnerabilities.
        </p>

        <h2>Platform Comparison: Custom Code vs. WordPress vs. SaaS Builders</h2>
        <div class="compare-table-wrap">
          <table class="compare-table">
            <thead>
              <tr>
                <th>Factor</th>
                <th>Angsumi Custom Code</th>
                <th>WordPress Agency</th>
                <th>Shopify / Wix</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Mobile Page Speed</strong></td>
                <td><span style="color:#059669; font-weight:800;">Sub-Second (&lt;0.8s)</span></td>
                <td>4.5s – 7.0s (Slow)</td>
                <td>3.5s – 5.5s (Heavy)</td>
              </tr>
              <tr>
                <td><strong>Core Web Vitals Score</strong></td>
                <td><span style="color:#059669; font-weight:800;">100 / 100</span></td>
                <td>45 – 70 / 100</td>
                <td>60 – 80 / 100</td>
              </tr>
              <tr>
                <td><strong>2-Year Total Outflow</strong></td>
                <td><span style="color:#059669; font-weight:800;">₹2,000 – ₹8,500 (One-Time)</span></td>
                <td>₹25,000 – ₹50,000+</td>
                <td>₹84,000 – ₹1,20,000+</td>
              </tr>
              <tr>
                <td><strong>Code &amp; Asset Ownership</strong></td>
                <td><span style="color:#059669; font-weight:800;">100% Client Owned</span></td>
                <td>GPL Template</td>
                <td>0% (Locked into SaaS)</td>
              </tr>
              <tr>
                <td><strong>Security &amp; Maintenance</strong></td>
                <td>Zero Database / Zero Hacks</td>
                <td>Frequent Plugin Vulnerabilities</td>
                <td>Proprietary Closed System</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>How Angsumi Achieves Sub-Second Page Speeds</h2>
        <p>
          At Angsumi, we write clean, hand-coded semantic HTML5, pure CSS3, and lightweight vanilla JavaScript. We utilize global Cloudflare Edge caching so your website assets are served from the nearest server location to your customer in milliseconds.
        </p>
        <p>
          By eliminating server-side database bottlenecks and unnecessary third-party libraries, your website loads instantly, delivers effortless mobile navigation, and achieves top positions on Google search for your target keywords.
        </p>

        <h2>Ready to Upgrade Your Website Performance?</h2>
        <p>
          Whether you need a new high-speed website from scratch or want to migrate your slow existing WordPress/Wix site to clean, high-converting code, we provide free performance audits and instant transparent quotes.
        </p>
        <div style="display:flex; gap:14px; margin-top:24px; flex-wrap:wrap;">
          <a class="nav-cta" style="background:var(--brand);" href="/tools/cost-calculator/">Calculate Project Cost →</a>
          <a class="nav-cta" href="https://wa.me/917896595109" target="_blank" rel="noopener">Consult on WhatsApp →</a>
        </div>
      </article>
    </div>
  </section>

{FOOTER_HTML}

  <script>
    function calculateAudit() {{
      const platform = document.getElementById('platform-select').value;
      const traffic = parseInt(document.getElementById('traffic-monthly').value);
      const plugins = parseInt(document.getElementById('plugins-count').value);
      document.getElementById('plugins-display').innerText = plugins + " active plugins / tracking scripts";

      let loadTime = 0.6;
      let weight = 0.15;
      let cost = 0;
      let badgeText = "Ultra Fast";
      let badgeBg = "#10b981";

      if (platform === 'wordpress') {{
        loadTime = 2.0 + (plugins * 0.12);
        weight = 1.0 + (plugins * 0.08);
        cost = 35000 + (traffic > 10000 ? 15000 : 5000);
        badgeText = plugins > 15 ? "Heavy Plugin Bloat" : "Moderate Speed";
        badgeBg = plugins > 15 ? "#ef4444" : "#f59e0b";
      }} else if (platform === 'wix') {{
        loadTime = 3.2 + (plugins * 0.08);
        weight = 2.8 + (plugins * 0.05);
        cost = 68000;
        badgeText = "SaaS Monthly Subscription Bloat";
        badgeBg = "#ef4444";
      }} else if (platform === 'shopify') {{
        loadTime = 2.8 + (plugins * 0.1);
        weight = 2.5 + (plugins * 0.06);
        cost = 96000;
        badgeText = "High Recurring Subscription Cost";
        badgeBg = "#ef4444";
      }} else if (platform === 'custom_agency') {{
        loadTime = 1.8 + (plugins * 0.05);
        weight = 1.4 + (plugins * 0.04);
        cost = 55000;
        badgeText = "Complex Agency Overhead";
        badgeBg = "#f59e0b";
      }} else {{
        loadTime = 0.6 + (plugins * 0.02);
        weight = 0.18 + (plugins * 0.01);
        cost = 5000;
        badgeText = "100% Core Web Vitals Optimized";
        badgeBg = "#10b981";
      }}

      document.getElementById('res-loadtime').innerText = loadTime.toFixed(1) + "s";
      document.getElementById('res-weight').innerText = weight.toFixed(2) + " MB";
      document.getElementById('res-cost').innerText = "₹" + cost.toLocaleString('en-IN');
      const badgeEl = document.getElementById('res-badge');
      badgeEl.innerText = badgeText;
      badgeEl.style.background = badgeBg;
    }}

    calculateAudit();
  </script>
</body>
</html>"""
    with open("tools/tech-detector/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Generated /tools/tech-detector/index.html")

if __name__ == "__main__":
    build_about()
    build_privacy()
    build_terms()
    build_404()
    build_tech_detector()
