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

# Select high-priority commercial hubs for matrix generation
PRIORITY_CITY_IDS = {
    # Assam
    "guwahati", "dibrugarh", "silchar", "jorhat", "tezpur", "nagaon", 
    "tinsukia", "bongaigaon", "barpeta", "nalbari", "sivasagar", "golaghat",
    # Northeast State Hubs & Gateways
    "shillong", "agartala", "dimapur", "kohima", "itanagar", "siliguri"
}

def get_matrix_page_html(state, city, service):
    city_name = city["city_name"]
    state_name = state["state_name"]
    city_id = city["city_id"]
    state_id = state["state_id"]
    service_id = service["service_id"]
    short_title = service["short_title"]
    service_h1 = service["h1"].replace("in Assam", f"in {city_name}, {state_name}").replace("in Northeast India", f"in {city_name}")
    tagline = service["tagline"]
    desc = service["description"]
    icon = service["icon"]
    badge = service["hero_badge"]
    starter_price = service["starter_price"]
    business_price = service["business_price"]
    custom_price = service["custom_price"]

    canonical_url = f"{BASE_URL}/locations/{state_id}/{city_id}/{service_id}/"
    page_title = f"{short_title} in {city_name}, {state_name} — Angsumi"
    page_desc = f"Top-rated {short_title.lower()} development in {city_name}, {state_name}. {tagline}. Fixed pricing from {starter_price} with zero monthly SaaS fees."

    wa_msg = f"Hi Angsumi, I am looking for {short_title} in {city_name}, {state_name}."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"

    # Features
    features_html = "".join([
        f'<div class="ind-card"><div><div class="ind-icon">{icon}</div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>'
        for f in service["key_features"]
    ])

    # Steps
    steps_html = "".join([
        f'<div class="addon-item" style="padding:14px 18px; font-size:14px; color:#e2e8f0;"><span style="color:#38bdf8; font-weight:850; font-size:16px;">⚡</span> {step}</div>\n'
        for step in service["workflow_steps"]
    ])

    # FAQs customized for city
    faq_schema = []
    faqs_html = ""
    for i, faq in enumerate(service["faqs"]):
        q = faq["q"].replace("in Assam", f"in {city_name}").replace("Assam", city_name)
        a = faq["a"].replace("in Assam", f"in {city_name}").replace("across Assam", f"across {city_name} and {state_name}")
        is_open = " open" if i == 0 else ""
        faqs_html += f'<details class="faq-card"{is_open}><summary>{q}</summary><p>{a}</p></details>\n'
        faq_schema.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": { "@type": "Answer", "text": a }
        })

    # Sister services in this city
    other_services_in_city_html = "".join([
        f'<a href="{BASE_URL}/locations/{state_id}/{city_id}/{s["service_id"]}/" class="city-pill{" active" if s["service_id"] == service_id else ""}">⚡ {s["short_title"]}</a>\n'
        for s in SERVICES_DATA
    ])

    # Sister cities for this service
    other_cities_for_service_html = "".join([
        f'<a href="{BASE_URL}/locations/{s["state_id"]}/{c["city_id"]}/{service_id}/" class="city-pill{" active" if c["city_id"] == city_id else ""}">📍 {c["city_name"]}</a>\n'
        for s in LOCATIONS_DATA for c in s["cities"] if c["city_id"] in PRIORITY_CITY_IDS
    ])

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{canonical_url}#service",
                "name": f"{short_title} in {city_name}",
                "url": canonical_url,
                "provider": {
                    "@type": "ProfessionalService",
                    "name": "Angsumi",
                    "url": BASE_URL,
                    "telephone": PHONE,
                    "email": EMAIL
                },
                "areaServed": {
                    "@type": "City",
                    "name": city_name,
                    "containedInPlace": { "@type": "State", "name": state_name }
                },
                "description": f"Professional {short_title.lower()} development engineered for businesses in {city_name}, {state_name}.",
                "offers": {
                    "@type": "Offer",
                    "price": starter_price.replace("₹", "").replace(",", ""),
                    "priceCurrency": "INR"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/" },
                    { "@type": "ListItem", "position": 2, "name": "Locations", "item": f"{BASE_URL}/locations/" },
                    { "@type": "ListItem", "position": 3, "name": state_name, "item": f"{BASE_URL}/locations/{state_id}/" },
                    { "@type": "ListItem", "position": 4, "name": city_name, "item": f"{BASE_URL}/locations/{state_id}/{city_id}/" },
                    { "@type": "ListItem", "position": 5, "name": short_title, "item": canonical_url }
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
  <meta name="keywords" content="{short_title.lower()} {city_name}, {service_id.replace('-', ' ')} {city_name}, website designer {city_name}, app developer {city_name} {state_name}">
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
        <a href="{BASE_URL}/tools/">Tools</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="{BASE_URL}/blog/">Insights</a>
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
      <a href="{BASE_URL}/locations/">Locations</a> <span>/</span>
      <a href="{BASE_URL}/locations/{state_id}/">{state_name}</a> <span>/</span>
      <a href="{BASE_URL}/locations/{state_id}/{city_id}/">{city_name}</a> <span>/</span>
      <strong>{short_title}</strong>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> {icon} {badge} · {city_name}, {state_name}
        </div>
        <h1>{service_h1}</h1>
        <p class="hero-sub" style="font-weight:700; color:var(--ink); font-size:20px; margin-bottom:12px;">
          {tagline}
        </p>
        <p class="hero-sub" style="margin-top:0;">
          {city["market_desc"]} Angsumi engineers custom {short_title.lower()} tailored for institutions and commercial operators in {city_name} with zero monthly SaaS commissions and direct senior engineer support.
        </p>
        <div class="actions">
          <a class="primary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Get Instant Quote for {city_name}</span> &rarr;
          </a>
          <a class="secondary-btn" href="{BASE_URL}/locations/{state_id}/{city_id}/">
            <span>📍 Explore All {city_name} Packages</span>
          </a>
        </div>
        <div class="trust-badges">
          <span>⚡ Sub-Second Mobile 4G Speed</span>
          <span>💰 Fixed Honest Pricing from {starter_price}</span>
          <span>🔒 Google Maps Local SEO Included</span>
          <span>🤝 Direct Northeast Developer</span>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-badge">Platform Capabilities</div>
        <div class="section-head">
          <h2>Engineered for Daily Operations in {city_name}</h2>
          <p>Here is what makes our custom {short_title.lower()} superior to expensive city agencies and slow WordPress templates:</p>
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
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">Operational Workflow</div>
            <h2 style="color:#fff;">How It Operates for Your {city_name} Business</h2>
            <p style="color:#94a3b8;">Streamlined for maximum conversions and zero technical headaches.</p>
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
        <div class="section-badge">Guaranteed Transparent Rates</div>
        <div class="section-head">
          <h2>Affordable {short_title} Pricing for {city_name}</h2>
          <p>No monthly retainer lock-ins. You own 100% of your source code, domain, and data.</p>
        </div>
        <div class="pricing-grid">
          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Starter Tier</div>
              <h3>Starter System</h3>
              <div class="price-amt">{starter_price}</div>
              <p style="font-size:13px; color:var(--muted)">Essential digital pipeline for single practitioners or local setups in {city_name}.</p>
              <ul class="price-features">
                <li>High-Speed Mobile Landing Page</li>
                <li>WhatsApp 1-Tap Booking &amp; Inquiries</li>
                <li>Google Maps Local SEO Schema</li>
                <li>Delivery in 3 to 5 Days</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Starter%20Tier%20for%20{short_title.replace(' ', '%20')}%20in%20{city_name}." target="_blank" rel="noopener">Choose Starter Tier</a>
          </div>

          <div class="price-card" style="border: 2px solid var(--brand); box-shadow: 0 10px 30px rgba(18,87,214,0.1);">
            <div class="popular-tag">Most Recommended</div>
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Business Tier</div>
              <h3>Full Digital Platform</h3>
              <div class="price-amt">{business_price}</div>
              <p style="font-size:13px; color:var(--muted)">Complete operational portal with automated workflows, forms &amp; CMS for {city_name}.</p>
              <ul class="price-features">
                <li>Complete Multi-Page Management Portal</li>
                <li>UPI Online Payment Integration</li>
                <li>Automated WhatsApp / Email Alerts</li>
                <li>Rank #1 Local Google SEO Setup</li>
                <li>Delivery in 7 to 10 Days</li>
              </ul>
            </div>
            <a class="primary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Business%20Tier%20for%20{short_title.replace(' ', '%20')}%20in%20{city_name}." target="_blank" rel="noopener">Choose Business Tier</a>
          </div>

          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Enterprise Tier</div>
              <h3>Custom ERP / Mobile App</h3>
              <div class="price-amt">{custom_price}</div>
              <p style="font-size:13px; color:var(--muted)">Multi-branch operations, native Flutter mobile app, and dedicated database.</p>
              <ul class="price-features">
                <li>Android &amp; iOS Native Flutter Mobile App</li>
                <li>Multi-User Staff &amp; Admin Roles</li>
                <li>Custom Cloud Database &amp; Auto Backups</li>
                <li>24/7 Priority SLA Technical Support</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20to%20discuss%20Custom%20Enterprise%20for%20{short_title.replace(' ', '%20')}%20in%20{city_name}." target="_blank" rel="noopener">Discuss Enterprise</a>
          </div>
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="section-badge">Frequently Asked Questions</div>
        <div class="section-head" style="text-align:center; margin-left:auto; margin-right:auto;">
          <h2>{short_title} in {city_name} FAQ</h2>
          <p>Everything you need to know about pricing, delivery, and ongoing maintenance.</p>
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
            <h2>Let's Build Your {short_title} in {city_name}</h2>
            <p>Tell us what your business needs. We will respond with an honest quote and a live working prototype within hours.</p>
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
            <input type="hidden" name="_subject" value="New Inquiry for {short_title} in {city_name} ({city_id})">
            <input type="hidden" name="_next" value="{canonical_url}">
            <input type="hidden" name="service_id" value="{service_id}">
            <input type="hidden" name="location_city" value="{city_name}">
            <input type="hidden" name="location_state" value="{state_name}">
            <div class="form-row">
              <input required name="name" placeholder="Your Name">
              <input required name="phone" type="tel" placeholder="Phone / WhatsApp Number">
            </div>
            <input required name="email" type="email" placeholder="Your Email Address">
            <select required name="tier_preference">
              <option value="">Select Package Tier</option>
              <option>Starter System ({starter_price})</option>
              <option>Full Business Platform ({business_price})</option>
              <option>Custom Mobile App / ERP ({custom_price})</option>
              <option>Need Advice / Free Proposal First</option>
            </select>
            <textarea required name="project_details" placeholder="Briefly describe your requirements or current workflow in {city_name}..."></textarea>
            <button class="submit-btn" type="submit">
              <span>Send Project Inquiry</span> &rarr;
            </button>
          </form>
        </div>
      </div>
    </section>

    <section style="background:#fff; border-top:1px solid var(--line);">
      <div class="container">
        <div class="interlink-box">
          <h3 style="font-size:18px; font-weight:850; margin-bottom:6px;">Other Specialized Digital Systems in {city_name}</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">Looking for other turnkey platforms in {city_name}?</p>
          <div class="city-pill-grid">
            {other_services_in_city_html}
          </div>
          <h3 style="font-size:18px; font-weight:850; margin-top:28px; margin-bottom:6px;">{short_title} in Other Northeast Hubs</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">We deploy {short_title.lower()} across all key commercial centers in Northeast India:</p>
          <div class="city-pill-grid">
            {other_cities_for_service_html}
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
        <strong style="color:var(--ink)">Angsumi</strong> — Top {short_title} Developer serving {city_name}, {state_name}, and Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="{wa_url}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
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

def build_matrix():
    matrix_urls = []
    generated_count = 0

    for state in LOCATIONS_DATA:
        for city in state["cities"]:
            if city["city_id"] in PRIORITY_CITY_IDS:
                for service in SERVICES_DATA:
                    target_dir = os.path.join("locations", state["state_id"], city["city_id"], service["service_id"])
                    os.makedirs(target_dir, exist_ok=True)

                    target_file = os.path.join(target_dir, "index.html")
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(get_matrix_page_html(state, city, service))

                    matrix_urls.append((f"{BASE_URL}/locations/{state['state_id']}/{city['city_id']}/{service['service_id']}/", "weekly", "0.80"))
                    generated_count += 1

    print(f"✓ Successfully generated {generated_count} Matrix pSEO Intersection Landing Pages.")
    return matrix_urls

if __name__ == "__main__":
    build_matrix()
