# Changelog

### Pre-release

### Fixed bugs

## [3.3.1](https://github.com/uktrade/navigator/releases/tag/3.3.1)

[Full Changelog](https://github.com/uktrade/navigator/compare/3.3.0...3.3.1)

### Fixed bugs
- GLS-328 - Fix a typo in commission on markets detail page

## [3.3.0](https://github.com/uktrade/navigator/releases/tag/3.3.0)

[Full Changelog](https://github.com/uktrade/navigator/compare/3.2.0...3.3.0)

- GBAU-947 - Removed default special terms message
- GP2-2841 - Standardisation of python buildpack

## [3.2.0](https://github.com/uktrade/navigator/releases/tag/3.2.0)

[Full Changelog](https://github.com/uktrade/navigator/compare/3.1.0...3.2.0)

- GP2-2863 - Uploading/viewing logos fix

## [3.1.0](https://github.com/uktrade/navigator/releases/tag/3.1.0)

[Full Changelog](https://github.com/uktrade/navigator/compare/2020.07.09...3.1.0)

- No Ticket - Django version upgrade to 2.2.22
- GP2-2381 - corrected contact footer link
- No ticket - added magna header under feature flag
- No Ticket - updating team name in error message for internal SSO
- GP2-2332 - upgrade directory-components package
- GP2-2784 - upgrade directory-components package

### Fixed bugs

- Upgrade vulnerable Django from 1.11.28 to 1.11.29
- Upgrade vulnerable Pillow from 3.3.2 to 7.1.0
- Upgrade vulnerable jQuery 3.1.1 to 3.5.0
- Upgrade python-dateutil to 2.8.1
- Upgrade markdown2 to 2.3.9
- Update test to reflect Mohawk exception

## [2020.07.09](https://github.com/uktrade/navigator/releases/tag/2020.07.09)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.03.19...2020.07.09)

## Hotfix
- GAA-13 - Add alt text
- GAA-17 - An incorrect role value had been applied
- No ticket - v3-cipipeline manifest.yml file fix
- TT-2328 - rename Commision -> commission

## [2020.03.19](https://github.com/uktrade/navigator/releases/tag/2020.03.19)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.03.10...2020.03.19)

### Fixed bugs

- No Ticket - Removed visibility of unpublished markets

## [2020.03.19](https://github.com/uktrade/navigator/releases/tag/2020.03.19)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.03.10...2020.03.19)

### Fixed bugs

- No Ticket - Removed visibility of unpublished markets

## [2020.03.10](https://github.com/uktrade/navigator/releases/tag/2020.03.10)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.02.04...2020.03.10)

### Fixed bugs

- No Ticket - Incorrectly showing seller support hours as customer support hours on Market detail page
- No Ticket - Re-add missing back button to detail page

## Pre-release

- no ticket - update components for new cookie banner
- MVP-40 - Add GA360 context processor and remove GA360 Middleware
- Remove existing SSO Middleware and move to directory-components SSO Middleware
- Remove feature flagging for Authbroker Staff SSO
- Remove unneccessary code in Market View
- Fix Market homepage bug showing unpublished markets to logged-in users
- Upgrade directory-components to 35.17.0
- Use standard directory-components header

## [2019.02.04](https://github.com/uktrade/navigator/releases/tag/2019.02.04)

[Full Changelog](https://github.com/uktrade/navigator/compare/2020.01.22-b...2019.02.04)

### Fixed bugs

- Upgrade Django from 1.11.23 to 1.11.28

## [2020.01.22-b](https://github.com/uktrade/navigator/releases/tag/2020.01.22-b)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.09.23...2020.01.22-b)

### Implemented enhancements

- DATAPROJECTS-259 - Updated country names and removed UK from find a marketplace search
- XOT-1119 - small text changes to homepage and search form
- XOT-856 - Staff SSO Integration for Admin Centre including 401 error if user not given admin rights
- XOT-1077 - Get case studies from CMS on homepage
- XOT-856 - Increase Django SSO Staff Client library

### Fixed bugs

- TT-1614 - Set the CSRF and session cooke to secure by default

## [2019.09.23](https://github.com/uktrade/navigator/releases/tag/2019.09.23)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.08.22...2019.09.23)

### Implemented enhancements

- XOT-1010 - Header is fixed for signing in and out
- GTRANSFORM-372 - upgrade components to 34.0.0 for accessibility footer link

## [2019.08.22](https://github.com/uktrade/navigator/releases/tag/2019.08.22)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.08.08...2019.08.22)

### Implemented enhancements

- GTRANSFORM-352 - search form, change select sizes for accessibility issue on search country filter
- XOT-999 - remove arrow button from new designs and change spelling on homepage
- GTRANSFORM-346 directory components upgrade for external link helpers in footer

### Fixed bugs

## [2019.08.08](https://github.com/uktrade/navigator/releases/tag/2019.08.08)

[Full Changelog](https://github.com/uktrade/navigator/compare/2019.08.06...2019.08.08)

### Implemented enhancements

- XOT-994 - wrap no deal text in paragraph
- XOT-994 - changelog, requirements and small CSS change
- XOT-994 - update special terms test

### Fixed bugs

- No ticket - Update header

## [2019.08.06](https://github.com/uktrade/navigator/releases/tag/2019.08.06)

[Full Changelog](https://github.com/uktrade/navigator/compare/cba35dba000639efa336db8904bc7e5331feef0f..2019.08.06)

### Implemented enhancements

- GTRANSFORM - add accessibility helper text to external link
- COT-989 - breadcrumb text changes and inject backbutton for no js users
- XOT-987 - last minute design changes and detail.html pulling correct offer text
- XOT-987 - add content changes, add missing separator for detail page, change font for search results heading and add border
- XOT-980 - remove trailing zeros from search results float values
- XOT-976 - add missing test requirement and update verson number
- XOT-976 - market detail page - design review changes and add utility classes to markup to reduce css
- XOT-951 - homepage and search page reviews fixes
- XOT-975 - homepage content changes
- XOT-917 - build redesigned market detail page
- XOT-635 - SOO Design - more dates for landing and search results page, updated directory components version to 26.1.0, added pagination to search results landing.
- XOT-635 - SOO Design updated for landing and search results page.

### Fixed bugs

- XOT-994 - wrap no deal text in paragraph, upgrade directory components to fix header input bug
- XOT-976 - add missing test requirement and update verson number
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- XOT-828 - GA360 tagging key name and selector corrections
- XOT-840 - display correct link to marketplace
- No ticket - Upgrade vulnerable django version to django 1.11.22
- No ticket - Upgrade vulnerable django rest framework version

## [2019.06.16](https://github.com/uktrade/navigator/releases/tag/2019.06.16)

**Implemented enhancements:**

- XOT-840 - Links provided to Great.gov search now use user-facing URLs
