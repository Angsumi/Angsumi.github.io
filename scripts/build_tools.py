#!/usr/bin/env python3
import os
import json
from datetime import datetime

BASE_URL = "https://angsumi.online"
PHONE = "+917896595109"
PHONE_DISPLAY = "+91 78965 95109"
EMAIL = "angudas62@gmail.com"
TODAY = datetime.now().strftime("%Y-%m-%d")

with open("scripts/style.css", "r", encoding="utf-8") as f:
    CSS_STYLES = f.read()

def get_calculator_html():
    canonical_url = f"{BASE_URL}/tools/cost-calculator/"
    page_title = "Interactive Website & App Cost Calculator Assam & Northeast — Angsumi"
    page_desc = "Calculate the exact cost and delivery timeline to build your website, doctor clinic portal, school system, or mobile app in Assam & Northeast India. 100% transparent pricing."

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "@id": f"{canonical_url}#app",
                "name": "Angsumi Digital Project Cost & Timeline Calculator",
                "url": canonical_url,
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "All",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "INR"
                },
                "provider": {
                    "@type": "ProfessionalService",
                    "name": "Angsumi",
                    "url": BASE_URL,
                    "telephone": PHONE,
                    "email": EMAIL
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/" },
                    { "@type": "ListItem", "position": 2, "name": "Tools", "item": f"{BASE_URL}/tools/" },
                    { "@type": "ListItem", "position": 3, "name": "Cost Calculator", "item": canonical_url }
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
  <meta name="keywords" content="website cost calculator assam, web design price estimator guwahati, mobile app development cost northeast india, affordable website rates assam">
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
  .calc-card-hero {{
    background: #fff; border: 1px solid var(--line); border-radius: 28px; padding: 40px; box-shadow: var(--shadow);
  }}
  .tool-option-card {{
    background: var(--bg); border: 2px solid var(--line); border-radius: 16px; padding: 18px;
    cursor: pointer; transition: all 0.2s ease;
  }}
  .tool-option-card:hover {{ border-color: #93c5fd; background: #f0f7ff; transform: translateY(-2px); }}
  .tool-option-card.active {{ border-color: var(--brand); background: #eef4ff; box-shadow: 0 0 0 2px rgba(18, 87, 214, 0.2); }}
  .addon-check-box {{
    background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 12px 16px;
    display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: all 0.2s;
  }}
  .addon-check-box:hover {{ border-color: var(--brand); }}
  .addon-check-box input {{ width: 18px; height: 18px; accent-color: var(--brand); cursor: pointer; }}
  @media print {{
    .nav, footer, .mobile-sticky-wa, .actions, .cta-box {{ display: none !important; }}
    body {{ background: #fff; }}
    .calc-card-hero {{ border: none; box-shadow: none; padding: 0; }}
  }}
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
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
      </nav>
      <a class="nav-cta" href="https://wa.me/917896595109?text=Hi%20Angsumi%2C%20I%20used%20your%20Cost%20Calculator." target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
    </div>
  </header>

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <a href="{BASE_URL}/tools/">Tools</a> <span>/</span>
      <strong>Interactive Cost &amp; Timeline Estimator</strong>
    </div>
  </div>

  <main>
    <section class="hero" style="padding: 40px 0 30px;">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 🧮 100% Free Estimator Tool
        </div>
        <h1>Interactive Website &amp; App Cost Calculator</h1>
        <p class="hero-sub" style="margin-bottom: 0;">
          Select your requirements, required modules, and business features below to calculate transparent, fixed pricing and exact delivery turnaround for your project in Assam &amp; Northeast India.
        </p>
      </div>
    </section>

    <section style="padding: 30px 0 70px;">
      <div class="container">
        <div class="calc-card-hero">
          <div style="display: grid; grid-template-columns: 1.3fr 0.7fr; gap: 40px; align-items: start;" class="calc-grid">
            
            <div>
              <h3 style="font-size: 19px; font-weight: 850; margin-bottom: 14px; color: var(--ink);">
                1. Select Platform &amp; Architecture
              </h3>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 28px;" id="platform-grid">
                <div class="tool-option-card active" data-price="2000" data-name="Starter Single-Page Website" data-days="2 to 3 Days">
                  <div style="font-size: 24px; margin-bottom: 6px;">⚡</div>
                  <strong style="font-size: 15px; display: block; color: var(--ink);">Starter Landing Page</strong>
                  <div style="font-size: 12.5px; color: var(--muted); margin: 4px 0 8px;">Fast mobile site with WhatsApp lead capture.</div>
                  <div style="color: var(--brand); font-weight: 850; font-size: 14px;">₹2,000</div>
                </div>

                <div class="tool-option-card" data-price="5000" data-name="Multi-Page Business Portal" data-days="4 to 7 Days">
                  <div style="font-size: 24px; margin-bottom: 6px;">🏢</div>
                  <strong style="font-size: 15px; display: block; color: var(--ink);">Business Web Portal</strong>
                  <div style="font-size: 12.5px; color: var(--muted); margin: 4px 0 8px;">Up to 5 pages, Google Maps SEO &amp; CMS.</div>
                  <div style="color: var(--brand); font-weight: 850; font-size: 14px;">₹5,000</div>
                </div>

                <div class="tool-option-card" data-price="8500" data-name="E-Commerce / Direct Booking Engine" data-days="7 to 10 Days">
                  <div style="font-size: 24px; margin-bottom: 6px;">🛍️</div>
                  <strong style="font-size: 15px; display: block; color: var(--ink);">E-Commerce / Booking</strong>
                  <div style="font-size: 12.5px; color: var(--muted); margin: 4px 0 8px;">Online store, homestay booking or QR menu.</div>
                  <div style="color: var(--brand); font-weight: 850; font-size: 14px;">₹8,500</div>
                </div>

                <div class="tool-option-card" data-price="18000" data-name="Custom Mobile App & Management ERP" data-days="12 to 18 Days">
                  <div style="font-size: 24px; margin-bottom: 6px;">📱</div>
                  <strong style="font-size: 15px; display: block; color: var(--ink);">Mobile App / ERP</strong>
                  <div style="font-size: 12.5px; color: var(--muted); margin: 4px 0 8px;">Android &amp; iOS Flutter app with live database.</div>
                  <div style="color: var(--brand); font-weight: 850; font-size: 14px;">₹18,000</div>
                </div>
              </div>

              <h3 style="font-size: 19px; font-weight: 850; margin-bottom: 14px; color: var(--ink);">
                2. Select Advanced Addon Features
              </h3>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;" class="addons-grid">
                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">100% Mobile 4G Fast Speed</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">Sub-1s loading on mobile</small>
                  </div>
                  <input type="checkbox" checked disabled class="tool-addon" data-price="0" data-name="Sub-1s Mobile Speed">
                </label>

                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">Google Maps &amp; Local SEO</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">+₹500 (Rank #1 locally)</small>
                  </div>
                  <input type="checkbox" checked class="tool-addon" data-price="500" data-name="Google Maps & Local SEO">
                </label>

                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">WhatsApp 1-Tap Ordering Bot</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">+₹1,000 (Direct lead pipeline)</small>
                  </div>
                  <input type="checkbox" class="tool-addon" data-price="1000" data-name="WhatsApp Smart Bot">
                </label>

                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">UPI Online Payment Gateway</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">+₹1,500 (GPay, PhonePe, Cards)</small>
                  </div>
                  <input type="checkbox" class="tool-addon" data-price="1500" data-name="UPI Payment Gateway">
                </label>

                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">OPD / Doctor Appointment Queue</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">+₹2,500 (Live token slots)</small>
                  </div>
                  <input type="checkbox" class="tool-addon" data-price="2500" data-name="OPD Queue System">
                </label>

                <label class="addon-check-box">
                  <div>
                    <strong style="font-size: 13.5px; display: block;">Custom Admin Billing Dashboard</strong>
                    <small style="color: var(--muted); font-size: 11.5px;">+₹3,500 (Invoicing &amp; CRM)</small>
                  </div>
                  <input type="checkbox" class="tool-addon" data-price="3500" data-name="Admin Billing Dashboard">
                </label>
              </div>

              <div style="margin-top: 24px;">
                <label style="display: block; font-weight: 800; font-size: 13px; text-transform: uppercase; color: var(--brand); letter-spacing: .06em; margin-bottom: 8px;">
                  Your Primary Location in Assam / Northeast
                </label>
                <select id="user-location" style="width: 100%; border: 1.5px solid var(--line); background: #fff; padding: 12px 16px; border-radius: 12px; font-weight: 650; font-size: 14px; outline: none;">
                  <option value="Guwahati, Assam">Guwahati, Assam</option>
                  <option value="Dibrugarh, Assam">Dibrugarh, Assam</option>
                  <option value="Silchar, Assam">Silchar, Assam</option>
                  <option value="Jorhat, Assam">Jorhat, Assam</option>
                  <option value="Tezpur, Assam">Tezpur, Assam</option>
                  <option value="Nagaon, Assam">Nagaon, Assam</option>
                  <option value="Tinsukia, Assam">Tinsukia, Assam</option>
                  <option value="Bongaigaon, Assam">Bongaigaon, Assam</option>
                  <option value="Shillong, Meghalaya">Shillong, Meghalaya</option>
                  <option value="Agartala, Tripura">Agartala, Tripura</option>
                  <option value="Dimapur, Nagaland">Dimapur, Nagaland</option>
                  <option value="Itanagar, Arunachal Pradesh">Itanagar, Arunachal Pradesh</option>
                  <option value="Other Northeast District">Other Northeast District</option>
                </select>
              </div>
            </div>

            <div style="background: linear-gradient(145deg, #0b1220 0%, #111e33 100%); color: #fff; border-radius: 24px; padding: 32px; border: 1.5px solid #1e2d45; box-shadow: var(--shadow);">
              <div style="font-size: 12px; font-weight: 850; text-transform: uppercase; color: #38bdf8; letter-spacing: .08em;">
                Generated Project Estimate
              </div>
              
              <div style="font-size: 46px; font-weight: 900; color: #38bdf8; margin: 12px 0 4px; letter-spacing: -.04em;" id="calc-total-display">
                ₹2,500
              </div>
              <div style="font-size: 13.5px; color: #a7f3d0; font-weight: 750; margin-bottom: 22px;" id="calc-days-display">
                ⏱️ Delivery: 2 to 3 Business Days
              </div>

              <div style="border-top: 1px solid #1e2e47; border-bottom: 1px solid #1e2e47; padding: 16px 0; margin-bottom: 22px; font-size: 13px; display: grid; gap: 8px;">
                <div style="display: flex; justify-content: space-between; color: #cbd5e1;">
                  <span>Platform:</span> <strong style="color: #fff;" id="sum-platform">Starter Landing Page</strong>
                </div>
                <div style="display: flex; justify-content: space-between; color: #cbd5e1;">
                  <span>Location:</span> <strong style="color: #fff;" id="sum-loc">Guwahati, Assam</strong>
                </div>
                <div style="display: flex; justify-content: space-between; color: #cbd5e1;">
                  <span>Addons Selected:</span> <strong style="color: #38bdf8;" id="sum-addons">1 Addon (₹500)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; color: #cbd5e1;">
                  <span>Monthly SaaS Fees:</span> <strong style="color: #10b981;">₹0 Forever</strong>
                </div>
                <div style="display: flex; justify-content: space-between; color: #cbd5e1;">
                  <span>Code Ownership:</span> <strong style="color: #10b981;">100% Client Owned</strong>
                </div>
              </div>

              <div style="display: grid; gap: 10px;">
                <a class="calc-btn" id="wa-submit-btn" href="#" target="_blank" rel="noopener">
                  <span>💬 Lock Quote on WhatsApp</span> &rarr;
                </a>
                <button onclick="window.print()" class="secondary-btn" style="width: 100%; justify-content: center; background: transparent; color: #cbd5e1; border-color: #24354f;">
                  <span>🖨️ Print / Save PDF Estimate</span>
                </button>
              </div>

              <div style="margin-top: 16px; font-size: 11.5px; color: #94a3b8; text-align: center; line-height: 1.5;">
                ✓ Zero advance commitment required.<br>We engineer an interactive prototype for your review first.
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <section style="background: #fff; border-top: 1px solid var(--line); padding: 60px 0;">
      <div class="container">
        <div class="section-badge">Transparent Pricing Guarantee</div>
        <div class="section-head">
          <h2>Why Our Quotes Have Zero Hidden Costs</h2>
          <p>Traditional agencies in Guwahati and Kolkata charge ₹25,000–₹50,000 for slow WordPress templates. Here is how our transparent direct engineering model works:</p>
        </div>

        <div class="industry-grid">
          <div class="ind-card">
            <div class="ind-icon">💰</div>
            <h3>Fixed Price Promise</h3>
            <p>The price you see here is the exact price you pay. No extra maintenance taxes or unmentioned server onboarding markups.</p>
          </div>
          <div class="ind-card">
            <div class="ind-icon">🎯</div>
            <h3>See Results Before Final Payment</h3>
            <p>We build and demonstrate a working mobile prototype so you can test features and speeds before completing the project.</p>
          </div>
          <div class="ind-card">
            <div class="ind-icon">⚡</div>
            <h3>Sub-Second Core Web Vitals</h3>
            <p>Every website is hand-crafted for sub-1-second loading speeds on spotty mobile networks across Northeast India.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

  <a class="mobile-sticky-wa" id="mob-wa-btn" href="#" target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Interactive Web &amp; App Cost Estimator for Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="https://wa.me/917896595109" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
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

    const platformCards = document.querySelectorAll('.tool-option-card');
    const addonChecks = document.querySelectorAll('.tool-addon');
    const locationSelect = document.getElementById('user-location');
    const totalDisplay = document.getElementById('calc-total-display');
    const daysDisplay = document.getElementById('calc-days-display');
    const sumPlatform = document.getElementById('sum-platform');
    const sumLoc = document.getElementById('sum-loc');
    const sumAddons = document.getElementById('sum-addons');
    const waSubmitBtn = document.getElementById('wa-submit-btn');
    const mobWaBtn = document.getElementById('mob-wa-btn');

    let basePrice = 2000;
    let baseName = 'Starter Single-Page Website';
    let baseDays = '2 to 3 Days';

    function recalculate() {{
      let addonTotal = 0;
      let selectedAddons = [];

      addonChecks.forEach(cb => {{
        if (cb.checked && !cb.disabled) {{
          addonTotal += parseInt(cb.dataset.price, 10);
          selectedAddons.push(cb.dataset.name);
        }}
      }});

      const loc = locationSelect.value;
      const total = basePrice + addonTotal;

      totalDisplay.textContent = '₹' + total.toLocaleString('en-IN');
      daysDisplay.textContent = '⏱️ Delivery: ' + baseDays;
      sumPlatform.textContent = baseName;
      sumLoc.textContent = loc;
      sumAddons.textContent = selectedAddons.length + ' Addons (+₹' + addonTotal.toLocaleString('en-IN') + ')';

      const waMsg = `Hi Angsumi, I calculated an estimate on your website tool:%0A• Platform: ${{baseName}}%0A• Location: ${{loc}}%0A• Features: ${{selectedAddons.join(', ') || 'Standard Fast Speed'}}%0A• Estimated Total: ₹${{total.toLocaleString('en-IN')}}%0A• Timeline: ${{baseDays}}%0APlease share proposal and prototype details!`;
      const waUrl = `https://wa.me/917896595109?text=${{waMsg}}`;

      waSubmitBtn.href = waUrl;
      mobWaBtn.href = waUrl;
    }}

    platformCards.forEach(card => {{
      card.addEventListener('click', () => {{
        platformCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        basePrice = parseInt(card.dataset.price, 10);
        baseName = card.dataset.name;
        baseDays = card.dataset.days;
        recalculate();
      }});
    }});

    addonChecks.forEach(cb => cb.addEventListener('change', recalculate));
    locationSelect.addEventListener('change', recalculate);

    recalculate();
  </script>
</body>
</html>'''

def get_tools_hub_html():
    canonical_url = f"{BASE_URL}/tools/"
    page_title = "Free Digital Tools & Cost Calculators for Northeast Businesses — Angsumi"
    page_desc = "Free digital tools, instant website cost calculators, and digital transformation guides for businesses in Assam and Northeast India."

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#tools",
                "name": "Angsumi Digital Tools",
                "url": canonical_url,
                "description": "Free digital tools and cost estimators for Northeast India businesses."
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/" },
                    { "@type": "ListItem", "position": 2, "name": "Tools", "item": canonical_url }
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
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
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
        <a href="https://blog.angsumi.online" target="_blank" rel="noopener">Blog</a>
      </nav>
      <a class="nav-cta" href="https://wa.me/917896595109?text=Hi%20Angsumi" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
    </div>
  </header>

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <strong>Digital Tools &amp; Calculators</strong>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 🛠️ Free Digital Utilities
        </div>
        <h1>Free Tools &amp; Calculators for Northeast Businesses</h1>
        <p class="hero-sub">
          Transparent estimators, performance benchmarks, and planning tools engineered specifically for business owners, doctors, educators, and entrepreneurs across Northeast India.
        </p>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="products-grid">
          
          <div class="proof-card" style="padding: 32px;">
            <div>
              <div style="font-size: 36px; margin-bottom: 12px;">🧮</div>
              <span class="proof-badge">Interactive Cost Calculator</span>
              <h3 style="font-size: 22px; margin: 10px 0 8px;">Website &amp; App Cost Estimator</h3>
              <p style="font-size: 14px; color: var(--muted); line-height: 1.6;">
                Select your required platform, payment gateway, WhatsApp bots, or OPD token modules to get instant transparent fixed pricing with zero agency markup.
              </p>
            </div>
            <a class="primary-btn" style="width: 100%; justify-content: center; margin-top: 18px;" href="{BASE_URL}/tools/cost-calculator/">
              <span>Launch Cost Calculator</span> &rarr;
            </a>
          </div>

          <div class="proof-card" style="padding: 32px;">
            <div>
              <div style="font-size: 36px; margin-bottom: 12px;">🗺️</div>
              <span class="proof-badge">Geographic Coverage</span>
              <h3 style="font-size: 22px; margin: 10px 0 8px;">Northeast Locations Directory</h3>
              <p style="font-size: 14px; color: var(--muted); line-height: 1.6;">
                Explore localized web development packages and industry profiles across 46+ district headquarters in Assam, Meghalaya, Tripura, and beyond.
              </p>
            </div>
            <a class="secondary-btn" style="width: 100%; justify-content: center; margin-top: 18px;" href="{BASE_URL}/locations/">
              <span>Explore Locations Directory</span> &rarr;
            </a>
          </div>

          <div class="proof-card" style="padding: 32px;">
            <div>
              <div style="font-size: 36px; margin-bottom: 12px;">⚡</div>
              <span class="proof-badge">Industry Solutions</span>
              <h3 style="font-size: 22px; margin: 10px 0 8px;">Specialized Systems Directory</h3>
              <p style="font-size: 14px; color: var(--muted); line-height: 1.6;">
                Browse turnkey digital platforms engineered for tea estates, homestays, private clinics, schools, and silk e-commerce brands.
              </p>
            </div>
            <a class="secondary-btn" style="width: 100%; justify-content: center; margin-top: 18px;" href="{BASE_URL}/services/">
              <span>Browse All Systems</span> &rarr;
            </a>
          </div>

        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Free Tools for Growing Northeast Businesses.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="https://wa.me/917896595109" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
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

def build_tools():
    os.makedirs("tools", exist_ok=True)
    os.makedirs("tools/cost-calculator", exist_ok=True)

    with open("tools/index.html", "w", encoding="utf-8") as f:
        f.write(get_tools_hub_html())
    print("✓ Generated /tools/index.html")

    with open("tools/cost-calculator/index.html", "w", encoding="utf-8") as f:
        f.write(get_calculator_html())
    print("✓ Generated /tools/cost-calculator/index.html")

    return [
        ("https://angsumi.online/tools/", "weekly", "0.85"),
        ("https://angsumi.online/tools/cost-calculator/", "weekly", "0.90"),
    ]

if __name__ == "__main__":
    build_tools()
