# CeneoScraper
# Etap 1 - pobranie pojedynczej opinii 
- opinia: li.review-box
- identyfikator: li.review-box["data-entry-id"] 
- autor: div.reviever-name-line
- rekomendacja: .product-review-summary > em
- liczba gwiazdek: span.review-score-count
- czy potwierdzona zakupem: div.product-review-pz
- data wystawienia: time['datetime']
- data zakupu: time['datetime']
- przydatna: button.vote-yes['data-total-vote']
- nieprzydatna: button.vote-no['data-total-vote']
- treść: p.product-reveiew-body
- wady: div.cons-cell > ul
- zalety: div.pros-cell > ul
