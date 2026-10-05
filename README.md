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

## Learn GitHub workshop checkout
The homepage footer opens a workshop registration dialog. Coupon `GBF` changes the total from $20 to $0 and sends the attendee's name and email to the existing Formspree inbox. After a successful free registration, the dialog displays the Google Meet link, calendar event, and a WhatsApp share link containing both. The browser cannot automatically send an email or WhatsApp message to the attendee.

To enable paid registration, set the three values near the end of `index.html`: `workshopIndiaPriceInr` (the agreed fixed INR amount), `workshopPaymentLinks.india` (an Indian gateway payment link for that amount), and `workshopPaymentLinks.international` (a PayPal Payment Link for a **$20 USD** workshop product). Each paid route stays unavailable until its price and link are configured. When enabled, the site saves a pending registration to Formspree before redirecting to the selected gateway. Match each transaction against the registration email and send the workshop links after verifying payment; this static site cannot verify gateway transactions itself.
