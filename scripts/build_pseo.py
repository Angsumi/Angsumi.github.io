#!/usr/bin/env python3
"""
Angsumi Programmatic SEO (pSEO) Site Generator
Re-generates all location landing pages and updates sitemap.xml.
Usage: python3 scripts/build_pseo.py
"""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://angsumi.online"
PHONE = "+917896595109"
PHONE_DISPLAY = "+91 78965 95109"
EMAIL = "angudas62@gmail.com"
TODAY = datetime.now().strftime("%Y-%m-%d")

with open("scripts/locations.json", "r", encoding="utf-8") as f:
    LOCATIONS_DATA = json.load(f)

with open("scripts/style.css", "r", encoding="utf-8") as f:
    CSS_STYLES = f.read()

def get_city_html(state, city):
    city_name = city["city_name"]
    state_name = state["state_name"]
    city_id = city["city_id"]
    state_id = state["state_id"]
    canonical_url = f"{BASE_URL}/locations/{state_id}/{city_id}/"
    page_title = f"Top Website and App Designer in {city_name}, {state_name} — Angsumi"
    page_desc = f"Looking for the best website & mobile app designer in {city_name}, {state_name}? Angsumi builds fast, affordable websites, clinic/school portals & custom apps from ₹2,000. 100% mobile-ready."
    
    wa_msg = f"Hi Angsumi, I am looking for a website / app developer in {city_name}, {state_name}."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "@id": f"{canonical_url}#service",
                "name": f"Angsumi — Website & App Designer in {city_name}",
                "url": canonical_url,
                "logo": f"{BASE_URL}/logo.png",
                "image": f"{BASE_URL}/logo.png",
                "description": f"Professional website design, mobile app development, and digital management systems for businesses, clinics, and schools in {city_name}, {state_name}.",
                "telephone": PHONE,
                "email": EMAIL,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": city_name,
                    "addressRegion": state_name,
                    "addressCountry": "IN"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": city["lat"],
                    "longitude": city["lng"]
                },
                "areaServed": [
                    { "@type": "City", "name": city_name },
                    { "@type": "State", "name": state_name },
                    { "@type": "Country", "name": "India" }
                ],
                "priceRange": "₹2000 - ₹35000",
                "currenciesAccepted": "INR",
                "paymentAccepted": "UPI, Bank Transfer, Card",
                "openingHours": "Mo-Su 08:00-21:00"
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": f"{BASE_URL}/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": state_name,
                        "item": f"{BASE_URL}/locations/{state_id}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": city_name,
                        "item": canonical_url
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How much does it cost to build a website in {city_name}, {state_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"At Angsumi, high-speed professional starter websites in {city_name} begin at just ₹2,000. Multi-page business web portals with CMS and Google Maps SEO start from ₹5,000, and custom mobile apps or clinic/school platforms start from ₹15,000."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"How long will it take to design and launch a website in {city_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Starter business websites in {city_name} are typically delivered in 2 to 4 business days. Custom portals and management platforms take 7 to 14 days with complete testing and domain configuration."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Can Angsumi build custom Android and iOS mobile apps for businesses in {city_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Yes. Angsumi builds cross-platform Flutter and Progressive Web Apps (PWAs) tailored for {city_name} businesses, including doctor appointment systems, school fee portals, and e-commerce apps with UPI integration."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Why choose Angsumi over an expensive agency in {city_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Traditional agencies in {city_name} often charge ₹25,000 to ₹50,000+ for slow, bloated WordPress templates with recurring monthly fees. Angsumi provides direct senior engineer communication, hand-coded lightweight architecture for sub-second speeds, zero lock-in, and local Northeast understanding."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Do you help with Google Maps and local SEO in {city_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Yes. Every website we build for clients in {city_name} includes local schema markup, Google Search Console indexing, and Google Business Profile optimization to help you rank at the top when local customers search for your services."
                        }
                    }
                ]
            }
        ]
    }

    sister_cities_html = "".join([
        f'<a href="{BASE_URL}/locations/{state_id}/{c["city_id"]}/" class="city-pill{" active" if c["city_id"] == city_id else ""}">📍 {c["city_name"]}</a>\n'
        for c in state["cities"]
    ])

    states_pill_html = "".join([
        f'<a href="{BASE_URL}/locations/{s["state_id"]}/" class="city-pill{" active" if s["state_id"] == state_id else ""}">🌲 {s["state_name"]}</a>\n'
        for s in LOCATIONS_DATA
    ])

    icons = ["🏥", "🎓", "🛍️", "💼", "🏨", "🚚"]
    sectors_html = ""
    for i, sec in enumerate(city["local_sectors"]):
        icon = icons[i % len(icons)]
        sectors_html += f"""
        <div class="ind-card">
          <div>
            <div class="ind-icon">{icon}</div>
            <h3>{sec}</h3>
            <p>Tailored digital workflow, online booking, lead capture, and payment integration engineered specifically for {sec.lower()} in {city_name}.</p>
          </div>
          <div class="ind-tag">Explore System →</div>
        </div>
        """

    challenges_html = "".join([
        f'<li><span style="color:#ef4444; font-weight:900;">✕</span> {ch}</li>\n'
        for ch in city["challenges"]
    ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary SEO -->
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <meta name="keywords" content="website designer in {city_name}, app developer {city_name}, web development {city_name} {state_name}, affordable web design {city_name}, mobile app development {city_name}, clinic website {city_name}, school management software {city_name}, top web developer Northeast India">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">

  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{page_desc}">
  <meta name="twitter:image" content="{BASE_URL}/logo.png">

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {json.dumps(schema, indent=2)}
  </script>

  <style>
  {CSS_STYLES}
  </style>
</head>
<body>

  <!-- Sticky Nav -->
  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="{BASE_URL}/">
        <div class="logo-mark"><img src="{BASE_URL}/logo.png" alt="Angsumi Logo"></div>
        <span>Angsumi</span>
      </a>
      <nav class="links">
        <a href="{BASE_URL}/#vp">What We Do</a>
        <a href="{BASE_URL}/#proof">Live Systems</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/blog/">Insights</a>
        <a href="{BASE_URL}/learning/">Learning Hub</a>
      </nav>
      <a class="nav-cta" href="{wa_url}" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> →
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">☰</button>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <a href="{BASE_URL}/locations/">Locations</a> <span>/</span>
      <a href="{BASE_URL}/locations/{state_id}/">{state_name}</a> <span>/</span>
      <strong>{city_name}</strong>
    </div>
  </div>

  <main>
    <!-- HERO -->
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 📍 Top Website &amp; App Designer in {city_name}, {state_name}
        </div>
        <h1>Top Website &amp; Mobile App Designer in {city_name}</h1>
        <p class="hero-sub">
          {city["market_desc"]} Angsumi builds ultra-fast, modern websites, clinic/school portals, and mobile apps designed to convert visitors into loyal paying customers — starting from just ₹2,000 with zero agency markup.
        </p>

        <div class="actions">
          <a class="primary-btn" href="#calculator">
            <span>Calculate Instant Project Cost</span> →
          </a>
          <a class="secondary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Chat on WhatsApp</span>
          </a>
        </div>

        <div class="trust-badges">
          <span>⚡ Sub-Second Load Speeds</span>
          <span>📱 100% Mobile &amp; 4G Optimized</span>
          <span>💰 Fixed Honest Pricing from ₹2,000</span>
          <span>🔒 Google Maps &amp; Local SEO Ready</span>
          <span>🤝 Direct Northeast Developer</span>
        </div>
      </div>
    </section>

    <!-- LOCAL MARKET INSIGHTS -->
    <section>
      <div class="container">
        <div class="section-badge">Local Market Analysis</div>
        <div class="section-head">
          <h2>Why Businesses in {city_name} Need Modern Digital Systems</h2>
          <p>The consumer market in {city_name} has moved completely mobile-first. Here is how our custom digital solutions solve the most pressing local business challenges.</p>
        </div>

        <div class="market-box">
          <div class="market-grid">
            <div class="challenge-card">
              <h4>Common Roadblocks in {city_name}</h4>
              <ul class="market-list">
                {challenges_html}
              </ul>
            </div>
            <div class="opp-card">
              <h4>The Angsumi Solution</h4>
              <ul class="market-list">
                <li><span style="color:#059669; font-weight:900;">✓</span> <strong>Hand-Coded Performance:</strong> Blazing fast load times even on spotty mobile networks across {state_name}.</li>
                <li><span style="color:#059669; font-weight:900;">✓</span> <strong>1-Tap WhatsApp Conversion:</strong> Direct customer booking and product inquiry pipelines straight into your pocket.</li>
                <li><span style="color:#059669; font-weight:900;">✓</span> <strong>Local SEO Dominance:</strong> Comprehensive schema markup so {city_name} customers find you at #1 on Google Maps.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- INDUSTRY VERTICALS -->
        <div class="section-head" style="margin-top: 50px;">
          <h2>Custom Solutions for {city_name}'s Key Industries</h2>
          <p>We tailor every website and digital application to the exact operational needs of your specific trade.</p>
        </div>

        <div class="industry-grid">
          {sectors_html}
        </div>
      </div>
    </section>

    <!-- INTERACTIVE ESTIMATOR WIDGET -->
    <section id="calculator">
      <div class="container">
        <div class="calc-section">
          <div class="calc-header">
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">Live Cost Estimator</div>
            <h2>Interactive Project Cost &amp; Timeline Calculator for {city_name}</h2>
            <p>Select your project requirements below to see instant transparent pricing with zero surprise charges.</p>
          </div>

          <div class="calc-grid">
            <div>
              <div class="calc-step">
                <label>1. Select Primary Platform</label>
                <div class="calc-options" id="platform-opts">
                  <div class="calc-opt active" data-base="2000" data-days="2-3" data-name="Starter Website">
                    <div>Starter Website</div>
                    <small style="color:#94a3b8; font-size:11px;">From ₹2,000</small>
                  </div>
                  <div class="calc-opt" data-base="5000" data-days="4-7" data-name="Business Portal">
                    <div>Business Web Portal</div>
                    <small style="color:#94a3b8; font-size:11px;">From ₹5,000</small>
                  </div>
                  <div class="calc-opt" data-base="15000" data-days="10-15" data-name="Mobile App / Custom System">
                    <div>Mobile App / System</div>
                    <small style="color:#94a3b8; font-size:11px;">From ₹15,000</small>
                  </div>
                </div>
              </div>

              <div class="calc-step">
                <label>2. Add Essential Features</label>
                <div class="addons-grid">
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="0" checked disabled>
                    <span>100% Mobile &amp; 4G Speed (Free)</span>
                  </label>
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="500" data-feature="Google Maps & Local SEO" checked>
                    <span>Google Maps &amp; Local SEO (+₹500)</span>
                  </label>
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="1000" data-feature="WhatsApp Ordering Bot">
                    <span>WhatsApp Ordering / Lead Bot (+₹1,000)</span>
                  </label>
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="1500" data-feature="Online Payments & UPI Gateway">
                    <span>UPI &amp; Online Payment Gateway (+₹1,500)</span>
                  </label>
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="2500" data-feature="Appointment / Booking System">
                    <span>Doctor/Service Booking System (+₹2,500)</span>
                  </label>
                  <label class="addon-item">
                    <input type="checkbox" class="addon-cb" data-price="3500" data-feature="Custom Admin & Billing Portal">
                    <span>Custom Admin / Billing Portal (+₹3,500)</span>
                  </label>
                </div>
              </div>
            </div>

            <div class="calc-summary">
              <div class="summary-title">Estimated Investment in {city_name}</div>
              <div class="calc-price" id="total-price">₹2,500</div>
              <div class="calc-time" id="delivery-time">Estimated Delivery: 2 to 4 Days</div>

              <div class="calc-breakdown" id="breakdown-list">
                <div><span>Platform:</span> <strong id="selected-platform">Starter Website</strong></div>
                <div><span>Included Addons:</span> <strong id="addons-count">1 Selected</strong></div>
                <div><span>Support:</span> <strong>Free Ongoing Maintenance</strong></div>
              </div>

              <a class="calc-btn" id="wa-calc-btn" href="{wa_url}" target="_blank" rel="noopener">
                <span>💬 Lock In Quote on WhatsApp</span> →
              </a>
              <small style="color:#64748b; font-size:11px; display:block; margin-top:10px;">
                No advance commitment required. We show you a live interactive preview first.
              </small>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- PROVEN TRACK RECORD / DEMOS -->
    <section>
      <div class="container">
        <div class="section-badge">Live Proof of Work</div>
        <div class="section-head">
          <h2>Battle-Tested Digital Platforms Built for Northeast India</h2>
          <p>We don't just talk about code — we engineer high-traffic production platforms that serve thousands of users daily.</p>
        </div>

        <div class="products-grid">
          <div class="proof-card">
            <div>
              <div class="proof-badge">Govt Exam Tech Platform</div>
              <h3>AxomRank / Learning Hub Platform</h3>
              <p>Full-fledged online examination, live timer, and state-wide rank predictor built for over 25,000+ candidates across Assam.</p>
            </div>
            <a class="proof-link" href="{BASE_URL}/learning/" target="_blank">View Live Platform →</a>
          </div>

          <div class="proof-card">
            <div>
              <div class="proof-badge">Interactive Vector Geography</div>
              <h3>Northeast India Interactive Portal</h3>
              <p>High-performance vector cartography platform rendering sub-district river systems, railway corridors, and topographic terrain.</p>
            </div>
            <a class="proof-link" href="{BASE_URL}/learning/geography/" target="_blank">View Live Interactive Map →</a>
          </div>

          <div class="proof-card">
            <div>
              <div class="proof-badge">Healthcare Management</div>
              <h3>Doctor &amp; Clinic Digital System</h3>
              <p>Modern OPD token generation, WhatsApp prescription delivery, and patient history ledger system for private clinics.</p>
            </div>
            <a class="proof-link" href="{BASE_URL}/blog/clinic-digital-system.html">View Case Study →</a>
          </div>

          <div class="proof-card">
            <div>
              <div class="proof-badge">Education Management</div>
              <h3>School &amp; Academy Digital Portal</h3>
              <p>Zero-maintenance parent portal, attendance tracking, online noticeboard, and report card generator without recurring SaaS fees.</p>
            </div>
            <a class="proof-link" href="{BASE_URL}/blog/school-web-design-assam.html">View Case Study →</a>
          </div>
        </div>
      </div>
    </section>

    <!-- TRANSPARENT PRICING -->
    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="section-badge">Guaranteed Transparent Pricing</div>
        <div class="section-head">
          <h2>Affordable Web &amp; App Packages for {city_name} Businesses</h2>
          <p>No hidden agency markups. No monthly hostage fees. You own 100% of your source code and domain.</p>
        </div>

        <div class="pricing-grid">
          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Starter Pack</div>
              <h3>Fast Business Website</h3>
              <div class="price-amt">₹2,000</div>
              <p style="font-size:13px; color:var(--muted)">Perfect for local stores, freelancers, and individual consultants in {city_name}.</p>
              <ul class="price-features">
                <li>High-Converting Landing Page</li>
                <li>100% Mobile &amp; Tablet Optimized</li>
                <li>WhatsApp 1-Tap Call &amp; Chat Button</li>
                <li>Google Maps Location Embed</li>
                <li>Delivery in 48-72 Hours</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Starter%20Package%20for%20{city_name}." target="_blank" rel="noopener">Get Starter Pack</a>
          </div>

          <div class="price-card" style="border: 2px solid var(--brand); box-shadow: 0 10px 30px rgba(18,87,214,0.1);">
            <div class="popular-tag">Most Popular</div>
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Business Pack</div>
              <h3>Full Web Portal + SEO</h3>
              <div class="price-amt">₹5,000</div>
              <p style="font-size:13px; color:var(--muted)">Ideal for clinics, schools, coaching institutes, and established companies in {city_name}.</p>
              <ul class="price-features">
                <li>Up to 5 Custom High-Speed Pages</li>
                <li>Local SEO &amp; Google Search Indexing</li>
                <li>Lead Inquiry &amp; Booking Forms</li>
                <li>Product Catalog / Service Showcase</li>
                <li>Free Domain &amp; SSL Assistance</li>
                <li>Delivery in 4-7 Days</li>
              </ul>
            </div>
            <a class="primary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Business%20Portal%20Package%20for%20{city_name}." target="_blank" rel="noopener">Get Business Portal</a>
          </div>

          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Custom System</div>
              <h3>Mobile App / Custom ERP</h3>
              <div class="price-amt">From ₹15,000</div>
              <p style="font-size:13px; color:var(--muted)">Tailored applications, e-commerce platforms, and internal management tools.</p>
              <ul class="price-features">
                <li>Cross-Platform Android &amp; iOS App</li>
                <li>Custom Admin Dashboard &amp; User Roles</li>
                <li>Automated Invoicing &amp; Payment Gateway</li>
                <li>Real-Time Database &amp; Cloud Storage</li>
                <li>Dedicated Technical Support</li>
              </ul>
            </div>
            <a class="secondary-btn" style="width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20to%20discuss%20a%20Custom%20App%20for%20{city_name}." target="_blank" rel="noopener">Discuss Custom App</a>
          </div>
        </div>
      </div>
    </section>

    <!-- COMPARISON TABLE -->
    <section>
      <div class="container">
        <div class="section-badge">Why Angsumi</div>
        <div class="section-head">
          <h2>How Angsumi Compares to Other Options in {city_name}</h2>
          <p>See why forward-thinking Northeast business owners choose our lean, high-speed engineering approach.</p>
        </div>

        <div class="compare-box">
          <table class="compare-table">
            <thead>
              <tr>
                <th>Feature / Benchmark</th>
                <th style="color:var(--brand); font-weight:900;">Angsumi</th>
                <th>Traditional City Agencies</th>
                <th>DIY Builders (Wix/Shopify)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Starting Price</strong></td>
                <td><strong style="color:#059669;">₹2,000 Fixed</strong></td>
                <td>₹25,000 – ₹60,000+</td>
                <td>₹1,500 – ₹3,000 every month forever</td>
              </tr>
              <tr>
                <td><strong>Page Load Speed (Mobile 4G)</strong></td>
                <td><strong style="color:#059669;">Sub-1.0s (100% Core Web Vitals)</strong></td>
                <td>4.5s – 8.0s (Heavy WordPress bloat)</td>
                <td>3.5s – 6.0s (Heavy JavaScript)</td>
              </tr>
              <tr>
                <td><strong>WhatsApp Integration</strong></td>
                <td><strong style="color:#059669;">Custom 1-Tap Smart Bots</strong></td>
                <td>Basic static plugin</td>
                <td>Requires paid monthly app store addons</td>
              </tr>
              <tr>
                <td><strong>Local Northeast India Context</strong></td>
                <td><strong style="color:#059669;">Deep local market knowledge</strong></td>
                <td>Outsourced to sub-vendors</td>
                <td>Generic global templates</td>
              </tr>
              <tr>
                <td><strong>Code Ownership</strong></td>
                <td><strong style="color:#059669;">100% You Own All Files</strong></td>
                <td>Often locked in agency retainer</td>
                <td>Locked inside their proprietary walled garden</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- LOCAL FAQ -->
    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="section-badge">Frequently Asked Questions</div>
        <div class="section-head" style="text-align:center; margin-left:auto; margin-right:auto;">
          <h2>Website &amp; App Development in {city_name} FAQ</h2>
          <p>Have questions before starting? Here are straightforward answers about our process, pricing, and timelines.</p>
        </div>

        <div class="faq-grid">
          <details class="faq-card" open>
            <summary>How much does it cost to build a website in {city_name}, {state_name}?</summary>
            <p>Our starter websites in {city_name} begin at just ₹2,000 with mobile optimization and Google Maps integration. Multi-page business portals start at ₹5,000, and full custom web/mobile applications start from ₹15,000. No monthly lock-in fees.</p>
          </details>

          <details class="faq-card">
            <summary>How long will it take to build and launch my website in {city_name}?</summary>
            <p>Starter single-page websites are typically delivered within 48 to 72 hours. Comprehensive business portals take 4 to 7 days, and custom mobile apps take 10 to 15 days.</p>
          </details>

          <details class="faq-card">
            <summary>Can you build mobile apps for Android and iOS in {city_name}?</summary>
            <p>Yes. We build responsive progressive web apps (PWAs) as well as native-performance cross-platform Flutter mobile apps that publish smoothly to Google Play and Apple App Store.</p>
          </details>

          <details class="faq-card">
            <summary>Will my website rank on Google in {city_name}?</summary>
            <p>Yes. Every website we build includes local schema markup, semantic headings, meta tags, and Google Search Console registration to help your business rank at the top when local {city_name} customers search for your services.</p>
          </details>

          <details class="faq-card">
            <summary>How do I start a project with Angsumi?</summary>
            <p>Simply message us on WhatsApp at +91 78965 95109 or fill out the quick inquiry form below. Tell us what your business does, and we will prepare a free live preview and fixed proposal within a few hours.</p>
          </details>
        </div>
      </div>
    </section>

    <!-- LEAD CAPTURE CONTACT FORM -->
    <section>
      <div class="container">
        <div class="cta-box" id="contact">
          <div class="cta-left">
            <div class="section-badge" style="background:#1e3a66; color:#38bdf8; border-color:#2a5087;">Get Started Today</div>
            <h2>Let's Build Your Digital System in {city_name}</h2>
            <p>Tell us what your business needs. We will respond with an honest estimate and a free live preview within hours.</p>

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
            <input type="hidden" name="_subject" value="New Inquiry from {city_name}, {state_name} ({city_id})">
            <input type="hidden" name="_next" value="{canonical_url}">
            <input type="hidden" name="location_city" value="{city_name}">
            <input type="hidden" name="location_state" value="{state_name}">

            <div class="form-row">
              <input required name="name" placeholder="Your Name">
              <input required name="phone" type="tel" placeholder="Phone / WhatsApp Number">
            </div>

            <input required name="email" type="email" placeholder="Your Email Address">

            <select required name="business_type">
              <option value="">What kind of business do you run in {city_name}?</option>
              <option>Doctor / Healthcare Clinic</option>
              <option>School / College / Coaching</option>
              <option>Retail Store / E-Commerce Brand</option>
              <option>Hotel / Homestay / Tourism</option>
              <option>Contractor / Logistics / B2B</option>
              <option>Other Enterprise</option>
            </select>

            <select required name="project_type">
              <option value="">Select Required Package</option>
              <option>Starter Website (₹2,000)</option>
              <option>Business Web Portal (₹5,000)</option>
              <option>Mobile App / Custom System (From ₹15,000)</option>
              <option>Need Advice / Free Proposal First</option>
            </select>

            <textarea required name="project_details" placeholder="Briefly describe what you'd like to build for your business in {city_name}..."></textarea>

            <button class="submit-btn" type="submit">
              <span>Send Project Inquiry</span> →
            </button>
          </form>
        </div>
      </div>
    </section>

    <!-- REGIONAL DIRECTORY & SISTER CITIES -->
    <section style="background:#fff; border-top:1px solid var(--line);">
      <div class="container">
        <div class="interlink-box">
          <h3 style="font-size:18px; font-weight:850; margin-bottom:6px;">Explore More Locations in {state_name}</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">Looking for digital services across other towns in {state_name}? Explore our localized hubs:</p>
          <div class="city-pill-grid">
            {sister_cities_html}
          </div>

          <h3 style="font-size:18px; font-weight:850; margin-top:28px; margin-bottom:6px;">All Northeast India States &amp; Gateways</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">We provide high-speed website and mobile app design across all 8 Northeast states plus West Bengal:</p>
          <div class="city-pill-grid">
            {states_pill_html}
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Sticky Mobile WhatsApp Button -->
  <a class="mobile-sticky-wa" href="{wa_url}" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Top Website and Mobile App Designer serving {city_name}, {state_name}, and all of Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="{wa_url}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
        © 2026 Angsumi
      </div>
    </div>
  </footer>

  <!-- Interactive Calculator JavaScript -->
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

    // Calculator Logic
    const platformOpts = document.querySelectorAll('#platform-opts .calc-opt');
    const addonCheckboxes = document.querySelectorAll('.addon-cb');
    const totalPriceEl = document.getElementById('total-price');
    const deliveryTimeEl = document.getElementById('delivery-time');
    const selectedPlatformEl = document.getElementById('selected-platform');
    const addonsCountEl = document.getElementById('addons-count');
    const waCalcBtn = document.getElementById('wa-calc-btn');

    let basePrice = 2000;
    let basePlatformName = 'Starter Website';
    let baseDays = '2-3';

    function recalculate() {{
      let total = basePrice;
      let selectedAddons = [];
      
      addonCheckboxes.forEach(cb => {{
        if (cb.checked) {{
          total += parseInt(cb.dataset.price || '0', 10);
          if (cb.dataset.feature) {{
            selectedAddons.push(cb.dataset.feature);
          }}
        }}
      }});

      totalPriceEl.textContent = '₹' + total.toLocaleString('en-IN');
      selectedPlatformEl.textContent = basePlatformName;
      addonsCountEl.textContent = selectedAddons.length + ' Selected';
      deliveryTimeEl.textContent = 'Estimated Delivery: ' + baseDays + ' Business Days';

      const waMsg = 'Hi Angsumi, I configured a custom project estimate for {city_name}:\\n' +
                    '• Platform: ' + basePlatformName + '\\n' +
                    '• Features: ' + (selectedAddons.join(', ') || 'Standard') + '\\n' +
                    '• Estimated Budget: ₹' + total.toLocaleString('en-IN') + '\\n' +
                    'Can we discuss and preview this?';
      waCalcBtn.href = 'https://wa.me/917896595109?text=' + encodeURIComponent(waMsg);
    }}

    platformOpts.forEach(opt => {{
      opt.addEventListener('click', () => {{
        platformOpts.forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
        basePrice = parseInt(opt.dataset.base, 10);
        basePlatformName = opt.dataset.name;
        baseDays = opt.dataset.days;
        recalculate();
      }});
    }});

    addonCheckboxes.forEach(cb => {{
      cb.addEventListener('change', recalculate);
    }});

    recalculate();
  </script>
</body>
</html>"""
    return html


def get_state_html(state):
    state_name = state["state_name"]
    state_id = state["state_id"]
    canonical_url = f"{BASE_URL}/locations/{state_id}/"
    page_title = f"Top Website and App Designer in {state_name} — Angsumi Digital"
    page_desc = f"Looking for the top website & app designer in {state_name}? Angsumi builds fast, affordable websites, clinic/school management portals & custom mobile apps across {state_name} from ₹2,000."
    
    wa_msg = f"Hi Angsumi, I am looking for a website / app developer in {state_name}."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"

    cities_html = "".join([
        f"""
        <div class="ind-card">
          <div>
            <div class="ind-icon">📍</div>
            <h3>{c["city_name"]}</h3>
            <p style="font-weight:700; color:var(--brand); font-size:12px; text-transform:uppercase; margin-bottom:6px;">{c["tagline"]}</p>
            <p>{c["market_desc"][:160]}...</p>
          </div>
          <a class="primary-btn" style="margin-top:16px; padding:8px 16px; font-size:13px;" href="{BASE_URL}/locations/{state_id}/{c["city_id"]}/">Explore {c["city_name"]} Hub →</a>
        </div>
        """
        for c in state["cities"]
    ])

    other_states_html = "".join([
        f'<a href="{BASE_URL}/locations/{s["state_id"]}/" class="city-pill{" active" if s["state_id"] == state_id else ""}">🌲 {s["state_name"]}</a>\n'
        for s in LOCATIONS_DATA
    ])

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "@id": f"{canonical_url}#service",
                "name": f"Angsumi — Website & App Designer in {state_name}",
                "url": canonical_url,
                "logo": f"{BASE_URL}/logo.png",
                "image": f"{BASE_URL}/logo.png",
                "description": f"Professional website design, mobile app development, and digital management systems for businesses, clinics, and schools across {state_name}.",
                "telephone": PHONE,
                "email": EMAIL,
                "address": {
                    "@type": "PostalAddress",
                    "addressRegion": state_name,
                    "addressCountry": "IN"
                },
                "areaServed": [
                    { "@type": "State", "name": state_name },
                    { "@type": "Country", "name": "India" }
                ],
                "priceRange": "₹2000 - ₹35000",
                "currenciesAccepted": "INR"
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": f"{BASE_URL}/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": state_name,
                        "item": canonical_url
                    }
                ]
            }
        ]
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary SEO -->
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <meta name="keywords" content="website designer {state_name}, app developer {state_name}, web design company {state_name}, affordable website {state_name}, software developer {state_name}, Northeast India web developer">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">

  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {json.dumps(schema, indent=2)}
  </script>

  <style>
  {CSS_STYLES}
  </style>
</head>
<body>

  <!-- Sticky Nav -->
  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="{BASE_URL}/">
        <div class="logo-mark"><img src="{BASE_URL}/logo.png" alt="Angsumi Logo"></div>
        <span>Angsumi</span>
      </a>
      <nav class="links">
        <a href="{BASE_URL}/#vp">What We Do</a>
        <a href="{BASE_URL}/#proof">Live Systems</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/blog/">Insights</a>
        <a href="{BASE_URL}/learning/">Learning Hub</a>
      </nav>
      <a class="nav-cta" href="{wa_url}" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> →
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">☰</button>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <a href="{BASE_URL}/locations/">Locations</a> <span>/</span>
      <strong>{state_name}</strong>
    </div>
  </div>

  <main>
    <!-- HERO -->
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 📍 State Web &amp; App Engineering Hub
        </div>
        <h1>Top Website &amp; Mobile App Designer in {state_name}</h1>
        <p class="hero-sub">
          {state["region_description"]} {state["state_focus"]} Angsumi builds fast, affordable, high-converting digital platforms for businesses, schools, and clinics across {state_name}.
        </p>

        <div class="actions">
          <a class="primary-btn" href="#cities">
            <span>Explore Commercial City Hubs</span> →
          </a>
          <a class="secondary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Chat on WhatsApp (+91 78965 95109)</span>
          </a>
        </div>

        <div class="trust-badges">
          <span>⚡ 100/100 Google Core Web Vitals</span>
          <span>📱 Mobile &amp; 4G Network Ready</span>
          <span>💰 Transparent Pricing from ₹2,000</span>
          <span>🤝 Direct Northeast Developer</span>
        </div>
      </div>
    </section>

    <!-- CITIES LIST -->
    <section id="cities">
      <div class="container">
        <div class="section-badge">Key Commercial Centers</div>
        <div class="section-head">
          <h2>Select Your City Hub in {state_name}</h2>
          <p>Choose your city below for localized pricing, industry solutions, and instant WhatsApp quote estimates.</p>
        </div>

        <div class="industry-grid">
          {cities_html}
        </div>
      </div>
    </section>

    <!-- PRICING TIERS -->
    <section style="background:#fff; border-top:1px solid var(--line); border-bottom:1px solid var(--line);">
      <div class="container">
        <div class="section-badge">Simple Fixed Pricing</div>
        <div class="section-head">
          <h2>Standard Digital Packages for {state_name}</h2>
          <p>Transparent pricing with no hidden costs or recurring agency hostage fees.</p>
        </div>

        <div class="pricing-grid">
          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Starter Pack</div>
              <h3>Fast Business Website</h3>
              <div class="price-amt">₹2,000</div>
              <p style="font-size:13px; color:var(--muted)">High-converting mobile landing page with WhatsApp button &amp; Google Maps.</p>
            </div>
            <a class="secondary-btn" style="margin-top:20px; width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Starter%20Package%20in%20{state_name}." target="_blank" rel="noopener">Get Starter Pack</a>
          </div>

          <div class="price-card" style="border: 2px solid var(--brand); box-shadow: 0 10px 30px rgba(18,87,214,0.1);">
            <div class="popular-tag">Popular</div>
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Business Pack</div>
              <h3>Full Web Portal + SEO</h3>
              <div class="price-amt">₹5,000</div>
              <p style="font-size:13px; color:var(--muted)">Multi-page website with local SEO, Google Search indexing, and lead inquiry system.</p>
            </div>
            <a class="primary-btn" style="margin-top:20px; width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20the%20Business%20Portal%20Package%20in%20{state_name}." target="_blank" rel="noopener">Get Business Portal</a>
          </div>

          <div class="price-card">
            <div>
              <div style="font-size:12px; font-weight:850; color:var(--brand); text-transform:uppercase;">Custom System</div>
              <h3>Mobile App / Custom ERP</h3>
              <div class="price-amt">From ₹15,000</div>
              <p style="font-size:13px; color:var(--muted)">Cross-platform Android/iOS app, doctor/school management portal &amp; payment gateway.</p>
            </div>
            <a class="secondary-btn" style="margin-top:20px; width:100%; justify-content:center;" href="{wa_url}&text=Hi%20Angsumi%2C%20I%20want%20to%20discuss%20a%20Custom%20App%20in%20{state_name}." target="_blank" rel="noopener">Discuss Custom App</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ALL STATES DIRECTORY -->
    <section>
      <div class="container">
        <div class="interlink-box">
          <h3 style="font-size:18px; font-weight:850; margin-bottom:6px;">All Northeast India States &amp; Gateways</h3>
          <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">Angsumi builds digital systems across all 8 Northeast states and gateway regions:</p>
          <div class="city-pill-grid">
            {other_states_html}
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Sticky Mobile WhatsApp Button -->
  <a class="mobile-sticky-wa" href="{wa_url}" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Top Website and Mobile App Designer serving {state_name} &amp; Northeast India.
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
</html>"""
    return html


def get_hub_html():
    canonical_url = f"{BASE_URL}/locations/"
    page_title = "Northeast India Website & App Design Directory — Angsumi"
    page_desc = "Directory of top website and mobile app design services across Northeast India — Assam, Meghalaya, Tripura, Manipur, Mizoram, Nagaland, Arunachal Pradesh, Sikkim & West Bengal."
    
    wa_msg = "Hi Angsumi, I am looking for a website / app developer in Northeast India."
    wa_url = f"https://wa.me/917896595109?text={wa_msg.replace(' ', '%20')}"

    state_sections_html = ""
    for state in LOCATIONS_DATA:
        city_links = "".join([
            f'<a class="city-pill" href="{BASE_URL}/locations/{state["state_id"]}/{c["city_id"]}/">📍 {c["city_name"]}</a> '
            for c in state["cities"]
        ])

        state_sections_html += f"""
        <div class="market-box" style="margin-bottom:24px;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <span class="section-badge" style="margin-bottom:6px;">{state["state_short"]}</span>
              <h3 style="font-size:24px; font-weight:850; letter-spacing:-.03em;">{state["state_name"]}</h3>
            </div>
            <a class="primary-btn" style="padding:8px 18px; font-size:13px;" href="{BASE_URL}/locations/{state["state_id"]}/">Explore {state["state_name"]} Hub →</a>
          </div>
          <p style="font-size:14.5px; color:var(--muted); line-height:1.6; margin-bottom:18px;">{state["region_description"]} {state["state_focus"]}</p>
          <div style="font-size:13px; font-weight:800; color:#334155; margin-bottom:8px;">Commercial City Hubs:</div>
          <div class="city-pill-grid">
            {city_links}
          </div>
        </div>
        """

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#directory",
                "name": page_title,
                "url": canonical_url,
                "description": page_desc,
                "publisher": {
                    "@type": "Organization",
                    "name": "Angsumi",
                    "url": f"{BASE_URL}/"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": canonical_url
                    }
                ]
            }
        ]
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary SEO -->
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <meta name="keywords" content="website designer Northeast India, app development Assam, web designer Guwahati, web developer Shillong, web designer Agartala, web designer Imphal, web designer Aizawl, web designer Kohima, web designer Itanagar, web designer Gangtok, web designer Siliguri">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">

  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {json.dumps(schema, indent=2)}
  </script>

  <style>
  {CSS_STYLES}
  </style>
</head>
<body>

  <!-- Sticky Nav -->
  <header class="nav">
    <div class="container nav-inner">
      <a class="logo" href="{BASE_URL}/">
        <div class="logo-mark"><img src="{BASE_URL}/logo.png" alt="Angsumi Logo"></div>
        <span>Angsumi</span>
      </a>
      <nav class="links">
        <a href="{BASE_URL}/#vp">What We Do</a>
        <a href="{BASE_URL}/#proof">Live Systems</a>
        <a href="{BASE_URL}/#pricing">Pricing</a>
        <a href="{BASE_URL}/locations/">Locations</a>
        <a href="{BASE_URL}/blog/">Insights</a>
        <a href="{BASE_URL}/learning/">Learning Hub</a>
      </nav>
      <a class="nav-cta" href="{wa_url}" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> →
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">☰</button>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <strong>Locations Directory</strong>
    </div>
  </div>

  <main>
    <!-- HERO -->
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 📍 Northeast India Regional Directory
        </div>
        <h1>Top Website &amp; App Design Across Northeast India</h1>
        <p class="hero-sub">
          Angsumi engineers ultra-fast, affordable websites, clinic/school management portals, and custom mobile apps for entrepreneurs, healthcare institutions, educators, and businesses across all 8 states of Northeast India and gateway hubs.
        </p>

        <div class="actions">
          <a class="primary-btn" href="{wa_url}" target="_blank" rel="noopener">
            <span>💬 Free WhatsApp Consultation (+91 78965 95109)</span>
          </a>
        </div>

        <div class="trust-badges">
          <span>⚡ Sub-Second Load Speeds</span>
          <span>📱 100% Mobile Optimized</span>
          <span>💰 Transparent Rates from ₹2,000</span>
          <span>🤝 Direct Northeast Developer</span>
        </div>
      </div>
    </section>

    <!-- STATES DIRECTORY -->
    <section>
      <div class="container">
        <div class="section-badge">Regional Coverage</div>
        <div class="section-head">
          <h2>Select Your State or City Hub</h2>
          <p>Click into any state or city below to explore localized packages, industry solutions, and instant cost calculators.</p>
        </div>

        {state_sections_html}
      </div>
    </section>
  </main>

  <!-- Sticky Mobile WhatsApp Button -->
  <a class="mobile-sticky-wa" href="{wa_url}" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Top Website &amp; Mobile App Designer serving Northeast India.
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
</html>"""
    return html

from build_services import build_services
from build_tools import build_tools
from build_blog import build_blog
from build_matrix import build_matrix

def update_sitemap(all_urls):
    sitemap_path = "sitemap.xml"
    if not os.path.exists(sitemap_path):
        print("Warning: sitemap.xml not found.")
        return

    # Core base URLs in sitemap
    core_urls = [
        ("https://angsumi.online/", "daily", "1.0"),
        ("https://angsumi.online/blog/github-projects.html", "monthly", "0.7"),
        ("https://angsumi.online/learning/", "weekly", "0.8"),
        ("https://angsumi.online/learning/geography/", "weekly", "0.8"),
        ("https://angsumi.online/learning/history/", "weekly", "0.8"),
        ("https://angsumi.online/learning/polity/", "weekly", "0.8"),
    ]

    new_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Write core URLs
    new_xml += "  <!-- Core Platform Pages -->\n"
    for url, changefreq, priority in core_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    # Write Tools URLs
    new_xml += "\n  <!-- ===== DIGITAL TOOLS & CALCULATORS ===== -->\n"
    tool_urls = [u for u in all_urls if "/tools/" in u[0]]
    for url, changefreq, priority in tool_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    # Write Blog URLs
    new_xml += "\n  <!-- ===== ENGINEERING & STRATEGY INSIGHTS ===== -->\n"
    blog_urls = [u for u in all_urls if "/blog/" in u[0] and u[0] not in [c[0] for c in core_urls]]
    for url, changefreq, priority in blog_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    # Write Services URLs
    new_xml += "\n  <!-- ===== PROGRAMMATIC SEO: SPECIALIZED SERVICES ===== -->\n"
    service_urls = [u for u in all_urls if "/services/" in u[0]]
    for url, changefreq, priority in service_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    # Write Locations URLs (Hubs & Cities)
    new_xml += "\n  <!-- ===== PROGRAMMATIC SEO: REGIONAL LOCATIONS & DISTRICTS ===== -->\n"
    location_urls = [u for u in all_urls if "/locations/" in u[0] and u[0].count("/") <= 5]
    for url, changefreq, priority in location_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    # Write Matrix Intersection URLs
    new_xml += "\n  <!-- ===== PROGRAMMATIC SEO: MATRIX CITY × SERVICE INTERSECTIONS ===== -->\n"
    matrix_urls = [u for u in all_urls if "/locations/" in u[0] and u[0].count("/") > 5]
    for url, changefreq, priority in matrix_urls:
        new_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    new_xml += "</urlset>\n"

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(new_xml)

    print(f"✓ Rebuilt sitemap.xml with {len(core_urls) + len(all_urls)} total verified URLs.")

def build_all():
    all_urls = []

    # 1. Build Location Hub
    os.makedirs("locations", exist_ok=True)
    with open("locations/index.html", "w", encoding="utf-8") as f:
        f.write(get_hub_html())
    print("✓ Generated /locations/index.html")
    all_urls.append(("https://angsumi.online/locations/", "weekly", "0.9"))

    # 2. Build States & Cities
    total_cities = 0
    for state in LOCATIONS_DATA:
        state_dir = os.path.join("locations", state["state_id"])
        os.makedirs(state_dir, exist_ok=True)

        with open(os.path.join(state_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(get_state_html(state))
        print(f"✓ Generated /locations/{state['state_id']}/index.html")
        all_urls.append((f"https://angsumi.online/locations/{state['state_id']}/", "weekly", "0.85"))

        for city in state["cities"]:
            city_dir = os.path.join(state_dir, city["city_id"])
            os.makedirs(city_dir, exist_ok=True)

            with open(os.path.join(city_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(get_city_html(state, city))
            print(f"  ✓ Generated /locations/{state['state_id']}/{city['city_id']}/index.html")
            all_urls.append((f"https://angsumi.online/locations/{state['state_id']}/{city['city_id']}/", "weekly", "0.85"))
            total_cities += 1

    # 3. Build Services
    print("\n--- Generating Specialized Services ---")
    service_urls = build_services()
    all_urls.extend(service_urls)

    # 4. Build Tools
    print("\n--- Generating Interactive Tools Hub ---")
    tool_urls = build_tools()
    all_urls.extend(tool_urls)

    # 5. Build Blog
    print("\n--- Generating Authority Insights & Guides ---")
    blog_urls = build_blog()
    all_urls.extend(blog_urls)

    # 6. Build Matrix pSEO Intersections
    print("\n--- Generating Matrix City × Service Intersections ---")
    matrix_urls = build_matrix()
    all_urls.extend(matrix_urls)

    print(f"\n=======================================================")
    print(f"SUMMARY OF COMPLETE DIGITAL ECOSYSTEM GENERATION:")
    print(f"- Location Hub: 1")
    print(f"- State Hubs: {len(LOCATIONS_DATA)}")
    print(f"- City Landing Pages: {total_cities} (25 in Assam, 21 in other NE states)")
    print(f"- Services Hub: 1")
    print(f"- Specialized Service Pages: {len(service_urls) - 1}")
    print(f"- Interactive Tools & Calculators: {len(tool_urls)}")
    print(f"- Authority Blog & Case Studies: {len(blog_urls)}")
    print(f"- Matrix City × Service Intersections: {len(matrix_urls)}")
    print(f"Total Unique Programmatic & Core URLs Generated: {len(all_urls)}")
    print(f"=======================================================\n")

    update_sitemap(all_urls)

if __name__ == "__main__":
    build_all()
