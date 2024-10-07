# FOTOLITOGRAFICZNE MASKI AMPLITUDOWE – O CO CHODZI?

Proces polega na zaprojektowaniu takiej maski fotolitograficznej, która jednorodny rozkład intensywności wiązki o długości fali 365 nm przekształci na rozkład zmienny i wielostopniowy. Tą zmodulowaną przestrzennie energią zostanie naświetlona cienka warstwa światłoczułego polimeru zwanego fotorezystem, co spowoduje lokalne rozbijanie wiązań międzycząsteczkowych. Cząstki o osłabionych wiązaniach zostaną następnie wypłukane rozpuszczalnikiem w procesie wywołania, a pozostała warstwa polimeru będzie miała dwu-i-półwymiarowy kształt. Może ona stanowić finalny element funkcjonalny, albo zostać użyta jako dawca kształtu do innych procesów jak trawienie czy galwanizacja.
Dobra wiadomość: każdy z poniższych kroków (może poza 2) został w jakimś stopniu ruszony i maski działają.
Zła wiadomość: każdy z tych kroków wymaga ogromnej ilości pracy optymalizacyjnej. Jest to zadanie zdecydowanie przerastające zarówno czas, jak i zakres praktyk, ale ważne jest to, czego się nauczycie podczas tej pracy. Każdym krokiem możecie się w miarę swoich zainteresowań zająć, jeżeli będziecie mieli na to ochotę.

## ELEMENTY PROCESU WYTWARZANIA FOTOLITOGRAFICZNEJ MASKI AMPLITUDOWEJ:

## 1.	Generacja powierzchni na bazie założeń geometrycznych

Każdy element optyczny trzeba wygenerować w postaci, która będzie stanowić bazę do obliczania maski. Typowe elementy to soczewki i siatki dyfrakcyjne i skrypt musi umożliwiać łatwą generację, kontrolę parametrów i zapis.

## 2.	Symulacje propagacji światła

Interakcja światła z małymi metalicznymi szczelinami ma charakter elektrodynamiczny. Oprogramowanie takie jak ANSYS Lumerical posiada wbudowane solvery, które potrafią modelować taką propagację.

## 3.	Przekształcenie powierzchni na piksele maski amplitudowej

Żeby kontrolować lokalną transmisję maski za pomocą wzoru binarnego, można zastosować dwa podejścia:

- Pulse Width Modulation (PWM) – sygnał ciągły jest zamieniany na serię impulsów dyskretnych o stałym okresie i różnej szerokości

![obraz](https://github.com/user-attachments/assets/4f10c128-dfe3-4942-a8ef-06edde440b44)

[źródło](https://www.realdigital.org/doc/333049590c67cb553fc7f9880b2f79c3)

- Pulse Density Modulation (PDM) – sygnał ciągły jest zamieniany na serię impulsów dyskretnych o zmiennym okresie i stałej szerokości

![obraz](https://github.com/user-attachments/assets/c72343a5-793a-46d1-91a3-20d35cb18008)

[źródło](https://www.realdigital.org/doc/333049590c67cb553fc7f9880b2f79c3)

W przypadku maski amplitudowej można spróbować zastosować obie metody, bo obie mają swoje zalety i wady. PWM przyjmie formę pikseli o stałym okresie i różnych polach powierzchni otworów. Póki co stosowano otwory prostokątne lub zaokrąglone, ale możliwe, że są lepsze rozwiązania do wyznaczenia poprzez symulacje z punktu 2.

![obraz](https://github.com/user-attachments/assets/89963b21-dd67-416c-b832-293b01b6dd0c)![obraz](https://github.com/user-attachments/assets/9231d4ba-2007-4d43-b0c6-79c88e434243)

![obraz](https://github.com/user-attachments/assets/ddddaf13-7090-4ea0-a004-1bb05dd2d46a)![obraz](https://github.com/user-attachments/assets/07e084c3-afa8-4e3e-a6be-9dd2c2659e3d)

PDM jest do zrealizowania za pomocą szeroko dostępnych funkcji typu dither.

![obraz](https://github.com/user-attachments/assets/c6ab1e74-5303-465c-a308-2588598ff801)![obraz](https://github.com/user-attachments/assets/8b5a3e73-1860-467b-ba84-0716e8a70fd6)

Dane wsadowe do procesu generacji maski stanowią powierzchnie z punktu 1. Należy z bitmapy stworzyć macierz elementów PWM lub PDM, gdzie parametry każdej komórki są sterowane stopniem szarości piksela wsadowej bitmapy. Format docelowy to GDS i DXF.

## 4.	Naświetlanie maski amplitudowej

Sam proces naświetlania maski stanowi szerokie pole do optymalizacji. Przede wszystkim chodzi o redukcję czasu produkcji i co za tym idzie, ceny finalnego produktu. Do zbadania pozostaje kwestia, na jak wiele kompromisów możemy pójść, żeby maska nadal działała, a proces był jak najszybszy.
Proces naświetlania przy niewłaściwym dobraniu parametrów może skutkować szeregiem błędów, od prześwietlenia czy niedoświetlenia do poważnego zaburzenia kształtu elementów.

![obraz](https://github.com/user-attachments/assets/5ea65855-cca8-4fb1-bb05-df07e34daee7)![obraz](https://github.com/user-attachments/assets/cde64133-2714-4aec-bcd6-cdbf4de0ae84)

## 5.	Trawienie maski amplitudowej

Maska fotolitograficzna składa się zazwyczaj z płyty szklanej lub kwarcowej pokrytej ok. 100nm dwuwarstwy Cr-CrO. Przeniesienie wzoru do warstwy metalu dokonywane jest poprzez trawienie jonami reaktywnymi (ICP RIE). To skomplikowany proces fizykochemiczny o wielu stopniach swobody. Stosuje się do niego plazmę chlorową, a proces ma dwojaki charakter – reakcja chemiczna z materiałem oraz fizyczne kolizje dosyć ciężkich jonów. Wyjaśniając obrazowo – ICP odpowiada za gęstość plazmy, a RIE za jej kierunkowość. Do tej pory stosowano dosyć standardowy proces bez większych optymalizacji, co widać po profilu zmierzonym za pomocą mikroskopu sił atomowych. Idealny profil powinien być pionowy, a mamy tu do czynienia z wyraźnym zboczem.

![obraz](https://github.com/user-attachments/assets/dd264ce9-585c-499e-96cf-7bc6ae23d0e5)![obraz](https://github.com/user-attachments/assets/65bb5eff-ea84-4fcb-96d5-62940072f476)

## 6.	Projektowanie procesu fotolitografii

Maska jest elementem pośrednim, który potem ma być stosowany w produkcji docelowych struktur optycznych. Konieczne jest dobranie parametrów fotolitografii (rodzaj fotorezystu, dawka, odległość maski od podłoża, rodzaj oświetlenia), zapewne jako proces iteracyjny do porównania z krokami 1-5 i wprowadzenia niezbędnych poprawek.

![obraz](https://github.com/user-attachments/assets/b3d05e9c-92f2-42c7-b790-46e4383017bd)![obraz](https://github.com/user-attachments/assets/1de42a71-bfe3-4a5e-8e99-0b9db9455858)






