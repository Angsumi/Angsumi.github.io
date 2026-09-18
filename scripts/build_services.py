#!/usr/bin/env python3
import os
import json
from datetime import datetime

BASE_URL = "https://angsumi.online"
PHONE = "+917896595109"
PHONE_DISPLAY = "+91 78965 95109"
EMAIL = "angudas62@gmail.com"
TODAY = datetime.now().strftime("%Y-%m-%d")

with open("scripts/locations.json", "r", encoding="utf-8") as f:
    LOCATIONS_DATA = json.load(f)

with open("scripts/services.json", "r", encoding="utf-8") as f:
    SERVICES_DATA = json.load(f)

with open("scripts/style.css", "r", encoding="utf-8") as f:
    CSS_STYLES = f.read()

def get_other_services_pills(current_id=None):
    return "".join([
        f'<a href="{BASE_URL}/services/{s["service_id"]}/" class="city-pill{" active" if s["service_id"] == current_id else ""}">⚡ {s["short_title"]}</a>\n'
        for s in SERVICES_DATA
    ])

def get_assam_cities_pills():
    assam = next((s for s in LOCATIONS_DATA if s["state_id"] == "assam"), None)
    if not assam:
        return ""
    return "".join([
        f'<a href="{BASE_URL}/locations/assam/{c["city_id"]}/" class="city-pill">📍 {c["city_name"]}</a>\n'
        for c in assam["cities"]
    ])

def get_states_pills():
    return "".join([
        f'<a href="{BASE_URL}/locations/{s["state_id"]}/" class="city-pill">🌲 {s["state_name"]}</a>\n'
        for s in LOCATIONS_DATA
    ])

def get_service_html(s):
    service_id = s["service_id"]
    h1 = s["h1"]
    tagline = s["tagline"]
    desc = s["description"]
    short = s["short_title"]
    icon = s["icon"]
    badge = s["hero_badge"]
    canonical_url = f"{BASE_URL}/services/{service_id}/"
    page_title = f"{h1} — Angsumi"
    page_desc = f"{desc[:150]}... Transparent pricing from {s['starter_price']}."
    wa_msg = f"Hi Angsumi, I am looking for a {short} system for my business."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"

    features_html = "".join([
        f'<div class="ind-card"><div><div class="ind-icon">{icon}</div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>'
        for f in s["key_features"]
    ])

    steps_html = "".join([
        f'<div class="addon-item" style="padding:14px 18px; font-size:14px; color:#e2e8f0;"><span style="color:#38bdf8; font-weight:850; font-size:16px;">⚡</span> {step}</div>\n'
        for step in s["workflow_steps"]
    ])

    faq_schema = []
    faqs_html = ""
    for i, faq in enumerate(s["faqs"]):
        is_open = " open" if i == 0 else ""
        faqs_html += f'<details class="faq-card"{is_open}><summary>{faq["q"]}</summary><p>{faq["a"]}</p></details>\n'
        faq_schema.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })

    demo_btn = ""
    if "case_study_link" in s and s["case_study_link"]:
        demo_btn = f'<a class="secondary-btn" href="{BASE_URL}{s["case_study_link"]}" target="_blank"><span>Explore Live Case Study &rarr;</span></a>'

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{canonical_url}#service",
                "name": s["service_title"],
                "url": canonical_url,
                "provider": {
                    "@type": "ProfessionalService",
                    "name": "Angsumi",
                    "url": BASE_URL,
                    "telephone": PHONE,
                    "email": EMAIL
                },
                "areaServed": [
                    { "@type": "State", "name": "Assam" },
                    { "@type": "Country", "name": "India" }
                ],
                "description": desc,
                "offers": {
                    "@type": "Offer",
                    "price": s["starter_price"].replace("₹", "").replace(",", ""),
                    "priceCurrency": "INR"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/" },
                    { "@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE_URL}/services/" },
                    { "@type": "ListItem", "position": 3, "name": short, "item": canonical_url }
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": faq_schema
            }
        ]
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <meta name="keywords" content="{short.lower()} assam, {short.lower()} guwahati, {service_id.replace('-', ' ')} northeast india, top web developer assam">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{page_desc}">
  <meta name="twitter:image" content="{BASE_URL}/logo.png">
  <script type="application/ld+json">
{json.dumps(schema, indent=2)}
  </script>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>
  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="{BASE_URL}/">
        <div class="logo-mark"><img src="{BASE_URL}/logo.png" alt="Angsumi Logo"></div>
        <span>Angsumi</span>
      </a>
      <nav class="links">
        <a href="{BASE_URL}/#vp">What We Do</a>
        <a href="{BASE_URL}/#proof">Live Systems</a>
        <a href="{BASE_URL}/services/">Services</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
        <a href="{BASE_URL}/learning/">Learning Hub</a>
      </nav>
      <a class="nav-cta" href="{wa_url}" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
    </div>
  </header>

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <a href="{BASE_URL}/services/">Services</a> <span>/</span>
      <strong>{short}</strong>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> {icon} {badge}
        </div>
        <h1>{h1}</h1>
        <p class="hero-sub" style="font-weight:700; color:var(--ink); font-size:20px; margin-bottom:12px;">
          {tagline}
        </p>
        <p class="hero-sub" style="margin-top:0;">
          {desc}
        </p>
        <div class="actions">
          <a class="primary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Get Instant Quote on WhatsApp</span> &rarr;
          </a>
          {demo_btn}
        </div>
        <div class="trust-badges">
          <span>⚡ 100% Mobile &amp; 4G Ready</span>
          <span>💰 Zero Monthly SaaS Commissions</span>
          <span>🔒 Google Maps Local SEO Included</span>
          <span>🤝 Direct Northeast Developer</span>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-badge">Key Capabilities</div>
        <div class="section-head">
          <h2>Engineered Specifically for Real Daily Operations</h2>
          <p>Here is what makes our {short.lower()} far superior to slow, generic website templates:</p>
        </div>
        <div class="industry-grid">
          {features_html}
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="calc-section" style="background: linear-gradient(145deg, #0b1220 0%, #111e33 100%);">
          <div class="calc-header">
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">End-to-End Workflow</div>
            <h2 style="color:#fff;">How the System Works in 4 Steps</h2>
            <p style="color:#94a3b8;">Designed to make life effortlessly simple for both your customers and your staff.</p>
          </div>
          <div style="display:grid; gap:14px; margin-top:24px;">
            {steps_html}
          </div>
          <div style="margin-top:32px; text-align:center;">
            <a class="calc-btn" href="{wa_url}" target="_blank" rel="noopener" style="max-width:380px; margin:auto;">
              <span>💬 Test Live Preview on WhatsApp</span> &rarr;
            </a>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-badge">Guaranteed Transparent Pricing</div>
        <div class="section-head">
          <h2>Fixed Pricing with Zero Hidden Charges</h2>
          <p>No monthly SaaS commissions. No recurring licensing fees. You own 100% of your system.</p>
        </div>
        <div class="pricing-grid">
          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Starter Tier</div>
              <h3>Starter System</h3>
              <div class="price-amt">{s["starter_price"]}</div>
              <p style="font-size:13px; color:var(--muted)">Essential setup for individual professionals and single-location setups.</p>
              <ul class="price-features">
                <li>High-Speed Mobile Landing Page</li>
                <li>WhatsApp Instant Lead &amp; Booking Pipeline</li>
                <li>Google Maps Location Schema</li>
                <li>Delivery in 3-5 Business Days</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Starter%20Tier%20for%20{short.replace(' ', '%20')}." target="_blank" rel="noopener">Choose Starter Tier</a>
          </div>

          <div class="price-card" style="border: 2px solid var(--brand); box-shadow: 0 10px 30px rgba(18,87,214,0.1);">
            <div class="popular-tag">Most Recommended</div>
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Business Tier</div>
              <h3>Full Digital Platform</h3>
              <div class="price-amt">{s["business_price"]}</div>
              <p style="font-size:13px; color:var(--muted)">Complete operational portal with automated workflows, forms &amp; CMS.</p>
              <ul class="price-features">
                <li>Complete Multi-Page Management Portal</li>
                <li>UPI Online Payment Integration</li>
                <li>Automated WhatsApp / Email Alerts</li>
                <li>Search Engine Optimization for Assam &amp; NE</li>
                <li>Delivery in 7-10 Days</li>
              </ul>
            </div>
            <a class="primary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Business%20Tier%20for%20{short.replace(' ', '%20')}." target="_blank" rel="noopener">Choose Business Tier</a>
          </div>

          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Enterprise Tier</div>
              <h3>Custom ERP / Mobile App</h3>
              <div class="price-amt">{s["custom_price"]}</div>
              <p style="font-size:13px; color:var(--muted)">Multi-branch institutions, custom mobile apps, and dedicated databases.</p>
              <ul class="price-features">
                <li>Android &amp; iOS Native Flutter Mobile App</li>
                <li>Multi-Branch / Multi-User Staff Roles</li>
                <li>Custom Cloud Database &amp; Automated Backups</li>
                <li>Priority 24/7 Technical SLA Support</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20to%20discuss%20Custom%20Enterprise%20for%20{short.replace(' ', '%20')}." target="_blank" rel="noopener">Discuss Enterprise</a>
          </div>
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="section-badge">Frequently Asked Questions</div>
        <div class="section-head" style="text-align:center; margin-left:auto; margin-right:auto;">
          <h2>{short} FAQ</h2>
          <p>Common questions about technical setup, delivery timelines, and ongoing support.</p>
        </div>
        <div class="faq-grid">
          {faqs_html}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="cta-box">
          <div class="cta-left">
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">Get Started Today</div>
            <h2>Let's Build Your {short}</h2>
            <p>Tell us about your organization. We will respond with an honest quote and a live working prototype within hours.</p>
            <div class="cta-chips">
              <a class="cta-chip wa" href="{wa_url}" target="_blank" rel="noopener">
                <span>💬 WhatsApp Direct:</span> <strong>{PHONE_DISPLAY}</strong>
              </a>
              <a class="cta-chip" href="mailto:{EMAIL}">
                <span>✉ Email Directly:</span> <strong>{EMAIL}</strong>
              </a>
            </div>
          </div>
          <form class="lead-form" action="https://formspree.io/f/xwlegzkn" method="POST">
            <input type="hidden" name="_subject" value="New Inquiry for {short} ({service_id})">
            <input type="hidden" name="_next" value="{canonical_url}">
            <input type="hidden" name="service_id" value="{service_id}">
            <input type="hidden" name="service_title" value="{short}">
            <div class="form-row">
              <input required name="name" placeholder="Your Name">
              <input required name="phone" type="tel" placeholder="Phone / WhatsApp Number">
            </div>
            <input required name="email" type="email" placeholder="Your Email Address">
            <select required name="location_district">
              <option value="">Your District or Town in Assam / Northeast</option>
              <option>Guwahati / Kamrup</option>
              <option>Dibrugarh / Tinsukia</option>
              <option>Silchar / Cachar</option>
              <option>Jorhat / Golaghat / Sivasagar</option>
              <option>Tezpur / Sonitpur</option>
              <option>Nagaon / Morigaon</option>
              <option>Bongaigaon / Barpeta / Nalbari</option>
              <option>Other Assam District</option>
              <option>Other Northeast State (Meghalaya, Tripura, etc.)</option>
            </select>
            <select required name="tier_preference">
              <option value="">Select Package Tier</option>
              <option>Starter System ({s["starter_price"]})</option>
              <option>Full Business Platform ({s["business_price"]})</option>
              <option>Custom Mobile App / ERP ({s["custom_price"]})</option>
              <option>Need Advice / Free Proposal First</option>
            </select>
            <textarea required name="project_details" placeholder="Briefly describe your requirements, current workflow, or questions..."></textarea>
            <button class="submit-btn" type="submit">
              <span>Send System Inquiry</span> &rarr;
            </button>
          </form>
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line);">
      <div class="container">
        <div class="interlink-box">
          <h3 style="font-size:18px; font-weight:850; margin-bottom:6px;">Available Across All 25 Districts in Assam</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">We deploy {short.lower()} with on-ground local SEO across all commercial hubs in Assam:</p>
          <div class="city-pill-grid">
            {get_assam_cities_pills()}
          </div>
          <h3 style="font-size:18px; font-weight:850; margin-top:28px; margin-bottom:6px;">Other Specialized Digital Systems</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">Explore our other turnkey digital platforms for Northeast businesses:</p>
          <div class="city-pill-grid">
            {get_other_services_pills(service_id)}
          </div>
          <h3 style="font-size:18px; font-weight:850; margin-top:28px; margin-bottom:6px;">All Northeast India States</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">We deliver high-speed web and app engineering throughout all Northeast states:</p>
          <div class="city-pill-grid">
            {get_states_pills()}
          </div>
        </div>
      </div>
    </section>
  </main>

  <a class="mobile-sticky-wa" href="{wa_url}" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Top Website &amp; Mobile App Designer serving Assam and Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="{wa_url}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a> · 
        © 2026 Angsumi
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
  </script>
</body>
</html>'''

def get_services_hub_html():
    canonical_url = f"{BASE_URL}/services/"
    page_title = "Specialized Website & Digital System Services in Assam — Angsumi"
    page_desc = "Custom digital systems tailored for Assam & Northeast India: Doctor OPD booking, school portals, online mock test platforms, homestay direct booking, WhatsApp stores, and mobile apps. No recurring SaaS fees."
    wa_msg = "Hi Angsumi, I want to explore your specialized digital systems and services."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"

    services_grid_html = ""
    for s in SERVICES_DATA:
        services_grid_html += f'''
        <div class="proof-card" style="padding: 30px;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
              <span style="font-size:36px;">{s["icon"]}</span>
              <span class="proof-badge">{s["hero_badge"]}</span>
            </div>
            <h3 style="font-size:22px; font-weight:850; margin-bottom:8px;">{s["short_title"]}</h3>
            <p style="font-size:14px; color:var(--muted); line-height:1.55;">{s["tagline"]}</p>
            <div style="margin: 18px 0; padding: 12px 16px; background: var(--bg); border: 1px solid var(--line); border-radius: 12px; font-size: 13.5px; font-weight: 750; color: var(--brand);">
              Starting from {s["starter_price"]} (Zero Monthly SaaS Fees)
            </div>
          </div>
          <a class="primary-btn" style="width:100%; justify-content:center; margin-top:12px;" href="{BASE_URL}/services/{s["service_id"]}/">Explore System &amp; Live Demo &rarr;</a>
        </div>
        '''

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "@id": f"{canonical_url}#service",
                "name": "Angsumi — Specialized Web & Digital Systems",
                "url": canonical_url,
                "logo": f"{BASE_URL}/logo.png",
                "image": f"{BASE_URL}/logo.png",
                "description": "Specialized website design, mobile apps, and digital platforms for doctors, schools, homestays, e-commerce, and enterprises across Assam and Northeast India.",
                "telephone": PHONE,
                "email": EMAIL,
                "priceRange": "₹2000 - ₹35000",
                "currenciesAccepted": "INR"
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/" },
                    { "@type": "ListItem", "position": 2, "name": "Services", "item": canonical_url }
                ]
            }
        ]
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <meta name="keywords" content="doctor website design assam, school management system guwahati, online exam portal northeast, homestay booking website shillong, ecommerce website assam, mobile app development northeast india">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">
  <script type="application/ld+json">
{json.dumps(schema, indent=2)}
  </script>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>
  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="{BASE_URL}/">
        <div class="logo-mark"><img src="{BASE_URL}/logo.png" alt="Angsumi Logo"></div>
        <span>Angsumi</span>
      </a>
      <nav class="links">
        <a href="{BASE_URL}/#vp">What We Do</a>
        <a href="{BASE_URL}/#proof">Live Systems</a>
        <a href="{BASE_URL}/services/">Services</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
        <a href="{BASE_URL}/learning/">Learning Hub</a>
      </nav>
      <a class="nav-cta" href="{wa_url}" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
    </div>
  </header>

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <strong>Specialized Services</strong>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> ⚡ Specialized Digital Infrastructure · Assam &amp; Northeast India
        </div>
        <h1>High-Impact Digital Systems Built for Real Business Growth</h1>
        <p class="hero-sub">
          We don't build generic cookie-cutter templates. We engineer tailored web portals, automated WhatsApp funnels, and native mobile apps designed specifically for Northeast India's clinics, schools, homestays, and local enterprises — with zero monthly SaaS commissions.
        </p>
        <div class="actions">
          <a class="primary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Discuss Your System on WhatsApp</span> &rarr;
          </a>
          <a class="secondary-btn" href="{BASE_URL}/locations/">
            <span>🗺️ Explore Regional Coverage</span>
          </a>
        </div>
        <div class="trust-badges">
          <span>⚡ Sub-Second Load Speeds</span>
          <span>🔒 100% Code Ownership</span>
          <span>💰 Zero Monthly Hostage Fees</span>
          <span>📱 Mobile &amp; 4G Optimized</span>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-badge">Service Solutions</div>
        <div class="section-head">
          <h2>Choose Your Industry Solution</h2>
          <p>Every system includes responsive mobile design, local Google SEO setup, WhatsApp integration, and direct senior engineer support.</p>
        </div>
        <div class="products-grid">
          {services_grid_html}
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="cta-box">
          <div class="cta-left">
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">Get Started Today</div>
            <h2>Let's Engineer Your Digital Platform</h2>
            <p>Tell us what your institution or business needs. We will prepare a tailored blueprint and live preview within hours.</p>
            <div class="cta-chips">
              <a class="cta-chip wa" href="{wa_url}" target="_blank" rel="noopener">
                <span>💬 WhatsApp Us:</span> <strong>{PHONE_DISPLAY}</strong>
              </a>
              <a class="cta-chip" href="mailto:{EMAIL}">
                <span>✉ Email Directly:</span> <strong>{EMAIL}</strong>
              </a>
            </div>
          </div>
          <form class="lead-form" action="https://formspree.io/f/xwlegzkn" method="POST">
            <input type="hidden" name="_subject" value="New Service Inquiry from Services Hub">
            <input type="hidden" name="_next" value="{canonical_url}">
            <div class="form-row">
              <input required name="name" placeholder="Your Name">
              <input required name="phone" type="tel" placeholder="Phone / WhatsApp Number">
            </div>
            <input required name="email" type="email" placeholder="Your Email Address">
            <select required name="service_required">
              <option value="">Select Specialized System</option>
              <option>Doctor &amp; Clinic OPD System</option>
              <option>School &amp; Coaching Management Portal</option>
              <option>Online Mock Exam Portal</option>
              <option>Hotel &amp; Homestay Direct Booking</option>
              <option>High-Speed E-Commerce Store</option>
              <option>Cross-Platform Mobile App (Android / iOS)</option>
              <option>Contractor / Corporate Profile Website</option>
              <option>WhatsApp Store &amp; Catalog System</option>
              <option>Restaurant QR Menu System</option>
            </select>
            <textarea required name="project_details" placeholder="Tell us about your business requirements and timeline..."></textarea>
            <button class="submit-btn" type="submit">
              <span>Request Free System Blueprint</span> &rarr;
            </button>
          </form>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="interlink-box">
          <h3 style="font-size:18px; font-weight:850; margin-bottom:6px;">Serving All Key Districts Across Assam</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">Our digital solutions are actively deployed across all 25 major commercial hubs in Assam:</p>
          <div class="city-pill-grid">
            {get_assam_cities_pills()}
          </div>
          <h3 style="font-size:18px; font-weight:850; margin-top:28px; margin-bottom:6px;">All Northeast India States &amp; Gateways</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">We also engineer custom web and mobile systems for clients throughout Northeast India:</p>
          <div class="city-pill-grid">
            {get_states_pills()}
          </div>
        </div>
      </div>
    </section>
  </main>

  <a class="mobile-sticky-wa" href="{wa_url}" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Specialized Digital Systems &amp; Web Development for Assam &amp; Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="{wa_url}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a> · 
        © 2026 Angsumi
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
  </script>
</body>
</html>'''

def build_services():
    os.makedirs("services", exist_ok=True)
    with open("services/index.html", "w", encoding="utf-8") as f:
        f.write(get_services_hub_html())
    print("✓ Generated /services/index.html")

    urls = [("https://angsumi.online/services/", "weekly", "0.95")]

    for s in SERVICES_DATA:
        s_dir = os.path.join("services", s["service_id"])
        os.makedirs(s_dir, exist_ok=True)
        with open(os.path.join(s_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(get_service_html(s))
        print(f"  ✓ Generated /services/{s['service_id']}/index.html")
        urls.append((f"https://angsumi.online/services/{s['service_id']}/", "weekly", "0.90"))

    return urls

if __name__ == "__main__":
    build_services()
