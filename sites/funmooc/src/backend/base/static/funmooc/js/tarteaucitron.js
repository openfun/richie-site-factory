(function () {
  // Enforce to use document language
  tarteaucitronForceLanguage = (document.documentElement.lang || '-').split('-')[0].toLowerCase();
  var privacyUrl = window.__funmooc_context__.privacy.tarteaucitron.privacyUrl || '';

  tarteaucitron.init({
    "AcceptAllCta": true, /* Show the accept all button when highPrivacy on */
    "adblocker": false, /* Show a Warning if an adblocker is detected */
    "bodyPosition": "top", /* Position in the html */
    "closePopup": true, /* Show a close X on the banner */
    // "cookieDomain": ".my-multisite-domaine.fr", /* Shared cookie for multisite */
    "cookieName": "tarteaucitron", /* Cookie name */
    "cookieslist": false, /* Show the cookie list */
    "DenyAllCta": true, /* Show the deny all button */
    "handleBrowserDNTRequest": true, /* If Do Not Track == 1, disallow all */
    "hashtag": "#tarteaucitron", /* Open the panel with this hashtag */
    "highPrivacy": true, /* Disable auto consent */
    "iconPosition": "BottomRight", /* BottomRight, BottomLeft, TopRight and TopLeft */
    "mandatory": true, /* Show a message about mandatory cookies */
    "moreInfoLink": true, /* Show more info link */
    "orientation": "bottom", /* Banner position (top - bottom) */
    "privacyUrl": privacyUrl, /* Privacy policy url */
    "readmoreLink": "", /* Change the default readmore link */
    "removeCredit": true, /* Remove credit link */
    "showAlertSmall": false, /* Show the small banner on bottom right */
    "showIcon": false, /* Show cookie icon to manage cookies */
    "useExternalCss": false, /* If false, the tarteaucitron.css file will be loaded */
    "useExternalJs": false, /* If false, the tarteaucitron.js file will be loaded */
  });

  tarteaucitron.job = tarteaucitron.job || [];

  // If xiti is used, add this service
  if (!!window.__funmooc_context__.marketing.xiti.site_id) {
    tarteaucitron.services.xiti = {
      key: 'xiti',
      type: 'analytic',
      name: 'Xiti',
      uri: 'https://www.atinternet.com/societe/rgpd-et-vie-privee/',
      needConsent: true,
      safeanalytic: true,
      cookies: ['atid', 'idrxvr', 'atuserid', 'atidx', 'atidvisitor'],
    }

    tarteaucitron.job.push('xiti');
  }
})();

