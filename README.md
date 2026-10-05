# Angsumi Digital Agency Portfolio

The official digital agency portfolio website for Angsumi. Hosted directly on GitHub Pages, this repository contains the static source files that power the digital presence, showcasing services, previous work, and business information.

## 🌟 Features
- **Agency Showcase:** Highlights digital agency services and past projects.
- **SEO Optimized:** Includes sitemap and robots.txt for search engine indexing.
- **Responsive & Fast:** Built as a static site for maximum performance.

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS
- **Hosting:** GitHub Pages

## 🚀 Getting Started
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Angsumi/Angsumi.github.io.git
   ```
2. **View Locally:**
   Open `index.html` in your web browser.

## 🔗 Live Site
Visit the live portfolio at: [https://angsumi.online](https://angsumi.online)

## Google Analytics 4
Public site pages load `/assets/analytics-consent.js` with GA4 Measurement ID `G-DKV62LEMV2`. The Google tag loads only after a visitor accepts analytics; rejection sends no Analytics request from this script. Visitors can reopen **Privacy choices** and change their decision; the saved choice expires after 180 days. The script sends a single page view per page load using URLs and referrers without query strings, keeps advertising consent denied, and does not attach form values or attendee details to analytics events. A successful workshop form submission also sends GA4's `generate_lead` event with a fixed free/pending label, only when analytics is accepted.

In the GA4 web stream, disable Enhanced Measurement events that collect form interactions or automatic history-based page views, so they cannot duplicate the site's controlled page views. Set your preferred data retention and internal-traffic exclusions in Analytics Admin, then verify an opt-in visit in Realtime and a rejected visit in browser network tools.

## Learn GitHub workshop checkout
The homepage footer opens a workshop registration dialog. The price is $20 USD internationally or ₹2,000 in India. Coupon `GBF` changes the selected total to zero and sends the attendee's name and email to the existing Formspree inbox. After a successful free registration, the dialog displays the Google Meet link and calendar event. The browser does not automatically send an email or WhatsApp message to the attendee.

Paid registrations are sent to the existing Formspree inbox with the attendee's name, email, region, price, and payment-pending status. Until a payment link is configured, the attendee sees a confirmation that payment is pending and must be contacted by email; the Meet link is not shown in this flow. To enable immediate paid checkout, set the two provider-hosted links near the end of `index.html`: `workshopPaymentLinks.india` (an Indian gateway payment link for **₹2,000**) and `workshopPaymentLinks.international` (a PayPal Payment Link for **$20 USD**). When a link is configured, the site saves the pending registration before redirecting to that gateway. Match each transaction against the registration email and send the workshop links after verifying payment; this static site cannot verify gateway transactions itself.
