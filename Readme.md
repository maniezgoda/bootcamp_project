# Kodołamacz Bootcamp projekt zaliczeniowy
by Maciej Niezgoda (GR. I Katowice)

---

## Opis celu projektu:
Celem projektu jest budowa modelu predykcji wartości cen lokali mieszkalnych w Katowicach na podstawie danych pochodzących z serwisu ```otodom.pl```.

Pierwszym etapem projektu było przygotowanie scrappera, który pobrał z serwisu ```otodom.pl``` następnie przygotowano skrypt, który przyjmował pobrane informacje o nieruchomościach i przetworzył je w czytelny dataframe. 

Przetworzoną csv wraz zrzutem danych na dzień **2019-04-20** przerzucono do folderu ```model```, w którym przystąpiono do procesu budowy modelu w edytorze jupyter notebook

## Uwaga!
**Serwis otodom.pl zmienia często układ strony w celu ochrony przed scrappingiem w związku z czym selectory css mogą być nieaktualne.**

W związku z powyższym do modelowania wykorzystano zrzut danych z dnia **2019-04-20** w którym obecne selektory działały.

## Opis danych

Przykładowe rekordy ze zeskrapowanego zbioru (przed processingiem):

| area   | building         | building_floors | chamber | construction_year | floor | market    | price     | standard        | url                                                                                                     |
|--------|------------------|-----------------|---------|-------------------|-------|-----------|-----------|-----------------|---------------------------------------------------------------------------------------------------------|
| 58.62  | blok             | 3.0             | 3       | 2020.0            | 1.0   | pierwotny | 349372.0  | do wykończenia  | https://www.otodom.pl/oferta/nowe-mieszkanie-dla-rodziny-2-2-ID3XXa4.html#4ad60757c7                    |
| 92.0   | apartamentowiec  | 2.0             | 3       | 1990.0            | 1.0   | wtórny    | 649000.0  | do zamieszkania | https://www.otodom.pl/oferta/ptasie-osiedle-garaz-w-cenie-okna-na-park-ID3XXmQ.html#4ad60757c7          |
| 41.34  | blok             | 3.0             | 2       | 2020.0            | 2.0   | pierwotny | 246632.0  | do wykończenia  | https://www.otodom.pl/oferta/katowice-premier-park-na-witosa-nowosc-ID3XXdi.html#4ad60757c7             |
| 82.28  | apartamentowiec  | 5.0             | 4       |                   | 3.0   | pierwotny | 560000.0  |                 | https://www.otodom.pl/oferta/nowe-ptasie-spokojna-zielona-okolica-0-pcc-ID3XXC0.html#4ad60757c7         |
| 47.7   | apartamentowiec  | 5.0             | 2       |                   | 3.0   | pierwotny | 325000.0  | do wykończenia  | https://www.otodom.pl/oferta/zamieszkaj-w-okolicy-parku-i-lasu-nowe-ptasie-ID3XXCQ.html#4ad60757c7      |

### Opis kolumn:

Nie wszystkie kolumny są wypełnione dane, gdyż część ofert nie jest w pełni kompletna. Braki zostały uzupełnione lub odrzucone w preprocessingu modelowania.

* ```area``` - zawiera powierzchnię lokalu wyrażoną w metrach kwadratowych
* ```building``` - zawiera informację o rodzaju budynku w którym mieści się mieszkanie
* ```building_floors``` - zawiera informację o ilości pięter w budynku (w przypadku gdy podano wartość >10 przyjęto 11)
* ```chamber``` - zawiera informację o ilości pokoi w mieszkaniu
* ```construction_year``` - zawiera informację o roku budowy (jeżeli jest przyszła oznacza, że jest to oferta sprzedaży od dewelopera)
* ```floor``` - zawiera informację o piętrze na którym mieści się lokal
* ```market``` - informacja o tym czy mieszkanie jest z rynku pierwotnego lub wtórnego
* ```price``` - zawiera informację o cenie ofertowej
* ```standard``` - informacja o standardzie wykończenia lokalu
* ```url``` - źródłowy url z ofertą

### Struktura projektu:

* ```data_scraper``` - Część odpowiedzialna za pobranie i przetworzenie danych
  * ```data_scraper``` - Skrypt oparty o ```scrapy```, który pobiera dane z otodom i zapisuje je w formie pliku JSON
  * ```data_processing``` - Skrypt który pobiera dane wygenerowane z ```data_scraper``` parsuje html z cechami nieruchomości i tworzy wystandaryzowany csv.
* ```model``` - Budowa modelu
  * **```Model.ipynb```** - Jupyter notebook zawierający eksplorację danych, analizę oraz modelowanie i podsumowanie projektu. Najważniejszy plik i sugeruję, by po zapoznaniu się z readme udać się do niego.