/* Angsumi GA4: analytics loads only after a visitor opts in. */
(() => {
  'use strict';

  const measurementId = 'G-DKV62LEMV2';
  if (!/^G-[A-Z0-9]+$/.test(measurementId) || location.protocol !== 'https:') return;

  const preferenceKey = 'angsumi_analytics_choice_v1';
  const preferenceLifetimeMs = 180 * 24 * 60 * 60 * 1000;
  const choice = (() => {
    try {
      const [value, savedAt] = (localStorage.getItem(preferenceKey) || '').split(':');
      const age = Date.now() - Number(savedAt);
      return ['accepted', 'rejected'].includes(value) && age >= 0 && age < preferenceLifetimeMs ? value : null;
    } catch (_) { return null; }
  })();
  let currentChoice = choice;
  let tagLoaded = false;

  const safeReferrer = (() => {
    try {
      const url = new URL(document.referrer);
      return /^https?:$/.test(url.protocol) ? url.origin + url.pathname : '';
    } catch (_) { return ''; }
  })();

  function saveChoice(value) {
    try { localStorage.setItem(preferenceKey, value + ':' + Date.now()); } catch (_) { /* Consent remains valid for this page only. */ }
  }

  function removeAnalyticsCookies() {
    const domains = ['', location.hostname, '.' + location.hostname];
    document.cookie.split(';').forEach(part => {
      const name = part.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      domains.forEach(domain => {
        document.cookie = name + '=; Max-Age=0; Path=/' + (domain ? '; Domain=' + domain : '');
      });
    });
  }

  function loadAnalytics() {
    if (tagLoaded) return;
    tagLoaded = true;

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    const denied = {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    };
    window.gtag('consent', 'default', denied);
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: false,
      page_location: location.origin + location.pathname,
      page_referrer: safeReferrer,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: 60 * 60 * 24 * 30
    });
    window.gtag('event', 'page_view', {
      page_title: document.title,
      page_location: location.origin + location.pathname,
      page_referrer: safeReferrer,
      send_to: measurementId
    });

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    script.dataset.angsumiGa = 'true';
    document.head.appendChild(script);
  }

  // The only custom event exposed to page code uses a fixed, non-personal label.
  window.angsumiTrackWorkshopLead = function (kind) {
    if (!tagLoaded || currentChoice !== 'accepted' || !['free', 'payment_pending'].includes(kind)) return;
    window.gtag('event', 'generate_lead', {
      lead_source: kind === 'free' ? 'workshop_coupon' : 'workshop_registration',
      send_to: measurementId
    });
  };

  function buildControls() {
    const style = document.createElement('style');
    style.textContent = `
      #angsumi-privacy-choice { position: fixed; z-index: 9998; left: 14px; bottom: 14px; border: 1px solid #cbd5e1; border-radius: 999px; padding: 8px 12px; background: #fff; color: #0b3e35; font: 600 12px/1.3 system-ui,sans-serif; box-shadow: 0 4px 18px #0b132026; cursor: pointer; }
      #angsumi-privacy-panel { position: fixed; z-index: 9999; left: 14px; bottom: 58px; width: min(380px, calc(100vw - 28px)); padding: 18px; border: 1px solid #d1d5db; border-radius: 16px; background: #fff; color: #0b1320; box-shadow: 0 16px 44px #0b132033; font: 14px/1.5 system-ui,sans-serif; }
      #angsumi-privacy-panel[hidden] { display: none; }
      #angsumi-privacy-panel strong { display: block; margin-bottom: 7px; font-size: 16px; }
      #angsumi-privacy-panel p { margin: 0 0 12px; }
      #angsumi-privacy-panel a { color: #0b5b48; text-decoration: underline; }
      #angsumi-privacy-actions { display: flex; gap: 8px; margin-top: 14px; }
      #angsumi-privacy-actions button { flex: 1; min-height: 40px; padding: 8px; border-radius: 9px; font: 700 13px system-ui,sans-serif; cursor: pointer; }
      #angsumi-privacy-accept { border: 1px solid #0c3e35; background: #0c3e35; color: #fff; }
      #angsumi-privacy-reject { border: 1px solid #0c3e35; background: #fff; color: #0c3e35; }
    `;
    document.head.appendChild(style);

    const settings = document.createElement('button');
    settings.id = 'angsumi-privacy-choice';
    settings.type = 'button';
    settings.textContent = 'Privacy choices';
    settings.setAttribute('aria-controls', 'angsumi-privacy-panel');
    settings.setAttribute('aria-expanded', choice ? 'false' : 'true');

    const panel = document.createElement('section');
    panel.id = 'angsumi-privacy-panel';
    panel.setAttribute('aria-label', 'Analytics privacy choices');
    panel.hidden = Boolean(choice);
    panel.innerHTML = '<strong>Analytics is optional</strong><p>With your permission, we use Google Analytics to understand which pages help visitors. We do not send names, emails, form entries, or URL query details. You can change your choice here at any time. <a href="/privacy-policy/">Privacy policy</a></p><div id="angsumi-privacy-actions"><button type="button" id="angsumi-privacy-reject">Reject analytics</button><button type="button" id="angsumi-privacy-accept">Accept analytics</button></div>';

    settings.addEventListener('click', () => {
      panel.hidden = !panel.hidden;
      settings.setAttribute('aria-expanded', String(!panel.hidden));
    });
    panel.querySelector('#angsumi-privacy-accept').addEventListener('click', () => {
      saveChoice('accepted');
      currentChoice = 'accepted';
      panel.hidden = true;
      settings.setAttribute('aria-expanded', 'false');
      loadAnalytics();
    });
    panel.querySelector('#angsumi-privacy-reject').addEventListener('click', () => {
      saveChoice('rejected');
      currentChoice = 'rejected';
      panel.hidden = true;
      settings.setAttribute('aria-expanded', 'false');
      if (tagLoaded) {
        window.gtag('consent', 'update', { analytics_storage: 'denied' });
        removeAnalyticsCookies();
        location.reload();
      }
    });
    document.body.append(settings, panel);
  }

  if (choice === 'accepted') loadAnalytics();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildControls, { once: true });
  } else {
    buildControls();
  }
})();
