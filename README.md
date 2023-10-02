# Fortune 20 Domain Survey

A survey of domain security at the companies on the Fortune 20 list.

## Motive

> I wonder how many Fortune 20 domains have an enforced DMARC policy?

Professional curiosity turned into weeks of ADHD-fueled hyperfixation. As usual, I underestimated the amount of effort required. Berkshire Hathaway alone has over 200 domain names for various subsidiaries and brands! 😅

When an organization is evaluating its security posture, a common step is a comparison to organizations of a similar size and industry. I was curious to see how Fortune 20 companies are deploying security controls that protect their domains, brands, and email inboxes. For example, MX DNS records can reveal if a domain is being protected by a secure email gateway, providing information about which vendors are most popular. This data is not intended endorse or shame anyone. It's just data.

 Likewise, DMARC DNS records show which domains have implemented the DMARC standard,which can [prevent unauthorized spoofing][DMARC] of domains in email message from addresses. However, before a domain's DMARC policy can be changed from a monitor policy (i.e, `none`) to `quarantine` or `reject`, the domain owner must ensure that all legitimate email are properly authenticated. That can be difficult for large organizations, where different business units may use many different services to send emails as the same domain. Smaller subsidiaries tend to have an easier time, because they may only have a few sending services: e.g., an email gateway, marketing service, and a customer service platform.

## Methodology

The Fortune 20 list is sourced from [Wikipedia][wikipedia]. The latest version published there at the time of this writing is from 2022, even though Forbes published their 2023 Fortune 500 list behind a paywall on June 5, 2023.

Each company has many domains. The domains listed in this project are gathered based on brands and subsidiaries mentioned in public information, such as the SEC form 10-K annual report, available in [EDGAR][EDGAR]. The domain lists published here do not include all of the domains related to these companies.

The list of domains is then processed using [checkdmarc][checkdmarc], which checks each domain for DNSSEC, a valid SPF record, a valid DMARC record, and more.

## License

The Domain Survey source code licensed under the [Apache 2.0 License][LICENSE].

The domain lists and survey results are provided under the
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license][cc]. Please provide credit to Sean Whalen and the original project at https://github.com/seanthegeek/fortune-20-domain-survey.

[DMARC]: https://seanthegeek.net/459/demystifying-dmarc/
[wikipedia]: https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue
[EDGAR]: https://www.sec.gov/edgar/searchedgar/companysearch
[checkdmarc]: https://domainaware.github.io/checkdmarc/
[LICENSE]: https://github.com/seanthegeek/fortune-20-dmarc-survey/blob/main/LICENSE
[cc]: https://creativecommons.org/licenses/by-sa/4.0/
