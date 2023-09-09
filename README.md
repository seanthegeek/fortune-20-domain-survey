# Fortune 20 Domain Survey

A survey of domain security at the companies on the Fortune 20 list.

## Methodology

The Fortune 20 lists are sourced from [Wikipedia][wikipedia].

Each company has many domains. The domains listed in this project are gathered based on brands and subsidiaries mentioned in public information, such as the SEC form 10-K annual report, available in [EDGAR][EDGAR], and do not include all of the domains related to these companies.

The list of domains is then processed using [checkdmarc][checkdmarc], which checks each domain for DNSSEC, SPF, DMARC records, and more.

## License

The DMARC Survey source code licensed under the [Apache 2.0 License][LICENSE].

The domain lists and survey results are provided under the
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license][cc]. Please provide credit to Sean Whalen and the original project at https://github.com/seanthegeek/fortune-20-domain-survey.

[wikipedia]: https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue
[EDGAR]: https://www.sec.gov/edgar/searchedgar/companysearch
[checkdmarc]: https://domainaware.github.io/checkdmarc/
[LICENSE]: https://github.com/seanthegeek/fortune-20-dmarc-survey/blob/main/LICENSE
[cc]: https://creativecommons.org/licenses/by-sa/4.0/
