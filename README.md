
Projektet är en finanshanteringsapplikation utvecklad för att ge användare möjlighet att hantera sina personliga ekonomier på ett effektivt sätt. Applikationen är designad för att fungera i kommandotolken och ger användarna en serie interaktiva menyer för att navigera genom dess olika funktioner.

Insåg i efterhand att kanske ideén var mer att skapa en simple login funktion och inte en med registrering och funktion för flertal användare. Att login credz skulle vara hardkodad i koden som bara använda applikationen för en användare.

Applikationen är utformad för att vara enkel att konfigurera och köra, med minimala beroenden och förutsättningar. Vid första körningen kommer nödvändiga filer att skapas automatiskt, vilket säkerställer en smidig användarupplevelse. Ett viktigt moment att notera är dock vid användning av backup-funktionen.

Backupfunktionen skapar en säkerhetskopia av användardata, som sparas i en fil med namnet `back_{username}_data.json`. När denna fil återställs, ändras namnet till `{username}_data.json` för att applikationens olika funktioner ska kunna känna igen den. Det är viktigt att den ursprungliga JSON-filen inte finns kvar i mappen under återställningen. Om den gamla filen fortfarande existerar kan det uppstå problem eftersom applikationen kan bli förvirrad av två filer med liknande namn. Det är därför rekommenderat att användare tar bort eller flyttar den existerande filen innan de återställer från en backup.

Det finns också en möjlighet att förbättra denna process i framtiden, exempelvis genom att implementera en kontrollfunktion som verifierar backupfilens integritet utan att riskera de befintliga användardata. Detta skulle ytterligare förbättra användarupplevelsen och säkerheten kring hanteringen av personlig finansiell information.

**Användning**: Steg-för-steg-guide om hur man använder applikationen, inklusive hur man navigerar genom de olika funktionerna.

1. **Starta Programmet**
		    
		    - Kör programmet. Du kommer att se en huvudmeny med alternativen: Login, Register, Exit.
2. **Registrera ett Nytt Konto (Valfritt)**
		    
		    - Välj 'Register' om du är en ny användare.
		    - Ange ett användarnamn och ett lösenord.
		    - Du kommer att bli ombedd att ange en initial balans för ditt konto.
3. **Logga In**
		    
		    - Välj 'Login'.
		    - Ange ditt användarnamn och lösenord.
		    - Om inloggningen lyckas, kommer du till användarmenyn.
4. **Användarmeny**
		    
		    - I användarmenyn kan du välja mellan olika alternativ som Track Income/Expense, Create/Monitor Budget, Generate Financial Report, Backup Data, Restore Data och Logout.
5. **Spåra Inkomster och Utgifter**
		    
		    - Välj 'Track Income/Expense' för att registrera nya transaktioner.
		    - Välj mellan att registrera inkomst eller utgift, ange belopp, kategori och datum.
6. **Skapa och Övervaka Budget**
		    
		    - Välj 'Create/Monitor Budget' för att skapa budgetgränser för olika kategorier eller för att se dina nuvarande budgetar.
7. **Generera Finansiell Rapport**
		    
		    - Välj 'Generate Financial Report' för att skapa rapporter.
		    - Du kan välja mellan Summary Report och Budget Report.
		    - För Summary Report, välj perioden (vecka/månad/år) och specificera tidsintervall.
		    - För Budget Report, får du en översikt av din nuvarande budget jämfört med dina utgifter.
8. **Exportera Rapport**
		    
		    - Efter att ha genererat en rapport, kommer du att få möjlighet att exportera den.
		    - Om du väljer att exportera, ange ett filnamn för att spara rapporten.
9. **Backup och Återställning av Data**
		    
		    - Välj 'Backup Data' för att skapa en säkerhetskopia av dina data.
		    - Välj 'Restore Data' för att återställa data från en säkerhetskopia.
10. **Logga Ut**
		    
		    - När du är klar, välj 'Logout' för att avsluta sessionen och återgå till huvudmenyn.
		
		    - **Referenser**: Om du har använt några externa bibliotek eller resurser, se till att ge lämpliga krediter.
		    Externa bibliotek som använts medföljer vid Python 3.6 installationen och behöver inte importeras via pythons pip funktion. Följande bibliotek som har använts är:

	Använda Bibilotek:
	1. **collections**: Innehåller specialiserade container-datatyper som `defaultdict`. `defaultdict` är som en vanlig dictionary, men den skapar automatiskt en ny default-värde om nyckeln inte finns.
	    
	2. **shutil**: Används för att hantera högnivå filoperationer, som att kopiera och flytta filer.
	    
	3. **datetime**: Ger funktioner för att hantera datum och tid, som att skapa och ändra datumobjekt.
	    
	4. **json**: Används för att arbeta med JSON-data. Det kan konvertera mellan JSON-strängar och Python-dictionarys.
	    
	5. **os**: Ger ett sätt att använda operativsystemets funktionalitet, som att hantera filvägar och kontrollera filers existens.
