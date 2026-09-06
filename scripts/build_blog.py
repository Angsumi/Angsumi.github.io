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

BLOG_POSTS = [
    {
        "slug": "website-cost-assam-2026.html",
        "title": "How Much Does a Website Cost in Assam in 2026? (Honest Pricing Breakdown)",
        "desc": "Real pricing comparison for website design in Assam. Learn why agencies charge ₹25,000–₹50,000 for slow WordPress templates, and how you can get sub-second custom sites starting from ₹2,000.",
        "date": "2026-03-01",
        "read_time": "6 min read",
        "category": "Pricing & Strategy",
        "content_html": """
        <p>If you're a business owner, doctor, school principal, or entrepreneur in Guwahati, Dibrugarh, Silchar, or Jorhat looking to build a website in 2026, you've likely received wildly conflicting quotes. One local agency quotes ₹45,000, a freelancer offers ₹8,000, and online platforms promise "free" websites that suddenly cost ₹3,000 every month.</p>
        
        <h2>The Real Cost of Building a Website in Assam</h2>
        <p>Let's break down the actual market rates across Assam and Northeast India based on platform type and technical requirements:</p>
        
        <div class="compare-box" style="margin: 24px 0;">
          <table class="compare-table">
            <thead>
              <tr>
                <th>Type of Website</th>
                <th>Traditional Agency Rate</th>
                <th>Angsumi Direct Rate</th>
                <th>Ideal For</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Starter Landing Page</strong></td>
                <td>₹15,000 – ₹25,000</td>
                <td><strong style="color:#059669;">₹2,000 Fixed</strong></td>
                <td>Local shops, freelancers, consultants</td>
              </tr>
              <tr>
                <td><strong>Business Web Portal (5-7 Pages)</strong></td>
                <td>₹30,000 – ₹60,000</td>
                <td><strong style="color:#059669;">₹5,000 Fixed</strong></td>
                <td>Clinics, coaching institutes, contractors</td>
              </tr>
              <tr>
                <td><strong>E-Commerce / Direct Booking Engine</strong></td>
                <td>₹50,000 – ₹1,20,000</td>
                <td><strong style="color:#059669;">₹8,500 Fixed</strong></td>
                <td>Assam silk stores, homestays, tour operators</td>
              </tr>
              <tr>
                <td><strong>Custom Mobile App (Flutter PWA)</strong></td>
                <td>₹1,50,000+</td>
                <td><strong style="color:#059669;">From ₹18,000</strong></td>
                <td>Schools, multi-doctor OPD, mock exam portals</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>Why Do Traditional City Agencies Charge So Much?</h2>
        <p>Most traditional web agencies in Northeast India operate with heavy overheads: office rent in central Guwahati, account managers, sales commissions, and multiple layers of hierarchy. Worse, 90% of them simply download a generic WordPress template, install 30+ unvetted plugins, and hand you a slow website that takes 6 seconds to load on mobile 4G.</p>
        
        <h2>How Angsumi Delivers Better Speed at a Fraction of the Cost</h2>
        <p>At Angsumi, we write <strong>clean, hand-coded semantic HTML, CSS, and modern JavaScript</strong>. We eliminate database bloat, plugin vulnerabilities, and recurring licensing fees. The result? Sub-second loading speeds (100% Core Web Vitals) and 100% code ownership for you.</p>

        <div class="market-box" style="margin-top: 30px; background: #eef4ff; border-color: #c7dcff;">
          <h3 style="color: var(--brand);">Ready to Get an Instant Transparent Quote?</h3>
          <p style="margin: 8px 0 16px;">Use our free interactive calculator to configure your exact platform and get an instant quote in 30 seconds.</p>
          <a class="primary-btn" href="/tools/cost-calculator/">Launch Cost Calculator &rarr;</a>
        </div>
        """
    },
    {
        "slug": "wix-shopify-vs-custom-website-assam.html",
        "title": "Why Wix, Shopify & Monthly SaaS Subscriptions Drain Small Northeast Businesses",
        "desc": "Thinking of using Wix or Shopify for your business in Assam? Discover the hidden monthly costs, slow mobile load times, and why custom code gives you 100% ownership.",
        "date": "2026-02-20",
        "read_time": "5 min read",
        "category": "Technology & ROI",
        "content_html": """
        <p>When starting an online store or business website in Assam, DIY platforms like Shopify, Wix, and Squarespace look tempting with promises of "build your website in minutes". But after 6 to 12 months, Northeast business owners realize they are trapped in a costly subscription treadmill.</p>
        
        <h2>The Hidden Math: What Shopify & Wix Actually Cost Over 2 Years</h2>
        <ul style="margin: 16px 0 24px 20px; line-height: 1.8;">
          <li><strong>Base Subscription:</strong> ₹2,000 to ₹3,000/month (&times; 24 months = ₹48,000 to ₹72,000)</li>
          <li><strong>Essential App Store Addons:</strong> WhatsApp chat, invoice generator, pin-code checker (+₹1,500/month = ₹36,000)</li>
          <li><strong>Transaction Fee Surcharges:</strong> 1.5% to 2.0% extra on every order unless using proprietary gateways</li>
          <li><strong>Total 2-Year Outflow:</strong> <span style="color:#ef4444; font-weight:850;">₹84,000 – ₹1,20,000+</span></li>
        </ul>

        <h2>The Performance Problem on Northeast 4G Networks</h2>
        <p>Wix and Shopify inject massive bundles of third-party tracking scripts, stylesheets, and iframe wrappers. While these sites load okay on high-speed broadband in Mumbai, they struggle on mobile connections in rural Assam, Meghalaya, and Arunachal Pradesh, causing bounce rates over 65%.</p>

        <h2>The Angsumi Alternative: Zero Monthly Hostage Fees</h2>
        <p>With an Angsumi-built custom platform, you pay once (starting at ₹2,000–₹8,500) and own your code forever. You can host for free on modern global edge networks (like GitHub Pages, Cloudflare, or Vercel) with <strong>₹0/month hosting costs</strong> and instant UPI payment integrations.</p>
        """
    },
    {
        "slug": "axomrank-exam-portal-case-study.html",
        "title": "Case Study: How We Built AxomRank & ADRE Prep Platform for 25,000+ Candidates",
        "desc": "Deep dive into the architecture and performance engineering behind Assam's high-speed online exam portal and rank predictor, handling concurrent mock tests with zero latency.",
        "date": "2026-02-10",
        "read_time": "7 min read",
        "category": "Case Study & Architecture",
        "content_html": """
        <p>When the Assam Direct Recruitment Examination (ADRE) and state recruitment tests were announced, thousands of candidates across all 35 Assam districts needed a fast, reliable, and mobile-friendly way to practice timed mock tests and evaluate their state-wide rank.</p>
        
        <h2>The Engineering Challenge</h2>
        <ul style="margin: 16px 0 24px 20px; line-height: 1.8;">
          <li>Over 25,000 candidates accessing tests simultaneously across varying 3G/4G connectivity.</li>
          <li>Zero-latency live countdown timer and anti-cheating question shuffling.</li>
          <li>Instant state-wide rank prediction based on negative marking algorithms.</li>
          <li>Zero budget for expensive multi-thousand-dollar monthly cloud servers.</li>
        </ul>

        <h2>The Solution: Pure Static-First Client-Side Architecture</h2>
        <p>Instead of relying on heavy database queries for every single question render, we pre-compiled and compressed the entire question bank into lightweight encrypted JSON bundles. The entire mock exam engine runs client-side with instant UI reactivity and sub-50ms score calculations.</p>

        <h2>The Results</h2>
        <div class="products-grid" style="margin: 24px 0;">
          <div class="proof-card" style="padding: 20px; text-align: center;">
            <div style="font-size: 32px; font-weight: 900; color: var(--brand);">25,000+</div>
            <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">Active Candidates Served</div>
          </div>
          <div class="proof-card" style="padding: 20px; text-align: center;">
            <div style="font-size: 32px; font-weight: 900; color: #10b981;">0.4s</div>
            <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">Average Page Load Speed</div>
          </div>
          <div class="proof-card" style="padding: 20px; text-align: center;">
            <div style="font-size: 32px; font-weight: 900; color: var(--brand);">₹0</div>
            <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">Server Downtime or Crashes</div>
          </div>
        </div>

        <p>This exact high-performance engineering is applied to every business website, clinic system, and online store we build for our clients in Assam.</p>
        <div style="margin-top: 24px;">
          <a class="primary-btn" href="/learning/" target="_blank">Explore Live Learning Platform &rarr;</a>
        </div>
        """
    }
]

def get_post_html(post):
    canonical_url = f"{BASE_URL}/blog/{post['slug']}"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["desc"],
        "datePublished": post["date"],
        "dateModified": TODAY,
        "author": {
            "@type": "Person",
            "name": "Angsumi",
            "url": BASE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "Angsumi",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{post['title']} — Angsumi Blog</title>
  <meta name="description" content="{post['desc']}">
  <meta name="author" content="Angsumi">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0b1220">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{post['title']}">
  <meta property="og:description" content="{post['desc']}">
  <meta property="og:image" content="{BASE_URL}/logo.png">
  <meta property="og:site_name" content="Angsumi">
  <meta property="og:locale" content="en_IN">
  <script type="application/ld+json">
{json.dumps(schema, indent=2)}
  </script>
  <style>
{CSS_STYLES}
  .article-container {{
    max-width: 780px; margin: auto; padding: 40px 20px 80px; font-size: 16.5px; line-height: 1.75; color: #2d3748;
  }}
  .article-container h2 {{ font-size: 26px; font-weight: 850; margin: 36px 0 14px; color: var(--ink); }}
  .article-container p {{ margin-bottom: 18px; }}
  .article-meta {{ display: flex; gap: 14px; font-size: 13px; color: var(--muted); font-weight: 700; margin-bottom: 24px; }}
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
      <a class="nav-cta" href="https://wa.me/917896595109?text=Hi%20Angsumi" target="_blank" rel="noopener">
        <span>WhatsApp Call</span> &rarr;
      </a>
      <button class="menu" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
    </div>
  </header>

  <div class="breadcrumb-strip">
    <div class="container breadcrumbs">
      <a href="{BASE_URL}/">Home</a> <span>/</span>
      <a href="{BASE_URL}/blog/">Blog</a> <span>/</span>
      <strong>{post['category']}</strong>
    </div>
  </div>

  <main>
    <article class="article-container">
      <div class="section-badge">{post['category']}</div>
      <h1 style="font-size: clamp(30px, 4vw, 44px); line-height: 1.12; margin: 12px 0 16px;">{post['title']}</h1>
      
      <div class="article-meta">
        <span>📅 {post['date']}</span> ·
        <span>⏱️ {post['read_time']}</span> ·
        <span>✍️ By Angsumi</span>
      </div>

      <div class="article-body">
        {post['content_html']}
      </div>
    </article>
  </main>

  <a class="mobile-sticky-wa" href="https://wa.me/917896595109?text=Hi%20Angsumi%2C%20I%20read%20your%20article%20and%20want%20to%20discuss%20a%20project." target="_blank" rel="noopener">
    <span class="pulse"></span> 💬 Chat on WhatsApp ({PHONE_DISPLAY})
  </a>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Digital Infrastructure for Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="https://wa.me/917896595109" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
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

def get_blog_hub_html():
    canonical_url = f"{BASE_URL}/blog/"
    page_title = "Insights, Case Studies & Web Development Guides — Angsumi Blog"
    page_desc = "Practical insights, real pricing guides, and technical case studies on website design, mobile apps, and digital systems in Assam and Northeast India."

    cards_html = ""
    for p in BLOG_POSTS:
        cards_html += f'''
        <div class="proof-card" style="padding: 28px;">
          <div>
            <div class="section-badge" style="margin-bottom: 8px;">{p['category']}</div>
            <h3 style="font-size: 20px; font-weight: 850; margin-bottom: 8px;">{p['title']}</h3>
            <p style="font-size: 13.5px; color: var(--muted); line-height: 1.55;">{p['desc']}</p>
            <div style="font-size: 12px; color: #64748b; margin-top: 12px; font-weight: 700;">
              📅 {p['date']} · ⏱️ {p['read_time']}
            </div>
          </div>
          <a class="proof-link" href="{BASE_URL}/blog/{p['slug']}">Read Full Guide &rarr;</a>
        </div>
        '''

    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Angsumi Insights & Engineering Blog",
        "url": canonical_url,
        "description": page_desc
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
        <a href="{BASE_URL}/blog/">Insights</a>
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
      <strong>Engineering Insights &amp; Guides</strong>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="dot"></span> 📚 Northeast Digital Insights
        </div>
        <h1>Insights, Case Studies &amp; Pricing Breakdowns</h1>
        <p class="hero-sub">
          Straightforward technical guides, architecture breakdowns, and transparent pricing facts for Northeast India businesses.
        </p>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="products-grid">
          {cards_html}
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div>
        <strong style="color:var(--ink)">Angsumi</strong> — Engineering Insights for Northeast India.
      </div>
      <div>
        <a href="mailto:{EMAIL}">{EMAIL}</a> · 
        <a href="https://wa.me/917896595109" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · 
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

def build_blog():
    os.makedirs("blog", exist_ok=True)
    with open("blog/index.html", "w", encoding="utf-8") as f:
        f.write(get_blog_hub_html())
    print("✓ Generated /blog/index.html")

    urls = [("https://angsumi.online/blog/", "weekly", "0.85")]
    for p in BLOG_POSTS:
        with open(f"blog/{p['slug']}", "w", encoding="utf-8") as f:
            f.write(get_post_html(p))
        print(f"  ✓ Generated /blog/{p['slug']}")
        urls.append((f"https://angsumi.online/blog/{p['slug']}", "monthly", "0.80"))

    return urls

if __name__ == "__main__":
    build_blog()
